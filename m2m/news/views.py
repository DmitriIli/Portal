import requests
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.mail import send_mail
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from .filter import *


# Create your views here.

class NewsList(ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'news/news.html'
    ordering = '-date'
    paginate_by = 10

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewsFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class DetailList(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'news/detail.html'

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            return redirect('news')
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        user = self.request.user
        post = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        if user.is_authenticated:
            category_list = [i.name for i in Post.objects.get(pk=post).post_category.all()]
            user_category = User.objects.get(pk=user.id).subscribers_set.all()
            category_sub = [i.category.name for i in user_category]
            context['cat'] = list(set(category_list).difference(set(category_sub)))
            context['auth'] = True
        else:
            context['auth'] = False

        return context

    def post(self, request, *args, **kwargs):

        user = request.user
        post = self.kwargs.get('pk')

        if user.is_authenticated:
            category_list = [i.name for i in Post.objects.get(pk=post).post_category.all()]
            user_category = User.objects.get(pk=user.id).subscribers_set.all()
            category_sub = [i.category.name for i in user_category]
            sub_cat = list(set(category_list).difference(set(category_sub)))
        if request.POST:
            for item in sub_cat:
                if item in request.POST:
                    cat_id = Category.objects.get(name__iexact=f'{item}')
                    subscriber = Subscribers(
                        user=user,
                        category=cat_id
                    )
                    subscriber.save()
                    break
        return redirect('/')


class CreatePost(PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'news/create.html'
    permission_required = ('news.add_post')
    fields = [
        'author',
        'types_of_topic',
        'title',
        'text',
        'post_category'
    ]


class EditPost(PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'news/create.html'
    permission_required = ('news.change_post')
    fields = [
        'author',
        'types_of_topic',
        'title',
        'text',
        'post_category'
    ]

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            return redirect('search')
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('news')
    template_name = 'news/delete.html'
    permission_required = ('news.delete_post')

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            return redirect('search')
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class Redirect(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'accounts/logout.html'

    def get_redirect_url(self, *args, **kwargs):
        return super().get_redirect_url(*args, **kwargs)
