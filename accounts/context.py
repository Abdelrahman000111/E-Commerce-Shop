from .models import Profile
def pro(request , profile = None):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
    return {'profile': profile,}