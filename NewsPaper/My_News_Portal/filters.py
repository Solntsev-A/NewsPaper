from django_filters import FilterSet, DateTimeFilter, CharFilter
from django.forms.widgets import DateTimeInput
from .models import Post

class PostFilter(FilterSet):
    title = CharFilter(field_name='title', lookup_expr='icontains', label='по названию')

    categoryType = CharFilter(field_name='categoryType', lookup_expr='exact', label='по категории')

    added_after = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        label='позже указываемой даты',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        )
    )

    class Meta:
        model = Post
        fields = {}