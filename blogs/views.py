from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Blog, Category

# Create your views here.


def posts_by_category(request, category_id):
    # fetch the posts that belong to that category_id
    posts = Blog.objects.filter(status="Published", category=category_id)
    # try:
    # category = Category.objects.get(pk=category_id)
    # except:
    # return redirect("home")

    category = get_object_or_404(Category, pk=category_id)
    context = {
        "posts": posts,
        "category": category,
    }
    return render(request, "post_by_category.html", context)


def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status="Published")
    context = {
        "single_blog": single_blog,
    }
    return render(request, "blogs.html", context)


def search(request):
    keyword = request.GET.get("keyword")
    if not keyword:
        posts = Blog.objects.none()
    else:
        posts = Blog.objects.filter(
            Q(title__icontains=keyword)
            | Q(short_description__icontains=keyword)
            | Q(blog_body__icontains=keyword),
            status="Published",
        )
    context = {
        "posts": posts,
        "keyword": keyword,
    }

    return render(request, "search.html", context)
