from django.views import generic
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .forms import PostForm, CommentForm
from .models import Post, Comment
from django.contrib.auth.decorators import login_required


class HomeView(generic.TemplateView):
    template_name = 'home.html'


class AboutView(generic.TemplateView):
    template_name = "about.html"


def pagination(request, post_list):
    query = request.GET.get('q')
    if query:
        if query.strip():
            post_list = post_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()
            if not post_list:
                messages.info(request, "Aramanızla ilgili bir sonuç bulunamadı.")

    paginator = Paginator(post_list, 5)  # Show 5 posts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return posts


def post_index(request, slug=None):
    if not request.user.is_authenticated():  # is_staff or not request.user.is_superuser:
        if slug is None:
            post_list = Post.objects.active()
        else:
            post_list = Post.objects.filter(tags__slug=slug)
    else:
        if slug is None:
            post_list = Post.objects.all()
        else:
            post_list = Post.objects.filter(tags__slug=slug)

    posts = pagination(request, post_list)

    today = timezone.now().date()
    total = post_list.count()
    return render(request, "post/index.html", {"posts": posts, "today": today, "total": total, 'tags': slug})


def post_detail(request, slug=None):
    post = get_object_or_404(Post, slug=slug)
    if post.draft or post.publish > timezone.now().date():
        if not request.user.is_authenticated():
            raise Http404

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return HttpResponseRedirect(comment.get_absolute_url())

    today = timezone.now().date()
    return render(request, "post/detail.html", {'post': post, "today": today, "form": form})


def post_create(request):
    if not request.user.is_authenticated():
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # Without this next line the tags won't be saved.
        form.save_m2m()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    return render(request, "post/post_form.html", {'form': form, "header": "Add a New Post"})


def post_update(request, slug=None):
    if not request.user.is_authenticated():
        raise Http404

    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        form.save_m2m()
        messages.success(request, "Item Saved")
        return HttpResponseRedirect(instance.get_absolute_url())

    return render(request, "post/post_form.html", {"form": form, "header": "Edit Post"})


def post_delete(request, slug=None):
    if not request.user.is_authenticated():
        raise Http404

    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect("post:index")


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return HttpResponseRedirect(comment.get_absolute_url())


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return HttpResponseRedirect(comment.get_absolute_url())


