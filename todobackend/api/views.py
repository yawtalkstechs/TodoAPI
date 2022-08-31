from django.db import IntegrityError
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

from rest_framework import generics,permissions
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from rest_framework import status

from .serializers import TodoSerializers, TodoToggleCompleteSerializer
from todo.models import Todo


''' TODOLISTCREATE the ff: 
# queryset - which allow us to filter by recently created.
# serializer_class - allow us to use the name of the serializers 
# which was created inside serializer module.
# permission_classess - ensures that only authenticated users 
# can view the information or data.
# perform_create - is called before the user is allowed to create todo.
'''

class TodoListCreate(generics.ListCreateAPIView):
    queryset = Todo.objects.filter().order_by('-created')
    serializer_class = TodoSerializers
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# permission_classess - ensures that only authenticated users 
# are allowed to perform CRUD functions

class TodoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializers


# perform_update - is called before the todo is allowed to be updated.
class TodoToggleComplete(generics.UpdateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoToggleCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.instance.completed=not(serializer.instance.completed)
        serializer.save()

'''
signup - check whether request.method is POST, request is converted into a JSON
    user.object.create_user create a user with username and password, then saves it.
    token - is use to create a user and when successfully created return a status 201
     otherwise return an error bad request

'''
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request) # data is a dictionary
            user = User.objects.create_user(
                username=data['username'],
                password=data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)},status=201)
            
        except IntegrityError:
            return JsonResponse({'error':'username taken. choose another username'},
                    status=400)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(
            request, 
            username=data['username'],
            password=data['password'])
            
        if user is None:
            return JsonResponse(
                {'error':'unable to login. check username and password'},
                status=400)
        else: # return user token
            try:
                token = Token.objects.get(user=user)
            except: # if token not in db, create a new one
                token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)}, status=201)