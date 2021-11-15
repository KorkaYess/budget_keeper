from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.views.generic import DetailView
from django.template.loader import get_template
from django.views.generic import TemplateView
from django.contrib.auth.models import User

from budget_manager.models import Account, ProxyUser
from budget_manager.forms import UserRegisterForm


def index(request):
	user = ProxyUser.objects.get(id=request.user.id)
	print(f'WHAT A DIFF BEETWEEN {type(request.user)} AND {type(user)}')
	context = {
        'title': 'Home page',
        'user': user,
		'total_amount': user.total_budget()
    }

	return render(request, 'index.html', context)


def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			html = get_template('email.html')
			subject, from_email, to = 'Welcome', 'your_email@gmail.com', email
			html_content = html.render({ 'username': username })
			msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			messages.success(request, f'Your account has been created! You are now able to log in')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'register.html', {'form': form, 'title':'Registration'})


# class MainPageView(TemplateView):
#     template_name = "account.html"

#     def get_context_data(self, request, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['user'] = request.user

#         return context
