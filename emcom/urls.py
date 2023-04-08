from . import views
from django.urls import path

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('accounts/login/', views.user_login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('business', views.my_business, name='business'),
    path('add_business', views.add_business, name='add_business'),
    path('business/<int:id>', views.business_detail, name='business_detail'),
    path('market', views.marketplace, name='marketplace'),
    path('delete/<int:item_id>', views.delete_item, name='delete_item'),
    path('update/<int:item_id>', views.update_item, name='update_item'),
]