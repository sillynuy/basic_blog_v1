from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse
from django.db.models import F
from django.core.paginator import Paginator
from django.db.models import Count, Min, Max
from django.contrib.auth.models import User

from .models import Comment, Post, UserPostMark
from .forms import AddCommentForm, AddCommentFormAuth, AddPostForm, SetMarkPostForm


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
    mark = None
    if request.method == 'GET':
        # template = 'blog/post_detailed.html'
        template = 'blog/post_detailed.html'
        mark_form = SetMarkPostForm()
        comment_form = AddCommentForm()
        comment_form_auth = AddCommentFormAuth()
        mark_comment_form = SetMarkPostForm()
        comments = Comment.objects.filter(post=post_id)
        mark_value = None
        user = request.user
        if isinstance(user, User):
            # получение текущей оценки поста
            try:
                mark = UserPostMark.objects.get(user=request.user, post=post)
            except UserPostMark.DoesNotExist:
                pass
            if mark is not None:
                mark_value = '+' if mark.mark_positive else '-'
        context = {
            'post': post,
            'mark_form': mark_form,
            'comment_form': comment_form,
            'comment_form_auth': comment_form_auth,
            'comments': comments,
            'mark_comment_form': mark_comment_form,
            'mark': mark_value,
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
        if 'add_comment_auth' in request.POST:
            user = request.user
            text = request.POST.get('text')
            new_comment = Comment(
                post=post,
                author=user,
                text=text,
                date_published=timezone.now()
            )
            new_comment.save()
            return HttpResponseRedirect(reverse('blog:post', args=(post_id,)))

        if 'set_mark_post' in request.POST:
            form = SetMarkPostForm(request.POST)

            marks = {
                '+': True,
                '-': False
            }

            user = request.user
            if isinstance(user, User):
                val = request.POST.get("set_mark_post")
                # проверить, есть ли в БД оценка
                try:
                    mark = UserPostMark.objects.get(user=request.user, post=post)
                except UserPostMark.DoesNotExist:
                    UserPostMark.objects.create(
                        post=post,
                        user=user,
                        mark_positive=marks[val]
                    )
                else:
                    UserPostMark.objects.update(
                        post=post,
                        user=user,
                        mark_positive=marks[val]
                    )
                # обновление рейтинга поста
                pos_marks = UserPostMark.objects.filter(post=post, mark_positive=True).count()
                neg_marks = UserPostMark.objects.filter(post=post, mark_positive=False).count()
                Post.objects.filter(id=post_id).update(pos_marks=pos_marks)
                Post.objects.filter(id=post_id).update(neg_marks=neg_marks)
                Post.objects.filter(id=post_id).update(rating=pos_marks-neg_marks)
                return HttpResponseRedirect(reverse('blog:post', args=(post_id,)))
            else:
                return HttpResponse('не авторизован')




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


def profile(request, user_id):
    user = User.objects.get(id=user_id)
    comments = Comment.objects.filter(author_id=user_id).order_by('-date_published')
    context = {
        'comments': comments,
        'user': user
    }
    template = 'blog/profile.html'
    return HttpResponse(render(request, template, context))

