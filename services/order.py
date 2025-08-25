from django.db import transaction
from django.contrib.auth import get_user_model
from db.models import Order, Ticket

User = get_user_model()

def create_order(tickets: list[dict], username: str, date=None) -> Order:
    user = User.objects.get(username=username)
    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save(update_fields=["created_at"])
        for t in tickets:
            Ticket.objects.create(
                movie_session_id=t["movie_session"],
                order=order,
                row=t["row"],
                seat=t["seat"],
            )
        return order

def get_orders(username: str | None = None):
    qs = Order.objects.select_related("user")
    if username:
        qs = qs.filter(user__username=username)
    return qs
