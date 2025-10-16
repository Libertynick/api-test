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


def _prepare_delivery_options(offer_payload, delivery_key, config):
    """
    Подготовка delivery options в зависимости от типа материала

    Args:
        offer_payload: Основной payload для offer
        delivery_key: Ключ типа доставки ('deliveryOptions', 'deliveryOptionsProd', 'deliveryOptionsDZRProd')
        config: Конфигурация теста
    """
    if delivery_key == 'deliveryOptionsProd':
        # Для BTP используем deliveryOptionsProd вместо deliveryOptions
        if "deliveryOptions" in offer_payload:
            offer_payload["deliveryOptionsProd"] = offer_payload.pop("deliveryOptions")

    elif delivery_key == 'deliveryOptionsDZRProd':
        # Для Industrial (HEX) используем deliveryOptionsDZRProd
        if "deliveryOptions" in offer_payload:
            offer_payload.pop("deliveryOptions")

        # Используем готовый payload
        offer_payload["deliveryOptionsDZRProd"] = dict(
            PayloadsCreateOffer.delivery_options_dzr_prod_industrial
        )

        # Добавляем projectObject для Industrial
        project_obj = dict(PayloadsCreateOffer.project_object_industrial)
        project_obj["id"] = config.get('passportId')  # Обновляем ID из конфига
        offer_payload["projectObject"] = project_obj


