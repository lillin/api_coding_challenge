# Coding Challenge

## Requirements
* Python 3.5+
* SQLite

## Challenge
Create an endpoint that will allow a user to activate their own AT&T and/or Sprint subscription. This should include the following:

- Checks for proper user permissions
- Applies to any existing subscription with a status of `new`
- Checks required subscription data is present before activation, including `plan`, `phone_number`, `device_id`
- Changes the subscription status from `new` to `active`
- Creates a purchase with a status of `overdue` related to the subscription and the subscription's plan

*Note: The activation endpoint can be added to AT&T subscriptions, Sprint subscriptions, or both.*

## Bonuses
- Create a way to link a purchase directly to a subscription, not just a user
- Improve and/or optimize the code

## Superuser Login
username: `admin`
password: `admin`
