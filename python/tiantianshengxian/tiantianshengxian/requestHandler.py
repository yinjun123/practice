from django.http import HttpResponse

from users.models import UserInfo


class RequestHandler():

    def process_request(self, request):
        uid = request.session.get('uid', None)
        if uid is not None:
            userinfo = UserInfo.objects.filter(pk=uid)
            if userinfo:
                request.userinfo = userinfo[0]
            else:
                request.userinfo = None
        else:
            request.userinfo = None
