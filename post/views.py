from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect, Http404
from .models import Post
from .forms import PostForm, CommentForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


def post_index(request):

    posts_list = Post.objects.all()
    query = request.GET.get('q')

    if query:
        posts_list = posts_list.filter(Q(title__icontains=query) |
                                       Q(content__icontains=query) |
                                       Q(user__first_name__icontains=query) |
                                       Q(user__last_name__icontains=query)
                                       ).distinct()

    paginator = Paginator(posts_list, 5)  # Show 25 contacts per page

    page = request.GET.get('sayfa')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(request, 'post/index.html', {'posts': posts})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'post/detail.html', context)


def post_create(request):

    if not request.user.is_authenticated():
        raise Http404()

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.user = request.user
        new_post.save()
        messages.success(request, "Başarılı bir şekilde oluşturdunuz.", extra_tags="mesaj-basarili")
        return HttpResponseRedirect(new_post.get_absolute_url())

    context = {
        'form': form
    }

    return render(request, 'post/form.html', context)


def post_update(request, slug):
    if not request.user.is_authenticated():
        raise Http404()
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        new_post = form.save()
        messages.success(request, "Başarılı bir şekilde oluşturdunuz.", extra_tags="mesaj-basarili")
        return HttpResponseRedirect(new_post.get_absolute_url())

    context = {
        'form': form
    }

    return render(request, 'post/form.html', context)


def post_delete(request, slug):
    if not request.user.is_authenticated():
        raise Http404()
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect('post:index')

