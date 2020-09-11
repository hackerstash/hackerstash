import stripe
from hackerstash.db import db
from hackerstash.config import config
from hackerstash.lib.logging import logging
from hackerstash.models.member import Member

stripe.api_key = config['stripe_api_secret_key']


def create_customer(user):
    logging.info(f'Created a new customer for "{user.username}"')
    customer = stripe.Customer.create(email=user.email)
    user.member.stripe_customer_id = customer['id']
    db.session.commit()
    return customer


def create_session(member):
    logging.info(f'Creating session for "{member.user.username}"')
    return stripe.checkout.Session.create(
        customer=member['customer_id'],
        payment_method_types=['card'],
        line_items=[{'price': config['stripe_price_id'], 'quantity': 1}],
        mode='subscription',
        success_url=config['stripe_success_uri'],
        cancel_url=config['stripe_failure_uri']
    )


def handle_invoice_paid(customer_id):
    member = Member.query.filter_by(stripe_customer_id=customer_id).first()
    project = member.project
    project.published = True
    logging.info(f'Setting project "{project.name}" as published with customer_id "{customer_id}"')
    db.session.commit()


def handle_payment_failed(customer_id):
    member = Member.query.filter_by(stripe_customer_id=customer_id).first()
    project = member.project
    project.published = False
    logging.info(f'Setting project "{project.name}" as unpublished with customer_id "{customer_id}"')
    db.session.commit()


def handle_subscription_deleted(customer_id):
    member = Member.query.filter_by(stripe_customer_id=customer_id).first()
    project = member.project
    member.stripe_customer_id = None
    member.stripe_subscription_id = None
    project.published = False
    logging.info(f'Setting project "{project.name}" as unpublished with customer_id "{customer_id}"')
    db.session.commit()


def handle_checkout_complete(customer_id, subscription_id):
    member = Member.query.filter_by(stripe_customer_id=customer_id).first()
    member.stripe_subscription_id = subscription_id
    logging.info(f'Setting subscription for project "{member.project.name}"')
    db.session.commit()


def handle_subscription_cancelled(member, subscription_id):
    logging.info(f'Cancelling subscription for project "{member.project.name}"')
    member.project.published = False
    stripe.Subscription.delete(subscription_id)
    db.session.commit()
