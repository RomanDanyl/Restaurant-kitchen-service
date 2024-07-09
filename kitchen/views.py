from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from kitchen.forms import CookCreationForm
from kitchen.models import Cook, Dish, DishType


#@login_required
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


class DishTypeListView(generic.ListView):
    model = DishType
    template_name = "kitchen/dish_type_list.html"
    context_object_name = "dish_type_list"


class DishTypeDetailView(generic.DetailView):
    model = DishType

    def get_queryset(self):
        return DishType.objects.select_related("dishes").all()


class DishTypeCreateView(generic.CreateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")
    template_name = "kitchen/dish_type_form.html"


class DishTypeUpdateView(generic.UpdateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")
    template_name = "kitchen/dish_type_form.html"


class DishTypeDeleteView(generic.DeleteView):
    model = DishType
    success_url = reverse_lazy("kitchen:dish-type-list")


class CookListView(generic.ListView):
    model = Cook
    queryset = Cook.objects.prefetch_related("specialties")


class CookCreateView(generic.CreateView):
    model = Cook
    form_class = CookCreationForm


class CookDetailView(generic.DetailView):
    model = Cook


class CookUpdateView(generic.UpdateView):
    model = Cook
    form_class = CookCreationForm


class CookDeleteView(generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("kitchen:cook-list")


class DishListView(generic.ListView):
    model = Dish
    paginate_by = 3
    queryset = Dish.objects.select_related("dish_type").prefetch_related("cooks")


class DishCreateView(generic.CreateView):
    model = Dish
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-list")


class DishDetailView(generic.DetailView):
    model = Dish


class DishUpdateView(generic.UpdateView):
    model = Dish
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-list")


class DishDeleteView(generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("kitchen:dish-list")
