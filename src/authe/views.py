from django.shortcuts import render
from django.contrib.auth import authenticate, login

from .models import Author, ConfirmCode
from .forms import AuthorRegisterForm, LoginForm
from .utils import send_verified_link

# Create your views here.


# -------- register --------
def register(request):
    form = AuthorRegisterForm
    if request.method == 'POST':
        save_form = AuthorRegisterForm(request.POST)

        # If author with such data is already exists
        if Author.objects.filter(email=request.POST['email'], verified=True) or Author.objects.filter(username=request.POST['username'], verified=True):
            return render(request, 'register.html', {'form': form, 'error_message': 'Пользователь с таким именем или почтой уже существует'})

        # If existing author isn't verified
        if Author.objects.filter(email=request.POST['email'], verified=False):
            author = Author.objects.get(email=request.POST['email'])
            author.codes.all().delete()
            code = ConfirmCode.objects.create(author=author)
            send_verified_link(f'Чтобы подтвердить почту, перейдите по ссылке http://127.0.0.1:8000/auth/confirm/{code.code}/', code.author.email)
            return render(request, 'reply.html', context={'success_message':'Проверьте вашу почту'})

        # Successful registration
        if save_form.is_valid:
            author = Author.objects.create(
                username = request.POST['username'],
                password = request.POST['password'],
                email = request.POST['email'],
                )
            code = ConfirmCode.objects.create(author=author)
            send_verified_link(f'Чтобы подтвердить почту, перейдите по ссылке http://127.0.0.1:8000/auth/confirm/{code.code}', code.author.email)
            return render(request, 'reply.html', context={'success_message':'Проверьте вашу почту'})
    return render(request, 'register.html', {'form': form})


# -------- confirm --------
def confirm(request, code):
    if ConfirmCode.objects.filter(code=code):
        code = ConfirmCode.objects.get(code=code)
        if not code.confirm:
            code.confrim = True
            code.save()
            code.author.verified = True
            code.author.save()
            return render(request, 'reply.html', {'success_message': 'Ваша почта подтверждена', 'success': True})
        return render(request, 'reply.html', {'success_message': 'Ваша почта уже подтверждена', 'success': True})
    return render(request, 'reply.html', {'error_message': 'Ваш код подтверждения устарел, либо неправильный', 'success': True})


# -------- login --------
def login(request):
    form = LoginForm()
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            if user.is_active:
                # Successful log in
                login(request, user)
                return render(request, 'reply.html', {'form':form, 'success_message': 'Вы вошли в аккаунт', 'success':True})

            # Disabled account error
            return render(request, 'reply.html', {'form':form, 'error_message': 'Аккаунт не активен', 'success':True})

        # Invalid login error
        return render(request, 'login.html', {'form':form, 'error_message': 'Такого пользователя не существует', 'success':False})

    return render(request, 'login.html', {'form': form})
    