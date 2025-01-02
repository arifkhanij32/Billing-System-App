from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from .models import Product, Purchase, PurchaseItem, Denomination
from django.conf import settings



def home(request):
    """
    Renders the home page.
    """
    return render(request, 'home.html')

def product_list(request):
    products = Product.objects.all()  # Fetch all products from the database
    return render(request, 'billingApp/product_list.html', {'products': products})


def purchase_list(request):
    """
    Display a list of all purchases.
    """
    purchases = Purchase.objects.all()
    return render(request, 'billingApp/purchase_list.html', {'purchases': purchases})

def purchase_detail(request, purchase_id):
    """
    Display the details of a specific purchase.
    """
    purchase = get_object_or_404(Purchase, id=purchase_id)
    return render(request, 'billingApp/purchase_detail.html', {'purchase': purchase})

def denomination_list(request):
    """
    Display the list of all denominations.
    """
    denominations = Denomination.objects.all()
    return render(request, 'billingApp/denomination_list.html', {'denominations': denominations})

def add_denomination(request):
    """
    Add a new denomination.
    """
    if request.method == 'POST':
        value = request.POST.get('value')
        count = request.POST.get('count')

        Denomination.objects.create(value=value, count=count)
        return redirect('denomination_list')

    return render(request, 'billingApp/denomination_form.html', {'denomination': None})

def update_denomination(request, denomination_id):
    """
    Update an existing denomination.
    """
    denomination = get_object_or_404(Denomination, id=denomination_id)

    if request.method == 'POST':
        denomination.value = request.POST.get('value')
        denomination.count = request.POST.get('count')
        denomination.save()
        return redirect('denomination_list')

    return render(request, 'billingApp/denomination_form.html', {'denomination': denomination})

 
def billing_page(request):
    """
    Handles the billing page functionality.
    Processes the form submission for creating a purchase and calculates totals.
    """
    if request.method == 'POST':
        # Collect data from the form
        customer_email = request.POST.get('customer_email')
        paid_amount = float(request.POST.get('paid_amount', 0))
        product_ids = request.POST.getlist('product_id[]')
        quantities = request.POST.getlist('quantity[]')

        # Create a new purchase instance
        purchase = Purchase.objects.create(
            customer_email=customer_email,
            total_price_without_tax=0,
            total_tax=0,
            net_price=0,
            paid_amount=paid_amount,
            balance_due=0
        )

        # Process each product and calculate prices
        total_price_without_tax = 0
        total_tax = 0

        for product_id, quantity in zip(product_ids, quantities):
            product = get_object_or_404(Product, product_id=product_id)
            quantity = int(quantity)

            # Calculate price and tax
            purchase_price = product.price * quantity
            tax_payable = (purchase_price * product.tax_percentage) / 100
            total_price = purchase_price + tax_payable

            # Create a purchase item
            PurchaseItem.objects.create(
                purchase=purchase,
                product=product,
                quantity=quantity,
                purchase_price=purchase_price,
                tax_payable=tax_payable,
                total_price=total_price
            )

            total_price_without_tax += purchase_price
            total_tax += tax_payable

        # Update purchase totals
        net_price = total_price_without_tax + total_tax
        rounded_net_price = round(net_price)
        balance_due = rounded_net_price - paid_amount

        purchase.total_price_without_tax = total_price_without_tax
        purchase.total_tax = total_tax
        purchase.net_price = rounded_net_price
        purchase.balance_due = balance_due
        purchase.save()

        # Calculate balance denominations
        balance_denominations = calculate_denominations(balance_due)

        # Send invoice email
        send_invoice_email(customer_email, purchase, balance_denominations)

        # Render the summary page
        return render(request, 'bill_summary.html', {
            'purchase': purchase,
            'balance_denominations': balance_denominations,
            'items': purchase.purchaseitem_set.all()
        })

    # Render billing page with available products
    return render(request, 'billing_page.html', {'products': Product.objects.all()})


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

        count = remaining_balance // denomination.value
        if count > 0:
            result[denomination.value] = int(count)
            remaining_balance %= denomination.value

    return result


def send_invoice_email(email, purchase, balance_denominations):
    """
    Sends an invoice email to the customer.
    """
    subject = "Invoice for Your Purchase"
    message = f"""
    Thank you for your purchase!

    Total Price Without Tax: {purchase.total_price_without_tax}
    Total Tax: {purchase.total_tax}
    Net Price: {purchase.net_price}
    Balance Due: {purchase.balance_due}

    Balance Denominations:
    {', '.join(f'{key}: {value}' for key, value in balance_denominations.items())}
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])


def bill_summary(request, purchase_id):
    """
    Displays the bill summary for a given purchase.
    """
    # Fetch the purchase object by ID
    purchase = get_object_or_404(Purchase, id=purchase_id)
    

    # Calculate balance denominations dynamically
    balance_denominations = calculate_denominations(purchase.balance_due)

    # Ensure this action happens only for POST requests
    if request.method == "POST":
        # Send the invoice email
        send_invoice_email(purchase.customer_email, purchase, balance_denominations)

    # Render the bill summary page
    return render(request, 'bill_summary.html', {
        'purchase': purchase,
        'balance_denominations': balance_denominations,
        'items': purchase.purchaseitem_set.all()
    })
