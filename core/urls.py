from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/profile/', views.UserProfileView.as_view(), name='profile'),
    path('adverts/', views.JobAdvertListView.as_view(), name='jobadvert-list'),
    path('adverts/<int:pk>/', views.JobAdvertDetailView.as_view(), name='jobadvert-detail'),
    path('adverts/create/', views.JobAdvertCreateView.as_view(), name='jobadvert-create'),
    path('adverts/<int:pk>/update/', views.JobAdvertUpdateView.as_view(), name='jobadvert-update'),
    path('adverts/<int:pk>/delete/', views.JobAdvertDeleteView.as_view(), name='jobadvert-delete'),
    path('adverts/<int:job_advert_id>/apply/', views.JobApplicationCreateView.as_view(), name='jobapplication-create'),
    path('applications/', views.JobApplicationListView.as_view(), name='jobapplication-list'),
    path('applications/<int:pk>/', views.JobApplicationDetailView.as_view(), name='jobapplication-detail'),
    path('applications/<int:pk>/update/', views.JobApplicationUpdateView.as_view(), name='jobapplication-update'),
    path('skills/', views.SkillListView.as_view(), name='skill-list'),
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('', views.api_root, name='api-root'),
]
