class PayloadsUpdateOrderInOneCrm:
    """Отправляемые данные на /api/Offer/UpdateOrderInOneCrm"""

    false = False
    true = True
    null = None

    # Базовый payload для обновления заказа в OneCrm
    # ВАЖНО: Многие поля будут заполняться динамически из данных созданного заказа
    # Дефолтные значения взяты из реального рабочего примера API
    update_order_basic = {
        "completed": "1",  # "1" = выполнен
        "deleted": "0",  # "0" = не удалён
        "date": "string",  # Дата заказа - будет заполнена
        "documentNumber": "string",  # Номер документа из Order/Create - будет заполнен
        "contractNumber": "",  # Обязательное поле
        "paymentTermsCode": "RU00",  # Из Order/Create
        "headOffice": "",  # Обязательное поле
        "partnerSAPID": "",  # Обязательное поле
        "partnerINN": "",  # Обязательное поле
        "partnerNamе": "",  # Обязательное поле (русская "е")

        # Организация (с пустым approvers согласно спецификации)
        "organization": {
            "contractorId": "19b59c30-cf60-4000-8fd0-30fc6821a301",  # Будет заполняться
            "inn": "string",
            "contractorName": "string",
            "approvers": []  # Пустой массив (спецификация требует но реальный пример не использует)
        },

        "currency": "RUB",  # Из Order/Create
        "totalAmount": 0,  # Будет рассчитываться
        "warehouse": "0010 Склад Лешково ",  # Дефолт из реального примера
        "taxIncluded": "0",  # "0" = НДС не включён в цену
        "responsibleEngineer": "",  # Обязательное поле
        "addlInfo": "",  # Обязательное поле
        "completeDelivery": false,
        "status": "К выполнению / В резерве",  # Дефолт из реального примера
        "prepayAmountToCollect": 0,
        "prepayAmountToDelivery": 0,
        "deliveryDate": "",  # Обязательное поле
        "deliveryAddress": "",  # Обязательное поле
        "taxType": "Продажа облагается НДС",  # Дефолт из реального примера
        "delayedDeliveryDiscountValue": 0,
        "deliveryCost": 0,
        "discountsCalculated": "1",  # "1" = скидки рассчитаны
        "engineerComment": "test_update_order_in_one_crm",  # Комментарий для теста
        "clientComment": "string",
        "referenceNumber": "Z0000052452",  # Из Order/Create
        "quotationNumber": "string",
        "consignee": "",  # Обязательное поле
        "consigneeSAPID": "",  # Обязательное поле
        "consigneeName": "",  # Обязательное поле
        "salesDepartmentName": "",  # Обязательное поле
        "salesDepartmentCode": "",  # Обязательное поле
        "author": "0000612383",  # authorNumber из Order/Create
        "deliveryType": "Pickup",  # Из deliveryOptions
        "deliveryPartner": "",  # Обязательное поле
        "deliveryAddressValue": "",  # Обязательное поле
        "deliveryAddlInfo": "",  # Обязательное поле
        "contactPerson": "",  # Обязательное поле
        "salesGroup": "RU1",  # Из Order/Create
        "paidInCurrency": "0",  # "0" = оплата не в валюте
        "governmentContract": "",  # Согласно спецификации API

        # Массив материалов
        "materials": [
            {
                "lineNo": 1,
                "deliveryDate": "",  # Будет заполнена датой
                "odid": "19b59c30-cf70-4000-8a50-792e49739201",
                "materialNumber": "003L0144R",
                "materialName": "string",
                "packType": "шт",  # Тип упаковки
                "packsAmount": 25,  # Количество упаковок
                "amountInWareUnits": 25,
                "itemQuantityInCollection": 0,
                "collectionQuantity": 0,
                "priceCondition": "",  # Из реального примера
                "price": 0,
                "amount": 0,
                "tax": "20%",  # Ставка НДС
                "taxAmount": 0,
                "amountWithTax": 0,
                "discountPercent": 0,
                "discountAmount": 0,
                "autoDiscountPercent": 0,
                "cancelReason": "",
                "code": 1,  # Код позиции
                "cancelled": "0",
                "relationshipKey": 0,  # Из реального примера
                "description": "string",
                "warehouse": "",
                "deliveryDays": 0,  # Из реального примера
                "supplyType": "Отгрузить",
                "collectionTypeNumber": "",
                "collectionTypeName": "",
                "salesDepartmentName": "",  # Из реального примера
                "salesDepartmentCode": "",  # Из реального примера
                "stock": 0,  # Складские остатки
                "reservation": 0,
                "onStock": 0,
                "transit": []  # Будет заполнен
            }
        ],

        # График платежей (будет пустым если нет данных)
        "stagesSchedulePayment": [],

        "completeDeliveryFrom": "1970-01-01T00:00:00.000Z",

        # Платное хранение (будет пустым если нет данных)
        "paidStorage": [],

        # Ошибки (будет пустым если нет ошибок)
        "errors": [],

        "currentStatus": "Готов к отгрузке",  # Дефолт из реального примера
        "paymentPercent": 0
    }