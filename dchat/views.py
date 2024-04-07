from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import LoginForm, UserRegistrationForm, SendMessageForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import Message
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import logout

def indexView(request):
    return render(request, 'index.html')

def user_unlogin(request):
    logout(request)
    return redirect("/")

@login_required(login_url='/')
def chatView(request):
    if request.method == 'POST':
        message_form = SendMessageForm(request.POST)
        if message_form.is_valid():
            # Create a new user object but avoid saving it yet
            Message.objects.create(user=request.user, content=message_form.cleaned_data['message'])
            return HttpResponseRedirect(request.path)
    else:
        message_form = SendMessageForm()
    messages = Message.objects.all()
    return render(request, 'chat.html', {'message_form': message_form, 'messages': messages})

def authView(request):
    if request.user.is_authenticated:
        return redirect('/chat')
    else:
        if request.method == 'POST':
            error={}
            form = LoginForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user = authenticate(username=cd['username'], password=cd['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect("/chat")
                    else:
                        
                        error["name"]="Disabled account"
                        error["description"] = "Пользователь заблокирован. Обратитесь к администратору"

                        return render(request, 'errors_form.html', {'error': error})
                else:
                    error["name"] = "Invalid login"
                    error["description"] = "Неверное имя пользователя или пароль"
                    return render(request, 'errors_form.html', {'error': error})
        else:
            form = LoginForm()
        return render(request, 'auth.html', {'form': form})
    
def registerView(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = form.save(commit=False)
            # Set the chosen password
            new_user.set_password(form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return redirect('/auth')
    else:
        form = UserRegistrationForm()
    return render(request, 'reg.html', {'form': form})
@xframe_options_exempt
def rawChatView(request):
    messages = Message.objects.all()
    return render(request, 'messages.html', {'messages': messages})

def apiView(request):
    return JsonResponse({"messages": len(Message.objects.all())})