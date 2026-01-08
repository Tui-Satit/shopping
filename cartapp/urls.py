from django.urls import path
from cartapp import views3

urlpatterns=[
    path("cart",views3.cart),
    path("cart/add/<int:product_id>",views3.addCart,name="addCart"),
    path("cart/remove/<int:prodoct_id>",views3.removeCart,name="removeCart"),
]