def _add_config_fields_to_payload(payload, config, exclude_fields):
    """
    Добавляет специфичные поля из конфига в payload

    Args:
        payload: Словарь payload для запроса
        config: Конфигурация теста
        exclude_fields: Множество полей, которые не нужно добавлять
    """
    for key, value in config.items():
        if key not in exclude_fields:
            payload[key] = value


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
        # Поля для проектного условия
        'personId': '1c26afd2-1d97-4b7f-92fb-dd21ed412eea',
        'passportId': '4DBB2A44-D895-468D-A51F-AE98B9B3D487',
        'specTypeId': '02061701-51E6-402E-B18F-7BAE7A27F6FB',
        'specificationId': '29CDC69A-1CBA-47CF-9F93-8DECBDAF3D9A',
        'purchaseType': 'C8EC0EE8-FB5D-4AE1-A664-B2C46A914E46',
        'finalBuyerId': 'daa47b0f-8c66-42f9-a5df-44fae4ff18e8',
        'customerId': 'acb8f425-c3b6-4b38-9f34-1e7fbfd53fa9',
        'exchangeRateType': 'YRU',
        'currencySpecialFixation': True,
        'setContractDiscounts': True,
        'isDraft': True
    },
    'Industrial': {
    'simulate_payload': PayloadsOrderSimulate.order_simulate_add_to_cart_industrial,
    'delivery_options_key': 'deliveryOptionsDZRProd',
    'line_type': 'HEX',
    'quantity_increase': 1,
    'discount_percent': 0,
    'description': 'Industrial HEX code - FROM ORGANIZATION with Project Condition',
    'offerType': 3,
    'passportId': '9abbcb6b-91ac-4d69-bbee-d0d0f583e18d',
    'specificationId': 'ece5153c-fbbd-4b55-816e-e7dd035364ad',
    'finalBuyerId': 'BF2FE82C-FED9-414B-9BA3-403CE76C9000',
    'customerId': 'BF2FE82C-FED9-414B-9BA3-403CE76C9000',
    'purchaseType': '121B015A-E76D-4688-9BB6-2A56EC6DE2EF',
    'personId': 'b898f86a-6070-451b-9a14-47ba949c8cb8',
    'isDraft': True,
    'currencySpecialFixation': True,
    'setContractDiscounts': True,
    'exchangeRateType': 'YRU',
    'clientInn': '5249173547',
    'sellerId': '20C340FE-6AFF-486F-B248-FD8DBE2C93CD',
    'userName': 'RUCO1845',
    'validDays': 3,
    'docType': 'Order',
    'usePromoCurrency': False,
    'surchargesPayment': '0',
    'surchargesConversion': 0,
    'payPercentBeforePlacingIntoProduction': 100,
    'isEndUserPQ': False,
    'availableForDistributor': False,
    'autoAvailableForDistributor': True,
    'isExport': False,
    'autoFromEngSpec': False,
    'isNew': False,
    'sourceOfferId': None,
    'IsATOffer': False,
    'priceFixingCorridorValue': None,
    'isEstimateOffer': False,
    'referenceNumber': None
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
        if material_code and odid:
            code_to_odid[material_code] = odid
            print(f"Mapping: {material_code} → {odid}")

    # Обновляем ODID в orderLines
    for line in order_lines:
        mat_code = line.get("materialCode")
        if mat_code in code_to_odid:
            line["odid"] = code_to_odid[mat_code]
            print(f"✓ Updated ODID for {mat_code}: {line['odid']}")
        else:
            print(f"⚠ No ODID found for {mat_code}")

    return order_lines


def _prepare_order_lines_for_update(order_lines, quantity_increase, discount_percent):
    """
    Подготовка orderLines для UpdateOffer:
    - Увеличиваем quantity на заданное значение
    - Добавляем скидки endClientDiscountPercent
    - Удаляем поля с None значениями для DateTime
    """
    updated_lines = []

    for line in order_lines:
        updated_line = dict(line)

        # Увеличиваем quantity
        current_qty = line.get("quantity", 0)
        new_qty = current_qty + quantity_increase
        updated_line["quantity"] = new_qty

        # Добавляем скидки
        updated_line["endClientDiscountPercent"] = discount_percent
        updated_line["discountPercent"] = 0

        # Удаляем deliveryDate если он None
        if updated_line.get("deliveryDate") is None:
            updated_line.pop("deliveryDate", None)
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
        2. CreateOffer - создаем КП (isDraft=True для Industrial)
        3. FullCommerceNew (1) - получаем ODID позиций
        4. UpdateOffer - обновляем КП (quantity +1, скидки, isDraft=False для Industrial)
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

            # Подготовка delivery options в зависимости от типа
            _prepare_delivery_options(offer_payload, delivery_key, config)

            # Добавляем специфичные поля для типа материала из конфига
            exclude_fields = {'simulate_payload', 'delivery_options_key', 'line_type',
                              'quantity_increase', 'discount_percent', 'description'}

            _add_config_fields_to_payload(offer_payload, config, exclude_fields)

            offer_payload['userComment'] = 'ТЕСТ флоу методов - CreateOffer'

            print("\n" + "=" * 80)
            print("CREATE OFFER PAYLOAD (что отправляем):")
            print(offer_payload)
            print("=" * 80 + "\n")

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

            full_data = full_resp.get("objects", [{}])[0].get("data") or []
            assert full_data, "FullCommerce: пустой data"

            full_offer = full_data[0]
            assert (
                    full_offer.get("crmCommerceId") == offer_id
                    or (offer_number and full_offer.get("commerceNumber") == offer_number)
            ), f"В FullCommerceNew не нашли оффер id={offer_id}, number={offer_number}"

            # Обновляем orderLines с правильными ODID
            order_lines = _update_order_lines_with_odid(order_lines, full_resp)
            print(f"Updated order lines with ODID: {order_lines}")

        # Шаг 4 — UpdateOffer (обновляем КП: quantity +1, скидки, isDraft → False для Industrial)
        with allure.step("POST /api/Order/UpdateOffer (quantity +1, discounts, isDraft → False)"):
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

            # Формируем payload для UpdateOffer на основе base_update_offer
            update_payload = dict(PayloadsOrderUpdateOffer.base_update_offer)
            update_payload["offerId"] = offer_id
            update_payload["opportunityId"] = opportunity_id  # ← ВАЖНО!
            update_payload["orderLines"] = updated_order_lines
            update_payload.setdefault("paymentTerms", "RU00")

            # Подготовка delivery options для UpdateOffer
            _prepare_delivery_options(update_payload, delivery_key, config)

            # Добавляем специфичные поля из конфига (включая проектное условие)
            exclude_fields = {'simulate_payload', 'delivery_options_key', 'line_type',
                              'quantity_increase', 'discount_percent', 'description', 'isDraft'}

            _add_config_fields_to_payload(update_payload, config, exclude_fields)

            # Для Industrial переводим из черновика в согласованный
            if config_key == 'Industrial':
                update_payload['isDraft'] = False

            update_payload['userComment'] = 'ТЕСТ флоу методов - UpdateOffer'

            print("\n" + "=" * 80)
            print("UPDATE OFFER PAYLOAD (что отправляем):")
            print(update_payload)
            print("=" * 80 + "\n")

            update_resp = self.update_offer_api.post_update_offer(update_payload)
            print("UPDATE OFFER RESPONSE")
            print(update_resp)

            assert update_resp["status"] == "Ok", f"UpdateOffer status != Ok: {update_resp}"
            print("✓ UpdateOffer успешно выполнен!")

        # Шаг 5 — FullCommerceNew (второй раз - проверяем изменения после UpdateOffer)
        with allure.step("GET /api/CrmCommerce/FullCommerceNew (после UpdateOffer)"):
            full_resp_after = self.full_api.get_full_commerce_new_by_request_id(offer_id)
            print("FULL COMMERCE NEW RESPONSE (после UpdateOffer)")
            print(full_resp_after)

            assert full_resp_after["status"] == "Ok", f"FullCommerce status != Ok: {full_resp_after}"

            # Проверяем, что изменения применились
            details = full_resp_after["objects"][0].get("details", [])
            assert details, "FullCommerce: нет details после UpdateOffer"

            for detail in details:
                material_code = detail.get("materialCode") or detail.get("code")
                qty = detail.get("qty")
                end_client_discount = detail.get("clientDiscountPercent", 0)

                print(f"\nПроверка позиции {material_code}:")
                print(f"  Количество: {qty}")
                print(f"  Скидка конечного клиента: {end_client_discount}%")

                # Проверяем количество
                expected_qty = original_quantity + quantity_increase
                assert qty == expected_qty, \
                    f"Количество не обновилось для {material_code}. " \
                    f"Ожидали {expected_qty}, получили {qty}"

                # Проверяем скидку
                assert end_client_discount == discount_percent, \
                    f"Скидка конечного клиента не обновилась для {material_code}. " \
                    f"Ожидали {discount_percent}%, получили {end_client_discount}%"

            print(f"✓ Все изменения успешно применились для материала {material_code}!")

            # Обновляем orderLines для Order/Create с новыми ODID (на случай если они изменились)
            order_lines_for_create = _update_order_lines_with_odid(updated_order_lines, full_resp_after)

        # Шаг 6 — Order/Create (создаем заказ из обновленного КП)
        with allure.step("POST /api/Order/Create"):
            order_payload = dict(
                PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_materials_prepayment_pickup)
            order_payload["orderLines"] = order_lines_for_create
            order_payload["offerId"] = offer_id
            _prepare_delivery_options(order_payload, delivery_key, config)
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

    @pytest.mark.stage
    def test_industrial_chain_without_order(self):
        """
        Флоу для Industrial (HEX) БЕЗ создания заказа:
        1. Simulate - получаем информацию о материале
        2. CreateOffer - создаем КП (isDraft=True)
        3. FullCommerceNew (1) - получаем ODID позиций
        4. UpdateOffer - обновляем КП (quantity +1, скидки, isDraft=False)
        5. FullCommerceNew (2) - проверяем что изменения применились

        ВАЖНО: Order/Create НЕ делаем, т.к. КП остается в статусе "Согласование"
        """
        # Получаем конфигурацию для Industrial
        config = TEST_CONFIGS['Industrial']
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

            # Подготовка delivery options в зависимости от типа
            _prepare_delivery_options(offer_payload, delivery_key, config)

            # Добавляем специфичные поля для типа материала из конфига
            exclude_fields = {'simulate_payload', 'delivery_options_key', 'line_type',
                              'quantity_increase', 'discount_percent', 'description'}

            _add_config_fields_to_payload(offer_payload, config, exclude_fields)

            offer_payload['userComment'] = 'ТЕСТ флоу методов Industrial - CreateOffer'

            print("\n" + "=" * 80)
            print("CREATE OFFER PAYLOAD (что отправляем):")
            print(offer_payload)
            print("=" * 80 + "\n")

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

            full_data = full_resp.get("objects", [{}])[0].get("data") or []
            assert full_data, "FullCommerce: пустой data"

            full_offer = full_data[0]
            assert (
                    full_offer.get("crmCommerceId") == offer_id
                    or (offer_number and full_offer.get("commerceNumber") == offer_number)
            ), f"В FullCommerceNew не нашли оффер id={offer_id}, number={offer_number}"

            # Обновляем orderLines с правильными ODID
            order_lines = _update_order_lines_with_odid(order_lines, full_resp)
            print(f"Updated order lines with ODID: {order_lines}")

        # Шаг 4 — UpdateOffer (обновляем КП: quantity +1, скидки, isDraft → False)
        with allure.step("POST /api/Order/UpdateOffer (quantity +1, discounts, isDraft → False)"):
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

            # Формируем payload для UpdateOffer на основе base_update_offer
            update_payload = dict(PayloadsOrderUpdateOffer.base_update_offer)
            update_payload["offerId"] = offer_id
            update_payload["opportunityId"] = opportunity_id
            update_payload["orderLines"] = updated_order_lines
            update_payload.setdefault("paymentTerms", "RU00")

            # Подготовка delivery options для UpdateOffer
            _prepare_delivery_options(update_payload, delivery_key, config)

            # Добавляем специфичные поля из конфига (включая проектное условие)
            exclude_fields = {'simulate_payload', 'delivery_options_key', 'line_type',
                              'quantity_increase', 'discount_percent', 'description'}

            _add_config_fields_to_payload(update_payload, config, exclude_fields)

            # Для Industrial от организации isDraft ОСТАЕТСЯ True (не меняем на False!)
            # Все остальные поля уже добавлены из конфига

            update_payload['userComment'] = 'ТЕСТ флоу методов Industrial - UpdateOffer'

            print("\n" + "=" * 80)
            print("UPDATE OFFER PAYLOAD (что отправляем):")
            print(update_payload)
            print("=" * 80 + "\n")

            update_resp = self.update_offer_api.post_update_offer(update_payload)
            print("UPDATE OFFER RESPONSE")
            print(update_resp)

            assert update_resp["status"] == "Ok", f"UpdateOffer status != Ok: {update_resp}"
            print("✓ UpdateOffer успешно выполнен!")

        # Шаг 5 — FullCommerceNew (второй раз - проверяем изменения после UpdateOffer)
        with allure.step("GET /api/CrmCommerce/FullCommerceNew (после UpdateOffer)"):
            full_resp_after = self.full_api.get_full_commerce_new_by_request_id(offer_id)
            print("FULL COMMERCE NEW RESPONSE (после UpdateOffer)")
            print(full_resp_after)

            assert full_resp_after["status"] == "Ok", f"FullCommerce status != Ok: {full_resp_after}"

            # Проверяем, что изменения применились
            details = full_resp_after["objects"][0].get("details", [])
            assert details, "FullCommerce: нет details после UpdateOffer"

            for detail in details:
                material_code = detail.get("materialCode") or detail.get("code")
                qty = detail.get("qty")
                end_client_discount = detail.get("clientDiscountPercent", 0)

                print(f"\nПроверка позиции {material_code}:")
                print(f"  Количество: {qty}")
                print(f"  Скидка конечного клиента: {end_client_discount}%")

                # Проверяем количество
                expected_qty = original_quantity + quantity_increase
                assert qty == expected_qty, \
                    f"Количество не обновилось для {material_code}. " \
                    f"Ожидали {expected_qty}, получили {qty}"

                # Проверяем скидку
                assert end_client_discount == discount_percent, \
                    f"Скидка конечного клиента не обновилась для {material_code}. " \
                    f"Ожидали {discount_percent}%, получили {end_client_discount}%"

            print(f" Все изменения успешно применились для Industrial!")

            # Проверяем статус КП
            status_display = full_resp_after["objects"][0]["data"][0].get("statusDisplay")
            print(f"\n Статус КП после UpdateOffer: {status_display}")
            print("Order/Create НЕ выполняется - КП остается в статусе согласования")

            print("\n Тест Industrial успешно выполнен! (без Order/Create)")