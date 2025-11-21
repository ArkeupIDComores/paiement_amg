from django.urls import path
from . import views

app_name = 'amg_payement'


urlpatterns = [
    path('payments/initier-paiement', views.initier_paiement, name='initier_paiement'),
    # Anciens chemins (compatibilité)
    path('payment/holo/accept', views.redirect_accept, name='holo_accept'),
    path('payment/holo/decline', views.redirect_decline, name='holo_decline'),
    path('payment/holo/cancel', views.redirect_cancel, name='holo_cancel'),
    # Nouveaux chemins alignés à la config HOLO
    path('holo/acceptpaiement', views.redirect_accept, name='holo_accept_alias'),
    path('holo/declinepaiement', views.redirect_decline, name='holo_decline_alias'),
    path('holo/cancelpaiement', views.redirect_cancel, name='holo_cancel_alias'),
    path('api/payment/holo/initiate', views.api_initiate, name='api_holo_initiate'),
    path('api/payment/holo/notify', views.api_notify, name='api_holo_notify'),
    # Alias pour la notification selon la config HOLO
    path('holo/notificationpaiement', views.api_notify, name='api_holo_notify_alias'),
]