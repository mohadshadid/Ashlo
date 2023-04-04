from django.urls import path
from . import views
urlpatterns = [
    path('', views.main),
    path('login', views.login),
    path('login_form', views.login_form),
    path('register', views.register),
    path('registration', views.registration),
    path('boys',views.boys),
    path('girls', views.girls),
    path('view/<id>',views.view_cloth),
    path('checkout', views.checkout),
    path('admin', views.admin),
    path('create_cloth',views.create_cloth),
    path('add_to_cart/<id>', views.add_to_cart),
    path('cart',views.cart),

]