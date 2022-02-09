from django.urls import path, re_path, include
from django.views.generic.base import TemplateView
from django.conf import settings



from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signout", views.logout_user, name="logout"),

    path("login", views.login_user, name="login"),
    path("success", views.success, name="success"),  
    path("signup", views.signup, name="signup"),
    path("info", views.info, name="info"),  
    path("profile", views.profile, name="profile"),
    path("order/<int:order_pk>/", views.order, name="order"),
    path("options/<str:item_name>/<int:item_id>/", views.options, name="options"),
    path("pizza", views.pizza_menu, name="pizza"),
    path("pizza/tops", views.SendTops.as_view(), name="send_tops"),
    path("sessions", views.SendSession.as_view(), name="send_sessions"),
    path("status", views.Status.as_view(), name="status"),

    path("post_sessions", views.GetSession.as_view(), name="get_sessions"),
    path("fd_data", views.GetFd.as_view(), name="get_fd"),

    path("pz_data", views.GetPz.as_view(), name="get_pz"),
    path("test", views.test, name="test"),
    path("subs", views.subs_menu, name="subs"),
    path("pasta", views.pasta_menu, name="pasta"),
    path("salad", views.salad_menu, name="salads"),
    path("cart", views.cart, name="cart"),
    path("orders", views.orders, name="orders"),


    path("remove/<str:item_name>/<int:item_id>/", views.remove, name="remove"),


]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
