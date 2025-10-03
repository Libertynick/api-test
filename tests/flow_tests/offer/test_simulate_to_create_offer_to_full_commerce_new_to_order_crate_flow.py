import allure
import pytest

from api_testing_project.services.order.api.api_order_simulate import ApiOrderSimulate
from api_testing_project.services.order.payloads.payloads_order_simulate import PayloadsOrderSimulate
from api_testing_project.services.crm_commerce.create_offer.api.api_create_offer import ApiCreateOffer
from api_testing_project.services.crm_commerce.create_offer.payloads.payloads_create_offer import PayloadsCreateOffer
from api_testing_project.services.crm_commerce.full_commerce_new.api.api_full_commerce_new import FullCommerceNewApi
from api_testing_project.services.order.api.api_order_create import ApiOrderCreate
from api_testing_project.services.order.api.api_order_update_offer import ApiOrderUpdateOffer
from api_testing_project.services.order.payloads.payloads_order_create import PayloadsOrderCreateWithOneCode
from api_testing_project.services.order.payloads.payloads_order_update_offer import PayloadsOrderUpdateOffer


# Конфигурация тестов для разных типов КП (материалов)
TEST_CONFIGS = {
    'Material': {
        'simulate_payload': PayloadsOrderSimulate.order_simulate_add_to_cart_material,
        'delivery_options_key': 'deliveryOptions',
        'line_type': 'Material',
        'quantity_increase': 5,
        'discount_percent': 10,
        'description': 'Material code - full flow with UpdateOffer'
    },
    'BTP': {
    'simulate_payload': PayloadsOrderSimulate.order_simulate_add_to_cart_btp,
    'delivery_options_key': 'deliveryOptionsProd',
    'line_type': 'BTP',
    'quantity_increase': 1,
    'discount_percent': 10,
    'description': 'BTP code - full flow with UpdateOffer',
    'passportId': '4DBB2A44-D895-468D-A51F-AE98B9B3D487',
    'specTypeId': '02061701-51E6-402E-B18F-7BAE7A27F6FB'
    }
}

def _order_lines_from_simulate(sim_obj):
    """Создаем orderLines из ответа Simulate (без ODID)"""
    line = sim_obj["orderLines"][0]
    qty = line.get("orderedQuantity")

    item = {
        "materialCode": line.get("materialCode"),
        "quantity": qty,
        "lineNumber": line.get("lineNumber"),
        "lineType": line.get("lineType"),
        "odid": line.get("odid"),  # пока None, обновим позже
    }

    schedules = line.get("schedules") or []
    if schedules and schedules[0].get("deliveryDate"):
        item["deliveryDate"] = schedules[0]["deliveryDate"]

    return [item]


def _update_order_lines_with_odid(order_lines, full_resp):
    """Обновляем orderLines правильными ODID из ответа FullCommerceNew"""
    # Извлекаем позиции из FullCommerceNew
    full_objects = full_resp.get("objects", [])
    if not full_objects:
        print("Нет objects в ответе FullCommerceNew")
        return order_lines

    # ODID находится в details, а не в data.orders!
    details = full_objects[0].get("details", [])
    if not details:
        print("Нет details в ответе FullCommerceNew")
        return order_lines

    print(f"Найдено {len(details)} позиций в details")

    # Создаем маппинг materialCode - odid
    code_to_odid = {}
    for detail in details:
        material_code = detail.get("materialCode") or detail.get("code")
        odid = detail.get("id")  # в details ODID называется "id"!

        print(f"Detail: materialCode={material_code}, id={odid}")

        if material_code and odid:
            code_to_odid[material_code] = odid

    print(f"Маппинг code -> odid: {code_to_odid}")

    # Обновляем orderLines
    updated_lines = []
    for line in order_lines:
        updated_line = dict(line)  # копируем
        material_code = line.get("materialCode")

        if material_code in code_to_odid:
            updated_line["odid"] = code_to_odid[material_code]
            print(f"Обновили ODID для {material_code}: {code_to_odid[material_code]}")
        else:
            print(f"Не найден ODID для материала {material_code}")

        updated_lines.append(updated_line)

    return updated_lines


