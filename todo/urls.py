from django.urls import path
from . import views

app_name = "todo"
urlpatterns = [
    path("",views.index, name="index"),
    # path("login/", views.login_page, name="login"),
    # path("register/", views.register_page, name="register"),
    # path("logout/", views.logout_page, name="logout"),
    path("add_task/",views.add_task, name="add_task"),
    path("update_task/<task_id>",views.update_task, name="update_task"),
    path("completed/<task_id>", views.mark_as_completed, name="mark_as_completed"),
    path("delete_task/<task_id>", views.delete_task, name="delete_task")
]