from django.db import models
import uuid

class Product(models.Model):
    name = models.CharField(max_length=255)
    product_id = models.CharField(max_length=50, unique=True)
    available_stocks = models.PositiveIntegerField()
    price = models.FloatField()
    tax_percentage = models.FloatField()

    def __str__(self):
        return self.name

    @property
    def tax_amount(self):
        return self.price * (self.tax_percentage / 100)

    @property
    def total_price(self):
        return self.price + self.tax_amount


from django.utils.timezone import now

# class Purchase(models.Model):
#     purchase_id = models.CharField(max_length=3, unique=True, blank=True)
#     customer_email = models.EmailField()
#     purchase_date = models.DateTimeField(default=now)  # Use timezone-aware now
#     total_price_without_tax = models.FloatField(default=0)
#     total_tax = models.FloatField(default=0)
#     net_price = models.FloatField(default=0)
#     paid_amount = models.FloatField(default=0)
#     balance_due = models.FloatField(default=0)

#     def save(self, *args, **kwargs):
#         if not self.purchase_id:
#             self.purchase_id = f"{int(uuid.uuid4().int % 1000):03}"
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Purchase {self.purchase_id}"
    
class Purchase(models.Model):
    purchase_id = models.CharField(max_length=8, unique=True, blank=True)
    customer_email = models.EmailField()
    purchase_date = models.DateTimeField(default=now)  # Use timezone-aware now
    total_price_without_tax = models.FloatField(default=0)
    total_tax = models.FloatField(default=0)
    net_price = models.FloatField(default=0)
    paid_amount = models.FloatField(default=0)
    balance_due = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        if not self.purchase_id:
            self.purchase_id = f"PUR-{uuid.uuid4().hex[:5].upper()}"  # Generates a unique ID
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Purchase {self.purchase_id}"


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_price = models.FloatField()
    tax_payable = models.FloatField()
    total_price = models.FloatField()

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Denomination(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2, unique=True)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.value} - {self.count}"

    @property
    def total_amount(self):
        return self.value * self.count


