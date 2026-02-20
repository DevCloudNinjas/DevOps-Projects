from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from apps.snippets.models import Snippet, Sales
from apps.snippets.serializers import SnippetSerializer, SalesSerializer
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
import math


@csrf_exempt
def snippet_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def snippet_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)


@csrf_exempt
def sales_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        sales = Sales.objects.all()
        serializer = SalesSerializer(sales, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SalesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class Snippets(generics.GenericAPIView):
    serializer_class = SnippetSerializer
    queryset = Snippet.objects.all()

    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("search")
        notes = Snippet.objects.all()
        total_notes = notes.count()
        if search_param:
            notes = notes.filter(title__icontains=search_param)
        serializer = self.serializer_class(notes[start_num:end_num], many=True)
        return Response({
            "status": "success",
            "total": total_notes,
            "page": page_num,
            "last_page": math.ceil(total_notes / limit_num),
            "notes": serializer.data
        })

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": {"note": serializer.data}}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        

class SnippetsViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving notes.
    """
    def list(self, request):
        queryset = Snippets.objects.all()
        serializer = SnippetSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset =Snippets.objects.all()
        notes = get_object_or_404(queryset, pk=pk)
        serializer = SnippetSerializer(notes)
        return Response(serializer.data)