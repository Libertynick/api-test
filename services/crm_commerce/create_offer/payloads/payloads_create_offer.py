class PayloadsCreateOffer:
    """Отправляемые данные в API CrmCommerce/CreateOffer"""
    false = False
    true = True
    null = None

    # Базовый валидный шаблон.
    base_valid_offer = {
        "source": "CRM",
        "currency": "RUB",
        "exchangeRateType": "CBR",
        "debtorAccount": "RT25-7705238125-HE",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "paymentTerms": "RU00",
        "deliveryOptions": {
            "consigneeId": "00000000-0000-0000-0000-000000000000"
        },
        "orderLines": [
            {
                "materialCode": "003L0144R",
                "quantity": 1,
                "lineNumber": 1,
                "lineType": "Material"
            }
        ],
        "isDraft": true
    }

    # Delivery options для Industrial (HEX) - доставка до ТК
    delivery_options_dzr_prod_industrial = {
        "consigneeCode": None,
        "deliveryCost": 0,
        "totalDeliveryWeight": 154.26,
        "comment": None,
        "consigneeAgreementDelivery": {
            "sourceFiasId": "00000000-0000-0000-0000-000000000000",
            "destinationFiasId": None,
            "address": None,
            "paidDelivery": False,
            "conditionDescription": "Стандартные договорные условия",
            "inn": "5249173547"
        },
        "clientFinalDelivery": None,
        "consigneeContacts": None,
        "endPoint": "ToTK",  # ToTK для организации
        "desiredDeliveryDate": "2025-10-07T13:26:16+03:00",
        "deliverFullSetOnly": False,
        "costIncludedInOrder": False,
        "consigneeId": "00000000-0000-0000-0000-000000000000",
        "deliveryType": "PickupDZR",
        "condition": "RU"
    }

    # Project Object для Industrial с проектным условием
    project_object_industrial = {
        "id": "9abbcb6b-91ac-4d69-bbee-d0d0f583e18d",  # passportId
        "name": "Детский сад на 240 мест в г. Тарко-Сале, мкр.Южный",
        "address": "Ямало-Ненецкий АО, г Тарко-Сале, мкр Южный",
        "number": 1178586,
        "comment": " "
    }