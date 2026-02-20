from django.urls import path
from apps.snippets import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import Snippets
urlpatterns = [
    path('', views.snippet_list),
    path('apiview/', Snippets.as_view()),
    path('<int:pk>/', views.snippet_detail),
    path('sales/', views.sales_list),

]

urlpatterns = format_suffix_patterns(urlpatterns)
