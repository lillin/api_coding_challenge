from django.apps import AppConfig


# TODO: rename to subscriptions
class SubscriptionsConfig(AppConfig):
    name = 'wingtel.subscriptions'
    label = 'subscriptions'

    def ready(self):
        import wingtel.subscriptions.signals
