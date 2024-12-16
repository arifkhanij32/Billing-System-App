from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    product_id = models.CharField(max_length=50, unique=True)
    available_stocks = models.PositiveIntegerField()
    price = models.FloatField()
    tax_percentage = models.FloatField()

    def __str__(self):
        return self.name

class Purchase(models.Model):
    purchase_id = models.CharField(max_length=255, unique=True) 
    customer_email = models.EmailField()
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_price_without_tax = models.FloatField()
    total_tax = models.FloatField()
    net_price = models.FloatField()
    paid_amount = models.FloatField()
    balance_due = models.FloatField()

    def __str__(self):
        return f"{self.customer_email} - {self.purchase_date}"

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    purchase_price = models.FloatField()
    tax_payable = models.FloatField()
    total_price = models.FloatField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

class Denomination(models.Model):
    value = models.PositiveIntegerField()
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.value} - {self.count}"
