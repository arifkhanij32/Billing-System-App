from django.apps import AppConfig
from django.db.models.signals import post_migrate


class BillingappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'billingapp'

    def ready(self):
        from .models import Denomination
        from django.db.models.signals import post_migrate

        # Define the populate_denomination function here
        def populate_denomination(sender, **kwargs):
            denominations = [10, 20, 50, 100, 500, 2000]  # Example values
            for value in denominations:
                Denomination.objects.update_or_create(value=value)

        # Connect the post_migrate signal
        post_migrate.connect(populate_denomination, sender=self)
