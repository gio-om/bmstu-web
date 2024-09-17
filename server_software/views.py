from django.shortcuts import render

astronaut_list = [
    {
        'id': 1,
        'name': 'Вуди Хобург',
        'logo_file_name': '1.jpg',
        'specialization': 'Пилот',
        'country': 'USA',
        'expeditions': ['SpaceX_Crew-6'],
        'space_time': 185,
        'biography': 'В 2017 году Хобург был выбран в качестве кандидата в космонавты в 22-й группе астронавтов НАСА и в августе приступил к двухлетнему обучению. В декабре 2020 года он был объявлен одним из восемнадцати астронавтов НАСА, отобранных в рамках программы Артемида для лунной миссии в 2024 году.\n\nОн был выбран пилотом SpaceX Crew-6 и участником космических экспедиций МКС-68/МКС-69 в 2023 году.'
    },
    {
        'id': 2,
        'name': 'Джош Кассада',
        'logo_file_name': '2.jpg',
        'specialization': 'Астронавт',
        'country': 'USA',
        'expeditions': ['SpaceX_Crew-7'],
        'space_time': 155,
        'biography': '17 июня 2013 года был зачислен в отряд астронавтов НАСА в составе 21-го набора НАСА в качестве кандидата в астронавты. В августе того же года приступил к прохождению курса базовой общекосмической подготовки. 9 июля 2015 года получил статус активного астронавта.\n\n3 августа 2018 года на пресс-конференции в Космическом центре им. Джонсона в Хьюстоне было объявлено о включении Джоша Кассада вместе с Сунитой Уильямс в экипаж первого эксплуатационного полёта корабля «Starliner» по программе CTS-1, который должен состояться в 2019 году.\n\nВ 2019 году вместе с Сунитой Уильямс провёл пятинедельную подготовку в ЦПК им. Ю.А.Гагарина по изучению системы Российского сегмента МКС и действиям экипажа в аварийных ситуациях[1]. С 2019 года проходил подготовку в составе экипажа американского частного корабля Starliner CTS-1, однако, из-за задержек в разработке Starliner, был переведён пилотом в состав экипажа SpaceX Crew-5.'
    },
    {
        'id': 3,
        'name': 'Николь Манн',
        'logo_file_name': '3.jpg',
        'specialization': 'Астронавт',
        'country': 'USA',
        'expeditions': ['SpaceX_Crew-5'],
        'space_time': 199,  
        'biography': 'В сентябре 2019 года вместе с Майклом Финком и Крисом Фергюсоном приняла участие в тренировках по отработке эвакуации экипажа спускаемого аппарата космического корабля «Starliner», проводившихся на ракетном полигоне Уайт-Сэндз[англ.] близ Аламогордо.\n\n9 декабря 2020 года на заседании Национального совета по космосу США было объявлено о её включении в группу астронавтов для подготовки к пилотируемым лунным экспедициям в рамках программы «Артемида». 6 октября 2021 года агентство НАСА сообщило о её переводе из экипажа корабля «Старлайнер» в экипаж корабля «Кру Дрэгон», полет которого по программе SpaceX Crew-5 намечен на осень 2022 года.'  
    },
    {
        'id': 4,
        'name': 'Жасмин Могбелли',
        'logo_file_name': '4.jpg',
        'specialization': 'Астронавт',
        'country': 'USA',
        'expeditions': ['SpaceX_Crew-5'],
        'space_time': 199,
        'biography': '7 июня 2017 года была зачислена в отряд астронавтов НАСА в составе 22-го набора НАСА в качестве кандидата в астронавты. 18 августа 2017 года приступила к прохождению двухлетнего курса базовой общекосмической подготовки в Космическом центре им. Джонсона в Хьюстоне. 10 января 2020 года ей была присвоена квалификация астронавт.\n\n9 декабря 2020 года на заседании Национального совета по космосу США было объявлено о её включении в группу астронавтов для подготовки к пилотируемым лунным экспедициям в рамках программы «Артемида».'  
    },
    {
        'id': 5,
        'name': 'Терри Верст',
        'logo_file_name': '5.jpg',
        'specialization': 'Летчик-испытатель',
        'country': 'USA',
        'expeditions': ['STS-130', 'Союз ТМА-15'],
        'space_time': 213, 
        'biography': 'Стартовал в космос 8 февраля 2010 года в качестве пилота шаттла «Индевор» STS-130[3]. Основная цель полёта — стыковка с Международной космической станцией (МКС) (10 февраля) и доставка модулей «Транквилити» («Спокойствие») и «Купол». 22 февраля шаттл приземлился в Космическом центре имени Кеннеди на мысе Канаверал. Продолжительность полёта составила 13 суток 18 часов 06 минут.\n\nВторой раз стартовал 24 ноября 2014 года в качестве бортинженера космического корабля «Союз ТМА-15М». Вернулся 11 июня 2015 года. Продолжительность полёта 199 дней 16 часов 42 минут.'
    },
]

user_request = [
    {
        'id': 1,
        'name': 'Вуди Хобург',
        'logo_file_name': '1.jpg',
        'specialization': 'Летчик-испытатель',
    },
    {
        'id': 2,
        'name': 'Джош Кассада',
        'logo_file_name': '2.jpg',
        'specialization': 'Астронавт',
    },
    {
        'id': 3,
        'name': 'Николь Манн',
        'logo_file_name': '3.jpg',
        'specialization': 'Астронавт',
    },
]

MINIO_HOST = '127.0.0.1'
MINIO_PORT = 9000
MINIO_DIR = 'services'


def get_image_file_path(file_name: str) -> str:
    return f'http://{MINIO_HOST}:{MINIO_PORT}/{MINIO_DIR}/{file_name}'


def get_astronaut_list(search_query: str):
    res = []
    for astronaut in astronaut_list:
        if astronaut["name"].lower().startswith(search_query.lower()) or astronaut["name"].lower().split()[1]startswith(search_query.lower()):
            res.append(astronaut)
            res[-1]['logo_file_path'] = get_image_file_path(astronaut["logo_file_name"])
    return res


def get_request_data():
    res = user_request.copy()
    for i in range(len(res)):
        res[i]['logo_file_path'] = get_image_file_path(res[i]["logo_file_name"])

    s = 0# sum([i['price'] for i in res])
    return {
        'astronaut_list': res,
        'total': s,
    }


def astronaut_list_page(request):
    astronaut_name = request.GET.get('astronaut_name', '')

    return render(request, 'astronaut_list.html',
                  {'data': {
                      'astronaut_list': get_astronaut_list(astronaut_name),
                      'count': len(user_request),
                      'astronaut_name': astronaut_name,
                      'request_id': 0,
                  }, })


def astronaut_page(request, id):
    for astronaut in astronaut_list:
        if astronaut['id'] == id:
            astronaut['logo_file_path'] = get_image_file_path(astronaut["logo_file_name"])
            return render(request, 'astronaut.html',
                          {'data': astronaut})

    render(request, 'astronaut.html')


def request_page(request, id):
    if id != 0:
        return render(request, 'request.html')

    return render(request, 'request.html',
                  {'data': get_request_data()})
