from blogs.models import Blog, Category
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify

from .forms import BlogPostForm, CategoryForm


# Create your views here.
@login_required(login_url="login")
def dashboard(request):
    category_count = Category.objects.all().count()
    blogs_count = Blog.objects.all().count()
    context = {
        "category_count": category_count,
        "blogs_count": blogs_count,
    }
    return render(request, "dashboards/dashboard.html", context)


@login_required(login_url="login")
def categories(request):
    return render(request, "dashboards/categories.html")


@login_required(login_url="login")
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("categories")
    form = CategoryForm()
    context = {"form": form}
    return render(request, "dashboards/add_category.html", context)


def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("categories")
    form = CategoryForm(instance=category)
    context = {
        "form": form,
        "category": category,
    }
    return render(request, "dashboards/edit_category.html", context)


def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect("categories")


@login_required(login_url="login")
def posts(request):
    posts = Blog.objects.all()
    context = {
        "posts": posts,
    }
    return render(request, "dashboards/posts.html", context)


@login_required(login_url="login")
def add_post(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            title = form.cleaned_data["title"]
            post.slug = slugify(title) + "-" + str(post.id)
            form.save()
            return redirect("posts")
    else:
        print("form is invalid")
    form = BlogPostForm()
    context = {
        "form": form,
    }

    return render(request, "dashboards/add_post.html", context)


@login_required(login_url="login")
def edit_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            title = form.cleaned_data["title"]
            post.slug = slugify(title) + "-" + str(post.id)
            post.save()
            return redirect("posts")
    form = BlogPostForm(instance=post)
    context = {
        "form": form,
        "post": post,
    }
    return render(request, "dashboards/edit_post.html", context)


def delete_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    post.delete()
    return redirect("posts")
