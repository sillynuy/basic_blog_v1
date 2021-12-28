from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:post_id>', views.post_details, name='post'),
    path('add', views.post_add, name='post_add'),
    path('most_rated', views.most_rated, name='most_rated'),
    path('<int:post_id>/edit', views.post_edit, name='post_edit'),
    path('<int:post_id>/delete', views.post_delete, name='post_delete'),
    path('most_commented', views.most_commented, name='most_commented'),
]
