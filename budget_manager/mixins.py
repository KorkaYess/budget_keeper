from budget_manager.models import ProxyUser, User

class UserProxyMixin():

    def proxy_access_fn(self, request):
        return ProxyUser.objects.get(id=request.user.id)


    setattr(User, 'proxy', property(proxy_access_fn))