def _prepare_order_lines_for_update(order_lines, quantity_increase=5, discount_percent=10):
    """
    Подготавливаем orderLines для UpdateOffer с увеличением количества и добавлением скидок
    :param order_lines: Текущие orderLines с ODID
    :param quantity_increase: На сколько увеличить количество (по умолчанию +5)
    :param discount_percent: Процент скидки (по умолчанию 10)
    :return: Обновленные orderLines
    """
    updated_lines = []
    for line in order_lines:
        updated_line = dict(line)

        # Увеличиваем количество
        current_qty = line.get("quantity", 1)
        new_qty = current_qty + quantity_increase
        updated_line["quantity"] = new_qty

        # Добавляем скидки
        updated_line["discountPercent"] = discount_percent
        updated_line["endClientDiscountPercent"] = discount_percent

        # Добавляем дополнительные поля для UpdateOffer
        updated_line.setdefault("requestedMaterialCode", None)
        updated_line.setdefault("excludePosition", False)
        updated_line.setdefault("usePromoCurrency", False)
        updated_line.setdefault("useSpecialPrice", False)
        updated_line.setdefault("copiedFromId", None)

        # deliveryDate - НЕ добавляем, если его нет!
        # Сервер не может обработать None для DateTime полей

        print(f"Обновили позицию: {line.get('materialCode')} - quantity: {current_qty} -> {new_qty}, "
              f"discounts: 0% -> {discount_percent}%")

        updated_lines.append(updated_line)

    return updated_lines


