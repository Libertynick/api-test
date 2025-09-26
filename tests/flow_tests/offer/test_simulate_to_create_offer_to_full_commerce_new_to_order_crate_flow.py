import allure
import pytest

from api_testing_project.services.order.api.api_order_simulate import ApiOrderSimulate
from api_testing_project.services.order.payloads.payloads_order_simulate import PayloadsOrderSimulate
from api_testing_project.services.crm_commerce.create_offer.api.api_create_offer import ApiCreateOffer
from api_testing_project.services.crm_commerce.create_offer.payloads.payloads_create_offer import PayloadsCreateOffer
from api_testing_project.services.crm_commerce.full_commerce_new.api.api_full_commerce_new import FullCommerceNewApi
from api_testing_project.services.order.api.api_order_create import ApiOrderCreate
from api_testing_project.services.order.payloads.payloads_order_create import PayloadsOrderCreateWithOneCode


def _order_lines_from_simulate(sim_obj):
    """Создаем orderLines из ответа Simulate (без ODID)"""
    line = sim_obj["orderLines"][0]
    qty = line.get("orderedQuantity")

    item = {
        "materialCode": line.get("materialCode"),
        "quantity": qty,
        "lineNumber": line.get("lineNumber"),
        "lineType": "Material",
        "odid": line.get("odid"),  # пока None, обновим позже
    }

    schedules = line.get("schedules") or []
    if schedules and schedules[0].get("deliveryDate"):
        item["deliveryDate"] = schedules[0]["deliveryDate"]

    return [item]


def _update_order_lines_with_odid(order_lines, full_resp):
    """ Обновляем orderLines правильными ODID из ответа FullCommerceNew """
    # Извлекаем позиции из FullCommerceNew
    full_objects = full_resp.get("objects", [])
    if not full_objects:
        print("Нет objects в ответе FullCommerceNew")
        return order_lines

    #ODID находится в details, а не в data.orders!
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

        print(f"Detail: materialCode={material_code}, id={odid}")

        if material_code and odid:
            code_to_odid[material_code] = odid

    print(f"Маппинг code -> odid: {code_to_odid}")

    # Обновляем orderLines
    updated_lines = []
    for line in order_lines:
        updated_line = dict(line)  # копируем
        material_code = line.get("materialCode")

        if material_code in code_to_odid:
            updated_line["odid"] = code_to_odid[material_code]
            print(f"Обновили ODID для {material_code}: {code_to_odid[material_code]}")
        else:
            print(f"Не найден ODID для материала {material_code}")

        updated_lines.append(updated_line)

    return updated_lines


@pytest.mark.stage
@pytest.mark.dapi
@allure.feature("DAPI")
@allure.story("Simulate -> CreateOffer -> FullCommerceNew -> Order/Create")
class TestSimulateOfferFullOrderE2E:
    def setup_method(self):
        self.simulate_api = ApiOrderSimulate()
        self.create_offer_api = ApiCreateOffer()
        self.full_api = FullCommerceNewApi()
        self.order_create_api = ApiOrderCreate()

    @pytest.mark.stage
    def test_full_chain_ok(self):
        # Шаг 1 — Simulate
        with allure.step("POST /api/Order/Simulate"):
            sim_payload = PayloadsOrderSimulate.order_simulate_add_to_cart_material
            sim_resp = self.simulate_api.post_order_simulate(sim_payload)
            print("SIMULATE RESPONSE")
            print(sim_resp)

            assert sim_resp["status"] == "Ok", f"Simulate status != Ok: {sim_resp}"
            assert sim_resp["objects"], "Simulate: пустой objects"
            assert sim_resp["objects"][0].get("orderLines"), "Simulate: нет orderLines"
            order_lines = _order_lines_from_simulate(sim_resp["objects"][0])
            print(f"Order lines from Simulate: {order_lines}")

        # Шаг 2 — CreateOffer
        with allure.step("POST /api/CrmCommerce/CreateOffer"):
            offer_payload = dict(PayloadsCreateOffer.base_valid_offer)
            offer_payload["orderLines"] = order_lines
            offer_payload.setdefault("paymentTerms", "RU00")

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

        # Шаг 3 — FullCommerceNew (детали КП)
        with allure.step("GET /api/CrmCommerce/FullCommerceNew"):
            full_resp = self.full_api.get_full_commerce_new_by_request_id(offer_id)
            print()
            print()
            print("FULL COMMERCE NEW RESPONSE")
            print(full_resp, type(full_resp))
            print()
            print()

            assert full_resp["status"] == "Ok", f"FullCommerce status != Ok: {full_resp}"
            full_objects = full_resp.get("objects") or []
            assert full_objects, "FullCommerce: пустой objects"

            full_data = full_objects[0].get("data") or []
            assert full_data, "FullCommerce: пустой data"

            full_offer = full_data[0]
            assert (
                    full_offer.get("crmCommerceId") == offer_id
                    or (offer_number and full_offer.get("commerceNumber") == offer_number)
            ), f"В FullCommerceNew не нашли оффер id={offer_id}, number={offer_number}, full_offer={full_offer}"

            # Обновляем orderLines с правильными ODID
            order_lines = _update_order_lines_with_odid(order_lines, full_resp)
            print(f"Updated order lines with ODID: {order_lines}")

        # Шаг 4 — Order/Create
        with allure.step("POST /api/Order/Create"):
            order_payload = dict(
                PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_materials_prepayment_pickup)
            order_payload["orderLines"] = order_lines  # теперь с правильными ODID!
            order_payload["offerId"] = offer_id
            order_payload.setdefault("paymentTerms", "RU00")

            print("ORDER CREATE PAYLOAD")
            print(order_payload)

            order_resp = self.order_create_api.post_order_create(order_payload)
            print("ORDER CREATE RESPONSE")
            print(order_resp)

            assert order_resp["status"] == "Ok", f"Order/Create status != Ok: {order_resp}"
            assert order_resp.get("objects"), "Order/Create: пустой objects"

            print("Тест успешно выполнен!")