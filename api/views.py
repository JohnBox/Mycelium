from django.shortcuts import render_to_response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.generic.base import View
from django.db.models import Q
from rest_framework.renderers import JSONRenderer

from .models import User
from .serializers import UserSerializer


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
        serializer = UserSerializer(user.contacts, many=True)
        return JsonResponse({'a': serializer.data})


'''
@csrf_exempt
def addcontacttouser(request):
    if request.method == 'POST':
        contact = User.objects.get(username=request.POST['contact'])
        user = User.objects.get(username=request.POST['user'])
        creator = Contact(user=user, contact=contact, creator=True)
        creator.save()
        joined = Contact(user=contact, contact=user, creator=False)
        joined.save()
        return JsonResponse({'a': True})
    return None

@csrf_exempt
def getuserprofile(request):
    if request.method == 'POST':
        username = request.POST['username']
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        conv = lambda up: {'first_name': up.user.first_name,
                           'last_name': up.user.last_name,
                           'email': up.user.email,
                           'workplace': up.workplace,
                           'position': up.position
                           }
        return JsonResponse({'a': conv(user_profile)})
    return None

@csrf_exempt
def setuserprofile(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        user = User.objects.get(username=username)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        user_profile = UserProfile.objects.get(user=user)
        user_profile.workplace = request.POST['workplace']
        user_profile.position = request.POST['position']
        user_profile.save()
        return JsonResponse({'a': True})
    return None
'''