@pytest.mark.stage
@pytest.mark.dapi
@allure.feature("DAPI")
@allure.story("Simulate -> CreateOffer -> UpdateOffer -> FullCommerceNew -> Order/Create")
class TestSimulateOfferUpdateOfferFullOrderE2E:
    def setup_method(self):
        self.simulate_api = ApiOrderSimulate()
        self.create_offer_api = ApiCreateOffer()
        self.update_offer_api = ApiOrderUpdateOffer()
        self.full_api = FullCommerceNewApi()
        self.order_create_api = ApiOrderCreate()

    @pytest.mark.stage
    @pytest.mark.parametrize('config_key', ['Material', 'BTP'])
    def test_full_chain_with_update_offer(self, config_key):
        """
        Полный цикл теста с обновлением КП:
        1. Simulate - получаем информацию о материале
        2. CreateOffer - создаем КП
        3. FullCommerceNew (1) - получаем ODID позиций
        4. UpdateOffer - обновляем КП (quantity +5, скидки 10%)
        5. FullCommerceNew (2) - проверяем что изменения применились
        6. Order/Create - создаем заказ из обновленного КП
        """
        # Получаем конфигурацию для текущего типа материала
        config = TEST_CONFIGS[config_key]
        sim_payload = config['simulate_payload']
        delivery_key = config['delivery_options_key']
        quantity_increase = config['quantity_increase']
        discount_percent = config['discount_percent']

        print(f"\n=== Running test for: {config['description']} ===")


        # Шаг 1 — Simulate
        with allure.step("POST /api/Order/Simulate"):
            sim_resp = self.simulate_api.post_order_simulate(sim_payload)
            print("SIMULATE RESPONSE")
            print(sim_resp)

            assert sim_resp["status"] == "Ok", f"Simulate status != Ok: {sim_resp}"
            assert sim_resp["objects"], "Simulate: пустой objects"
            assert sim_resp["objects"][0].get("orderLines"), "Simulate: нет orderLines"

            # Сохраняем исходное количество для проверок
            original_quantity = sim_resp["objects"][0]["orderLines"][0].get("orderedQuantity")
            print(f"Исходное количество из Simulate: {original_quantity}")

            order_lines = _order_lines_from_simulate(sim_resp["objects"][0])
            print(f"Order lines from Simulate: {order_lines}")

        # Шаг 2 — CreateOffer
        with allure.step("POST /api/CrmCommerce/CreateOffer"):
            offer_payload = dict(PayloadsCreateOffer.base_valid_offer)
            offer_payload["orderLines"] = order_lines
            offer_payload.setdefault("paymentTerms", "RU00")

            # Для BTP используем deliveryOptionsProd вместо deliveryOptions
            if delivery_key == 'deliveryOptionsProd':
                if "deliveryOptions" in offer_payload:
                    offer_payload["deliveryOptionsProd"] = offer_payload.pop("deliveryOptions")

            # Добавляем passportId и specTypeId для проектных условий (если есть в конфиге)
            if 'passportId' in config:
                offer_payload['passportId'] = config['passportId']
            if 'specificationId' in config:
                offer_payload['specificationId'] = config['specificationId']

            offer_payload['userComment'] = 'ТЕСТ флоу методов - CreateOffer'

            offer_resp = self.create_offer_api.post_create_offer(offer_payload)
            print("CREATE OFFER RESPONSE")
            print(offer_resp)

            assert offer_resp["status"] == "Ok", f"CreateOffer status != Ok: {offer_resp}"
            assert offer_resp.get("objects"), "CreateOffer: пустой objects"

            offers = offer_resp["objects"][0].get("offers") or []
            assert offers, f"CreateOffer: нет offers в ответе: {offer_resp}"
            offer_id = offers[0]["id"]
            offer_number = offers[0].get("number")
            print(f"Created offer_id: {offer_id}")
            print(f"Created offer_number: {offer_number}")

        # Шаг 3 — FullCommerceNew (первый раз - получаем ODID)
        with allure.step("GET /api/CrmCommerce/FullCommerceNew (до UpdateOffer)"):
            full_resp = self.full_api.get_full_commerce_new_by_request_id(offer_id)
            print("FULL COMMERCE NEW RESPONSE (до UpdateOffer)")
            print(full_resp)

            assert full_resp["status"] == "Ok", f"FullCommerce status != Ok: {full_resp}"
            full_objects = full_resp.get("objects") or []
            assert full_objects, "FullCommerce: пустой objects"

            full_data = full_objects[0].get("data") or []
            assert full_data, "FullCommerce: пустой data"

            full_offer = full_data[0]
            assert (
                    full_offer.get("crmCommerceId") == offer_id
                    or (offer_number and full_offer.get("commerceNumber") == offer_number)
            ), f"В FullCommerceNew не нашли оффер id={offer_id}, number={offer_number}"

            # Обновляем orderLines с правильными ODID
            order_lines = _update_order_lines_with_odid(order_lines, full_resp)
            print(f"Updated order lines with ODID: {order_lines}")

        # Шаг 4 — UpdateOffer (обновляем КП: quantity +5, скидки 10%)
        with allure.step("POST /api/Order/UpdateOffer (quantity +5, discounts 10%)"):
            # Подготавливаем orderLines для обновления
            updated_order_lines = _prepare_order_lines_for_update(
                order_lines,
                quantity_increase=quantity_increase,
                discount_percent=discount_percent
            )

            # Извлекаем данные из FullCommerceNew
            full_data = full_resp["objects"][0]["data"][0]
            opportunity_id = full_data.get("opportunityId")

            print(f"OpportunityId из FullCommerceNew: {opportunity_id}")

            # Формируем payload для UpdateOffer на основе CreateOffer payload
            update_payload = dict(PayloadsOrderUpdateOffer.base_update_offer)
            update_payload["offerId"] = offer_id
            update_payload["opportunityId"] = opportunity_id  # ← ВАЖНО! Берем из FullCommerceNew
            update_payload["orderLines"] = updated_order_lines

            # Копируем важные поля из CreateOffer payload
            update_payload["debtorAccount"] = offer_payload.get("debtorAccount", "0014403847")
            update_payload["personId"] = offer_payload.get("personId", "920bb836-8ee4-4571-b5bd-94bd28c29d32")
            update_payload["paymentTerms"] = offer_payload.get("paymentTerms", "RU00")
            update_payload["currency"] = offer_payload.get("currency", "RUB")
            update_payload["source"] = offer_payload.get("source", "CRM")
            update_payload["exchangeRateType"] = offer_payload.get("exchangeRateType", "CBR")

            # Копируем правильный deliveryOptions в зависимости от типа материала
            if delivery_key in offer_payload:
                update_payload[delivery_key] = offer_payload[delivery_key]
            elif "deliveryOptions" in offer_payload:
                # Fallback на стандартный deliveryOptions если специфичного нет
                update_payload["deliveryOptions"] = offer_payload["deliveryOptions"]

            # Формируем headers с userId
            headers = {
                'userId': '770B060C-4A2F-4638-ADBB-DFBEB1813754'
            }

            print("UPDATE OFFER PAYLOAD")
            print(update_payload)
            print("UPDATE OFFER HEADERS")
            print(headers)

            update_resp = self.update_offer_api.post_update_offer(update_payload, headers=headers)
            print("UPDATE OFFER RESPONSE")
            print(update_resp)

            assert update_resp["status"] == "Ok", f"UpdateOffer status != Ok: {update_resp}"
            assert update_resp.get("objects"), "UpdateOffer: пустой objects"

            # Проверяем что обновление прошло успешно
            update_status = update_resp["objects"][0].get("status")
            assert update_status == True, f"UpdateOffer: status в objects != True: {update_status}"

            print("UpdateOffer выполнен успешно!")

        # Шаг 5 — FullCommerceNew (второй раз - проверяем изменения)
        with allure.step("GET /api/CrmCommerce/FullCommerceNew (после UpdateOffer) - проверка изменений"):
            full_resp_after = self.full_api.get_full_commerce_new_by_request_id(offer_id)
            print("FULL COMMERCE NEW RESPONSE (после UpdateOffer)")
            print(full_resp_after)

            assert full_resp_after["status"] == "Ok", f"FullCommerce status != Ok: {full_resp_after}"

            # Получаем details для проверки изменений
            details_after = full_resp_after.get("objects", [{}])[0].get("details", [])
            assert details_after, "FullCommerce: нет details после UpdateOffer"

            # Проверяем изменения в первой позиции
            first_detail = details_after[0]
            material_code = first_detail.get("materialCode") or first_detail.get("code")

            # Проверка 1: Количество должно увеличиться на 5
            updated_quantity = first_detail.get("quantity") or first_detail.get("qty")
            expected_quantity = original_quantity + quantity_increase
            print(f"Проверка количества: ожидаем {expected_quantity}, получили {updated_quantity}")
            assert updated_quantity == expected_quantity, \
                f"Количество не обновилось! Ожидали {expected_quantity}, получили {updated_quantity}"

            # Проверка 2: Скидка дистрибьютора должна быть 10%
            discount_distr = first_detail.get("discount") or first_detail.get("discountPercent")
            print(f"Проверка discount: ожидаем 10%, получили {discount_distr}%")
            assert discount_distr == 10, \
                f"discount не обновилась! Ожидали 10%, получили {discount_distr}%"

            # Проверка 3: Скидка конечного клиента должна быть 10%
            end_client_discount = (
                    first_detail.get("clientDiscountPercent") or
                    first_detail.get("endClientDiscountPercent")
            )
            if end_client_discount is not None:
                print(f"Проверка clientDiscountPercent: ожидаем 10%, получили {end_client_discount}%")
                assert end_client_discount == 10, \
                    f"clientDiscountPercent не обновилась! Ожидали 10%, получили {end_client_discount}%"

            print(f"✓ Все изменения успешно применились для материала {material_code}!")

            # Обновляем orderLines для Order/Create с новыми ODID (на случай если они изменились)
            order_lines_for_create = _update_order_lines_with_odid(updated_order_lines, full_resp_after)

        # Шаг 6 — Order/Create (создаем заказ из обновленного КП)
        with allure.step("POST /api/Order/Create"):
            order_payload = dict(
                PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_materials_prepayment_pickup)
            order_payload["orderLines"] = order_lines_for_create
            order_payload["offerId"] = offer_id
            order_payload.setdefault("paymentTerms", "RU00")
            order_payload['userComment'] = 'ТЕСТ флоу методов - Order/Create'

            print("ORDER CREATE PAYLOAD")
            print(order_payload)

            order_resp = self.order_create_api.post_order_create(order_payload)
            print("ORDER CREATE RESPONSE")
            print(order_resp)

            assert order_resp["status"] == "Ok", f"Order/Create status != Ok: {order_resp}"
            assert order_resp.get("objects"), "Order/Create: пустой objects"

            print("✓ Тест успешно выполнен! Весь цикл с UpdateOffer завершен.")