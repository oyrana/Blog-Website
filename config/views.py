from aboutus.models import About, SocialLinks
from blogs.models import Blog, Category
from django.shortcuts import render


def home(request):

    featured_posts = Blog.objects.filter(is_featured=True).order_by("updated_at")
    posts = Blog.objects.filter(
        is_featured=False,
        status="Published",
    )

    # Fetch About Us Details
    try:
        about = About.objects.get()
    except:
        about = None
    context = {
        "featured_posts": featured_posts,
        "posts": posts,
        "about": about,
    }

    return render(request, "home.html", context)
