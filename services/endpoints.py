from config import TestEnvironment


class Endpoints:
    """Сервисы (методы)"""

    """Получает информацию о клиенте - GetCustomer"""
    get_customer = \
        lambda self, debtor_account: f'{TestEnvironment.BASE_URL_DAPI}api/Customer/GetCustomer?debtorAccount={debtor_account}'
    get_customer_by_inn = lambda self, inn: f'{TestEnvironment.BASE_URL_DAPI}api/Customer/GetCustomerByInn?inn={inn}'
    get_customer_by_number = \
        lambda self, debtor_account: f'{TestEnvironment.BASE_URL_DAPI}api/Customer/GetCustomerByNumber?id={debtor_account}'

    """Рассчитать цены и проверить наличие для материалов - Order/Simulate"""
    post_order_simulate = f'{TestEnvironment.BASE_URL_DAPI}api/Order/Simulate'

    """Создание заказа или КП"""
    post_order_create = f"{TestEnvironment.BASE_URL_DAPI}api/Order/Create"

    """/api/Order/UpdateOffer"""
    post_order_update_offer = f"{TestEnvironment.BASE_URL_DAPI}api/Order/UpdateOffer"

    """Currency"""
    get_conventional_units = lambda self, exchange_rate_type: \
        f'{TestEnvironment.BASE_URL_DAPI}api/Currency/GetConventionalUnits?exchangeRateType={exchange_rate_type}'

    """FullCommerceNew"""
    get_full_commerce_new = \
        lambda self, request_id: f'{TestEnvironment.BASE_URL_DAPI}api/CrmCommerce/FullCommerceNew?requestId={request_id}'

    """/api/CrmCommerce/CreateOffer"""
    post_create_offer = f"{TestEnvironment.BASE_URL_DAPI}api/CrmCommerce/CreateOffer"

    """api/Material/UpdateMaterials"""
    post_update_materials = f'{TestEnvironment.BASE_URL_DAPI}api/Material/UpdateMaterials'

    """/api/Order/CreateDocumentRetry"""
    get_order_create_document_retry = f'{TestEnvironment.BASE_URL_DAPI}api/Order/CreateDocumentRetry'

    """/api/CrmRequest/RequestSave"""
    post_crm_request_request_save = f'{TestEnvironment.BASE_URL_DAPI}api/CrmRequest/RequestSave'
