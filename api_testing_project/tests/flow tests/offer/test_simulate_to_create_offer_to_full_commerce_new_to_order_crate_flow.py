import pytest
import allure

# 1) Order/Simulate
from api_testing_project.services.order.api.api_order_simulate import ApiOrderSimulate
from api_testing_project.services.order.payloads.payloads_order_simulate import PayloadsOrderSimulate

# 2) CrmCommerce/CreateOffer
from api_testing_project.services.crm_commerce.create_offer.api.api_create_offer import ApiCreateOffer
from api_testing_project.services.crm_commerce.create_offer.payloads.payloads_create_offer import PayloadsCreateOffer

# 3) FullCommerceNew (детали КП)
from api_testing_project.services.crm_commerce.full_commerce_new.api.api_full_commerce_new import FullCommerceNewApi

# 4) Order/Create
from api_testing_project.services.order.api.api_order_create import ApiOrderCreate
from api_testing_project.services.order.payloads.payloads_order_create import PayloadsOrderCreateWithOneCode


def _order_lines_from_simulate(sim_obj):
    line = sim_obj["orderLines"][0]
    qty = line.get("orderedQuantity") or line.get("quantity") or 1

    item = {
        "materialCode": line.get("materialCode"),
        "quantity": qty,
        "lineNumber": line.get("lineNumber") or 1,
        "lineType": "Material",
        "odid": line.get("odid"),  # даже если None, протаскиваем явно
    }

    schedules = line.get("schedules") or []
    if schedules and schedules[0].get("deliveryDate"):
        item["deliveryDate"] = schedules[0]["deliveryDate"]

    return [item]




@allure.feature("Offer E2E")
@allure.story("Simulate → CreateOffer → FullCommerceNew → Order/Create")
class TestSimulateOfferFullOrderE2E:
    def setup_method(self):
        self.simulate_api = ApiOrderSimulate()
        self.create_offer_api = ApiCreateOffer()
        self.full_api = FullCommerceNewApi()
        self.order_create_api = ApiOrderCreate()

    def test_full_chain_ok(self):
        # Шаг 1 — Simulate
        with allure.step("POST /api/Order/Simulate"):
            sim_payload = PayloadsOrderSimulate.order_simulate_add_to_cart_material
            sim_resp = self.simulate_api.post_order_simulate(sim_payload)
            print(sim_resp)

            assert sim_resp["status"] == "Ok", f"Simulate status != Ok: {sim_resp}"
            assert sim_resp["objects"], "Simulate: пустой objects"
            assert sim_resp["objects"][0].get("orderLines"), "Simulate: нет orderLines"
            order_lines = _order_lines_from_simulate(sim_resp["objects"][0])

        # Шаг 2 — CreateOffer
        with allure.step("POST /api/CrmCommerce/CreateOffer"):
            offer_payload = dict(PayloadsCreateOffer.base_valid_offer)  # твой новый шаблон
            offer_payload["orderLines"] = order_lines
            offer_payload.setdefault("paymentTerms", "RU00")  # чтобы не ловить status:3

            offer_resp = self.create_offer_api.post_create_offer(offer_payload)

            assert offer_resp["status"] == "Ok", f"CreateOffer status != Ok: {offer_resp}"
            assert offer_resp.get("objects"), "CreateOffer: пустой objects"

            # В моделях create_offer есть objects[0].offers[0].id/number — берём оттуда
            offers = offer_resp["objects"][0].get("offers") or []
            assert offers, f"CreateOffer: нет offers в ответе: {offer_resp}"
            offer_id = offers[0]["id"]
            offer_number = offers[0].get("number")

        # Шаг 3 — FullCommerceNew (детали КП)
        with allure.step("GET /api/CrmCommerce/FullCommerceNew"):
            full_resp = self.full_api.get_full_commerce_new_by_request_id(offer_id)

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

        # Шаг 4 — Order/Create
        with allure.step("POST /api/Order/Create"):
            # Берём готовый шаблон из проекта и ровно две вещи подменяем: orderLines и offerId.
            order_payload = dict(PayloadsOrderCreateWithOneCode.request_create_order_with_one_code_materials_prepayment_pickup)
            order_payload["orderLines"] = order_lines
            order_payload["offerId"] = offer_id
            order_payload.setdefault("paymentTerms", "RU00")

            order_resp = self.order_create_api.post_order_create(order_payload)
            print(order_resp)

            assert order_resp["status"] == "Ok", f"Order/Create status != Ok: {order_resp}"
            assert order_resp.get("objects"), "Order/Create: пустой objects"
