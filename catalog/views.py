import random
from datetime import datetime
from pyexpat.errors import messages


from django.core.files.storage import FileSystemStorage
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .forms import CreateUserForm, UserProfileForm
from .models import Client, TypesCard, Felial, User, Account, Card

from django.views import generic


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_clients = Client.objects.all().count()
    num_type = TypesCard.objects.all().count()

    cards = TypesCard.objects.all()
    count_card = TypesCard.objects.all().count()
    # Доступные книги (статус = 'a')
    # num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_felial = Felial.objects.count()  # Метод 'all()' применён по умолчанию.

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'cards': cards,
                 'count_cards': count_card,
                 'num_clients': num_clients,
                 'num_type': num_type,
                 'num_felial': num_felial},
    )


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


def order_card(request, slug):
    card_order = get_object_or_404(TypesCard, nameCard=slug)
    cbu = Felial.objects.all()
    client = Client.objects.filter(user=request.user).first()
    accounts = Account.objects.filter(user=client)
    # POST - обязательный метод
    # file_url = ""
    # if request.method == 'POST' and request.FILES:
    #     # получаем загруженный файл
    #     file = request.FILES['myfile1']
    #     fs = FileSystemStorage()
    #     # сохраняем на файловой системе
    #     filename = fs.save(file.name, file)
    #     # получение адреса по которому лежит файл
    #     file_url = fs.url(filename)
    if request.method == 'POST':
        pic = request.POST['cardPic']
        numCBU = request.POST['nameCBU']
        nameCBU = Felial.objects.filter(numFelial=numCBU.split(' ')[2]).first()
        numCard = random.randint(1000000000000000, 9999999999999999)
        while Card.objects.filter(numCard=numCard).count() > 0:
            numCard = random.randint(1000000000000000, 9999999999999999)
        account = request.POST['list_accounts']
        if account == 'Новый счет':
            account = random.randint(1000000, 9999999)
            while Account.objects.filter(numAccount=account).count() > 0:
                account = random.randint(1000000, 9999999)
            new_account = Account(numAccount=account, felial=nameCBU, user=client)
            new_account.save()
        else:
            new_account = Account.objects.filter(numAccount=account).first()
        dateFinish = datetime.today().replace(year=+3).strftime("%mm%YY")

        new_card = Card(numCard=numCard, dateFinish=dateFinish, image=pic, typeCard=card_order,
                        bankAccount=new_account, user=client)
        new_card.save()

    return render(
        request,
        'catalog/order_card.html',
        context={'card_order': card_order,
                 'filials': cbu,
                 'accounts': accounts,
                 }
    )


def base_generic(request):
    clients = Client.objects.filter(user=request.user).first()
    return render(
        request,
        'base_generic.html',
        context={
            'client': clients,
        },
    )


# def cards(request):
#     cards_list = {
#         "cards": TypesCard.objects.all(),
#         "count": TypesCard.objects.all().count()
#     }
#     return render(request, 'index.html', cards_list)


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
