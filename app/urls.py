import debug_toolbar

from django.contrib import admin
from django.urls import path, include
from budget_manager import views
from django.contrib.auth import views as auth
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView

urlpatterns = [

	path('admin/', admin.site.urls),
	path('__debug__/', include(debug_toolbar.urls)),

	path('', include('budget_manager.urls')),
	path('login/', LoginView.as_view(template_name='login.html'), name='login'),
	path('logout/', auth.LogoutView.as_view(template_name ='index.html'), name ='logout'),
	path('register/', views.register, name ='register'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
