from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Home, name="Home"),
    path('about/', views.About, name="About"),
    path('products/', views.Brand, name="Brand"),
    path('specials/', views.Specials, name="Specials"),
    path('contact/', views.Contact, name="Contact"),
    path('register/', views.Register, name="Register"),
    path('show/<int:cate_id>/<int:prod_id>/', views.ShowProduct, name="Show"),
    path('addtocart/<int:cate_id>/<int:prod_id>/', views.AddToCart, name="AddToCart"),
    path('view-cart/', views.ViewCart, name="ViewCart"),
    path('empty-cart/', views.EmptyCart, name="EmptyCart"),
    path('delete-product/<int:cate_id>/<int:prod_id>/', views.DeleteProduct, name="DeleteProduct"),
    path('checkout/<int:cate_id>/<int:prod_id>', views.CheckOut, name="CheckOut"),
    path('process-payment/<int:cate_id>/<int:prod_id>/', views.Process_Payment, name='Process_Payment'),
    path('payment-done/<int:cate_id>/<int:prod_id>/', views.Payment_Done, name='Payment_Done'),
    path('payment-cancelled/',views.Payment_Cancelled, name='Payment_Cancelled'),
]

urlpatterns += [
    path('accounts/', include("django.contrib.auth.urls"))
]
