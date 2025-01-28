from django import template

register = template.Library()

@register.filter
def calc_total(denominations):
    """
    Calculate the grand total for all denominations.
    """
    return sum(denomination.total_amount for denomination in denominations)
