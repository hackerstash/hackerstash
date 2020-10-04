import json
from flask import Blueprint, request, jsonify, g, redirect, url_for, get_template_attribute, abort, flash
from hackerstash.db import db
from hackerstash.config import config
from hackerstash.lib.logging import logging
from hackerstash.lib.stripe import create_customer, create_session, \
    handle_invoice_paid, handle_payment_failed, handle_checkout_complete, \
    handle_subscription_deleted, handle_subscription_cancelled, get_subscription, \
    handle_upcoming_invoice
from hackerstash.utils.auth import login_required

subscriptions = Blueprint('subscriptions', __name__)


@subscriptions.route('/stripe/webhook', methods=['POST'])
def webhook_received():
    request_data = json.loads(request.data)
    event_data = request_data['data']['object']
    event_type = request_data['type']

    logging.info(f'Handling webhook event type "{event_type}"')

    if event_type == 'invoice.paid':
        handle_invoice_paid(event_data)
    if event_type == 'invoice.payment_failed':
        handle_payment_failed(event_data)
    if event_type == 'checkout.session.completed':
        handle_checkout_complete(event_data)
    if event_type == 'customer.subscription.deleted':
        handle_subscription_deleted(event_data)
    if event_type == 'invoice.upcoming':
        handle_upcoming_invoice(event_data)

    return jsonify({'status': 'success'})


@subscriptions.route('/stripe/checkout', methods=['POST'])
@login_required
def checkout():
    member = g.user.member
    logging.info(f'Checking out user "{g.user.username}"')
    # Only the owner of a project can create a subscription
    if not member or not member.owner:
        # Not sure what to do in this case, they're fishing
        # around as we don't expose this anywhere
        return abort(403)

    project = member.project
    required_properties = ['name', 'description']
    for prop in required_properties:
        if getattr(project, prop) in [None, '', '<p><br></p>']:
            logging.info(f'Project "{project.name}" was missing required property "{prop}" to publish')
            flash('Project name and description are both required to publish', 'failure')
            return redirect(url_for('projects.edit', project_id=project.id))

    # Create the stripe customer and assign the customer id
    # to the member if they aren't already a customer
    if (customer_id := member.stripe_customer_id) is None:
        customer_id = create_customer(g.user)
        member.stripe_customer_id = customer_id
        db.session.commit()

    # If the subscription exists we should bail as we don't
    # want to create more than one subscription
    if (existing_sub := get_subscription(customer_id)) or member.stripe_subscription_id:
        # This is a weird case where they have a subscription but we don't
        # have anything on our end. Likely an error occurred during the checkout 🤷‍
        # Either way, update it now!
        if not member.stripe_subscription_id and existing_sub:
            logging.warning(f'Company "{member.project.name}" had a subscription but we didn\'t know about it!')
            member.stripe_subscription_id = existing_sub['id']
            member.project.published = True
            db.session.commit()
        return redirect(url_for('projects.subscription', project_id=member.project.id))

    # Create the session that allows them to check out if they
    # don't already have a subscription
    session = create_session(customer_id)

    # Render the checkout partial and send it. It will automatically
    # redirect the user to the checkout
    partial = get_template_attribute('partials/checkout.html', 'checkout')
    return partial(session, config['stripe_api_key'])


@subscriptions.route('/stripe/checkout/success')
@login_required
def checkout_success():
    # Callback from successful payment. This can't be relied
    # on as confirmation of payment so do not update anything.
    # Instead wait on the webook
    project = g.user.member.project
    logging.info(f'Payment succeeded for "{project.name}"')
    return redirect(url_for('projects.subscription', project_id=project.id))


@subscriptions.route('/stripe/checkout/failure')
@login_required
def checkout_failure():
    project = g.user.member.project
    logging.warning(f'Payment failed for "{project.name}"')
    return redirect(url_for('projects.edit', project_id=project.id))


@subscriptions.route('/stripe/subscription/cancel')
@login_required
def cancel_subscription():
    member = g.user.member
    if member.stripe_customer_id:
        handle_subscription_cancelled(member)
    return redirect(url_for('projects.edit', project_id=member.project.id))
