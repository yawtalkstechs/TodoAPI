from rest_framework import generics,permissions
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