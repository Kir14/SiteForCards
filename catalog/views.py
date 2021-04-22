from pyexpat.errors import messages

from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .forms import CreateUserForm, UserProfileForm
from .models import Client, TypesCard, Felial, User


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


def registration(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        player_form = UserProfileForm(request.POST)
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password2 != password1:
            messages.info(request, "Пароли не совпадают")
        elif User.objects.filter(email=request.POST['email']).exists():
            messages.info(request, "Пользователь с таким email уже существует")
        elif User.objects.filter(username=request.POST['username']).exists():
            messages.info(request, "Пользователь с таким логином уже существует")
        else:
            if form.is_valid() and player_form.is_valid():
                user = form.save()
                player = player_form.save(commit=False)
                player.user = user
                user.save()
                player.save()
                username = form.cleaned_data.get('username')
                messages.success(request, 'Аккаунт ' + username + ' успешно создан')
                return redirect('template/registration:login')

    context = {'form': form}

    return render(request, 'registration', context)
