from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("services/", views.services, name="services"),
    path("about/", views.about, name="about"),
    path("prodlist/<str:pk>", views.prodlist, name="prodlist"),
    path("ent/", views.addEnt, name="entrepreneurs"),
    path("edit_ent/", views.edit_ent, name="edit_ent"),
    path("part/", views.addPart, name="partners"),
    path("addprod/", views.addProd, name="addproduct"),
    path("editprod/<str:pk>", views.editProd, name="editproduct"),
    path("delprod/<str:pk>", views.delprod, name="deleteproduct"),
    path("prod/<str:pk>", views.product, name="product"),
    path("product/<str:pk>", views.productdash, name="productdash"),
    path("regAs/", views.registerAs, name="regAs"),
    path("conf/", views.confirmation, name="conf"),
    path("ent_dash/", views.ent_dash, name="ent_dash"),
    path("bp_dash/", views.bp_dash, name="productsdash"),
    path("admin_dash/", views.admin_dash, name="admin_dash"),
    path("pen_bps/", views.pending_bps, name="pen_bps"),
    path("pen_ents/", views.pending_ents, name="pen_ents"),
    path("view_ent/<str:pk>", views.view_ent, name="view_ent"),
    path("view_bp/<str:pk>", views.view_bp, name="view_bp"),
    path("accept_ent/<str:pk>", views.accept_ent, name="accept_ent"),
    path("reject_ent/<str:pk>", views.reject_ent, name="reject_ent"),
    path("accept_bp/<str:pk>", views.accept_bp, name="accept_bp"),
    path("reject_bp/<str:pk>", views.reject_bp, name="reject_bp"),
]
