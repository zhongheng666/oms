from django.urls import path
from .views import CustomLoginView
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordChangeForm

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('change-password/', auth_views.PasswordChangeView.as_view(
        template_name='users/change_password.html',
        success_url='/tickets',
        form_class=CustomPasswordChangeForm  # 使用自定义表单
    ), name='change_password'),
]