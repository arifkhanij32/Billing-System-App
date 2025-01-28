from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from billingapp.models import Product, Purchase, PurchaseItem, Denomination
from django.db.models import Count
from django.db import IntegrityError
import uuid

def home(request):
    """
    Renders the home page.
    """
    return render(request, 'home.html')

def product_list(request):
    if request.method == "POST":
        # Get form data
        name = request.POST.get("name")
        product_id = request.POST.get("product_id")
        available_stocks = int(request.POST.get("available_stocks"))
        price = float(request.POST.get("price"))
        tax_percentage = float(request.POST.get("tax_percentage"))

        # Save data to the database
        Product.objects.create(
            name=name,
            product_id=product_id,
            available_stocks=available_stocks,
            price=price,
            tax_percentage=tax_percentage
        )

        # Redirect to the same page to prevent form resubmission
        return redirect("product_list")

    # Fetch all products from the database
    products = Product.objects.all()
    return render(request, "product_list.html", {"products": products})


def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.name = request.POST.get("name")
        product.product_id = request.POST.get("product_id")
        product.available_stocks = int(request.POST.get("available_stocks"))
        product.price = float(request.POST.get("price"))
        product.tax_percentage = float(request.POST.get("tax_percentage"))
        product.save()

        return redirect("product_list")

    return render(request, "update_product.html", {"product": product})

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        return redirect("product_list")

    return render(request, "delete_product.html", {"product": product})


def purchase_list(request):
    if request.method == "POST":
        if "add_purchase" in request.POST:
            # Add a new purchase
            customer_email = request.POST.get("customer_email")
            total_price_without_tax = float(request.POST.get("total_price_without_tax"))
            total_tax = float(request.POST.get("total_tax"))
            paid_amount = float(request.POST.get("paid_amount"))

            # Calculate net price and balance due
            net_price = total_price_without_tax + total_tax
            balance_due = net_price - paid_amount

            # Create a new Purchase object
            Purchase.objects.create(
                customer_email=customer_email,
                total_price_without_tax=total_price_without_tax,
                total_tax=total_tax,
                net_price=net_price,
                paid_amount=paid_amount,
                balance_due=balance_due,
            )

        elif "add_item" in request.POST:
            # Add an item to a purchase
            purchase_id = request.POST.get("purchase_id")
            product_id = request.POST.get("product_id")
            quantity = int(request.POST.get("quantity"))

            purchase = get_object_or_404(Purchase, id=purchase_id)
            product = get_object_or_404(Product, id=product_id)

            purchase_price = product.price * quantity
            tax_payable = (purchase_price * product.tax_percentage) / 100
            total_price = purchase_price + tax_payable

            PurchaseItem.objects.create(
                purchase=purchase,
                product=product,
                quantity=quantity,
                purchase_price=purchase_price,
                tax_payable=tax_payable,
                total_price=total_price,
            )

            # Update purchase totals
            purchase.total_price_without_tax += purchase_price
            purchase.total_tax += tax_payable
            purchase.net_price = purchase.total_price_without_tax + purchase.total_tax
            purchase.balance_due = purchase.net_price - purchase.paid_amount
            purchase.save()

        elif "remove_item" in request.POST:
            # Remove an item from a purchase
            item_id = request.POST.get("item_id")
            item = get_object_or_404(PurchaseItem, id=item_id)

            purchase = item.purchase
            purchase.total_price_without_tax -= item.purchase_price
            purchase.total_tax -= item.tax_payable
            purchase.net_price = purchase.total_price_without_tax + purchase.total_tax
            purchase.balance_due = purchase.net_price - purchase.paid_amount
            purchase.save()

            item.delete()

        return redirect("purchase_list")

    # Fetch all purchases and products
    purchases = Purchase.objects.all()
    products = Product.objects.all()

    return render(request, "purchase_list.html", {
        "purchases": purchases,
        "products": products
    })
    
def delete_purchase(request, purchase_id):
    """
    Delete a specific purchase and its associated items.
    """
    purchase = get_object_or_404(Purchase, id=purchase_id)
    purchase.delete()
    return redirect('purchase_list')

def purchase_detail(request, purchase_id):
    """
    Display the details of a specific purchase and allow adding new items.
    """
    purchase = get_object_or_404(Purchase, id=purchase_id)

    if request.method == "POST":
        # Capture form data
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity"))

        # Fetch the product
        product = get_object_or_404(Product, id=product_id)

        # Calculate prices
        purchase_price = product.price * quantity
        tax_payable = (purchase_price * product.tax_percentage) / 100
        total_price = purchase_price + tax_payable

        # Create a new PurchaseItem
        PurchaseItem.objects.create(
            purchase=purchase,
            product=product,
            quantity=quantity,
            purchase_price=purchase_price,
            tax_payable=tax_payable,
            total_price=total_price
        )

        # Update the purchase totals
        purchase.total_price_without_tax += purchase_price
        purchase.total_tax += tax_payable
        purchase.net_price = purchase.total_price_without_tax + purchase.total_tax
        purchase.balance_due = purchase.net_price - purchase.paid_amount
        purchase.save()

        # return redirect("purchase_detail", purchase_id=purchase.id)
        return render(request, 'purchase_detail.html', {'purchase': purchase})

    # Fetch all products for the dropdown
    products = Product.objects.all()

    return render(request, "purchase_detail.html", {
        "purchase": purchase,
        "products": products
    })


