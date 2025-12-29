import allure
import pytest
from datetime import datetime, timedelta

from api_testing_project.services.order.api.api_order_simulate import ApiOrderSimulate
from api_testing_project.services.order.payloads.payloads_order_simulate import PayloadsOrderSimulate
from api_testing_project.services.crm_commerce.create_offer.api.api_create_offer import ApiCreateOffer
from api_testing_project.services.crm_commerce.create_offer.payloads.payloads_create_offer import PayloadsCreateOffer
from api_testing_project.services.crm_commerce.full_commerce_new.api.api_full_commerce_new import FullCommerceNewApi
from api_testing_project.services.order.api.api_order_create import ApiOrderCreate
from api_testing_project.services.order.payloads.payloads_order_create import PayloadsOrderCreateWithOneCode
from api_testing_project.services.order.api.api_update_order_in_one_crm import ApiUpdateOrderInOneCrm
from api_testing_project.services.order.payloads.payloads_update_order_in_one_crm import PayloadsUpdateOrderInOneCrm
from api_testing_project.services.order.models.update_order_in_one_crm_model import UpdateOrderInOneCrmModel
from api_testing_project.utils.offer_flow_helper import OfferFlowHelper


@pytest.mark.stage
@pytest.mark.dapi
@allure.feature("DAPI")
@allure.story("Simulate -> CreateOffer -> Order/Create -> UpdateOrderInOneCrm")
class TestUpdateOrderInOneCrmFlow:
    """Тест на полный флоу с обновлением заказа в OneCrm"""

    def setup_method(self):
        """Инициализация API классов перед каждым тестом"""
        self.simulate_api = ApiOrderSimulate()
        self.create_offer_api = ApiCreateOffer()
        self.full_api = FullCommerceNewApi()
        self.order_create_api = ApiOrderCreate()
        self.update_order_api = ApiUpdateOrderInOneCrm()

    @allure.title('Тест флоу: Simulate -> CreateOffer -> Order/Create -> UpdateOrderInOneCrm')
    @pytest.mark.stage
    def test_update_order_in_one_crm_flow(self):
        """
        Полный цикл теста с обновлением заказа в OneCRM:
        1. Simulate - получаем информацию о материале
        2. CreateOffer - создаем КП (isDraft=True)
        3. FullCommerceNew - получаем данные КП с ODID
        4. Order/Create - создаем заказ
        5. UpdateOrderInOneCrm - обновляем заказ в OneCRM
        """

        # ===== ШАГ 1: Simulate =====
        with allure.step("Шаг 1: POST /api/Order/Simulate"):
            print("\n" + "=" * 80)
            print("ШАГ 1: SIMULATE - Получаем данные о материале")
            print("=" * 80)

            # Создаём копию payload и меняем количество на 2 шт
            simulate_payload = dict(PayloadsOrderSimulate.order_simulate_add_to_cart_material)
            simulate_payload['materials'][0]['quantity'] = 2  # Меняем с 25 на 2

            simulate_response = self.simulate_api.post_order_simulate(simulate_payload)

            print(f"Simulate response status: {simulate_response.get('status')}")

            # Проверяем успешность
            assert simulate_response.get('status') == 'Ok', \
                f"Simulate failed: {simulate_response.get('messages')}"

            # Получаем данные материала - ПРАВИЛЬНО через метод API
            order_lines = self.simulate_api.get_list_order_lines()
            assert order_lines, "Simulate: нет orderLines"

            # ИСПРАВЛЕНО: используем правильные атрибуты модели OrderLine
            material_code = order_lines[0].material_code
            original_quantity = order_lines[0].ordered_quantity
            line_type = order_lines[0].line_type

            print(f"Материал: {material_code}")
            print(f"Количество: {original_quantity}")
            print(f"Тип линии: {line_type}")

        # ===== ШАГ 2: CreateOffer =====
        with allure.step("Шаг 2: POST /api/CrmCommerce/CreateOffer"):
            print("\n" + "=" * 80)
            print("ШАГ 2: CREATE OFFER - Создаём КП (не черновик)")
            print("=" * 80)

            # Готовим payload для CreateOffer - ИСПРАВЛЕНО: правильный payload
            create_offer_payload = dict(PayloadsCreateOffer.base_valid_offer)
            create_offer_payload['isDraft'] = False  # НЕ черновик, чтобы получить ODID
            create_offer_payload['orderLines'] = [
                {
                    'materialCode': material_code,
                    'quantity': original_quantity,
                    'lineNumber': 1,
                    'lineType': line_type
                }
            ]

            print("CreateOffer payload:")
            print(create_offer_payload)

            create_offer_response = self.create_offer_api.post_create_offer(create_offer_payload)

            print(f"CreateOffer response status: {create_offer_response.get('status')}")

            # Проверяем успешность
            assert create_offer_response.get('status') == 'Ok', \
                f"CreateOffer failed: {create_offer_response.get('messages')}"

            # ИСПРАВЛЕНО: правильное извлечение offer_id через хелпер
            offer_id = OfferFlowHelper.extract_offer_id(create_offer_response)
            offer_number = OfferFlowHelper.extract_offer_number(create_offer_response)

            print(f"Создан оффер: ID={offer_id}, Number={offer_number}")

        # ===== ШАГ 3: FullCommerceNew =====
        with allure.step("Шаг 3: GET /api/CrmCommerce/FullCommerceNew"):
            print("\n" + "=" * 80)
            print("ШАГ 3: FULL COMMERCE NEW - Получаем полные данные КП")
            print("=" * 80)

            full_response = self.full_api.get_full_commerce_new_by_request_id(offer_id)

            print(f"FullCommerceNew response status: {full_response.get('status')}")

            # Проверяем успешность
            assert full_response.get('status') == 'Ok', \
                f"FullCommerceNew failed: {full_response.get('messages')}"

            # Извлекаем details для получения ODID - через хелпер
            details = OfferFlowHelper.extract_details_from_full_commerce(full_response)

            assert details, "FullCommerceNew: нет details"

            # ВАЖНО: ODID находится в поле "id", а не "odid"!
            odid = details[0].get('id')
            material_code_from_full = details[0].get('materialCode') or details[0].get('code')

            print(f"\nПолучен ODID (из поля 'id'): {odid}")
            print(f"Material code: {material_code_from_full}")

        # ===== ШАГ 4: Order/Create =====
        with allure.step("Шаг 4: POST /api/Order/Create"):
            print("\n" + "=" * 80)
            print("ШАГ 4: ORDER CREATE - Создаём заказ")
            print("=" * 80)

            # Готовим payload для Order/Create
            order_create_payload = dict(
                PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_materials_prepayment_pickup
            )

            # Обновляем orderLines с правильными данными
            # ВАЖНО: Если odid=None, передаём None (null), а не строку "None"
            order_create_payload['orderLines'] = [
                {
                    'materialCode': material_code,
                    'quantity': original_quantity,
                    'lineNumber': 1,
                    'discountPercent': None,
                    'endClientDiscountPercent': None,
                    'odid': str(odid) if odid else None,  # Передаём None если odid пустой
                    'deliveryDate': order_create_payload['orderLines'][0]['deliveryDate'],
                    'lineType': line_type,
                    'requestedMaterialCode': None,
                    'excludePosition': False
                }
            ]

            order_create_payload['offerId'] = str(offer_id)
            order_create_payload['userComment'] = 'ТЕСТ флоу UpdateOrderInOneCrm'

            print("Order/Create payload:")
            print(order_create_payload)

            order_create_response = self.order_create_api.post_order_create(order_create_payload)

            print(f"Order/Create response status: {order_create_response.get('status')}")
            print("Order/Create response:")
            print(order_create_response)

            # Проверяем успешность
            assert order_create_response.get('status') == 'Ok', \
                f"Order/Create failed: {order_create_response.get('messages')}"

            # ИСПРАВЛЕНО: правильное извлечение данных заказа
            order_objects = order_create_response.get('objects', [])
            assert order_objects, "Order/Create: нет objects"

            # Получаем данные из первого объекта
            first_object = order_objects[0]
            doc_number = first_object.get('docNumber')  # Номер документа (PQ...)

            # Получаем orders из первого объекта
            orders = first_object.get('orders', [])
            assert orders, "Order/Create: нет orders"

            order_number = orders[0].get('orderNumber')  # Может быть None для Quotation
            created_offer_id = orders[0].get('offerId')
            created_offer_number = orders[0].get('offerNumber')

            print(f"Создан заказ:")
            print(f"  DocNumber: {doc_number}")
            print(f"  OrderNumber: {order_number}")
            print(f"  OfferID: {created_offer_id}")
            print(f"  OfferNumber: {created_offer_number}")

            # Для UpdateOrderInOneCrm используем docNumber (это номер КП)
            document_number_for_update = doc_number

        # ===== ШАГ 5: UpdateOrderInOneCrm =====
        with allure.step("Шаг 5: POST /api/Offer/UpdateOrderInOneCrm"):
            print("\n" + "=" * 80)
            print("ШАГ 5: UPDATE ORDER IN ONE CRM - Обновляем заказ в OneCRM")
            print("=" * 80)

            """
            ИСТОЧНИКИ ДАННЫХ ДЛЯ PAYLOAD UpdateOrderInOneCrm:

            Из Simulate (order_lines):
               - material_code, original_quantity, line_type

            Из CreateOffer request (create_offer_payload):
               - Используется минимально, т.к. берём из Order/Create

            Из FullCommerceNew (details):
               - organization: contractorId, inn, contractorName
               - material: text (name), salesPrice, total, vaTresult, totalVAT
               - discount, packageSize, warehouse, id (odid)

            Из Order/Create response:
               - documentNumber (docNumber)
               - offerNumber

            Из Order/Create request (order_create_payload):
               - currency, paymentTerms, referenceNumber
               - authorNumber (author), salesGroup
               - deliveryOptions: deliveryType, deliveryAddressValue
               - engineerComment, userComment (clientComment)

            Пустые строки (нет данных):
               - completed, deleted, status, taxType, taxIncluded
               - headOffice, partnerSAPID, partnerINN, partnerNamе
               - и другие необязательные поля...
            """

            # Готовим payload для UpdateOrderInOneCrm
            update_payload = dict(PayloadsUpdateOrderInOneCrm.update_order_basic)

            # ===== СОБИРАЕМ ДАННЫЕ ИЗ ВСЕХ ПРЕДЫДУЩИХ ШАГОВ =====

            # --- Данные из FullCommerceNew (details) ---
            material_data = details[0]
            org_data = material_data.get('organization', {})

            # --- Данные из Order/Create response ---
            # documentNumber, offerNumber уже есть

            # --- Данные из Create/Order request (order_create_payload) ---
            delivery_opts = order_create_payload.get('deliveryOptions', {})

            # ===== ЗАПОЛНЯЕМ ОСНОВНЫЕ ПОЛЯ =====

            # Основные данные заказа
            update_payload['documentNumber'] = document_number_for_update
            update_payload['quotationNumber'] = offer_number
            # Формат даты как в реальном API: "29.12.2025 13:29:39"
            update_payload['date'] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            # Currency в формате как в реальном API: "руб." вместо "RUB"
            currency_map = {'RUB': 'руб.', 'EUR': 'евро', 'USD': 'долл.'}
            original_currency = order_create_payload.get('currency', 'RUB')
            update_payload['currency'] = currency_map.get(original_currency, 'руб.')
            update_payload['paymentTermsCode'] = order_create_payload.get('paymentTerms', 'RU00')
            update_payload['referenceNumber'] = order_create_payload.get('referenceNumber', '')
            update_payload['author'] = order_create_payload.get('authorNumber', '')
            update_payload['salesGroup'] = order_create_payload.get('salesGroup', '')

            # Данные организации из FullCommerceNew
            update_payload['organization']['contractorId'] = org_data.get('contractorId', '')
            update_payload['organization']['inn'] = org_data.get('inn', '')
            update_payload['organization']['contractorName'] = org_data.get('contractorName', '')

            # Approvers согласно спецификации API (хотя в реальном примере их нет)
            # Оставляем с пустыми строками для email/phone/name
            if 'approvers' not in update_payload['organization']:
                update_payload['organization']['approvers'] = []

            # Данные доставки из Order/Create request
            update_payload['deliveryType'] = delivery_opts.get('deliveryType', 'Pickup')
            update_payload['deliveryAddress'] = delivery_opts.get('deliveryAddressValue', '')
            update_payload['deliveryAddlInfo'] = delivery_opts.get('comment', '')
            update_payload['deliveryCost'] = delivery_opts.get('deliveryCost', 0)

            # Комментарии
            update_payload['engineerComment'] = order_create_payload.get('engineerComment', '')
            update_payload['clientComment'] = order_create_payload.get('userComment', '')

            # Warehouse из FullCommerceNew (ОБЯЗАТЕЛЬНОЕ ПОЛЕ!)
            # Может быть None или пустым, поэтому используем дефолт
            warehouse_value = material_data.get('warehouse')
            print(f"\nDEBUG Warehouse из FullCommerceNew: '{warehouse_value}'")
            if not warehouse_value:  # None, '', или False
                warehouse_value = "0010"  # Минимальный дефолт (код склада)
                print(f"   Warehouse был пустой, используем дефолт: '{warehouse_value}'")
            update_payload['warehouse'] = warehouse_value
            print(f"   Установлен warehouse: '{update_payload['warehouse']}'")

            # Общая сумма из FullCommerceNew
            update_payload['totalAmount'] = material_data.get('totalVAT', 0)

            # ===== ОБЯЗАТЕЛЬНЫЕ ПОЛЯ - ИСПОЛЬЗУЕМ ДЕФОЛТЫ ИЗ РЕАЛЬНОГО ПРИМЕРА =====
            update_payload['completed'] = "1"  # "1" = выполнен
            update_payload['deleted'] = "0"  # "0" = не удалён
            update_payload['contractNumber'] = ""
            update_payload['headOffice'] = ""
            update_payload['partnerSAPID'] = ""
            update_payload['partnerINN'] = ""
            update_payload['partnerNamе'] = ""  # Русская "е"
            update_payload['taxIncluded'] = "0"  # "0" = НДС не включён в цену
            update_payload['responsibleEngineer'] = ""
            update_payload['addlInfo'] = ""
            update_payload['completeDelivery'] = False
            update_payload['status'] = "К выполнению / В резерве"  # Дефолт из реального примера
            update_payload['deliveryDate'] = ""
            update_payload['taxType'] = "Продажа облагается НДС"  # Дефолт из реального примера
            update_payload['discountsCalculated'] = "1"  # "1" = скидки рассчитаны
            update_payload['consignee'] = ""
            update_payload['consigneeSAPID'] = ""
            update_payload['consigneeName'] = ""
            update_payload['salesDepartmentName'] = ""
            update_payload['salesDepartmentCode'] = ""
            update_payload['deliveryPartner'] = ""
            update_payload['deliveryAddressValue'] = ""
            update_payload['contactPerson'] = ""
            update_payload['paidInCurrency'] = "0"  # "0" = оплата не в валюте
            update_payload['currentStatus'] = "Готов к отгрузке"  # Дефолт из реального примера
            update_payload['governmentContract'] = ""  # Согласно спецификации API

            # Убираем лишние поля которых нет даже в спецификации
            # (пока все поля из спецификации оставляем)

            # ===== ДАННЫЕ МАТЕРИАЛОВ =====

            # Основные данные материала из FullCommerceNew
            update_payload['materials'][0]['materialNumber'] = material_code
            update_payload['materials'][0]['materialName'] = material_data.get('text', '')
            update_payload['materials'][0]['description'] = material_data.get('text', '')
            update_payload['materials'][0]['amountInWareUnits'] = original_quantity
            update_payload['materials'][0]['odid'] = str(odid)
            update_payload['materials'][0]['lineNo'] = 1

            # Ценовые данные из FullCommerceNew
            update_payload['materials'][0]['price'] = material_data.get('salesPrice', 0)
            update_payload['materials'][0]['amount'] = material_data.get('total', 0)
            update_payload['materials'][0]['taxAmount'] = material_data.get('vaTresult', 0)
            update_payload['materials'][0]['amountWithTax'] = material_data.get('totalVAT', 0)
            update_payload['materials'][0]['discountPercent'] = material_data.get('discount', 0)
            update_payload['materials'][0]['autoDiscountPercent'] = material_data.get('discount', 0)

            # КРИТИЧНЫЕ ПОЛЯ из реального примера API:
            update_payload['materials'][0]['packType'] = "шт"  # Тип упаковки
            update_payload['materials'][0]['packsAmount'] = original_quantity  # Количество упаковок = количеству
            update_payload['materials'][0]['priceCondition'] = ""  # Условие цены (обычно пустое)
            update_payload['materials'][0]['tax'] = "20%"  # Ставка НДС
            update_payload['materials'][0]['code'] = 1  # Код позиции
            update_payload['materials'][0]['relationshipKey'] = 0
            update_payload['materials'][0]['deliveryDays'] = 0

            # Складские остатки (опциональные, ставим 0)
            update_payload['materials'][0]['stock'] = 0
            update_payload['materials'][0]['reservation'] = 0
            update_payload['materials'][0]['onStock'] = 0

            # Количества из FullCommerceNew
            update_payload['materials'][0]['itemQuantityInCollection'] = material_data.get('packageSize', 0)
            update_payload['materials'][0]['collectionQuantity'] = 0

            # ===== ОБЯЗАТЕЛЬНЫЕ СТРОКОВЫЕ ПОЛЯ MATERIALS =====
            # DeliveryDate должна быть заполнена! (не пустая строка)
            delivery_date = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")
            update_payload['materials'][0]['deliveryDate'] = delivery_date

            update_payload['materials'][0]['cancelReason'] = ""
            update_payload['materials'][0]['cancelled'] = "0"  # "0" = не отменено
            update_payload['materials'][0]['supplyType'] = "Отгрузить"  # Дефолт
            update_payload['materials'][0]['collectionTypeNumber'] = ""
            update_payload['materials'][0]['collectionTypeName'] = ""
            update_payload['materials'][0]['warehouse'] = warehouse_value  # ОБЯЗАТЕЛЬНО!
            update_payload['materials'][0]['salesDepartmentName'] = ""  # Из реального примера
            update_payload['materials'][0]['salesDepartmentCode'] = ""  # Из реального примера

            # Удаляем invoiceNumber и invoiceDate если они есть
            if 'invoiceNumber' in update_payload['materials'][0]:
                del update_payload['materials'][0]['invoiceNumber']
            if 'invoiceDate' in update_payload['materials'][0]:
                del update_payload['materials'][0]['invoiceDate']

            # Transit массив с данными (из реального примера API)
            # ВАЖНО: дата в формате ISO YYYY-MM-DD
            delivery_date_iso = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            update_payload['materials'][0]['transit'] = [
                {
                    "documentNumber": None,
                    "documentDate": None,
                    "documentType": 0,
                    "quantity": original_quantity,
                    "date": delivery_date_iso,  # ISO формат: "2025-12-30"
                    "status": "Обеспечен на складе",
                    "transitComment": ""
                }
            ]

            # Остальные массивы пустые
            update_payload['stagesSchedulePayment'] = []
            update_payload['paidStorage'] = []
            update_payload['errors'] = []

            print("\n" + "=" * 80)
            print("=== UpdateOrderInOneCrm payload - РЕАЛЬНЫЕ ДАННЫЕ ИЗ МЕТОДОВ ===")
            print("=" * 80)
            print("\nИз Order/Create response:")
            print(f"  documentNumber: {update_payload['documentNumber']}")
            print(f"  quotationNumber: {update_payload['quotationNumber']}")

            print("\nИз FullCommerceNew (organization):")
            print(f"  contractorId: {update_payload['organization']['contractorId']}")
            print(f"  inn: {update_payload['organization']['inn']}")
            print(f"  contractorName: {update_payload['organization']['contractorName']}")

            print("\nИз Order/Create request:")
            print(f"  currency: {update_payload['currency']}")
            print(f"  paymentTermsCode: {update_payload['paymentTermsCode']}")
            print(f"  referenceNumber: {update_payload['referenceNumber']}")
            print(f"  author: {update_payload['author']}")
            print(f"  salesGroup: {update_payload['salesGroup']}")
            print(f"  deliveryType: {update_payload['deliveryType']}")
            print(f"  warehouse: {update_payload['warehouse']}")

            print("\nИз FullCommerceNew (материал):")
            print(f"  materialNumber: {update_payload['materials'][0]['materialNumber']}")
            print(f"  materialName: {update_payload['materials'][0]['materialName']}")
            print(f"  amountInWareUnits: {update_payload['materials'][0]['amountInWareUnits']}")
            print(f"  warehouse: {update_payload['materials'][0]['warehouse']}")
            print(f"  price: {update_payload['materials'][0]['price']}")
            print(f"  amount: {update_payload['materials'][0]['amount']}")
            print(f"  taxAmount: {update_payload['materials'][0]['taxAmount']}")
            print(f"  amountWithTax: {update_payload['materials'][0]['amountWithTax']}")
            print(f"  discountPercent: {update_payload['materials'][0]['discountPercent']}")
            print(f"  odid: {update_payload['materials'][0]['odid']}")

            print(f"\ntotalAmount: {update_payload['totalAmount']}")

            print("\nДефолтные значения из реального примера:")
            print(f"  completed: {update_payload['completed']}")
            print(f"  deleted: {update_payload['deleted']}")
            print(f"  status: {update_payload['status']}")
            print(f"  currentStatus: {update_payload['currentStatus']}")
            print(f"  taxType: {update_payload['taxType']}")
            print(f"  taxIncluded: {update_payload['taxIncluded']}")
            print(f"  discountsCalculated: {update_payload['discountsCalculated']}")
            print(f"  paidInCurrency: {update_payload['paidInCurrency']}")
            print(f"  materials[0].cancelled: {update_payload['materials'][0]['cancelled']}")
            print(f"  materials[0].supplyType: {update_payload['materials'][0]['supplyType']}")

            print("\nОстальные обязательные поля: пустые строки")
            print("=" * 80)

            # DEBUG: Полный payload для анализа
            import json
            print("\n=== ПОЛНЫЙ PAYLOAD (согласно спецификации API) ===")
            print(json.dumps(update_payload, indent=2, ensure_ascii=False, default=str))
            print("=" * 80 + "\n")

            print("\nОтправляем UpdateOrderInOneCrm...")
            update_response = self.update_order_api.post_update_order_in_one_crm(update_payload)

            print(f"UpdateOrderInOneCrm response:")
            print(update_response)

            # Проверяем успешность через Pydantic модель
            result = UpdateOrderInOneCrmModel(**update_response)

            print(f"UpdateOrderInOneCrm status: {result.status}")

            assert result.status.value == 'Ok', \
                f"UpdateOrderInOneCrm failed: {result.messages}"

            # Проверяем objects
            assert result.objects, "UpdateOrderInOneCrm: нет objects в ответе"

            updated_order = result.objects[0]
            print(f"Заказ обновлён:")
            print(f"  OrderNumber: {updated_order.order_number}")
            print(f"  OfferID: {updated_order.offer_id}")
            print(f"  OfferNumber: {updated_order.offer_number}")

            # Проверяем что ID совпадают
            assert str(updated_order.offer_id) == str(offer_id), \
                f"Offer ID не совпадает! Ожидали {offer_id}, получили {updated_order.offer_id}"

        print("\n" + "=" * 80)
        print("✓ ТЕСТ УСПЕШНО ВЫПОЛНЕН!")
        print("Весь флоу Simulate -> CreateOffer -> Order/Create -> UpdateOrderInOneCrm завершен")
        print("=" * 80)