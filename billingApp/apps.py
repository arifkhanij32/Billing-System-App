from django.apps import AppConfig
from django.db.models.signals import post_migrate

class BillingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'billingApp'

    def ready(self):
        from .models import Denomination

        def populate_denomination(sender, **kwargs):
            for value in [500, 50, 20, 10, 5, 2, 1]:
                Denomination.objects.get_or_create(value=value)

        # Connect the post_migrate signal
        post_migrate.connect(populate_denomination, sender=self)
