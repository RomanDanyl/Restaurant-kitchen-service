from django.contrib.auth.forms import UserCreationForm

from kitchen.models import Cook


class CookCreationForm(UserCreationForm):
    class Meta:
        model = Cook
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "specialties", )
