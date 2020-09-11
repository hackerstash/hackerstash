import json
from flask import Blueprint, request, jsonify, g, redirect, url_for, flash
from hackerstash.db import db
from hackerstash.lib.logging import logging
from hackerstash.lib.stripe import create_customer, create_session, \
    handle_invoice_paid, handle_payment_failed, handle_checkout_complete, \
    handle_subscription_deleted, handle_subscription_cancelled
from hackerstash.utils.auth import login_required

subscriptions = Blueprint('subscriptions', __name__)


@subscriptions.route('/stripe/webhook', methods=['POST'])
def webhook_received():
    request_data = json.loads(request.data)
    event_data = request_data['data']['object']
    event_type = request_data['type']

    # Unused hooks:
    # ['invoice.finalized', 'customer.subscription.trial_will_end']

    if event_type == 'invoice.paid':
        logging.info(f'Handling webhook event type "{event_type}"')
        handle_invoice_paid(event_data['customer'])

    if event_type == 'invoice.payment_failed':
        logging.info(f'Handling webhook event type "{event_type}"')
        handle_payment_failed(event_data['customer'])

    if event_type == 'checkout.session.completed':
        logging.info(f'Handling webook event type "{event_type}"')
        handle_checkout_complete(event_data['customer'], event_data['subscription'])

    if event_type == 'customer.subscription.deleted':
        logging.info(f'Handling webhook event type "{event_type}"')
        handle_subscription_deleted(event_data['customer'])

    return jsonify({'status': 'success'})


@subscriptions.route('/stripe/customer', methods=['POST'])
@login_required
def create_stripe_customer():
    member = g.user.member
    if not member:
        logging.info(f'User "{g.user.username}" is not a member of a project so can\'t become a customer')
        return jsonify({'error': 'Not a member of a project'}), 400
    if member.stripe_customer_id:
        logging.info(f'User "{g.user.username}" is already a customer')
        return jsonify({'customer_id': member.stripe_customer_id})
    # TODO:
    # Additional checks should be added here to make sure there is not already
    # a paying user for this project
    customer = create_customer(g.user)
    db.session.commit()
    logging.info(f'Created a new customer for "{g.user.username}"')
    return jsonify({'customer_id': customer['id']})


@subscriptions.route('/stripe/session', methods=['POST'])
@login_required
def create_checkout_session():
    member = g.user.member
    if not member or not member.stripe_customer_id:
        logging.info(f'User "{g.user.username}" is not a customer so can\'t checkout')
        return jsonify({'error': 'Not a stripe customer'})
    session = create_session(member.stripe_customer_id)
    logging.info(f'Created session for "{g.user.username}"')
    return jsonify({'session': session})


@subscriptions.route('/stripe/checkout/success')
@login_required
def checkout_success():
    project = g.user.member.project
    logging.info(f'Payment succeeded for "{project.name}"')
    flash('Subscription created successfully')
    return redirect(url_for('projects.edit', project_id=project.id, tab='3'))


@subscriptions.route('/stripe/checkout/failure')
@login_required
def checkout_failure():
    project = g.user.member.project
    logging.warning(f'Payment failed for "{project.name}"')
    flash('Subscription failed to create', 'failure')
    return redirect(url_for('projects.edit', project_id=project.id, tab='3', success='0'))


@subscriptions.route('/stripe/subscription/cancel')
@login_required
def cancel_subscription():
    member = g.user.member
    handle_subscription_cancelled(member, member.stripe_subscription_id)
    return redirect(url_for('projects.edit', project_id=member.project.id, tab='3'))
