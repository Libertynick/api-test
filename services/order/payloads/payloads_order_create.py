from datetime import datetime, timedelta


def _generate_order_create_payload(material_configs: list) -> dict:
    """
    Генерирует payload для Order/Create на основе конфигурации материалов.

    :param material_configs: Список словарей с конфигурацией материалов.
                            Каждый словарь содержит: {'code': str, 'lineType': str, 'quantity': int}
    :return: Готовый payload для отправки в API Order/Create.

    Example:
        configs = [
            {'code': '003L0395R', 'lineType': 'Material', 'quantity': 1},
            {'code': 'w488900', 'lineType': 'HEX', 'quantity': 1}
        ]
        payload = _generate_order_create_payload(configs)
    """
    order_lines = []
    for idx, config in enumerate(material_configs, start=1):
        order_lines.append({
            "materialCode": config['code'],
            "quantity": config.get('quantity', 1),
            "lineNumber": idx,
            "discountPercent": None,
            "endClientDiscountPercent": None,
            "odid": None,
            "deliveryDate": (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:%S+03:00"),
            "lineType": config['lineType'],
            "requestedMaterialCode": None,
            "excludePosition": False
        })

    return {
        "orderLines": order_lines,
        "isEndUserPQ": False,
        "docType": "Quotation",
        "authorNumber": None,
        "currencyDate": None,
        "exchangeRateType": None,
        "projectDiscountConditions": False,
        "debtorAccount": "0014409993",
        "finalBuyerCDLId": None,
        "clientInn": None,
        "userComment": "",
        "engineerComment": "",
        "currency": "RUB",
        "methodCode": "ZWEB",
        "purchaseDate": datetime.now().strftime("%Y-%m-%dT%H:%M:%S+03:00"),
        "delayedDeliveryDiscountValue": None,
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": None,
        "passportId": None,
        "opportunityId": None,
        "specTypeId": None,
        "specificationId": None,
        "salesGroup": "RU1",
        "salesOffice": "RU01",
        "referenceNumber": "Z0000061827",
        "paymentTerms": "RU00",
        "isDraft": False,
        "purchaseType": None,
        "finalBuyerId": None,
        "availableForDistributor": False,
        "autoAvailableForDistributor": None,
        "payPercentComponentsBTP": None,
        "payPercentBeforePlacingIntoProduction": None,
        "customerId": None,
        "isCLHOffer": False,
        "deliveryOptions": {
            "consigneeCode": None,
            "deliveryCost": 2473.57,
            "totalDeliveryWeight": 63.667,
            "comment": "Доставка не включена в стоимость заказа",
            "consigneeAgreementDelivery": None,
            "clientFinalDelivery": {
                "sourceFiasId": "4d5edb43-18c6-4c75-934a-13f169f64c52",
                "destinationFiasId": "c1cfe4b9-f7c2-423c-abfa-6ed1c05a15c5",
                "destinationRegionFiasId": None,
                "address": "г Ростов-на-Дону",
                "paidDelivery": True,
                "wrongDeliveryAddress": None
            },
            "consigneeContacts": {
                "orgINN": "7705238125",
                "orgName": "ООО фирма \"ВОДОКОМФОРТ\" (7705238125)",
                "personName": "Тест",
                "personSurname": "НЕ_РАЗМЕЩАТЬ_НИЧЕГО",
                "personPhone": "+77999999999",
                "personAdditionalPhone": ""
            },
            "endPoint": "ToDoor",
            "desiredDeliveryDate": (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:%S+03:00"),
            "deliverFullSetOnly": True,
            "costIncludedInOrder": False,
            "consigneeId": None,
            "deliveryType": "ToAddress"
        },
        "deliveryOptionsHex": {
            "consigneeCode": None,
            "deliveryCost": 1628.3565,
            "totalDeliveryWeight": 16.733,
            "comment": "Доставка включена в стоимость заказа",
            "consigneeAgreementDelivery": None,
            "clientFinalDelivery": {
                "sourceFiasId": "1d5a97d5-9bdf-44c9-ac42-e201833e7f28",
                "destinationFiasId": "c1cfe4b9-f7c2-423c-abfa-6ed1c05a15c5",
                "destinationRegionFiasId": None,
                "address": "г Ростов-на-Дону, квартира/офис 1660300933",
                "paidDelivery": True,
                "wrongDeliveryAddress": None
            },
            "consigneeContacts": {
                "orgINN": "7705238125",
                "orgName": "ООО фирма \"ВОДОКОМФОРТ\" (7705238125)",
                "personName": "Тест",
                "personSurname": "НЕ_РАЗМЕЩАТЬ_НИЧЕГО",
                "personPhone": "+77999999999",
                "personAdditionalPhone": None
            },
            "endPoint": "ToDoor",
            "desiredDeliveryDate": (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:%S+03:00"),
            "deliverFullSetOnly": True,
            "costIncludedInOrder": True,
            "consigneeId": None,
            "deliveryType": "ToAddress"
        },
        "deliveryOptionsProd": {
            "consigneeCode": None,
            "deliveryCost": 1705.41,
            "totalDeliveryWeight": 26.7,
            "comment": "Доставка не включена в стоимость заказа",
            "consigneeAgreementDelivery": None,
            "clientFinalDelivery": {
                "sourceFiasId": "4d5edb43-18c6-4c75-934a-13f169f64c52",
                "destinationFiasId": "c1cfe4b9-f7c2-423c-abfa-6ed1c05a15c5",
                "destinationRegionFiasId": None,
                "address": "г Ростов-на-Дону",
                "paidDelivery": True,
                "wrongDeliveryAddress": None
            },
            "consigneeContacts": {
                "orgINN": "7705238125",
                "orgName": "ООО фирма \"ВОДОКОМФОРТ\" (7705238125)",
                "personName": "Тест",
                "personSurname": "НЕ_РАЗМЕЩАТЬ_НИЧЕГО",
                "personPhone": "+77999999999",
                "personAdditionalPhone": ""
            },
            "endPoint": "ToDoor",
            "desiredDeliveryDate": (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:%S+03:00"),
            "deliverFullSetOnly": True,
            "costIncludedInOrder": False,
            "consigneeId": None,
            "deliveryType": "ToAddress"
        },
        "deliveryOptionsDZRProd": {
            "consigneeCode": None,
            "deliveryCost": 17493.2865,
            "totalDeliveryWeight": 513.92,
            "comment": "Доставка включена в стоимость заказа",
            "consigneeAgreementDelivery": None,
            "clientFinalDelivery": {
                "sourceFiasId": "1d5a97d5-9bdf-44c9-ac42-e201833e7f28",
                "destinationFiasId": "c1cfe4b9-f7c2-423c-abfa-6ed1c05a15c5",
                "destinationRegionFiasId": None,
                "address": "г Ростов-на-Дону, квартира/офис 1660300933",
                "paidDelivery": True,
                "wrongDeliveryAddress": None
            },
            "consigneeContacts": {
                "orgINN": "7705238125",
                "orgName": "ООО фирма \"ВОДОКОМФОРТ\" (7705238125)",
                "personName": "Тест",
                "personSurname": "НЕ_РАЗМЕЩАТЬ_НИЧЕГО",
                "personPhone": "+77999999999",
                "personAdditionalPhone": None
            },
            "endPoint": "ToDoor",
            "desiredDeliveryDate": (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:%S+03:00"),
            "deliverFullSetOnly": True,
            "costIncludedInOrder": True,
            "consigneeId": None,
            "deliveryType": "ToAddress"
        },
        "deliveryNotificationSettings": None,
        "projectObject": None,
        "setContractDiscounts": False,
        "currencySpecialFixation": False,
        "extendValidit": 0,
        "showPriceWithDiscount": False,
        "showDiscount": False,
        "finalMarkup": None,
        "surchargesPayment": None,
        "surchargesConversion": None,
        "recommendedDistributors": []
    }


class PayloadsOrderCreateMultipleTypes:
    """
    Класс с тестовыми данными для проверки автоматической разбивки заказов.

    Содержит payloads для всех возможных комбинаций типов материалов (от 1 до 4 заказов).
    Каждый payload проверяет корректность разбивки на основе lineType материалов.

    Группы материалов:
    - Группа 1: Material (обычные торговые коды)
    - Группа 2: HEXAdditions (ЗИП и изоляция)
    - Группа 3: TDU, AutoShield, BTP (производственные материалы)
    - Группа 4: HEX, Pump (разборные ПТО и насосы)
    """

    # ========== 1 ЗАКАЗ (5 вариантов) ==========

    one_order_material_only = _generate_order_create_payload([
        {'code': '003L0395R', 'lineType': 'Material'}
    ])

    one_order_hex_additions_only = _generate_order_create_payload([
        {'code': '089N3104', 'lineType': 'HEXAdditions'}
    ])

    one_order_tdu_only = _generate_order_create_payload([
        {'code': 'TDU0011682', 'lineType': 'TDU'}
    ])

    one_order_hex_only = _generate_order_create_payload([
        {'code': 'w488900', 'lineType': 'HEX'}
    ])

    one_order_pump_only = _generate_order_create_payload([
        {'code': 'Q2603240003-5', 'lineType': 'Pump'}
    ])

    # ========== 2 ЗАКАЗА (6 вариантов) ==========

    two_orders_material_hex_additions = _generate_order_create_payload([
        {'code': '003L0395R', 'lineType': 'Material'},
        {'code': '089N3104', 'lineType': 'HEXAdditions'}
    ])

    two_orders_material_tdu = _generate_order_create_payload([
        {'code': '003L0395R', 'lineType': 'Material'},
        {'code': 'TDU0011682', 'lineType': 'TDU'}
    ])

    two_orders_material_hex = _generate_order_create_payload([
        {'code': '003L0395R', 'lineType': 'Material'},
        {'code': 'w488900', 'lineType': 'HEX'}
    ])

    two_orders_hex_additions_tdu = _generate_order_create_payload([
        {'code': '089N3104', 'lineType': 'HEXAdditions'},
        {'code': 'TDU0011682', 'lineType': 'TDU'}
    ])

    two_orders_hex_additions_hex = _generate_order_create_payload([
        {'code': '089N3104', 'lineType': 'HEXAdditions'},
        {'code': 'w488900', 'lineType': 'HEX'}
    ])

    two_orders_tdu_hex = _generate_order_create_payload([
        {'code': 'TDU0011682', 'lineType': 'TDU'},
        {'code': 'w488900', 'lineType': 'HEX'}
    ])

    # ========== 3 ЗАКАЗА (4 варианта) ==========

    three_orders_material_hex_additions_tdu = _generate_order_create_payload([
        {'code': '003L0395R', 'lineType': 'Material'},
        {'code': '089N3104', 'lineType': 'HEXAdditions'},
        {'code': 'TDU0011682', 'lineType': 'TDU'}
    ])

    three_orders_material_hex_additions_hex = _generate_order_create_payload([
        {'code': '003L0395R', 'lineType': 'Material'},
        {'code': '089N3104', 'lineType': 'HEXAdditions'},
        {'code': 'w488900', 'lineType': 'HEX'}
    ])

    three_orders_material_tdu_hex = _generate_order_create_payload([
        {'code': '003L0395R', 'lineType': 'Material'},
        {'code': 'TDU0011682', 'lineType': 'TDU'},
        {'code': 'w488900', 'lineType': 'HEX'}
    ])

    three_orders_hex_additions_tdu_hex = _generate_order_create_payload([
        {'code': '089N3104', 'lineType': 'HEXAdditions'},
        {'code': 'TDU0011682', 'lineType': 'TDU'},
        {'code': 'w488900', 'lineType': 'HEX'}
    ])

    # ========== 4 ЗАКАЗА (1 вариант) ==========

    four_orders_all_groups = _generate_order_create_payload([
        {'code': '003L0395R', 'lineType': 'Material'},
        {'code': 'w488900', 'lineType': 'HEX'},
        {'code': '089N3104', 'lineType': 'HEXAdditions'},
        {'code': '089N4178', 'lineType': 'HEXAdditions'},
        {'code': 'TDU0011682', 'lineType': 'TDU'},
        {'code': '065B2979R', 'lineType': 'Material'},
        {'code': 'Q2603240003-5', 'lineType': 'Pump'},
        {'code': '015P9157', 'lineType': 'Material'}
    ])