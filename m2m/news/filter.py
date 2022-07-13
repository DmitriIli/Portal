import django_filters
from django_filters import FilterSet
from .models import Post


# Создаем свой набор фильтров для модели Post.
class NewsFilter(FilterSet):
    # date = django_filters.DateTimeFilter(field_name='datetime_of_topic', lookup_expr='gt')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    types_of_topic = django_filters.CharFilter(field_name='types_of_topic', lookup_expr='iexact')

    # author = django_filters.NumberFilter(field_name='author_id', lookup_expr='exact')

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = ['title', 'types_of_topic']
