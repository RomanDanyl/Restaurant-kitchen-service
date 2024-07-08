from django import forms

from kitchen.models import DishType


class DishTypeForm(forms.ModelForm):
    class Meta:
        model = DishType
        fields = "__all__"
