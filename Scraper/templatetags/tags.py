from django import template

APP_NAME = "Anime Scraper"

register = template.Library()


@register.simple_tag
def app_name(request):
    return APP_NAME


@register.assignment_tag(takes_context=False)
def user_logged_in(request):
    if request.user.is_authenticated:
        return True
    return False


@register.simple_tag
def user_name(request):
    if request.user.is_authenticated:
        if request.user.first_name:
            return request.user.first_name
        else:
            return request.user.username
    return "Hacker alert"
