from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Message, Comment


def index(request):
    return render(request, 'index.html')


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            if key == 'log_email':
                messages.error(request, value, extra_tags='log_email')
            if key == 'log_password':
                messages.error(request, value, extra_tags='log_password')
        return redirect('/')
    else:
        user_list = User.objects.filter(email=request.POST['log_email'])
        if len(user_list) == 0:
            messages.error(
                request, "we could not find a user with that email address", extra_tags='log_email')
        else:
            user = user_list[0]
            if request.POST['log_password'] == user.password:
                request.session['user_id'] = user.id
                return redirect('/show_wall')
            else:
                messages.error(
                    request, "your password was incorrect", extra_tags="log_password")
                return redirect('/')

    return redirect(f'/show_wall/{user.id}')


def registration(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            if key == 'first_name':
                messages.error(request, value, extra_tags='first_name')
            if key == 'last_name':
                messages.error(request, value, extra_tags='last_name')
            if key == 'reg_email':
                messages.error(request, value, extra_tags='reg_email')
            if key == 'reg_password':
                messages.error(request, value, extra_tags='reg_password')
            if key == 'confirm_password':
                messages.error(request, value, extra_tags='confirm_password')
        return redirect('/')
    else:
        user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['reg_email'],
            password=request.POST['reg_password']
        )
        request.session['user_id'] = user.id


def show_wall(request):
    if "user_id" not in request.session:
        return redirect('/')
    
    else:
        context = {
            'this_user': User.objects.get(id=request.session['user_id']),
            'all_messages': Message.objects.all()
        }
        return render(request, "the_wall.html", context)

def message(request):
    errors = Message.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            if key == 'message_content':
                messages.error(request, value, extra_tags='message_content')
        return redirect('/show_wall')
    else:
        user = User.objects.get(id=request.session['user_id'])
        Message.objects.create(
            content= request.POST['message_content'],
            user_name = user
        )
        return redirect('/show_wall')
    
def comment(request):
    errors = Comment.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            if key == 'comment_content':
                messages.error(request, value, extra_tags='comment_content')
        return redirect('/show_wall')
    else:
        user = User.objects.get(id=request.session['user_id'])
        Comment.objects.create(
            parent_message = Message.objects.get(id=request.POST['message_id']),
            content= request.POST['comment_content'],
            user_name = user
        )
    return redirect("/show_wall")

def logout(request):
    request.session.flush()
    return redirect('/')
