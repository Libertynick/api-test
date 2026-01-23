import allure
import pytest

from api_testing_project.services.material.api.api_find_analogs import ApiFindAnalogs
from api_testing_project.services.material.models.find_analogs_model import FindAnalogsModel
from api_testing_project.services.material.payloads.payloads_find_analogs import PayloadsFindAnalogs


@pytest.mark.stage
@pytest.mark.dapi
@allure.feature('DAPI')
@allure.story('Тесты на api/Material/FindAnalogs')
class TestFindAnalogs:
    """Тесты на api/Material/FindAnalogs"""

    @allure.title('Тест на api/Material/FindAnalogs - проверка всех кодов с аналогами')
    @pytest.mark.stage
    def test_find_analogs_all_codes(self):
        """
        Тест на api/Material/FindAnalogs.
        Отправляем все 80 кодов и проверяем, что коды аналогов в ответе совпадают с ожидаемыми.
        """
        print(f'\n\nДелаем POST запрос на api/Material/FindAnalogs')
        print(f'Количество кодов в запросе: {len(PayloadsFindAnalogs.all_material_codes)}')

        # 1. Создаем API объект
        api_find_analogs = ApiFindAnalogs()

        # 2. Делаем POST запрос
        response = api_find_analogs.post_find_analogs(PayloadsFindAnalogs.request_find_analogs_all_codes)

        # 3. Проверяем HTTP статус код
        assert response.status_code == 200, \
            f'HTTP статус код - {response.status_code}, ожидался 200'
        print(f'✓ HTTP статус код: {response.status_code}')

        # 4. Валидируем ответ через Pydantic модель
        response_json = response.json()
        result = FindAnalogsModel(**response_json)

        # 5. Проверяем status в ответе
        status = result.status
        assert status == 'Ok', f'status в ответе - {status}, ожидался "Ok"'
        print(f'✓ Статус ответа: {status}')

        # 6. Получаем список объектов с аналогами
        objects = result.objects
        print(f'✓ Количество объектов в ответе: {len(objects)}')

        # 7. Извлекаем все коды аналогов из ответа
        actual_analogs = {}
        for obj in objects:
            if obj.material and obj.analogMaterial:
                original_code = obj.material.code
                analog_code = obj.analogMaterial.code
                actual_analogs[original_code] = analog_code

        print(f'\nКоличество найденных аналогов в ответе: {len(actual_analogs)}')
        print(f'Ожидаемое количество аналогов: {len(PayloadsFindAnalogs.expected_analogs)}')

        # 8. Сравниваем с ожидаемыми аналогами
        errors = []
        for original_code, expected_analog in PayloadsFindAnalogs.expected_analogs.items():
            if original_code not in actual_analogs:
                errors.append(f'Код {original_code} не найден в ответе')
            elif actual_analogs[original_code] != expected_analog:
                errors.append(
                    f'Для кода {original_code}: '
                    f'ожидался аналог {expected_analog}, '
                    f'получен {actual_analogs[original_code]}'
                )

        # 9. Проверяем результат
        if errors:
            print('\n НАЙДЕНЫ ОШИБКИ:')
            for error in errors:
                print(f'  - {error}')
            assert False, f'Найдено {len(errors)} несоответствий в кодах аналогов:\n' + '\n'.join(errors)
        else:
            print('\n Все коды аналогов совпадают с ожидаемыми!')
            print(f' Успешно проверено {len(actual_analogs)} пар код-аналог')