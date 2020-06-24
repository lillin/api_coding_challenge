"""wingtel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from wingtel.plans.views import PlanViewSet
from wingtel.purchases.views import PurchaseViewSet

from wingtel.subscriptions.views import (
    ATTSubscriptionViewSet,
    ATTSubscriptionActivationView,
    SprintSubscriptionViewSet,
    SprintSubscriptionsActivationView,
)


router = routers.DefaultRouter()

router.register(r'att_subscriptions', ATTSubscriptionViewSet)
router.register(r'plans', PlanViewSet)
router.register(r'purchases', PurchaseViewSet)
router.register(r'sprint_subscriptions', SprintSubscriptionViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/sprint_subscriptions/activate/', SprintSubscriptionViewSet.as_view({'put': 'activate'})),
    path('api/activate_att_subscriptions/', ATTSubscriptionActivationView.as_view()),
    path('api/activate_sprint_subscriptions/', SprintSubscriptionsActivationView.as_view()),

    url(r'^api/', include((router.urls, 'api'), namespace='api')),
]
