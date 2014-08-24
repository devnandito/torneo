from django import template
from decimal import Decimal

register = template.Library()

def valid_numeric(arg):
    if isinstance(arg, (int, float, Decimal)):
        return arg
    try:
        return int(arg)
    except ValueError:
        return float(arg)

@register.filter
def sub(value, arg):
    """Subtracts the arg from the value."""
    try:
        return valid_numeric(value) - valid_numeric(arg)
    except (ValueError, TypeError):
        try:
            return value - arg
        except Exception:
            return ''
sub.is_safe = False

@register.filter
def suma(value, arg):
    """Sum the arg from the value."""
    try:
        return valid_numeric(value) + valid_numeric(arg)
    except (ValueError, TypeError):
        try:
            return value + arg
        except Exception:
            return ''
suma.is_safe = False

@register.filter
def cutstring(value, arg):
    string = value
    cut_string = string.split(arg)
    new_string = cut_string[0]
    return new_string

# def paginator(context, adjacent_pages=2):
#         page_numbers = [n for n in \
#                         range (context['page'] - adjacent_pages, 
#                             context['page'] + adjacent_pages + 1) \
#                         if n > 0 and n <= context['page']]
#         return {
#             'hits': context['hits'],
#             'results_per_page': context['results_per_page'],
#             'page': context['page'],
#             'pages': context['pages'],
#             'page_numbers': page_numbers,
#             'next': context['next'],
#             'previous': context['previous'],
#             'has_next': context['has_next'],
#             'has_previous': context['has_previous'],
#             'show_first': 1 not in page_numbers,
#             'show_last': context['pages'] not in page_numbers,
#         }
# register.inclusion_tag('paginator.html', takes_context=True)(paginator)

# def render_paginator(context, first_last_amount=2, before_after_amount=4):
#     page_obj = context['page_obj']
#     paginator = context['paginator']
#     page_numbers = []

#     # Pages before current page
#     if page_obj.number > first_last_amount + before_after_amount:
#         for i in range(1, first_last_amount + 1):
#             page_numbers.append(i)

#         page_numbers.append(None)

#         for i in range(page_obj.number - before_after_amount, page_obj.number):
#             page_numbers.append(i)

#     else:
#         for i in range(1, page_obj.number):
#             page_numbers.append(i)

#     # Current page and pages after current page
#     if page_obj.number + first_last_amount + before_after_amount < paginator.num_pages:
#         for i in range(page_obj.number, page_obj.number + before_after_amount + 1):
#             page_numbers.append(i)

#         page_numbers.append(None)

#         for i in range(paginator.num_pages - first_last_amount + 1, paginator.num_pages + 1):
#             page_numbers.append(i)

#     else:
#         for i in range(page_obj.number, paginator.num_pages + 1):
#             page_numbers.append(i)

#     return {
#         'paginator': paginator,
#         'page_obj': page_obj,
#         'page_numbers': page_numbers
#     }

# register.inclusion_tag('paginator1.html', takes_context=True)(render_paginator)