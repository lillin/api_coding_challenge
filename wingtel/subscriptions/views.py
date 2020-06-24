from django.http import Http404
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import viewsets, views, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from wingtel.subscriptions.models import SprintSubscription, ATTSubscription
from wingtel.subscriptions.permissions import SubscriptionBelongsToUser
from wingtel.subscriptions.serializers import (
    ATTSubscriptionSerializer,
    SprintSubscriptionSerializer,
    SprintSubscriptionActivateSerializer
)


class ATTSubscriptionViewSet(mixins.CreateModelMixin,
                             mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    """
    A viewset that provides `retrieve`, `create`, and `list` actions.

    ViewSet was changed to custom one to implement actions were described in docstring only;
    also no permission were applied because of absence according requirements.
    """

    queryset = ATTSubscription.objects.all()
    serializer_class = ATTSubscriptionSerializer


class ATTSubscriptionActivationView(views.APIView):
    """
    Updates all subscriptions with status `New` (they belong to user from request).

    With current business logic we able to create multiple `subscriptions` and requirement to activate `any new`,
    how I understood, is opposite to specify instance to update by providing URL param
    as we often do with ModelViewSet,
    so approach to manage filtered queryset of `new` was implemented.

    Approach differs from Sprint Subscription update feature;
    """

    permission_classes = [IsAuthenticated, SubscriptionBelongsToUser, ]

    def put(self, request, *args, **kwargs):
        subscriptions_set = ATTSubscription.objects.filter(
            user_id=request.user.id,
            status=ATTSubscription.STATUS.new
        )
        if not subscriptions_set.exists():
            return Response(
                {'details': 'No such user or user does not have new subscriptions to activate.'},
                status=status.HTTP_404_NOT_FOUND
            )
        for obj in subscriptions_set:
            if all([obj.plan, obj.device_id, obj.phone_number]):
                obj.status = ATTSubscription.STATUS.active
                obj.save(update_fields=['status'])
        return Response(
            {'details': 'Subscriptions updated!'},
            status=status.HTTP_201_CREATED
        )


class SprintSubscriptionViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides `retrieve`, `create`, and `list` actions.

    Default `update` method was left as it is - here I prefer to save an ability to activate entity by it's ID.
    To activate random record was implemented corresponding extra action.
    """

    queryset = SprintSubscription.objects.all()
    serializer_class = SprintSubscriptionSerializer

    def get_serializer_class(self):
        if self.action == 'activate':
            return SprintSubscriptionActivateSerializer
        return super(SprintSubscriptionViewSet, self).get_serializer_class()

    def get_permissions(self):
        if self.action in ('update', 'activate'):
            return [IsAuthenticated(), SubscriptionBelongsToUser(), ]
        return [IsAuthenticated(), ]

    def get_queryset(self):
        if self.action == 'activate':
            return SprintSubscription.objects.filter(
                        status=SprintSubscription.STATUS.new,
                        user_id=self.request.user.id
                    )
        return super(SprintSubscriptionViewSet, self).get_queryset()

    def get_object(self):
        if self.action == 'activate':
            queryset = self.get_queryset()
            if not queryset.exists():
                raise Http404

            obj = queryset.first()
            self.check_object_permissions(self.request, obj)

            # we return any new subscription, no matter which one, so let it be first entity:
            return obj
        return super(SprintSubscriptionViewSet, self).get_object()

    @action(detail=False, methods=['put'])
    def activate(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data={})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class SprintSubscriptionsActivationView(UpdateAPIView):
    """
    Updates any subscription with status New (if only one Subscription instance with status New can exist at once.).

    Just standalone view as an example of multiple ways to implement feature.
    """

    permission_classes = (IsAuthenticated, SubscriptionBelongsToUser, )
    serializer_class = SprintSubscriptionActivateSerializer

    def get_queryset(self):
        queryset = SprintSubscription.objects.filter(
                        status=SprintSubscription.STATUS.new,
                        user_id=self.request.user.id
                    )
        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        if not queryset.exists():
            raise Http404

        obj = queryset.first()
        self.check_object_permissions(self.request, obj)

        # we return any new subscription, no matter which one, so let it be first entity:
        return obj
