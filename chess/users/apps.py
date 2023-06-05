from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

# class UserTable(AppConfig):
#     name = 'usertable'

#     def ready(self) -> None:
#         import 
