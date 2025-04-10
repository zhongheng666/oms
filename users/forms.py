from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError

class CustomPasswordChangeForm(PasswordChangeForm):
    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise ValidationError('两次新密码输入不一致')
        return new_password2