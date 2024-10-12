import requests


def hh_api():
    url = 'https://api.hh.ru/employers'
    headers = {'User-Agent': 'HH-User-Agent'}
    employer = []
    employer_id = [
        3529, 2180, 9498112,
        3776, 9498120, 78638,
        23427, 3127, 4181, 80
                   ]
    for i in employer_id:
        params = {'page': 0, 'per_page': 1, "sort_by": "by_vacancies_open"}
        url = f'https://api.hh.ru/employers/{i}'
        response = requests.get(url, headers=headers, params=params).json()
        new_dict = {
            'id': response['id'],
            'name': response['name'],
            'url': response['site_url']
        }
        employer.append(new_dict)
    return employer


def top_vacancies():
    url = 'https://api.hh.ru/vacancies'
    headers = {'User-Agent': 'HH-User-Agent'}
    employer = []
    employer_id = [
        3529, 2180, 9498112,
        3776, 9498120, 78638,
        23427, 3127, 4181, 80
    ]
    for i in employer_id:
        params = {"employer_id": i,
                  "per_page": 5,
                  "only_with_salary": True}
        response = requests.get(url,
                                headers=headers, params=params).json()['items']
        for i in response:
            vacancies_dict = {'id': i['id'],
                              'name': i['name'],
                              'url': i['url'],
                              'salary': i['salary'],
                              'employer_id': i['employer']['id']}
            employer.append(vacancies_dict)
    return employer


if __name__ == '__main__':
    print(top_vacancies())
