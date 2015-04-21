from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound,\
HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseRedirect
from models import url_Acortar
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def process(request):

    urls = ""

    if request.method == "GET":
        
        lista_Urls = url_Acortar.objects.all()
        urls+="<a>URLS GUARDADAS:</a></br></br>"
        for url in lista_Urls:
            urls += "<pre>Url acortada de: " + url.Url + "  -->  " + str(url.id)
        form = "</br></br></br><form action='' method='POST'>Introduzca su Url a acortar: <input type=\
                'text' name='url'><input type='submit' value='Enviar'></form>"
        return HttpResponse(urls + form)

    elif request.method == "POST":

        url = request.POST.get("url")

        if url == "":
            return HttpResponseBadRequest("PAGINA VACIA")
        elif not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        try:
            newUrl = url_Acortar.objects.get(Url=url)
        except url_Acortar.DoesNotExist:
            newUrl = url_Acortar(Url=url)
            newUrl.save()
        response = "<p>Url acortada: " + str(newUrl.id) + "</b></p>"
        response += "<a href=" + str(newUrl.id) + ">Pulse aqui para ir a la url</a></br></br>"
        response += "<a href=''>Pulse aqui para volver al acortador</a>"

        return HttpResponse(response)
    else:
        return HttpResponse("Something goes wrong :S")


def redirect(request, id):
    try:
        url = url_Acortar.objects.get(id=id)
    except url_Acortar.DoesNotExist:
        return HttpResponseNotFound(str(id) + " not found")
    return HttpResponseRedirect(url.Url)
