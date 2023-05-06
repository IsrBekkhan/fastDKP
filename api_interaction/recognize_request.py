from requests import post, codes
from requests.exceptions import ReadTimeout, ConnectionError, ConnectTimeout, RequestException

from os.path import basename
from typing import Dict, Union


class AdsSoft:
    __headers = {}
    __ads_token = None
    __ads_url = None

    @classmethod
    def image_recognizer(cls, image_path: str) -> Union[Dict, str]:
        file_name = basename(image_path)

        files = [
            ('image', (file_name, open(image_path, 'rb'), 'image/jpeg')
             )
        ]
        payload = {
            'token': cls.__ads_token,
            'include_b64_image': '0'
        }

        try:
            response = post(url=cls.__ads_url, headers=cls.__headers, data=payload, files=files, timeout=15)
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

                if deserialized_response['result']:
                    return deserialized_response

                return deserialized_response['message']

            elif response.status_code == 400:
                return 'Проверьте свой тариф сервиса https://ads-soft.ru/'

            return 'Ошибка: сервер не выдал запрошенную информацию.'

    @staticmethod
    def passport_data_getter(deserialized_response: Dict) -> Union[Dict, str]:
        data_list = list()
        try:
            data_list = deserialized_response['data'][0]['data']['results']
        except (KeyError, IndexError):
            return 'Ошибка в структуре полученных данных'

        data_dict = dict()
        try:
            for elem in data_list:

                if elem['label'] == 'lastname':
                    data_dict['firstname'] = elem['text'].title()

                elif elem['label'] == 'name':
                    data_dict['name'] = elem['text'].title()

                elif elem['label'] == 'middlename':
                    data_dict['surname'] = elem['text'].title()

                elif elem['label'] == 'birth_date':
                    data_dict['date_of_birth'] = elem['text']

                elif elem['label'] == 'birth_place':
                    data_dict['birth_place'] = elem['text']

                elif elem['label'] == 'serial_1':
                    data_dict['passport_id'] = elem['text']

                elif elem['label'] == 'issued':
                    data_dict['passport_issued_department'] = elem['text']

                elif elem['label'] == 'issued_date':
                    data_dict['passport_issued_date'] = elem['text']

                elif elem['label'] == 'issued_number':
                    data_dict['issued_number'] = elem['text']

        except KeyError:
            return 'Ошибка в результатах полученных данных'
        except Exception:
            return 'Непредвиденная ошибка при обработке полученных данных'

        return data_dict

    @classmethod
    def ads_token_setter(cls, token):
        cls.__ads_token = token

    @classmethod
    def ads_url_setter(cls, url):
        cls.__ads_url = url
