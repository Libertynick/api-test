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
        "debtorAccount": "0014403847",
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
        "isDraft": true  # ← ДОБАВИТЬ ЭТУ СТРОКУ!
    }