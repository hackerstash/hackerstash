# Stripe

We use Stripe to mange the recurring payments. In a non-production environment we use the stripe-cli within a Docker container to manage the webhooks.

I'm sure it goes without saying, but **NEVER** use the production keys in development!

In the console, you should enable "Viewing test data" in the sidebar.

### Configuration

Some environment variables are required:
```
stripe_api_key=<Publishable key>
stripe_api_secret_key=<Secret key>
stripe_price_id=<Product ID>
stripe_success_uri=http://localhost:5000/stripe/checkout/success
stripe_failure_uri=http://localhost:5000/stripe/checkout/failure
```

### Developing

Stripe provide card numbers to test our certain senarios:

| Card number      | Description                                                                                                                                                                                                          |
|------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 4242424242424242 | Succeeds and immediately creates an active subscription.                                                                                                                                                             |
| 4000002500003155 | Requires authentication. confirmCardPayment() will trigger a modal asking for the customer to authenticate. Once the user confirms, the subscription will become active. See manage payment authentication.          |
| 4000008260003178 | Always fails with a decline code of insufficient_funds. See create subscription step on how to handle this server side.                                                                                              |
| 4000000000000341 | Succeeds when it initially attaches to Customer object, but fails on the first payment of a subscription with the payment_intent value of requires_payment_method. See the manage subscription payment failure step. |

More information on the cards can be found here:

https://stripe.com/docs/billing/subscriptions/fixed-price#test

You can also trigger events through the cli via Docker:
```shell
$ docker-compose exec stripe sh
$ trigger my.event
``` 

More information on events can be found here:

https://stripe.com/docs/cli/trigger
