from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm
from django.http import Http404
from django.contrib.auth.models import Group
from .models import User  # Импорт вашей модели User
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User
from django.db.models import Q
from django.db.models import F, FloatField, ExpressionWrapper
from django.contrib.auth import logout



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_data = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(request, username=login_data, password=password)

            if user is not None:
                login(request, user)

                # Проверяем, является ли пользователь менеджером
                if user.is_staff:
                    return redirect('main_manager')  # Перенаправление на страницу для менеджеров
                else:
                    return redirect('main_user')  # Перенаправление на страницу для обычных пользователей
            else:
                form.add_error(None, 'Invalid login or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def main_manager_view(request):
    return render(request, "main_manager.html")



def main_user_view(request):
    return render(request, "main_user.html")





def statistics_view(request, id=None):
    # Вычисляем `orders_per_hour` для всех работников
    workers = (
        User.objects.filter(is_staff=False)
        .annotate(
            orders_per_hour=ExpressionWrapper(
                F('amount_completed_offers') / F('work_hours'),
                output_field=FloatField()  # Указываем FloatField для сохранения дробной части
            )
        )
        .order_by('-orders_per_hour')  # Сортировка по убыванию эффективности
    )

    if request.method == 'POST':  # Если отправлена форма поиска
        first_name = request.POST.get('first_name', '').strip()
        second_name = request.POST.get('second_name', '').strip()

        try:
            worker = User.objects.get(
                first_name__iexact=first_name,
                second_name__iexact=second_name,
                is_staff=False
            )
            orders_per_hour = (
                worker.amount_completed_offers / worker.work_hours
                if worker.work_hours > 0
                else 0
            )
            return render(request, 'statistics.html', {
                'worker': worker,
                'orders_per_hour': orders_per_hour,
                'workers': workers,
            })
        except User.DoesNotExist:
            return render(request, 'statistics.html', {
                'error_message': 'Работник с такими данными не найден.',
                'workers': workers,
            })

    if id:  # Если передан ID пользователя, показываем его статистику
        worker = get_object_or_404(User, id=id, is_staff=False)
        orders_per_hour = (
            worker.amount_completed_offers / worker.work_hours
            if worker.work_hours > 0
            else 0
        )
        return render(request, 'statistics.html', {
            'worker': worker,
            'orders_per_hour': orders_per_hour,
            'workers': workers,
        })

    # Если ID не передан, возвращаем список работников, отсортированных по эффективности
    return render(request, 'statistics.html', {'workers': workers})


def logout_view(request):
    logout(request)  # Выполняет выход пользователя
    return redirect('login')  # Перенаправляет на страницу входа


def worker_statistics(request, worker_id):
    worker = get_object_or_404(User, id=worker_id, is_staff=False)  # Получаем работника, у которого is_staff=False

    orders_per_hour = (
        worker.amount_completed_offers / worker.work_hours if worker.work_hours > 0 else 0
    )
    return render(request, 'worker_statistics.html', {
        'worker': worker,
        'orders_per_hour': orders_per_hour,
    })


def search_worker(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        second_name = request.POST.get('second_name', '').strip()

        try:
            # Попытка найти работника по имени и фамилии
            worker = User.objects.get(first_name__iexact=first_name, second_name__iexact=second_name, is_staff=False)

            # Если работник найден, перенаправляем на страницу редактирования
            return redirect('edit_user', worker_id=worker.id)

        except User.DoesNotExist:
            # Если работник не найден, показываем сообщение об ошибке
            workers = User.objects.filter(is_staff=False)
            return render(request, 'search_worker.html', {
                'error_message': 'Работник с такими данными не найден.',
                'workers': workers,
            })

    workers = User.objects.filter(is_staff=False)
    return render(request, 'search_worker.html', {'workers': workers})


def edit_user(request, worker_id):
    user = get_object_or_404(User, id=worker_id)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.second_name = request.POST.get('second_name')
        user.login = request.POST.get('login')
        # Проверка для пароля (если оно не пустое, то изменим пароль)
        password = request.POST.get('password')
        if password:
            user.set_password(password)  # Для хеширования пароля

        # Для булевых значений
        user.is_staff = 'is_staff' in request.POST  # Если checkbox отмечен
        user.is_active = 'is_active' in request.POST  # Если checkbox отмечен
        user.age = request.POST.get('age')
        user.adress = request.POST.get('adress')
        user.login = request.POST.get('login')
        user.date_of_birth = request.POST.get('date_of_birth')
        user.email_adress = request.POST.get('email_adress')
        user.phone_number = request.POST.get('phone_number')
        user.work_hours = request.POST.get('work_hours')
        user.amount_completed_offers = request.POST.get('amount_completed_offers')
        user.time_of_work = request.POST.get('time_of_work')

        # Сохраняем изменения
        user.save()

        # Перенаправляем на страницу после редактирования
        return redirect('search_worker')

    return render(request, 'edit_user.html', {'user': user})

def add_user_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        second_name = request.POST.get('second_name')
        age = request.POST.get('age')
        adress = request.POST.get('adress')
        login = request.POST.get('login')
        date_of_birth = request.POST.get('date_of_birth')
        email_adress = request.POST.get('email_adress')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')  # Получаем пароль из формы
        is_active = 'is_active' in request.POST
        is_staff = 'is_staff' in request.POST
        work_hours = request.POST.get('work_hours')
        amount_completed_offers = request.POST.get('amount_completed_offers')
        time_of_work = request.POST.get('time_of_work')

        # Хэшируем пароль
        hashed_password = make_password(password)

        # Создаем нового пользователя
        user = get_user_model().objects.create(
            first_name=first_name,
            second_name=second_name,
            age=age,
            adress=adress,
            login=login,
            date_of_birth=date_of_birth,
            email_adress=email_adress,
            phone_number=phone_number,
            password=hashed_password,
            is_active=is_active,
            is_staff=is_staff,
            work_hours=work_hours,
            amount_completed_offers=amount_completed_offers,
            time_of_work=time_of_work
        )
        return redirect('statistics')  # Перенаправление на страницу статистики

    return render(request, 'add_user.html')





def magazine_view(request):
    return render(request, 'magazine.html')

def add_task_view(request):
    # Логика для добавления работы
    return render(request, 'add_task.html')

def edit_task_view(request):
    # Логика для редактирования работы
    return render(request, 'edit_task.html')

def user_delete(request):
    #Логика для удаления пользователей
    return render(request, 'delete_user.html')
