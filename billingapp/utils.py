from .models import Denomination

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
