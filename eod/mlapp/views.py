import pandas as pd
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from deviceapp.functions import save_device_status
from .functions import predict_class

api_key = '94cea4adae3c452ebd3c2ff10dd54d7c'

# Create your views here.
class Helloml(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        string = 'Hello, ML'
        content = {'message': string}
        return Response(content)


class PredictSmell(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            if request.META["HTTP_OCP_APIM_SUBSCRIPTION_KEY"] == api_key:
                device_id = request.data["device_id"]
                rows = request.data["rows"]
                df = pd.DataFrame(rows, columns = ['id',"time","temp","pres","co", "lpg", "smoke"])
                # df.to_csv("datafile.csv", index = False)
                smell_class, category = predict_class(df)
                content={
                    "device_id": device_id,
                    "avg_pres": round(df["pres"].mean(),2),
                    "avg_temp": round(df["temp"].mean(),2),
                    "avg_co": int(df["co"].mean()),
                    "avg_lpg": int(df["lpg"].mean()),
                    "avg_smoke": int(df["smoke"].mean()),
                    "smell_class": smell_class,
                    "category": category
                    }
                if save_device_status(content):
                    status = 200
                else:
                    content = {
                    "message": "Error Occurred while saving data. Pls Try Again",
                    }
                    status = 400
            else:
                content = {
                "message": "Sorry You can't send request to this source",
                }
                status = 401
        except:
            content = {
            "message": "Error Occurred Send Correct Data",
            }
            status = 400
        print(content)
        return Response(data = content, status = status)
