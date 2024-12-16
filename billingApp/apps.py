from django.apps import AppConfig

class BillingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'billingApp'

    def ready(self):
        from billingApp.models import Denomination
        for value in [500, 50, 20, 10, 5, 2, 1]:
            Denomination.objects.get_or_create(value=value)
