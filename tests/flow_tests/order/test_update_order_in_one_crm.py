import allure
import pytest
from datetime import datetime, timedelta
import json
from api_testing_project.services.order.api.api_update_order_in_one_crm import ApiUpdateOrderInOneCrm
from api_testing_project.services.order.models.update_order_in_one_crm_model import UpdateOrderInOneCrmModel


@pytest.mark.stage
@pytest.mark.dapi
@allure.feature("DAPI")
@allure.story("UpdateOrderInOneCrm - с готовым заказом")
class TestUpdateOrderInOneCrmSimple:

    def setup_method(self):
        self.update_order_api = ApiUpdateOrderInOneCrm()

    @allure.title('Простой тест UpdateOrderInOneCrm на существующем заказе')
    @pytest.mark.stage
    def test_update_existing_order(self):
        print("\n" + "=" * 80)
        print("ИСХОДНЫЕ ДАННЫЕ ЗАКАЗА RT25-070765")
        print("=" * 80)

        original_date = "30.12.2025 11:51:16"
        original_comment = "test_order_create"
        original_addl_info = "test_order_create"

        print(f"Дата документа: {original_date}")
        print(f"Комментарий клиента: {original_comment}")
        print(f"Дополнительная информация: {original_addl_info}")

        new_date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        new_ref_date = datetime.now().strftime("%d.%m.%Y")
        new_payment_date = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")
        new_comment = f"test_order_create - ОБНОВЛЕНО {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        new_addl_info = f"Тест обновления заказа - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        print("\n" + "=" * 80)
        print("НОВЫЕ ЗНАЧЕНИЯ (что будем менять)")
        print("=" * 80)
        print(f"Дата документа: {original_date} → {new_date}")
        print(f"Дата референса: → {new_ref_date}")
        print(f"Дата оплаты: → {new_payment_date} (текущая дата + 1 день)")
        print(f"Комментарий клиента:")
        print(f"  было: '{original_comment}'")
        print(f"  стало: '{new_comment}'")
        print(f"Дополнительная информация:")
        print(f"  было: '{original_addl_info}'")
        print(f"  стало: '{new_addl_info}'")
        print("=" * 80)

        update_payload = {
            "Completed": "1",
            "Deleted": "0",
            "Date": new_date,
            "DocumentNumber": "RT25-070765",
            "QuotationNumber": "PQ04813171-1",
            "HeadOffice": "ФИРМА ВОДОКОМФОРТ (7705238125)",
            "PartnerSAPID": "",
            "PartnerINN": "7705238125",
            "PartnerNamе": "ФИРМА ВОДОКОМФОРТ (7705238125)",
            "Organization_old": "ООО \"Ридан Трейд\"",
            "Currency": "руб.",
            "TotalAmount": 1640.54,
            "Warehouse": "0010 Склад Лешково ",
            "ContractNumber": "RT25-7705238125-HE",
            "PaymentTermsCode": "RU00",
            "TaxIncluded": "0",
            "ResponsibleEngineer": "Семенов Даниил Александрович",
            "AddlInfo": new_addl_info,
            "CompleteDelivery": False,
            "Status": "К выполнению / В резерве",
            "CurrentStatus": "Ожидается оплата до обеспечения",
            "PaymentPercent": 0,
            "PrepayAmountToCollect": 1640.54,
            "PrepayAmountToDelivery": 0,
            "DeliveryDate": "",
            "DaliveryDate": "",
            "DeliveryAddress": "Нет данных",
            "TaxType": "Продажа облагается НДС",
            "DelayedDeliveryDiscountValue": 0,
            "DeliveryCost": 0,
            "DiscountsCalculated": "1",
            "EngineerComment": "Заказ создан 2025-12-30T11:51:16.124251+03:00 Тест НЕ_РАЗМЕЩАТЬ_НИЧЕГО (k.tertyshnyi@vodokomfort.ru)  +7 (906) 034-13-83\ntest_order_create",
            "ClientCommen": new_comment,
            "ReferenceNumber": "Z0000052452",
            "ReferenceDate": new_ref_date,
            "ConsigneeSAPID": "",
            "Consignee": "",
            "ConsigneeName": "",
            "SalesDepartmentName": "4101 Отдел продаж тепловой автоматики Москва",
            "SalesDepartmentCode": "4101",
            "Author": "http_robot",
            "DeliveryType": "Силами перевозчика",
            "DeliveryPartner": "Самовывоз",
            "DeliveryAddressValue": "",
            "DeliveryAddlInfo": "Доставка до двери.",
            "ContactPerson": "Арсланов ",
            "SalesGroup": "",
            "PaidInCurrency": "0",
            "Organization": {
                "ContractorId": "00000000-0000-0000-0000-000000000000",
                "INN": "5017132318",
                "ContractorName": "ООО \"Ридан Трейд\""
            },
            "Materials": [
                {
                    "LineNo": 1,
                    "DeliveryDate": "",
                    "ODID": "55ebb53b-83fd-44b0-934a-e6768d1c832f",
                    "MaterialNumber": "003L0144R",
                    "MaterialName": "LV Ду 15 Клапан запорный прям. никелир.",
                    "PackType": "шт",
                    "PacksAmount": 2,
                    "AmountInWareUnits": 2,
                    "PriceCondition": "",
                    "Price": 683.56,
                    "Amount": 1367.12,
                    "Tax": "20%",
                    "TaxAmount": 273.42,
                    "AmountWithTax": 1640.54,
                    "DiscountPercent": 0,
                    "DiscountAmount": 0,
                    "AutoDiscountPercent": 0,
                    "AutoDiscountAmount": 0,
                    "CancelReason": "",
                    "Code": 1,
                    "Cancelled": "0",
                    "RelationshipKey": 0,
                    "Warehouse": "0010 Склад Лешково ",
                    "DeliveryDays": 0,
                    "Description": "",
                    "SupplyType": "Не обеспечивать",
                    "CollectionTypeNumber": "",
                    "CollectionTypeName": "",
                    "SalesDepartmentName": "",
                    "SalesDepartmentCode": "",
                    "Stock": 7161,
                    "Reservation": 1816,
                    "OnStock": 8977,
                    "Transit": [
                        {
                            "Quantity": 2,
                            "Date": None,
                            "Status": "Не обеспечивать",
                            "TransitComment": ""
                        }
                    ]
                }
            ],
            "StagesSchedulePayment": [
                {
                    "LineNo": 1,
                    "PaymentType": "Оплата до обеспечения",
                    "Date": new_payment_date,
                    "PaymentPercent": 100,
                    "Amount": 1640.54,
                    "PaymentMove": 1,
                    "PaymentMoveType": "от даты заказа"
                }
            ],
            "CompleteDeliveryFrom": None,
            "PaidStorage": []
        }

        print("\n=== ПОЛНЫЙ PAYLOAD ===")
        print(json.dumps(update_payload, indent=2, ensure_ascii=False, default=str))
        print("=" * 80)

        update_response = self.update_order_api.post_update_order_in_one_crm(update_payload)

        print(f"\nUpdateOrderInOneCrm response:")
        print(json.dumps(update_response, indent=2, ensure_ascii=False, default=str))

        result = UpdateOrderInOneCrmModel(**update_response)

        assert result.status.value == 'Ok', f"UpdateOrderInOneCrm failed: {result.messages}"
        assert result.objects, "UpdateOrderInOneCrm: нет objects в ответе"

        updated_order = result.objects[0]

        print("\n" + "=" * 80)
        print("✓ ТЕСТ УСПЕШНО ВЫПОЛНЕН!")
        print("=" * 80)
        print(f"Заказ обновлён: {updated_order.order_number}")
        print(f"Offer ID: {updated_order.offer_id}")
        print(f"Offer Number: {updated_order.offer_number}")
        print("\n" + "=" * 80)
        print("ИТОГОВЫЕ ИЗМЕНЕНИЯ:")
        print("=" * 80)
        print(f"✓ Дата документа обновлена: {new_date}")
        print(f"✓ Дата референса обновлена: {new_ref_date}")
        print(f"✓ Дата оплаты обновлена: {new_payment_date} (завтра)")
        print(f"✓ Комментарий клиента обновлен")
        print(f"✓ Дополнительная информация обновлена")
        print("=" * 80)