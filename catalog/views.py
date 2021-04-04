from django.http import Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Client, TypesCard, Felial


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_clients = Client.objects.all().count()
    num_type = TypesCard.objects.all().count()
    # Доступные книги (статус = 'a')
    # num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_felial = Felial.objects.count()  # Метод 'all()' применён по умолчанию.

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_clients': num_clients, 'num_type': num_type, 'num_felial': num_felial},
    )


from django.views import generic


class TypeCardListView(generic.ListView):
    model = TypesCard


# class TypeCardDetailView(generic.DetailView):
#     model = TypesCard


def typescard_view(request, slug):
    typescard = get_object_or_404(TypesCard, nameCard=slug)
    return render(
        request,
        'catalog/typescard_detail.html',
        context={'typescard': typescard, }
    )
