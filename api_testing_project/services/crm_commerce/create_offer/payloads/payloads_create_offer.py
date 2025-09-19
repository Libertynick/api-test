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

        # Значения ниже бери из уже используемых в проекте валидных данных (как в order/create),
        # чтобы не плодить новые тестовые сущности.
        "debtorAccount": "0014403847",  # пример: как в payloads Order/Create
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "paymentTerms": "RU00",
        # Доставка: достаточно валидного consigneeId. Остальное опционально и может меняться стендом.
        "deliveryOptions": {
            "consigneeId": "00000000-0000-0000-0000-000000000000"
        },

        # Минимальный список позиций. В самих тестах мы подменяем его данными из Simulate.
        "orderLines": [
            {
                "materialCode": "003L0144R",
                "quantity": 1,
                "lineNumber": 1,
                "lineType": "Material"
                # "odid": null,                  # можно добавить, если Simulate вернет
                # "deliveryDate": "2025-09-18T00:00:00Z"  # подставим из schedules Simulate, если есть
            }
        ]
    }