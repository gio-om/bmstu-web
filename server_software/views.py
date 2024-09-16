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
    },
    {
        'id': 2,
        'name': 'Джош Кассада',
        'logo_file_name': '2.jpg',
        'specialization': 'Астронавт',
        'country': 'USA',
        'expeditions': ['SpaceX_Crew-7'],
        'space_time': 155,
    },
    {
        'id': 3,
        'name': 'Николь Манн',
        'logo_file_name': '3.jpg',
        'specialization': 'Астронавт',
        'country': 'USA',
        'expeditions': ['SpaceX_Crew-5'],
        'space_time': 199,    
    },
    {
        'id': 4,
        'name': 'Жасмин Могбелли',
        'logo_file_name': '4.jpg',
        'specialization': 'Астронавт',
        'country': 'USA',
        'expeditions': ['SpaceX_Crew-5'],
        'space_time': 199,  
    },
    {
        'id': 5,
        'name': 'Терри Верст',
        'logo_file_name': '5.jpg',
        'specialization': 'Летчик-испытатель',
        'country': 'USA',
        'expeditions': ['STS-130', 'Союз ТМА-15'],
        'space_time': 213, 
    },
]

user_request = [
    {
        'id': 0,
        'name': 'Docker',
        'logo_file_name': '0.png',
        'price': 100,
    },
    {
        'id': 1,
        'name': 'NodeJS',
        'logo_file_name': '1.png',
        'price': 150,
    },
    {
        'id': 2,
        'name': 'Python',
        'logo_file_name': '2.jpg',
        'price': 200,
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
        if astronaut["name"].lower().startswith(search_query.lower()):
            res.append(astronaut)
            res[-1]['logo_file_path'] = get_image_file_path(astronaut["logo_file_name"])
    return res


def get_request_data():
    res = user_request.copy()
    for i in range(len(res)):
        res[i]['logo_file_path'] = get_image_file_path(res[i]["logo_file_name"])

    s = sum([i['price'] for i in res])
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
