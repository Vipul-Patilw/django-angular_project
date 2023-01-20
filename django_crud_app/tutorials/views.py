from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework import status, generics,viewsets
from tutorials.models import Tutorial
from tutorials.serializers import TutorialSerializer
import math
from datetime import datetime

# Create your views here.


class TutorialView(generics.GenericAPIView):
    serializer_class = TutorialSerializer
    queryset = Tutorial.objects.all()

    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("title")
        remove_all = request.GET.get("DELETE")
        tutorial = Tutorial.objects.all()
        total_tutorial = tutorial.count()
        if remove_all:
        	remove = tutorial.delete()
        	return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(remove[0])}, status=status.HTTP_204_NO_CONTENT)
        	
        if search_param:
            tutorial = tutorial.filter(title__icontains=search_param)
        serializer = self.serializer_class(tutorial[start_num:end_num], many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED) 
        else:
        	return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   



class TutorialDetail(generics.GenericAPIView):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer

    def get_tutorial(self, pk):
        try:
            return Tutorial.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        tutorial = self.get_tutorial(pk=pk)
        if tutorial == None:
            return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 

        serializer = self.serializer_class(tutorial)
        return JsonResponse(serializer.data)

    def patch(self, request, pk):
        tutorial = self.get_tutorial(pk)
        if tutorial == None:
            return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            tutorial, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    def delete(self, request, pk):
        tutorial = self.get_tutorial(pk)
        if tutorial == None:
            return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 

        tutorial.delete()
        return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


class TutorialPublish(generics.GenericAPIView):
    queryset = Tutorial.objects.all()
    serializer_class = TutorialSerializer
    def get(self, request):
	       tutorials = Tutorial.objects.filter(published=True)
	       serializer = self.serializer_class(tutorials,many=True)
	       return JsonResponse(serializer.data,safe=False)








#from django.shortcuts import render

# Create your views here.
#from django.shortcuts import render

#from django.http.response import JsonResponse
#from rest_framework.parsers import JSONParser 
#from rest_framework import status
# 
#from tutorials.models import Tutorial
#from tutorials.serializers import TutorialSerializer
#from rest_framework.decorators import api_view


#@api_view(['GET', 'POST', 'DELETE'])
#def tutorial_list(request):
#    if request.method == 'GET':
#        tutorials = Tutorial.objects.all()
#        
#        title = request.query_params.get('title', None)
#        if title is not None:
#            tutorials = tutorials.filter(title__icontains=title)
#        
#        tutorials_serializer = TutorialSerializer(tutorials, many=True)
#        return JsonResponse(tutorials_serializer.data, safe=False)
#        # 'safe=False' for objects serialization
# 
#    elif request.method == 'POST':
#        tutorial_data = JSONParser().parse(request)
#        tutorial_serializer = TutorialSerializer(data=tutorial_data)
#        if tutorial_serializer.is_valid():
#            tutorial_serializer.save()
#            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
#        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#    
#    elif request.method == 'DELETE':
#        count = Tutorial.objects.all().delete()
#        return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
# 
# 
#@api_view(['GET', 'PUT', 'DELETE'])
#def tutorial_detail(request, pk):
#    try: 
#        tutorial = Tutorial.objects.get(pk=pk) 
#    except Tutorial.DoesNotExist: 
#        return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 
# 
#    if request.method == 'GET': 
#        tutorial_serializer = TutorialSerializer(tutorial) 
#        return JsonResponse(tutorial_serializer.data) 
# 
#    elif request.method == 'PUT': 
#        tutorial_data = JSONParser().parse(request) 
#        tutorial_serializer = TutorialSerializer(tutorial, data=tutorial_data) 
#        if tutorial_serializer.is_valid(): 
#            tutorial_serializer.save() 
#            return JsonResponse(tutorial_serializer.data) 
#        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
# 
#    elif request.method == 'DELETE': 
#        tutorial.delete() 
#        return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
#    
#        
#@api_view(['GET'])
#def tutorial_list_published(request):
#    tutorials = Tutorial.objects.filter(published=True)
#        
#    if request.method == 'GET': 
#        tutorials_serializer = TutorialSerializer(tutorials, many=True)
#        return JsonResponse(tutorials_serializer.data, safe=False)