from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from kitchen.models import Cook, Dish, DishType


@login_required
def index(request):
    """View function for home page of site."""

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()
    num_dish_types = DishType.objects.count()

    context = {
        "num_visits": num_visits + 1,
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_dish_types": num_dish_types,
    }
    return render(request, "kitchen/index.html", context=context)
