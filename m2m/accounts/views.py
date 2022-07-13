from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm
from django.shortcuts import redirect
from django.views.generic import TemplateView
from news.models import Author


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class IndexView(TemplateView):
    template_name = 'accounts/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def make_author(request, username):
    user = request.user
    group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        group.user_set.add(user)
        author = Author(author=user)
        author.save()
    return redirect('/')
