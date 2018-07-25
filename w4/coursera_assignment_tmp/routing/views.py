from django.http import HttpResponse

def simple_route(request):
    if request.method == "GET":
        return HttpResponse(status=200)
    return HttpResponse(status=405)

def slug_route(request, slug):
    return HttpResponse(
        request.path.split('/')[-2], content_type="text/plain", status=200)

def sum_route(request, a, b):
    res = int(request.path.split('/')[-2]) + int(request.path.split('/')[-3])
    return HttpResponse(res, status=200)

def sum_get_method(request):
    res = int(request.GET.get('a')) + int(request.GET.get('b'))
    return HttpResponse(res, status=200)

def sum_post_method(request):
    if request.method == "POST":
        res = int(request.POST.get('a')) + int(request.POST.get('b'))
        return HttpResponse(res, status=200)