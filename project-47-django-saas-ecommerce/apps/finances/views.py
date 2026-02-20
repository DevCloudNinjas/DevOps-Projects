import os
import datetime
import math
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.views import View

from .models import Account, Category, Transaction
from .serializer import (
    AccountSerializer,
    CategorySerializer,
    TransactionEditableSerializer,
    TransactionSerializer,
)

# Celery and Redis Cache File Upload
from django import forms
# from celery import current_app
# from .tasks import make_thumbnails




# File Upload with Celery start here
# class FileUploadForm(forms.Form):
#     image_file = forms.ImageField(required=True)

# class HomeView(View):
#     def get(self, request):
#         form = FileUploadForm()
#         return render(request, 'finances/home.html', { 'form': form })
    
#     def post(self, request):
#         form = FileUploadForm(request.POST, request.FILES)
#         context = {}

#         if form.is_valid():
#             file_path = os.path.join(settings.IMAGES_DIR, request.FILES['image_file'].name)

#             with open(file_path, 'wb+') as fp:
#                 for chunk in request.FILES['image_file']:
#                     fp.write(chunk)

#             task = make_thumbnails.delay(file_path, thumbnails=[(128, 128)])

#             context['task_id'] = task.id
#             context['task_status'] = task.status

#             return render(request, 'finances/home.html', context)

#         context['form'] = form

#         return render(request, 'finances/home.html', context)


# class TaskView(View):
#     def get(self, request, task_id):
#         task = current_app.AsyncResult(task_id)
#         response_data = {'task_status': task.status, 'task_id': task.id}

#         if task.status == 'SUCCESS':
#             response_data['results'] = task.get()

#         return JsonResponse(response_data)
    
# File Upload with Celery Ends Here


# Account Generic View
class Accounts(generics.GenericAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()

    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("search")
        accounts = Account.objects.all()
        total_accounts = accounts.count()
        if search_param:
            accounts = accounts.filter(title__icontains=search_param)
        serializer = self.serializer_class(accounts[start_num:end_num], many=True)
        return Response({
            "status": "success",
            "total": total_accounts,
            "page": page_num,
            "last_page": math.ceil(total_accounts / limit_num),
            "notes": serializer.data
        })

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": {"note": serializer.data}}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# Transactions Generic View
class Transactions(generics.GenericAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("search")
        transactions = Transaction.objects.all()
        total_transactions = transactions.count()
        if search_param:
            transactions = transactions.filter(title__icontains=search_param)
        serializer = self.serializer_class(transactions[start_num:end_num], many=True)
        return Response({
            "status": "success",
            "total": total_transactions,
            "page": page_num,
            "last_page": math.ceil(total_transactions / limit_num),
            "notes": serializer.data
        })

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": {"note": serializer.data}}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


#  Category Generic View
class  Categories(generics.GenericAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("search")
        categories = Category.objects.all()
        total_categories = categories.count()
        if search_param:
            categories = categories.filter(title__icontains=search_param)
        serializer = self.serializer_class(categories[start_num:end_num], many=True)
        return Response({
            "status": "success",
            "total": total_categories,
            "page": page_num,
            "last_page": math.ceil(total_categories / limit_num),
            "notes": serializer.data
        })

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": {"note": serializer.data}}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)      
        
class AccountDetail(generics.GenericAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_note(self, pk):
        try:
            return Account.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        account = self.get_note(pk=pk)
        if account == None:
            return Response({"status": "fail", "message": f"Note with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(account)
        return Response({"status": "success", "data": {"note": serializer.data}})

    def patch(self, request, pk):
        account = self.get_note(pk)
        if account == None:
            return Response({"status": "fail", "message": f"Note with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            account, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['updatedAt'] = datetime.now()
            serializer.save()
            return Response({"status": "success", "data": {"note": serializer.data}})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        account = self.get_note(pk)
        if account == None:
            return Response({"status": "fail", "message": f"Note with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)       
        
class AccountDetail(generics.GenericAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_note(self, pk):
        try:
            return Account.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        account = self.get_note(pk=pk)
        if account == None:
            return Response({"status": "fail", "message": f"Note with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(account)
        return Response({"status": "success", "data": {"note": serializer.data}})

    def patch(self, request, pk):
        account = self.get_note(pk)
        if account == None:
            return Response({"status": "fail", "message": f"Note with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            account, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['updatedAt'] = datetime.now()
            serializer.save()
            return Response({"status": "success", "data": {"note": serializer.data}})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        account = self.get_note(pk)
        if account == None:
            return Response({"status": "fail", "message": f"Note with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# Viewset
class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
    


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_serializer_class(self):
        if self.action in ["update", "partial_update", "create"]:
            return TransactionEditableSerializer
        return TransactionSerializer
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer   