from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Post
from .forms import PostForm
from .utils import check_for_word

def posts(request):
    '''
    view for list of posts
    '''
    user = request.user
    if user.is_authenticated:

        posts = Post.objects.filter().order_by('-published_date')

        return render(request, 'wall/posts.html', {'posts' : posts})
    else:
        messages.warning(request, 'You must be logged in to see that page')
        return redirect('login')

def post_detail(request, pk):

    user = request.user
    if user.is_authenticated:

        post = get_object_or_404(Post, pk=pk)

        return render(request, 'wall/post_detail.html', {'post': post})

    else:
        messages.warning(request, 'You must be logged in to see that page')
        return redirect('login')

def post_new(request):

    user = request.user
    if user.is_authenticated:

        if request.method == 'POST':

            form = PostForm(request.POST, request.FILES)

            if form.is_valid() and not check_for_word(form, "hack"):
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.write_on_chain()
                post.save()
                return redirect('post_detail', pk=post.pk)

            else:
                if check_for_word(form, "hack") == True:
                    messages.info(request, '\"hack\" word in posts is not allowed!!!')
                return render(request, 'wall/post_edit.html', {'form': form})

        else:
            form = PostForm()
            return render(request, 'wall/post_edit.html', {'form': form})
    else:
        messages.warning(request, 'You must be logged in to see that page')
        return redirect('login')

def user_profile(request, id):
    user = request.user
    if user.is_authenticated:
        if user.id == id:
            posts = Post.objects.filter(author_id=id)
            return render(request, 'wall/user_profile.html', {'posts': posts})
        else:
            messages.warning(request, 'You cannot access other users\' profile')
            return redirect('index')
    else:
        messages.info(request, 'You must be logged in to see that page')
        return redirect('login')

def post_edit(request, pk):

    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        if request.user.id == post.author_id:
            if request.method == 'POST':
                form = PostForm(request.POST, instance=post)
                if form.is_valid() and not check_for_word(form, "hack"):
                    post = form.save(commit=False)
                    post.author = request.user
                    post.published_date = timezone.now()
                    post.write_on_chain()
                    post.save()
                    return redirect('post_detail', pk=post.pk)

                else:

                    if check_for_word(form, "hack") == True:
                        messages.info(request, '\"hack\" word in posts is not allowed!!!')
                    return render(request, 'wall/post_edit.html', {'form': form})
            else:
                form = PostForm(instance=post)
                return render(request, 'wall/post_edit.html',{'form' : form })
        else:
            messages.warning(request, 'You cannot access other users\' profile')
            return redirect('index')
    else:
        messages.info(request, 'You must be logged in to see that page')
        return redirect('login')

def post_delete(request, pk):

    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        if request.user.id == post.author_id:
            id = post.author_id
            post.delete()
            posts = Post.objects.filter(author_id=id)

            return render(request, 'wall/user_profile.html', {'posts': posts})
        else:
            messages.warning(request, 'You cannot access other users\' profile')
            return redirect('index')
    else:
        messages.info(request, 'You must be logged in to see that page')
        return redirect('login')

def users_info(request):

    user = request.user
    if user.is_authenticated and user.is_staff:
        users_id = User.objects.filter().values_list('id', flat=True)
        details = []
        for id in users_id:
            count = len(Post.objects.filter(author_id=id))
            user = User.objects.get(id=id)
            username = user.username
            details.append([username, count])

        return render(request, 'wall/users_info.html', {'details': details})

    else:
        messages.info(request, 'You don\'t have necessary permissions to see this page')
        return redirect('login')

def json_response(request):

    this_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
    one_hour_later = this_hour + timedelta(hours=1)
    posts = Post.objects.filter(published_date__range=(this_hour, one_hour_later))

    response = []
    for post in posts:

        response.append(
            {
                'author': f"{User.objects.get(id=post.author_id).first_name} {User.objects.get(id=post.author_id).last_name}",
                'datetime' : post.published_date,
                'title' : post.title,
                'description' : post.description,
                'content' : post.content,
                'hash' : post.hash,
                'tx_id' : post.tx_id,
            })

    return JsonResponse(response, safe=False)

def string_response(request, response): #url "string_value"

    stringa = str(response)
    posts = Post.objects.all()

    count = 0
    for post in posts:

        count += post.title.lower().split().count(stringa) + post.description.lower().split().count(stringa) + post.content.lower().split().count(stringa)
    return HttpResponse(f"{count}")