from django.contrib.auth import get_user

def user_id(request):
    user = get_user(request)
    return {'user_id': user.id}
