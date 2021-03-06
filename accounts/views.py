from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash, get_user_model
from .forms import UserCustomChangeForm, UserCustomCreationForm


# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('boards:index')
    if request.method == 'POST':
        form = UserCustomCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('boards:index')
    else:
        form = UserCustomCreationForm()
    context = {'form': form}
    return render(request, 'accounts/auth_form.html', context)
    
    
def login(request):
    if request.user.is_authenticated:
        return redirect('boards:index')
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.POST.get('next') or 'boards:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
        'next': request.GET.get('next', ''),
    }
    return render(request, 'accounts/login.html', context)
    

def logout(request):
    auth_logout(request)
    return redirect('boards:index')


def delete(request):
    user = request.user
    if request.method == 'POST':
        # DELETE
        user.delete()
    return redirect('boards:index')


def edit(request):
    if request.method == 'POST':
        # 수정 로직 진행
        form = UserCustomChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('boards:index')
    else:
        form = UserCustomChangeForm(instance=request.user)
    context = {'form': form, }
    return render(request, 'accounts/auth_form.html', context)
    
    
def change_password(request):
    if request.method == 'POST':
        # 인자 순서 유의
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # 비밀번호 변경하고 나서 로그아웃 되는거 막아줌. 바꾸고 나서 계속 진행.
            update_session_auth_hash(request, user)
            return redirect('boards:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form': form,}
    return render(request, 'accounts/auth_form.html', context)
    

def profile(request, user_pk):
    user_info = get_object_or_404(get_user_model(), pk=user_pk)
    context = {
        'user_info': user_info
    }
    return render(request, 'accounts/profile.html', context)