def denomination_list(request):
    """
    Display the list of all denominations.
    Dynamically shows the denominations added by the user.
    """
    denominations = Denomination.objects.all()  # Fetch all dynamically added denominations
    return render(request, 'denomination_list.html', {'denominations': denominations})


def add_denomination(request):
    """
    Add a new denomination dynamically.
    """
    if request.method == 'POST':
        value = request.POST.get('value')
        count = request.POST.get('count')

        # Only add non-empty values and counts
        if value and count:
            try:
                Denomination.objects.create(value=value, count=count)
            except IntegrityError:
                return render(request, 'denomination_form.html', {
                    'denomination': None,
                    'error_message': f"Denomination with value {value} already exists."
                })
        return redirect('denomination_list')

    return render(request, 'denomination_form.html', {'denomination': None})


def update_denomination(request, denomination_id):
    """
    Update an existing denomination.
    """
    denomination = get_object_or_404(Denomination, id=denomination_id)

    if request.method == 'POST':
        value = request.POST.get('value')
        count = request.POST.get('count')

        # Update values only if provided
        try:
            if value:
                denomination.value = value
            if count:
                denomination.count = count

            denomination.save()
            return redirect('denomination_list')
        except IntegrityError:
            return render(request, 'denomination_form.html', {
                'denomination': denomination,
                'error_message': f"Denomination with value {value} already exists."
            })

    return render(request, 'denomination_form.html', {'denomination': denomination})

from django.shortcuts import get_object_or_404, redirect
from .models import Denomination

def delete_denomination(request, denomination_id):
    """
    Deletes a denomination by its ID.
    """
    denomination = get_object_or_404(Denomination, id=denomination_id)
    denomination.delete()
    return redirect('denomination_list')


from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import Denomination, Purchase, PurchaseItem, Product
from django.http import HttpResponse
from .utils import calculate_denominations


def calculate_denominations(balance_due):
    """
    Calculates the denominations for a given balance amount.
    """
    denominations = Denomination.objects.order_by('-value')
    remaining_balance = balance_due
    result = {}

    for denomination in denominations:
        if remaining_balance <= 0:
            break

        count = int(remaining_balance // denomination.value)
        if count > 0:
            result[denomination.value] = count
            remaining_balance %= denomination.value

    return result


from django.shortcuts import render, redirect
from .models import Purchase, Denomination, Product
from .utils import calculate_denominations

def billing_page(request):
    denominations = Denomination.objects.all()

    if request.method == 'POST':
        customer_email = request.POST.get('customer_email')
        paid_amount = float(request.POST.get('paid_amount', 0))
        product_ids = request.POST.getlist('product_id[]')
        quantities = request.POST.getlist('quantity[]')

        try:
            # Create Purchase
            purchase = Purchase.objects.create(
                customer_email=customer_email,
                paid_amount=paid_amount
            )

            total_price_without_tax = 0
            total_tax = 0
            net_price = 0

            for product_id, quantity in zip(product_ids, quantities):
                product = Product.objects.get(id=product_id)
                quantity = int(quantity)
                purchase_price = product.price * quantity
                tax = purchase_price * 0.18  # Assuming 18% tax
                total_price = purchase_price + tax

                # Save PurchaseItem
                purchase.items.create(
                    product=product,
                    quantity=quantity,
                    purchase_price=purchase_price,
                    tax_payable=tax,
                    total_price=total_price,
                )

                total_price_without_tax += purchase_price
                total_tax += tax
                net_price += total_price

            # Update Purchase totals
            purchase.total_price_without_tax = total_price_without_tax
            purchase.total_tax = total_tax
            purchase.net_price = net_price
            purchase.balance_due = net_price - paid_amount
            purchase.save()

            # Redirect to Bill Summary
            return redirect('billing_page', purchase_id=purchase.id)

        except Product.DoesNotExist:
            return render(request, 'billing_page.html', {
                'denominations': denominations,
                'error_message': 'One or more products do not exist.'
            })

    return render(request, 'billing_page.html', {'denominations': denominations})



def send_invoice_email(email, purchase, balance_denominations):
    """
    Sends an invoice email to the customer.
    """
    subject = "Invoice for Your Purchase"
    message = f"""
    Thank you for your purchase!

    Purchase ID: {purchase.purchase_id}
    Total Price Without Tax: {purchase.total_price_without_tax}
    Total Tax: {purchase.total_tax}
    Net Price: {purchase.net_price}
    Paid Amount: {purchase.paid_amount}
    Balance Due: {purchase.balance_due}

    Balance Denominations:
    {', '.join(f'{key}: {value}' for key, value in balance_denominations.items())}
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

from django.shortcuts import get_object_or_404, render
from .models import Purchase, PurchaseItem
from .utils import calculate_denominations

def bill_summary(request, purchase_id):
    """
    Displays the bill summary for a given purchase.
    """
    # Fetch the purchase object by ID
    purchase = get_object_or_404(Purchase, id=purchase_id)
    
    # Calculate balance denominations
    balance_denominations = calculate_denominations(purchase.balance_due)
    
    # Get purchase items
    items = PurchaseItem.objects.filter(purchase=purchase)
    # Render the summary template
    return render(request, 'billing_summary.html', {
        'purchase': purchase,
        'balance_denominations': balance_denominations,
        'items': items
    })


from billingapp.models import Purchase
Purchase.objects.all()

from billingapp.models import Purchase
for purchase in Purchase.objects.filter(purchase_id__isnull=True):
    purchase.save()

# Purchase.objects.all().delete()
