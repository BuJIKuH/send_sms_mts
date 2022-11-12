import requests
from requests.auth import HTTPBasicAuth


def sent_message(login, password, naming, to, text_message):
    url = 'https://omnichannel.mts.ru/http-api/v1/messages'
    body = {
        "messages": [
            {"content": {"short_text": text_message},
             "from": {"sms_address": naming},
             "to": [{"msisdn": to}]}
        ],
    }

    resp = requests.post(url, json=body, auth=HTTPBasicAuth(login, password))
    # Проверка статуса
    if resp.status_code == 200:
        message_id = resp.json()['messages'][0]["internal_id"]
        print("Запрос отработал успешно message_id = " + message_id)
        resp_info = check_message(login, password, message_id)
        if resp_info.status_code == 200:
            event_code = resp_info.json()[
                "events_info"][0]["events_info"][0]["status"]
            if event_code == 200:
                print("SMS отправлено получателю " + to + ". message_id = "
                      + message_id)
            elif event_code == 201:
                print(
                    "SMS НЕ отправлено message_id = " + message_id
                    + " Детали см по кодам ошибок в документации "
                    + str(resp_info.content))
    else:
        print("Запрос не отработал. Детали: " + str(resp.content))

    return resp


# Статус отправленного сообщения
def check_message(login, password, message_id):
    url = 'https://omnichannel.mts.ru/http-api/v1/messages/info'
    body = {"int_ids": [message_id]}
    resp_info = requests.post(
        url,
        json=body,
        auth=HTTPBasicAuth(login, password))

    return resp_info


# Параметры отправки
login = 'ЛОГИН_из_личного_кабинета_раздел_интеграции'
password = 'ПАРОЛЬ_из_личного_кабинета_раздел_интеграции'
naming = 'ИМЯ_согласованное_имя_отправителя_из_ЛК_Маркетолога'
text_message = 'Текст сообщения'
to = '79001111111'
message_id = 'ID сообщения'


if __name__ == '__main__':
    # Отправка сообщения
    sent_message(login, password, naming, to, text_message)

    # Проверка статуса сообщения
    check_message(login, password, message_id)