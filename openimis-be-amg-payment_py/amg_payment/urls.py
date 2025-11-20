from django.urls import path

# Proxy import vers les vues existantes de l’app payments
try:
    from payments.views import initier_paiement, api_notify
except Exception:  # pragma: no cover
    # En environnement openIMIS, ces vues devront être fournies par le module
    def initier_paiement(request):
        raise NotImplementedError("initier_paiement non disponible: module payments manquant")

    def api_notify(request):
        raise NotImplementedError("api_notify non disponible: module payments manquant")


app_name = "amg_payment"

urlpatterns = [
    path("payments/initier-paiement", initier_paiement, name="initier_paiement"),
    path("holo/notificationpaiement", api_notify, name="notify"),
]