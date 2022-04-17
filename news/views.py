from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, ListView

from .forms import *


def index(request):
    search_request = request.GET.get('search', '')
    if search_request:
        posts = Post.objects.filter(Q(title__icontains=search_request) | Q(text__icontains=search_request) | Q(
            author__username__icontains=search_request) | Q(pub_date__icontains=search_request))
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, 2)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''
    context = {'posts_var': page,
               'is_paginated': is_paginated,
               'prev_url': prev_url,
               'next_url': next_url}
    return render(request, template_name='news/index.html', context=context)


def post_detail(request, id_post):
    try:
        post = Post.objects.get(id=id_post)
    except Post.DoesNotExist:
        raise Http404('Статья не найдена')
    comments = post.comment_set.all()

    paginator = Paginator(comments, 2)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''
    context = {'post': post, 'form': CommentForm,
               'comments_var': page,
               'is_paginated': is_paginated,
               'prev_url': prev_url,
               'next_url': next_url}
    return render(request, 'news/post_detail.html', context)


@permission_required('comment.can_add_comment')
@login_required
def add_comment(request, id_post):
    form = CommentForm(request.POST)
    post = get_object_or_404(Post, id=id_post)

    if form.is_valid():
        comment = Comment()
        comment.fk_post = post
        comment.author = request.user
        comment.text = form.cleaned_data['text']
        comment.save()
    return redirect(post.get_absolute_url())


class TagCreate(View):
    @staticmethod
    def get(request, *args, **kwargs):
        form = TagForm()
        return render(request, 'news/tag_create_form.html', {'form': form})

    @staticmethod
    def post(request, *args, **kwargs):
        filled_form = TagForm(request.POST)

        if filled_form.is_valid():
            tag = Tag()
            tag.name = filled_form.cleaned_data['name']
            tag.save()
            return redirect(reverse("index_url"))
        return render(request, 'news/tag_create_form.html', {'form': filled_form})


class PostCreate(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = ('post.can_add_post',)
    raise_exception = True

    @staticmethod
    def get(request, *args, **kwargs):
        form = PostForm()
        return render(request, 'news/post_create_form.html', {'form': form})

    @staticmethod
    def post(request, *args, **kwargs):
        filled_form = PostForm(request.POST)

        if filled_form.is_valid():
            post = filled_form.save(commit=False)
            post.title = filled_form.cleaned_data['title']
            post.text = filled_form.cleaned_data['text']
            post.author = request.user
            post.save()
            # post.tags.set(filled_form.cleaned_data['tags'])
            filled_form.save_m2m()
            return redirect(post.get_absolute_url())
        return render(request, 'news/post_create_form.html', {'form': filled_form})


class PostUpdate(View):

    @staticmethod
    def get(request, id_post):
        post = Post.objects.get(pk=id_post)
        form = PostForm(instance=post)
        return render(request, 'news/post_update_form.html', context={'form': form, 'obj': post})

    @staticmethod
    def post(request, id_post):
        post = Post.objects.get(pk=id_post)
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            new_obj = form.save()
            return redirect(new_obj)
        return render(request, 'news/post_update_form.html', context={'form': form, 'obj': post})


class PostDelete(View):

    @staticmethod
    def get(request, id_post):
        post = Post.objects.get(pk=id_post)
        return render(request, 'news/post_delete_form.html', context={'obj': post})

    @staticmethod
    def post(request, id_post):
        post = Post.objects.get(pk=id_post)
        post.delete()
        return redirect(reverse('index_url'))


class TagUpdate(View):

    @staticmethod
    def get(request, id_tag):
        tag = Tag.objects.get(pk=id_tag)
        form = TagForm(instance=tag)
        return render(request, 'news/tag_update_form.html', context={'form': form, 'obj': tag})

    @staticmethod
    def post(request, id_tag):
        tag = Tag.objects.get(pk=id_tag)
        form = TagForm(request.POST, instance=tag)

        if form.is_valid():
            new_obj = form.save()
            return redirect(new_obj)
        return render(request, 'news/tag_update_form.html', context={'form': form, 'obj': tag})


class TagDelete(View):

    @staticmethod
    def get(request, id_tag):
        tag = Tag.objects.get(pk=id_tag)
        return render(request, 'news/tag_delete_form.html', context={'obj': tag})

    @staticmethod
    def post(request, id_tag):
        tag = Tag.objects.get(pk=id_tag)
        tag.delete()
        return redirect(reverse('index_url'))


class UserUpdateView(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        data_obj = User.objects.get(username=request.user.username)
        bound_form = UserUpdateForm(instance=data_obj)
        return render(request, 'news/user_account.html', context={'form': bound_form, 'obj': data_obj})

    @staticmethod
    def post(request):
        data_obj = User.objects.get(username=request.user.username)
        bound_form = UserUpdateForm(request.POST, instance=data_obj)

        if bound_form.is_valid():
            bound_form.save()
            return redirect('profile_detail_url')
        return render(request, 'news/user_account.html', context={'form': bound_form, 'obj': data_obj})


class UserPostsListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'news/posts_list.html'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('pub_date')
