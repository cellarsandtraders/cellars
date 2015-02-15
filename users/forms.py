from django.forms import ModelForm
from django.forms.fields import BooleanField
from users.models import CellarItem, UserProfile


class UserProfileForm(ModelForm):
    _required = ['username', 'first_name', 'last_name', 'email']
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        for key in self._required:
            self.fields[key].required = True

    class Meta:
        model = UserProfile
        fields = [
            'username', 'first_name', 'last_name', 'email', 'address',
            'address2', 'city', 'state', 'zipcode'
        ]


class CellarItemForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CellarItemForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            # To allow 'False' as a valid value
            if not isinstance(self.fields[key], BooleanField):
                self.fields[key].required = True

    class Meta:
        model = CellarItem
        fields = [
            'beer_id', 'beer_name', 'brewery_id', 'brewery_name',
            'style', 'abv', 'year', 'quantity', 'willing_to_trade', 'label'
        ]
