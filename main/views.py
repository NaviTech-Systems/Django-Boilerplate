from planner.settings import LOG_PATH
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
import json
from django.utils.timezone import now


# Create your views here.
class LogAdd(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        data.__setitem__("timestamp", now().isoformat())
        f = open(f"{LOG_PATH}/frontend.log.json", "a")
        f.write(json.dumps(data))
        f.write("\n")
        f.close()

        return JsonResponse({"detail": "OK"})
