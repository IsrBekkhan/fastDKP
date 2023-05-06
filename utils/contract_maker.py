from docxtpl import DocxTemplate

from typing import Dict
from json import dumps


def contract_maker(pattern_path: str,
                   save_path: str,
                   contract_location: str,
                   contract_date: str,
                   sellers_data: Dict,
                   buyers_data: Dict,
                   real_estate_data: Dict) -> None:

    pattern = DocxTemplate(pattern_path)

    context_dict = {'contract_location': contract_location,
                    'contract_date': contract_date,
                    'sellers_firstname': sellers_data['firstname'],
                    'sellers_name': sellers_data['name'],
                    'sellers_surname': sellers_data['surname'],
                    'sellers_date_of_birth': sellers_data['date_of_birth'],
                    'sellers_birth_place': sellers_data['birth_place'],
                    'sellers_passport_id': sellers_data['passport_id'],
                    'sellers_passport_issued_department': sellers_data['passport_issued_department'],
                    'sellers_passport_issued_date': sellers_data['passport_issued_date'],
                    'sellers_department_number': sellers_data['department_number'],
                    'sellers_registration_address': sellers_data['registration_address'],
                    'buyers_firstname': buyers_data['firstname'],
                    'buyers_name': buyers_data['name'],
                    'buyers_surname': buyers_data['surname'],
                    'buyers_date_of_birth': buyers_data['date_of_birth'],
                    'buyers_birth_place': buyers_data['birth_place'],
                    'buyers_passport_id': buyers_data['passport_id'],
                    'buyers_passport_issued_department': buyers_data['passport_issued_department'],
                    'buyers_passport_issued_date': buyers_data['passport_issued_date'],
                    'buyers_department_number': buyers_data['department_number'],
                    'buyers_registration_address': buyers_data['registration_address'],
                    'lands_square': real_estate_data['square'],
                    'lands_address': real_estate_data['address'],
                    'lands_cadastral_number': real_estate_data['cadastral_number'],
                    'lands_category': real_estate_data['lands_category'],
                    'lands_permitted_use': real_estate_data['permitted_use_type'],
                    'lands_registration_reason': real_estate_data['registration_reason'],
                    'state_registration_date_and_number': real_estate_data['state_registration_date_and_number'],
                    'lands_total_price': real_estate_data['price'],
                    'price_in_words': real_estate_data['price_string']}
    print(
        dumps(context_dict, sort_keys=True, indent=8, ensure_ascii=False)
    )
    pattern.render(context_dict)
    pattern.save(filename=save_path)








