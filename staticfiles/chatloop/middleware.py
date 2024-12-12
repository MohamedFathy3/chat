from django.utils.translation import override
from django.http import HttpResponseForbidden
from chatloop.models import BlockedBrowser


class ArabicAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # التأكد من أن الطلب مرتبط بلوحة التحكم
        if request.path.startswith('/admin/'):
            with override('ar'):
                response = self.get_response(request)
        else:
            response = self.get_response(request)
        return response



