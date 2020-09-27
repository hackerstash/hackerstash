import stripe
from hackerstash.db import db
from hackerstash.config import config
from hackerstash.lib.logging import logging
from hackerstash.models.member import Member

stripe.api_key = config['stripe_api_secret_key']


def create_customer(user):
    # Create a new stripe customer and assign their customer
    # id to the project member. With this information you can
    # create a session, which will allow you to request the
    # first payment
    customer = stripe.Customer.create(email=user.email)
    return customer['id']


def create_session(stripe_customer_id):
    # Create the session, this effectively gives them access to
    # the "cart". The session id is used by the front end to
    # redirect the user offsite to set up their payment details.
    return stripe.checkout.Session.create(
        customer=stripe_customer_id,
        payment_method_types=['card'],
        line_items=[{'price': config['stripe_price_id'], 'quantity': 1}],
        mode='subscription',
        success_url=config['stripe_success_uri'],
        cancel_url=config['stripe_failure_uri']
    )


def get_subscription(customer_id):
    # Get the customers subscription if they have one. We use this
    # to check that the user doesn't alreay have a subscription
    # before creating a new one as we don't want to double charge
    # them.
    response = stripe.Subscription.list(customer=customer_id, limit=1)
    subscriptions = response['data']
    return subscriptions[0] if subscriptions else None


def get_payment_details(user):
    # The first time this is requested we need to fetch it from
    # stripe. But subsequent requests should be fetched from the
    # database so that we don't get rate limited
    if details := user.member.stripe_payment_details:
        return details
    else:
        logging.info(f'Fetching payment details for "{user.username}"')
        payment_methods = stripe.PaymentMethod.list(customer=user.member.stripe_customer_id, type='card')
        data = payment_methods['data'][0]
        details = {
            'name': data['billing_details']['name'],
            'email': data['billing_details']['email'],
            'card_number': 'XXXX XXXX XXXX' + data['card']['last4']
        }
        user.member.stripe_payment_details = details
        db.session.commit()
        return details


def handle_invoice_paid(customer_id):
    # This event is sent when the user successfully signs up for
    # the first time. It is not safe to reply on the redirect!
    # This is the only place that should set the project as published.
    member = Member.query.filter_by(stripe_customer_id=customer_id).first()
    project = member.project
    project.published = True
    logging.info(f'Setting project "{project.name}" as published with customer_id "{customer_id}"')
    db.session.commit()


def handle_payment_failed(customer_id):
    # This is sent when the users card is declined whilst they
    # have a subscription (i.e. the direct debit fails). We only
    # want to unpublish the project as their customer/subscription
    # details are stil valid.
    member = Member.query.filter_by(stripe_customer_id=customer_id).first()
    project = member.project
    project.published = False
    logging.info(f'Setting project "{project.name}" as unpublished with customer_id "{customer_id}"')
    db.session.commit()


def handle_subscription_deleted(customer_id):
    # Triggered when the user deletes their account (I presume offsite?)
    # this can't be triggered from within HackerStash and only comes from
    # the event. In this case we remove all traces of the user's payment
    # details.
    member = Member.query.filter_by(stripe_customer_id=customer_id).first()
    project = member.project
    member.stripe_customer_id = None
    member.stripe_subscription_id = None
    member.stripe_payment_details = None
    project.published = False
    logging.info(f'Setting project "{project.name}" as unpublished with customer_id "{customer_id}"')
    db.session.commit()


def handle_checkout_complete(customer_id, subscription_id):
    # This is fired when the user sets up the subscription for the first
    # time. The subscription_id is very important for looking stuff up,
    # as well as for when the user choses to cancel their subscription.
    member = Member.query.filter_by(stripe_customer_id=customer_id).first()
    member.stripe_subscription_id = subscription_id
    logging.info(f'Setting subscription for project "{member.project.name}"')
    db.session.commit()


def handle_subscription_cancelled(member):
    # Triggered by the user when they click the cancel button. We can
    # immediately set the published status to False, although we will
    # wait for the events from stripe to set the user specific details
    # to None.
    logging.info(f'Cancelling subscription for project "{member.project.name}"')
    member.project.published = False
    stripe.Customer.delete(member.stripe_customer_id)
    # I think deleting the customer also deletes the subscription
    # stripe.Subscription.delete(member.stripe_subscription_id)
    db.session.commit()