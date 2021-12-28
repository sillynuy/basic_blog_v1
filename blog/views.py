from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.db.models import F
from django.core.paginator import Paginator
from django.db.models import Count, Min, Max

from .models import Comment, Post
from .forms import AddCommentForm, AddPostForm, SetMarkPostForm


def index(request):
    posts = Post.objects.all().order_by('-date_published')
    oldest_post_date = Post.objects.all().aggregate(Min('date_published'))['date_published__min']
    newest_post_date = Post.objects.all().aggregate(Max('date_published'))['date_published__max']
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'blog/index.html'
    context = {
        'posts': posts,
        'page_obj': page_obj,
        'oldest': oldest_post_date,
        'newest': newest_post_date,
    }
    return HttpResponse(render(request, template, context))


def post_details(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'GET':
        # template = 'blog/post_detailed.html'
        template = 'blog/post_detailed.html'
        mark_form = SetMarkPostForm()
        comment_form = AddCommentForm()
        mark_comment_form = SetMarkPostForm()
        comments = Comment.objects.filter(post=post_id)
        context = {
            'post': post,
            'mark_form': mark_form,
            'comment_form': comment_form,
            'comments': comments,
            'mark_comment_form': mark_comment_form,
        }
        return HttpResponse(render(request, template, context))
    else:
        if 'add_comment' in request.POST:
            author = request.POST.get('author')
            text = request.POST.get('text')
            new_comment = Comment(
                post=post,
                author=author,
                text=text,
                date_published=timezone.now()
            )
            new_comment.save()
            return HttpResponseRedirect(reverse('blog:post', args=(post_id,)))
        if 'set_mark_post' in request.POST:
            form = SetMarkPostForm(request.POST)
            val = request.POST.get("set_mark_post")
            if val == '+':
                Post.objects.filter(id=post_id).update(pos_marks=F("neg_marks") + 1)
            elif val == '-':
                Post.objects.filter(id=post_id).update(neg_marks=F("neg_marks") + 1)
            Post.objects.filter(id=post_id).update(rating=F("pos_marks") - F("neg_marks"))
            return HttpResponseRedirect(reverse('blog:post', args=(post_id,)))


def post_add(request):
    template_name = 'blog/new_post.html'
    if request.method == 'GET':
        add_post_form = AddPostForm()
        context = {
            'form': add_post_form,
        }
        return render(request, template_name, context)
    else:
        headline = request.POST.get('headline')
        text = request.POST.get('text')
        new_post = Post(
            headline=headline,
            text=text,
            date_published=timezone.now(),
            pos_marks=0,
            neg_marks=0
        )
        new_post.save()
        return HttpResponseRedirect(reverse('blog:index'))


def post_edit(request, post_id):
    template = 'blog/edit_post.html'
    post = Post.objects.get(id=post_id)
    if request.method == 'GET':
        edit_form = AddPostForm(
            initial={
                'headline': post.headline,
                'text': post.text,
            }
        )
        context = {
            'form': edit_form,
            'post': post,
        }
        return render(request, template, context)
    else:
        form = AddPostForm(request.POST)
        if form.is_valid():
            headline = form.cleaned_data['headline']
            text = form.cleaned_data['text']
            Post.objects.filter(id=post_id).update(
                headline=headline,
                text=text
            )
            return HttpResponseRedirect(reverse('blog:post', args=(post_id,)))


def post_delete(request, post_id):
    template = 'blog/delete_post.html'
    post = Post.objects.get(id=post_id)
    context = {
        'post': post,
    }
    if request.method == 'GET':
        return render(request, template, context)
    else:
        if 'post_delete_confirmation' in request.POST:
            val = request.POST.get('post_delete_confirmation')
            if val == 'Да':
                post.delete()
                return HttpResponseRedirect(reverse('blog:index'))
            else:
                return HttpResponseRedirect(reverse('blog:post', args=(post_id,)))


def most_rated(request):
    posts = Post.objects.all().order_by('-rating')[:3]
    context = {
        'posts': posts,
    }
    template = 'blog/most_rated.html'
    return HttpResponse(render(request, template, context))


def most_commented(request):
    posts = Post.objects.annotate(num_comms=Count('comment')).order_by('-num_comms')[:3]
    context = {
        'posts': posts,
    }
    template = 'blog/most_commented.html'
    return HttpResponse(render(request, template, context))


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'name.html', {'form': form})

