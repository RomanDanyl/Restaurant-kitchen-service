from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from kitchen.models import Cook, DishType, Dish

User = get_user_model()


class CookCreationForm(UserCreationForm):
    cooked_dishes = forms.ModelMultipleChoiceField(
        queryset=Dish.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    specialties = forms.ModelMultipleChoiceField(
        queryset=DishType.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "specialties", "cooked_dishes"
        )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError('Username already exists.')
        return username


class DishCreationForm(forms.ModelForm):
    cooks = forms.ModelMultipleChoiceField(
        queryset=Cook.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Dish
        fields = "__all__"


class DishSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by name"
            }
        ),
    )


class CookSearchForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by username"
            }
        ),
    )
