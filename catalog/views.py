import datetime
import random

from django.contrib import messages

from django.core.files.storage import FileSystemStorage
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .forms import CreateUserForm, UserProfileForm, SecurityUserForm
from .models import Client, TypesCard, Felial, User, Account, Card, Sending, SecurityUser

from django.views import generic


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    # num_clients = Client.objects.all().count()
    # num_type = TypesCard.objects.all().count()

    cards = TypesCard.objects.all()
    # count_card = TypesCard.objects.all().count()
    # Доступные книги (статус = 'a')
    # num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    # num_felial = Felial.objects.count()  # Метод 'all()' применён по умолчанию.
    paysystems = TypesCard.LOAN_STATUS_P
    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'cards': cards,
                 'paysystems': paysystems,
                 },
    )


class TypeCardListView(generic.ListView):
    model = TypesCard


# class TypeCardDetailView(generic.DetailView):
#     model = TypesCard


def typescard_view(request, slug):
    typescard = get_object_or_404(TypesCard, id=slug)
    return render(
        request,
        'catalog/typescard_detail.html',
        context={'typescard': typescard, }
    )


def order_card(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')
    card_order = get_object_or_404(TypesCard, id=slug)
    cbu = Felial.objects.all()
    client = Client.objects.filter(user=request.user).first()
    accounts = Account.objects.filter(user=client)
    if request.method == 'POST':
        pic = request.FILES.get('cardPic', '')
        numCBU = request.POST['nameCBU']
        check = request.POST.get('CheckBox', '')
        adres = request.POST.get('address', '')
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
        dt = datetime.datetime.today()
        dt = dt.replace(year=dt.year + 3).strftime("%m%Y")
        # dateFinish = datetime.datetime().today().replace(
        #     year=datetime.datetime().today().year + relativedelta() datetime.timedelta(days=3*365)).strftime("%m%Y")

        fs = FileSystemStorage()
        if pic == '':
            filename = fs.save(card_order.image.name, card_order.image)
        else:
            filename = fs.save(pic.name, pic)

        new_card = Card(numCard=numCard, dateFinish=dt, image=filename, typeCard=card_order,
                        bankAccount=new_account, user=client)
        new_card.save()

        numSend = random.randint(10, 500)

        if check == 'on':
            new_sending = Sending(card=new_card,
                                  sender=Client.objects.filter(
                                      user=User.objects.filter(username='admin').first()).first(),
                                  address=adres,
                                  checkbox=True)
        else:
            new_sending = Sending(card=new_card,
                                  sender=Client.objects.filter(
                                      user=User.objects.filter(username='admin').first()).first(),
                                  address=nameCBU.address,
                                  checkbox=False)


        new_sending.save()
        return redirect('my_card')
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


def my_card(request):
    if not request.user.is_authenticated:
        return redirect('login')
    client = Client.objects.filter(user=request.user).first()
    list_card = Card.objects.filter(user=client)
    sending = Sending.objects.filter(card__user=client)
    return render(
        request,
        'catalog/my_card.html',
        context={
            'my_card_list': list_card,
            'sendings': sending,
        },
    )


def cbu(request):
    cbus = Felial.objects.all()
    return render(
        request,
        'catalog/cbu.html',
        context={
            'cbus': cbus,
        }
    )


def registration(request):
    form = CreateUserForm()
    clientform = UserProfileForm()
    securityuserform = SecurityUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        client_form = UserProfileForm(request.POST)
        securityuserform = SecurityUserForm(request.POST)
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password2 != password1:
            messages.info(request, "Пароли не совпадают")
        elif User.objects.filter(email=request.POST['email']).exists():
            messages.info(request, "Пользователь с таким email уже существует")
        elif User.objects.filter(username=request.POST['username']).exists():
            messages.info(request, "Пользователь с таким логином уже существует")
        else:
            if form.is_valid():  # and player_form.is_valid():
                user = form.save()
                client = client_form.save(commit=False)
                securityuser = securityuserform.save(commit=False)
                # user=User()
                client.user = user
                securityuser.user = client
                user.save()
                client.save()
                securityuser.save()
                username = form.cleaned_data.get('username')
                messages.success(request, 'Аккаунт ' + username + ' успешно создан')
                return redirect('login')

    context = {'form': form,
               'clientform': clientform,
               'securityuserform': securityuserform}

    return render(request, 'catalog/registration.html', context)
