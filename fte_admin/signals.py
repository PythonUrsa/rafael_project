from django.dispatch import Signal

new_order = Signal(providing_args=['order'])