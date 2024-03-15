import math
import requests
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django.conf import settings
from django.core.files import File
from rest_framework import status, generics
from .models import Wishmodel
from rest_framework.response import Response
from rest_framework.permissions import  IsAuthenticated
from .serializers import Wishserializer, TextSerializer
import datetime

# Create your views here.
# class HomeView(generics.ListAPIView):
#     queryset = Wishmodel.objects.all()
#     serializer_class = TextSerializer

#     def create(self, request, *args, **kwargs):
#         data = request.data
#         serialized = TextSerializer(data=data)
#         if serialized.is_valid():
#             serialized.save()
#             return Response(serialized.data, status=status.HTTP_201_CREATED)
#         return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


# class Summ(APIView):
#
#     def get_summ_category(self, expense_list, category):
#         expenses = expense_list.filter(category = category)
#         summ=0
#         for expense in expenses:
#             summ += expense.summ
#         return {"summ":str(summ)}
#
#     def get_category(self, expense):
#             return expense.category
#
#     def get(self, request, *args, **kwargs):
#         ayear = datetime.date.today()-datetime.timedelta(weeks=52)
#         expenses = Wishmodel.objects.filter(author=request.user, date_of_send__gte=ayear, date_of_send__lte=datetime.date.today())
#         final = {}
#         categories = list(set(map(self.get_summ_category, expenses)))
#         for expense in expenses:
#             for category in categories:
#                 final[category]=self.get_summ_category(category, expense)
#                 print(f'{final[category]}')
#
#         return Response({"category":final}, status=status.HTTP_200_OK)


class WishesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Wishmodel.objects.all()
    serializer_class = Wishserializer

    def get_queryset(self):
        return Wishmodel.objects.filter(author=self.request.user)
    

class TextView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(request_body=Wishserializer)
    
    def post(self, request, *args, **kwargs):

        ser = Wishserializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()

        txt = request.data.get('text', False)


        audios = []
        for text in self.smart_split_text_by_limit(txt):
            audio = self.generate_audio(text)
            audios.append(audio)

        wish = Wishmodel.objects.get(id=ser.data['id'])
        wish.author = request.user
        wish.save()

        response = Response(audios, status=status.HTTP_200_OK)
        return response

    def generate_audio(self, text):
        API_URL = "https://tts.nutq.uz/api/v1/cabinet/synthesize/?t="
        response = requests.request("GET", API_URL + text)
        now = datetime.datetime.now()
        name = str(now.strftime("%H%M%S%d%m%Y"))
        filename = settings.MEDIA_ROOT + name + '.wav'
        print(filename)
        with open(filename, 'wb+', ) as file:
            file.write(response.content)
            File(open(filename, 'rb+'))
            f = str(filename)[27:]
        return f
        # return filename

    def smart_split_text_by_limit(self, txt, limit=418, near_stop=100):
        total_parts = math.ceil(len(txt) / limit)
        for _ in range(total_parts):
            part = txt[limit - near_stop:limit]
            dot_index = part[::-1].find('.')
            comma_index = part[::-1].find(',')
            exclamation_index = part[::-1].find('!')
            question_index = part[::-1].find('?')
            semicolon_inxed = part[::-1].find(';')
            if dot_index >= 0:
                p = txt[:limit - (dot_index)]
                yield p
                txt = txt[limit - (dot_index):]
            elif exclamation_index >= 0:
                p = txt[:limit - (exclamation_index)]
                yield p
                txt = txt[limit - (exclamation_index):]
            elif question_index >= 0:
                p = txt[:limit - (question_index)]
                yield p
                txt = txt[limit - (question_index):]

            elif semicolon_inxed >= 0:
                p = txt[:limit - (semicolon_inxed)]
                yield p
                txt = txt[limit - (semicolon_inxed):]

            elif comma_index >= 0:
                p = txt[:limit - (comma_index)]
                yield p
                txt = txt[limit - (comma_index):]

            elif txt[:limit + 1][-1].isalpha():
                space_index = part[::-1].find(' ')
                if space_index >= 0:
                    prob_text = txt[:limit - space_index]
                    yield prob_text
                    txt = txt[(limit - space_index):]
                else:
                    yield txt[:limit]
                    txt = txt[limit:]
            else:
                yield txt[:limit]
                txt = txt[limit:]




class ListenVoiceView(APIView):
    permission_classe = [IsAuthenticated]
    serializer_class = TextSerializer

    @swagger_auto_schema(request_body=TextSerializer)
    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            txt = serializer.data.get('text', False)

        audios = []
        for text in self.smart_split_text_by_limit(txt):
            audio = self.generate_audio(text)
            audios.append(audio)
        response = Response(audios, status=status.HTTP_200_OK)
        return response


    def generate_audio(self, text):
        API_URL = "https://tts.nutq.uz/api/v1/cabinet/synthesize/?t="
        response = requests.request("GET", API_URL + text)
        now = datetime.datetime.now()
        name = str(now.strftime("%H%M%S%d%m%Y"))
        filename = settings.MEDIA_ROOT + name + '.wav'
        print(filename)
        with open(filename, 'wb+', ) as file:
            file.write(response.content)
            File(open(filename, 'rb+'))
            f = str(filename)[27:]
        return f
        # /opt/tabriknoma.uz-backend

    def smart_split_text_by_limit(self, txt, limit=418, near_stop=100):
        total_parts = math.ceil(len(txt) / limit)
        for _ in range(total_parts):
            part = txt[limit - near_stop:limit]
            dot_index = part[::-1].find('.')
            comma_index = part[::-1].find(',')
            exclamation_index = part[::-1].find('!')
            question_index = part[::-1].find('?')
            semicolon_inxed = part[::-1].find(';')
            if dot_index >= 0:
                p = txt[:limit - (dot_index)]
                yield p
                txt = txt[limit - (dot_index):]
            elif exclamation_index >= 0:
                p = txt[:limit - (exclamation_index)]
                yield p
                txt = txt[limit - (exclamation_index):]
            elif question_index >= 0:
                p = txt[:limit - (question_index)]
                yield p
                txt = txt[limit - (question_index):]

            elif semicolon_inxed >= 0:
                p = txt[:limit - (semicolon_inxed)]
                yield p
                txt = txt[limit - (semicolon_inxed):]

            elif comma_index >= 0:
                p = txt[:limit - (comma_index)]
                yield p
                txt = txt[limit - (comma_index):]

            elif txt[:limit + 1][-1].isalpha():
                space_index = part[::-1].find(' ')
                if space_index >= 0:
                    prob_text = txt[:limit - space_index]
                    yield prob_text
                    txt = txt[(limit - space_index):]
                else:
                    yield txt[:limit]
                    txt = txt[limit:]
            else:
                yield txt[:limit]
                txt = txt[limit:]
