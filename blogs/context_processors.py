from aboutus.models import SocialLinks

from .models import Category


def get_categories(request):
    categories = Category.objects.all()
    return dict(categories=categories)


def get_social_links(request):
    links = SocialLinks.objects.all()
    return dict(links=links)
