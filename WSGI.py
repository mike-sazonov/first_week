# Задача - ASGI / WSGI функция которая проксирует курс валют
# Приложение должно отдавать курс валюты к доллару используя стороннее АПИ
# https://api.exchangerate-api.com/v4/latest/{currency}


import requests
import json



def simple_app(environ: dict[str, str], start_response) -> list[bytes]:

    API_URL = "https://api.exchangerate-api.com/v4/latest"

    request_url = f"{API_URL}{environ['PATH_INFO']}"
    r = requests.request(environ["REQUEST_METHOD"], request_url)

    start_response(r.status_code, [(k, v) for k, v in r.headers.items()])

    return [json.dumps(r.json()).encode('utf-8')]


def run_wsgi_app(app, environ: dict[str, str]) -> list[bytes]:
    status_line = None
    headers = None
    def start_response(status, response_headers):
        # Сохраняем статус и заголовки для последующей отправки
        nonlocal status_line, headers
        status_line = status
        headers = response_headers

    # Вызываем WSGI-приложение
    response_body = app(environ, start_response)

    # Формируем HTTP-ответ
    response = [f'HTTP/1.1 {status_line}'.encode()]
    for header in headers:
        response.append(f'{header[0]}: {header[1]}'.encode())
    response.append(b'')
    response.extend(response_body)

    return response


env = {
    'REQUEST_METHOD': 'GET',
    'PATH_INFO': '/USD',
    'SERVER_NAME': 'localhost',
    'SERVER_PORT': '8000',
    # Другие необходимые ключи
}


response = run_wsgi_app(simple_app, env)

print(b'\r\n'.join(response).decode())
