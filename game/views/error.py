from django.http import HttpResponse


def error_404(request, *args, **argv):
    response = HttpResponse(
        '<h1 style="margin-top: 300px; text-align: center; font-size: 100px"> H$?4.)0.>4?.$/ </h1>'
    )
    response.status_code = 404
    return response


def error_500(request, *args, **argv):
    response = HttpResponse(
        '<h1 style="margin-top: 300px; text-align: center; font-size: 100px"> H$?4.)0.>4?.$/ </h1>'
    )
    response.status_code = 500
    return response
