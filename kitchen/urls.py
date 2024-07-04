from django.urls import path

from kitchen.views import (
    index,
    DishTypeListView,
    DishTypeDetailView,
    DishTypeCreateView,
    DishTypeUpdateView,
    DishTypeDeleteView,
    CookListView,
)

urlpatterns = [
    path("", index, name="index"),
    path("dish-types", DishTypeListView.as_view(), name="dish-type-list"),
    path(
        "dish-types/<int:pk>",
        DishTypeDetailView.as_view(),
        name="dish-type-detail",
    ),
    path(
        "dish-types/create",
        DishTypeCreateView.as_view(),
        name="dish-type-create",
    ),
    path(
        "dish-types/<int:pk>/update",
        DishTypeUpdateView.as_view(),
        name="dish-type-update"
    ),
    path(
        "dish-types/<int:pk>/delete",
        DishTypeDeleteView.as_view(),
        name="dish-type-update"
    ),
    path("cooks/", CookListView.as_view(), name="cook-list"),
]
app_name = "kitchen"
