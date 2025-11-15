import pytest
import allure
from utils.helpers import Helpers


@allure.epic("Order API")
@allure.feature("Order Operations")
class TestOrderOperations:

    @allure.title("Accept order")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.order
    def test_accept_order(self, create_and_delete_courier, create_order, order_api):
        with allure.step("Create courier and order"):
            courier_data, courier_id = create_and_delete_courier
            order_data, track_number, _ = create_order

        with allure.step("Get order ID by track"):
            track_response = order_api.get_order_by_track(track_number)
            Helpers.check_response_status(track_response, 200)
            order_id = track_response.json()["order"]["id"]

        with allure.step("Accept order"):
            response = order_api.accept_order(order_id, courier_id)
            Helpers.check_response_status(response, 200)
            response_data = Helpers.extract_json(response)
            assert response_data.get("ok") == True

    @allure.title("Finish order")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.order
    def test_finish_order(self, create_and_delete_courier, create_order, order_api):
        with allure.step("Create courier and order"):
            courier_data, courier_id = create_and_delete_courier
            order_data, track_number, _ = create_order

        with allure.step("Get order ID by track"):
            track_response = order_api.get_order_by_track(track_number)
            Helpers.check_response_status(track_response, 200)
            order_id = track_response.json()["order"]["id"]

        with allure.step("Accept order first"):
            accept_response = order_api.accept_order(order_id, courier_id)
            Helpers.check_response_status(accept_response, 200)

        with allure.step("Finish order"):
            response = order_api.finish_order(order_id)
            Helpers.check_response_status(response, 200)
            response_data = Helpers.extract_json(response)
            assert response_data.get("ok") == True

    @allure.title("Try to cancel order")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.order
    def test_try_cancel_order(self, create_order, order_api):
        with allure.step("Create order"):
            order_data, track_number, _ = create_order

        with allure.step("Try to cancel order"):
            response = order_api.cancel_order(track_number)
            # API возвращает 400 при попытке отмены
            Helpers.check_response_status(response, 400)
            response_data = Helpers.extract_json(response)
            assert "code" in response_data
            assert response_data["code"] == 400

    @allure.title("Accept non-existent order")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.order
    def test_accept_nonexistent_order(self, create_and_delete_courier, order_api):
        with allure.step("Create courier"):
            courier_data, courier_id = create_and_delete_courier

        with allure.step("Try to accept non-existent order"):
            response = order_api.accept_order(999999, courier_id)

        with allure.step("Check error response"):
            Helpers.check_response_status(response, 404)
            response_data = Helpers.extract_json(response)
            assert "code" in response_data
            assert response_data["code"] == 404
            assert "message" in response_data

    @allure.title("Accept order without courier ID")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.order
    def test_accept_order_without_courier_id(self, create_order, order_api):
        with allure.step("Create order"):
            order_data, track_number, _ = create_order

        with allure.step("Get order ID by track"):
            track_response = order_api.get_order_by_track(track_number)
            Helpers.check_response_status(track_response, 200)
            order_id = track_response.json()["order"]["id"]

        with allure.step("Try to accept order without courier ID"):
            response = order_api.accept_order(order_id, "")

        with allure.step("Check error response"):
            Helpers.check_response_status(response, 400)
            response_data = Helpers.extract_json(response)
            assert "code" in response_data
            assert response_data["code"] == 400

    @allure.title("Finish non-existent order")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.order
    def test_finish_nonexistent_order(self, order_api):
        with allure.step("Try to finish non-existent order"):
            response = order_api.finish_order(999999)

        with allure.step("Check error response"):
            Helpers.check_response_status(response, 404)
            response_data = Helpers.extract_json(response)
            assert "code" in response_data
            assert response_data["code"] == 404

    @allure.title("Cancel non-existent order")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.order
    def test_cancel_nonexistent_order(self, order_api):
        with allure.step("Try to cancel non-existent order"):
            response = order_api.cancel_order(999999)

        with allure.step("Check error response"):
            Helpers.check_response_status(response, 400)
            response_data = Helpers.extract_json(response)
            assert "code" in response_data
            assert response_data["code"] == 400