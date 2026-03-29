from blogs.models import Blog, Category
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify

from .forms import AddUserForm, BlogPostForm, CategoryForm, EditUserForm


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


# Users CRUD
@login_required(login_url="login")
@permission_required(
    "auth.view_user", login_url="/dashboard/users/", raise_exception=True
)
def users(request):
    users = User.objects.filter(is_superuser=False)
    context = {"users": users}
    return render(request, "dashboards/users.html", context)


@login_required(login_url="login")
@permission_required(
    "auth.add_user", login_url="/dashboard/users/", raise_exception=True
)
def add_user(request):
    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users")
    form = AddUserForm()
    context = {"form": form}
    return render(request, "dashboards/add_user.html", context)


@login_required(login_url="login")
@permission_required(
    "auth.change_user", login_url="/dashboard/users/", raise_exception=True
)
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk, is_superuser=False)
    if request.method == "POST":
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("users")
    form = EditUserForm(instance=user)
    context = {
        "form": form,
        "user": user,
    }
    return render(request, "dashboards/edit_user.html", context)


def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk, is_superuser=False)
    user.delete()
    return redirect("users")
