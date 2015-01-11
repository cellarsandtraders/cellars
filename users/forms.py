from django.forms import ModelForm
from users.models import UserProfile


class UserProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True

    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'email']
