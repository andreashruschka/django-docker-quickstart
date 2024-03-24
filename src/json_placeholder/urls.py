from . import views

from django.urls import path


urlpatterns = [
    path("", views.api_overview, name="home"),
    path("login/", views.LoginView.as_view(), name="login"),

    path("post/create/", views.add_post, name="add-post"),
    path('post/all/', views.view_post, name='view-post'),
    path('post/update/<int:pk>/', views.update_post, name='update-post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete-post'),

    path("comment/create/", views.add_comment, name="add-comment"),
    path('comment/all/', views.view_comment, name='view-comment'),
    path('comment/update/<int:pk>/', views.update_comment, name='update-comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete-comment'),

]
