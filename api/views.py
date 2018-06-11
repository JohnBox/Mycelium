from django.shortcuts import render_to_response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.generic.base import View
from django.db.models import Q
from rest_framework import generics

from .models import User, Group
from .serializers import UserSerializer, GroupSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class HomeView(View):
    def get(self, request):
        return render_to_response('index.html')


class SignInView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SignInView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        if user:
            login(request, user)
            serializer = UserSerializer(user)
            return JsonResponse({'a': serializer.data})
        else:
            return JsonResponse({'e': 'Невірний логін або пароль'})


class SignUpView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SignUpView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        users = User.objects.filter(
            Q(username=request.POST['username']) | Q(email=request.POST['email'])
        )
        if users:
            return JsonResponse({'e': 'Користувач з такими даними вже існує'})
        else:
            user = User.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password']
            )
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()
            return JsonResponse({'a': True})


class UsersListView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UsersListView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        username = request.POST['username']
        users = User.objects.exclude(username=username)
        search = request.POST.get('search')
        if search:
            users = users.filter(
                Q(username__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        serializer = UserSerializer(users, many=True)
        return JsonResponse({'a': serializer.data})


class ContactsListView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ContactsListView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        user = User.objects.get(username=request.POST['username'])
        contacts = UserSerializer(user.contacts, many=True).data
        rooms = GroupSerializer(user.groups.filter(root=False), many=True).data
        audiences = GroupSerializer(user.groups.filter(root=True), many=True).data
        return JsonResponse({'a': {
            'contacts': contacts,
            'rooms': rooms,
            'audiences': audiences
        }})


class UserEditView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(UserEditView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        pk = request.POST['pk']
        user = User.objects.get(pk=pk)
        user.username = request.POST['username']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.workplace = request.POST['workplace']
        user.position = request.POST['position']
        user.save()
        return JsonResponse({'a': True})


class CreateContactView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateContactView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        username = request.POST['user']
        contact_username = request.POST['contact']
        user = User.objects.get_by_natural_key(username)
        contact = User.objects.get_by_natural_key(contact_username)
        user.contacts.add(contact)
        user.save()
        return JsonResponse({'a': True})


class DeleteContactView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DeleteContactView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        username = request.POST['user']
        contact_username = request.POST['contact']
        user = User.objects.get_by_natural_key(username)
        contact = User.objects.get_by_natural_key(contact_username)
        user.contacts.remove(contact)
        user.save()
        return JsonResponse({'a': True})


class CreateGroupView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateGroupView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        name = request.POST['name']
        root = request.POST['root'] == 'true'
        username = request.POST['username']
        contacts = request.POST.getlist('contacts[]')
        user = User.objects.get_by_natural_key(username)
        group = Group(name=name, creator=user, root=root)
        group.save()
        for pk in contacts:
            contact = User.objects.get(pk=pk)
            group.members.add(contact)
        group.save()
        user.groups.add(group)
        user.save()
        return JsonResponse({'a': True})
