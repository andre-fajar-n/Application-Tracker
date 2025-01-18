from django import template

register = template.Library()

@register.filter
def toggle_sort_direction(current_direction):
    return "asc" if current_direction == "desc" else "desc"

@register.filter
def show_arrow_order_by(current_direction):
    return "fa-arrow-up" if current_direction == "asc" else "fa-arrow-down"