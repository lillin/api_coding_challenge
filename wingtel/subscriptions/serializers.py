from rest_framework import serializers, exceptions
from wingtel.subscriptions.models import SprintSubscription, ATTSubscription


class SprintSubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = SprintSubscription
        fields = '__all__'


class ATTSubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ATTSubscription
        fields = "__all__"


class SprintSubscriptionActivateSerializer(serializers.Serializer):
    def validate(self, attrs):
        instance = self.instance
        if not all([instance.plan, instance.device_id, instance.phone_number]):
            raise exceptions.ValidationError({'details': 'Update subscription info first!'})

        return attrs

    def update(self, instance, validated_data):
        instance.status = SprintSubscription.STATUS.active
        instance.save(update_fields=['status'])
        return instance
