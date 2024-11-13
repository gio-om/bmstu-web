from django.core.management.base import BaseCommand
from minio import Minio

from ...models import *
from .utils import *


def add_users():
    User.objects.create_user("user", "user@user.com", "1234", first_name="user", last_name="user")
    User.objects.create_superuser("root", "root@root.com", "1234", first_name="root", last_name="root")

    for i in range(1, 10):
        User.objects.create_user(f"user{i}", f"user{i}@user.com", "1234", first_name=f"user{i}", last_name=f"user{i}")
        User.objects.create_superuser(f"root{i}", f"root{i}@root.com", "1234", first_name=f"user{i}", last_name=f"user{i}")

    print("Пользователи созданы")


def add_astronauts():
    Astronaut.objects.create(
        name="Вуди Хобург",
        description="В 2017 году Хобург был выбран в качестве кандидата в космонавты в 22-й группе астронавтов НАСА и в августе приступил к двухлетнему обучению. В декабре 2020 года он был объявлен одним из восемнадцати астронавтов НАСА, отобранных в рамках программы Артемида для лунной миссии в 2024 году.\n\nОн был выбран пилотом SpaceX Crew-6 и участником космических экспедиций МКС-68/МКС-69 в 2023 году.",
        space_time=185,
        country="США",
        specialization="Пилот",
        image="1.png"
    )

    Astronaut.objects.create(
        name="Джош Кассада",
        description="17 июня 2013 года был зачислен в отряд астронавтов НАСА в составе 21-го набора НАСА в качестве кандидата в астронавты. В августе того же года приступил к прохождению курса базовой общекосмической подготовки. 9 июля 2015 года получил статус активного астронавта.\n\n3 августа 2018 года на пресс-конференции в Космическом центре им. Джонсона в Хьюстоне было объявлено о включении Джоша Кассада вместе с Сунитой Уильямс в экипаж первого эксплуатационного полёта корабля «Starliner» по программе CTS-1, который должен состояться в 2019 году.\n\nВ 2019 году вместе с Сунитой Уильямс провёл пятинедельную подготовку в ЦПК им. Ю.А.Гагарина по изучению системы Российского сегмента МКС и действиям экипажа в аварийных ситуациях[1]. С 2019 года проходил подготовку в составе экипажа американского частного корабля Starliner CTS-1, однако, из-за задержек в разработке Starliner, был переведён пилотом в состав экипажа SpaceX Crew-5.",
        space_time=155,
        country="США",
        specialization="Астронавт",
        image="2.png"
    )

    Astronaut.objects.create(
        name="Николь Манн",
        description="В сентябре 2019 года вместе с Майклом Финком и Крисом Фергюсоном приняла участие в тренировках по отработке эвакуации экипажа спускаемого аппарата космического корабля «Starliner», проводившихся на ракетном полигоне Уайт-Сэндз[англ.] близ Аламогордо.\n\n9 декабря 2020 года на заседании Национального совета по космосу США было объявлено о её включении в группу астронавтов для подготовки к пилотируемым лунным экспедициям в рамках программы «Артемида». 6 октября 2021 года агентство НАСА сообщило о её переводе из экипажа корабля «Старлайнер» в экипаж корабля «Кру Дрэгон», полет которого по программе SpaceX Crew-5 намечен на осень 2022 года.",
        space_time=200,
        country="США",
        specialization="Астронавт",
        image="3.png"
    )

    Astronaut.objects.create(
        name="Жасмин Могбелли",
        description="7 июня 2017 года была зачислена в отряд астронавтов НАСА в составе 22-го набора НАСА в качестве кандидата в астронавты. 18 августа 2017 года приступила к прохождению двухлетнего курса базовой общекосмической подготовки в Космическом центре им. Джонсона в Хьюстоне. 10 января 2020 года ей была присвоена квалификация астронавт.\n\n9 декабря 2020 года на заседании Национального совета по космосу США было объявлено о её включении в группу астронавтов для подготовки к пилотируемым лунным экспедициям в рамках программы «Артемида»",
        space_time=50,
        country="США",
        specialization="Астронавт",
        image="4.png"
    )

    Astronaut.objects.create(
        name="Терри Верст",
        description="Стартовал в космос 8 февраля 2010 года в качестве пилота шаттла «Индевор» STS-130[3]. Основная цель полёта — стыковка с Международной космической станцией (МКС) (10 февраля) и доставка модулей «Транквилити» («Спокойствие») и «Купол». 22 февраля шаттл приземлился в Космическом центре имени Кеннеди на мысе Канаверал. Продолжительность полёта составила 13 суток 18 часов 06 минут.\n\nВторой раз стартовал 24 ноября 2014 года в качестве бортинженера космического корабля «Союз ТМА-15М». Вернулся 11 июня 2015 года. Продолжительность полёта 199 дней 16 часов 42 минут.",
        space_time=120,
        country="США",
        specialization="Летчик-испытатель",
        image="5.png"
    )

    Astronaut.objects.create(
        name="Роберт Бенкен",
        description="Американский астронавт НАСА, полковник ВВС (на 2009 год). Участник двух полётов на «Спейс шаттл» — STS-123 и STS-130. Пилот миссии SpaceX DM-2.",
        space_time=350,
        country="США",
        specialization="Пилот",
        image="6.png"
    )

    client = Minio("minio:9000", "minio", "minio123", secure=False)
    client.fput_object('images', '1.png', "app/static/images/1.png")
    client.fput_object('images', '2.png', "app/static/images/2.png")
    client.fput_object('images', '3.png', "app/static/images/3.png")
    client.fput_object('images', '4.png', "app/static/images/4.png")
    client.fput_object('images', '5.png', "app/static/images/5.png")
    client.fput_object('images', '6.png', "app/static/images/6.png")
    client.fput_object('images', 'default.png', "app/static/images/default.png")

    print("Услуги добавлены")


def add_flights():
    users = User.objects.filter(is_staff=False)
    moderators = User.objects.filter(is_staff=True)

    if len(users) == 0 or len(moderators) == 0:
        print("Заявки не могут быть добавлены. Сначала добавьте пользователей с помощью команды add_users")
        return

    astronauts = Astronaut.objects.all()

    for _ in range(30):
        status = random.randint(2, 5)
        owner = random.choice(users)
        add_flight(status, astronauts, owner, moderators)

    add_flight(1, astronauts, users[0], moderators)
    add_flight(2, astronauts, users[0], moderators)

    print("Заявки добавлены")


def add_flight(status, astronauts, owner, moderators):
    flight = Flight.objects.create()
    flight.status = status

    if status in [3, 4]:
        flight.moderator = random.choice(moderators)
        flight.date_complete = random_date()
        flight.date_formation = flight.date_complete - random_timedelta()
        flight.date_created = flight.date_formation - random_timedelta()
    else:
        flight.date_formation = random_date()
        flight.date_created = flight.date_formation - random_timedelta()

    if status == 3:
        flight.date = calc()

    flight.name = "Название миссии"
    flight.goal = "Цель полета"
    flight.owner = owner

    i = random.randint(0, 2)
    j = 0
    for astronaut in random.sample(list(astronauts), 3):
        item = AstronautFlight(
            flight=flight,
            astronaut=astronaut,
            value=i == j
        )
        j += 1
        item.save()

    flight.save()


def calc():
    return random_date()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        add_users()
        add_astronauts()
        add_flights()
