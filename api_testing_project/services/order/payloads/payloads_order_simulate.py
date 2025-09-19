class PayloadsOrderSimulate:
    """Отправляемые данные в API Order/Simulate"""
    false = False
    true = True
    null = None

    #  Запрос на добавление в корзину материалов (стандартный запрос, без спец. условий)
    order_simulate_add_to_cart_material = {
        "debtorAccount": "0014403847",
        "materials": [
            {
                "materialCode": "003L0144R",
                "quantity": 25,
                "lineNumber": 1,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    # Запрос на добавление в корзину ПТО (стандартный запрос, без спец. условий)
    order_simulate_add_to_cart_pto = {
        "debtorAccount": "0014403847",
        "materials": [
            {
                "materialCode": "878139",
                "quantity": 10,
                "lineNumber": 1,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    #  Запрос на добавление в корзину расчета - моноблок (стандартный запрос, без спец. условий)
    order_simulate_add_to_cart_monoblock = {
        "debtorAccount": "0014403847",
        "materials": [
            {
                "materialCode": "w102207033",
                "quantity": 15,
                "lineNumber": 0,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    #  Запрос на добавление в корзину насоса (стандартный запрос, без спец. условий)
    order_simulate_add_to_cart_pumps = {
        "debtorAccount": "0014403847",
        "materials": [
            {
                "materialCode": "Q1512230012-1",
                "quantity": 25,
                "lineNumber": 0,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    #  Запрос на добавление в корзину БОМов (стандартный запрос, без спец. условий)
    order_simulate_add_to_cart_bom = {
        "debtorAccount": "0014403847",
        "materials": [
            {
                "materialCode": "065B2931R",
                "quantity": 7,
                "lineNumber": 0,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    #  Запрос на добавление в корзину ША БАСТ (стандартный запрос, без спец. условий)
    order_simulate_add_to_cart_bast = {
        "debtorAccount": "0014403847",
        "materials": [
            {
                "materialCode": "BQ1512230012-1",
                "quantity": 11,
                "lineNumber": 0,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    #  Запрос на добавление в корзину ЗИП (стандартный запрос, без спец. условий)
    order_simulate_add_to_cart_zip = {
        "debtorAccount": "0014403847",
        "materials": [
            {
                "materialCode": "089U1029",
                "quantity": 101,
                "lineNumber": 0,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    #  Запрос на добавление в корзину TDU (стандартный запрос, без спец. условий)
    order_simulate_add_to_cart_tdu = {
        "debtorAccount": "0014403847",
        "materials": [
            {
                "materialCode": "TDU1009575",
                "quantity": 10,
                "lineNumber": 0,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    # Запрос на добавление в корзину кода со спец. ценой
    order_simulate_add_to_cart_special_price = {
        "debtorAccount": "0014403847",
        "materials": [
            {
                "materialCode": "082G5402",
                "quantity": 111,
                "lineNumber": 1,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    # Запрос на добавление в корзину кода с прайсом в уе
    order_simulate_add_to_cart_code_with_price_cu = {
        "debtorAccount": "0014403847",
        "materials": [
            {
                "materialCode": "ZZZTEST1YE",
                "quantity": 1,
                "lineNumber": 1,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": "YRU",
        "returnAutoPrice": false
    }

    # Запрос на переключение кода в корзине с рублей на уе
    order_simulate_request_switching_code_in_basket_from_rubles_to_cu = {
        "debtorAccount": "0014403847",
        "materials": [
            {
                "materialCode": "003L0144R",
                "quantity": 1,
                "lineNumber": 0,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "CU",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    # Запрос на переключение кода в корзине с уе на рубли
    order_simulate_request_switching_code_in_basket_from_cu_to_rubles = {
        "debtorAccount": "0014403847",
        "materials": [
            {
                "materialCode": "003L0144R",
                "quantity": 10,
                "lineNumber": 0,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    # Запрос на добавление в корзину заблокированного кода
    order_simulate_request_add_blocked_code_to_cart = {
        "debtorAccount": "0014403847",
        "materials": [
            {
                "materialCode": "004B1201",
                "quantity": 99,
                "lineNumber": 1,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    # Запрос на добавление в корзину несуществующего кода
    order_simulate_request_add_non_existent_code_to_cart = {
        "debtorAccount": "0014403847",
        "materials": [
            {
                "materialCode": "87813",
                "quantity": 1,
                "lineNumber": 0,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }

    # Запрос на добавление в корзину символов
    order_simulate_bad_request_add_to_cart_symbols = {
        "debtorAccount": "0014403847",
        "materials": [
            {
                "materialCode": "!@#$%%",
                "quantity": 1,
                "lineNumber": 0,
                "odid": null
            }
        ],
        "paymentTerms": "RU00",
        "personId": "920bb836-8ee4-4571-b5bd-94bd28c29d32",
        "offerId": null,
        "returnEndClientDiscount": false,
        "currency": "RUB",
        "currencyDate": null,
        "exchangeRateType": null,
        "returnAutoPrice": false
    }
