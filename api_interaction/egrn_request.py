from requests import post, codes
from requests.exceptions import ReadTimeout, ConnectionError, ConnectTimeout, RequestException

from json import dumps
from typing import Dict, Union


class ApiEGRN:
    __api_egrn_host = None
    __api_egrn_token = None
    __url = None

    @classmethod
    def real_estate_data_request(cls, cadastral_number: str) -> Union[Dict, str]:
        headers = {
            'Host': cls.__api_egrn_host,
            'Token': cls.__api_egrn_token,
            'Content-Type': 'application/json'
        }
        params_dict = {
            "query": cadastral_number,
            'deep': 0
        }
        params_json = dumps(params_dict)
        try:
            response = post(url=cls.__url, headers=headers, data=params_json, timeout=30)
        except ReadTimeout:
            return 'Тайм-аут запроса. Повторите попытку.'
        except (ConnectionError, ConnectTimeout):
            return 'Проверьте интернет-соединение'
        except RequestException:
            return 'Непредвиденная ошибка запроса'
        except Exception:
            return 'Непредвиденная ошибка'
        else:
            deserialized_response = response.json()

            if response.status_code == codes.ok:
                return deserialized_response

            return 'Ошибка: сервер не выдал запрошенную информацию.'

    @classmethod
    def real_estate_data_getter(cls, deserialized_response: Dict) -> Union[Dict, str]:
        state_registration_date_and_number = None
        rights = deserialized_response.get('EGRN', {}).get('rights')

        if rights:

            if len(rights) != 0:
                first_elem = rights[0]

                if first_elem['type'] == "Собственность":
                    number = first_elem.get('number')
                    date = first_elem.get('date')

                    if number and date:
                        state_registration_date_and_number = cls.__date_and_number_maker(number, date)

        try:
            real_estate_data_temp = deserialized_response['EGRN']['details']
        except KeyError:
            return 'Ошибка в структуре полученных данных'

        return {'address': real_estate_data_temp.get('Адрес (местоположение)'),
                'square': str(real_estate_data_temp.get('Площадь')),
                'lands_category': real_estate_data_temp.get('Категория земель'),
                'permitted_use_type': real_estate_data_temp.get('Разрешенное использование'),
                'state_registration_date_and_number': state_registration_date_and_number}

    @staticmethod
    def __date_and_number_maker(number, date):
        number_split = number.split('\\')
        number_temp = ''.join(number_split)
        right_number = ''.join(('№', number_temp))

        date_split = date.split('-')
        date_reversed = reversed(date_split)
        right_date = '.'.join(date_reversed)

        return ' '.join((right_number, 'от', right_date))

    @classmethod
    def host_setter(cls, host: str):
        cls.__api_egrn_host = host

    @classmethod
    def token_setter(cls, token: str):
        cls.__api_egrn_token = token

    @classmethod
    def url_setter(cls, url: str):
        cls.__url = url


