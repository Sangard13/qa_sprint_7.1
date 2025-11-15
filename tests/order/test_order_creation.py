import pytest
import allure
from utils.helpers import Helpers


@allure.epic("Order API")
@allure.feature("Order Creation")
class TestOrderCreation:

    @allure.title("Successful order creation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.order
    def test_create_order_success(self, order_api, order_data):
        """Тест успешного создания заказа"""
        with allure.step("Create order with valid data"):
            response = order_api.create_order(order_data)

        with allure.step("Check order creation response"):
            Helpers.check_response_status(response, 201)
            response_data = Helpers.extract_json(response)
            assert "track" in response_data
            assert isinstance(response_data["track"], int)

    @allure.title("Create order with different colors")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.order
    def test_create_order_with_different_colors(self, order_api, order_data):
        """Тест создания заказа с разными цветами"""
        with allure.step("Test order creation with various color combinations"):
            color_combinations = [
                ["BLACK"],
                ["GREY"],
                ["BLACK", "GREY"],
                []
            ]

            for colors in color_combinations:
                with allure.step(f"Create order with colors: {colors}"):
                    order_data["color"] = colors
                    response = order_api.create_order(order_data)

                with allure.step(f"Check order creation with colors {colors}"):
                    Helpers.check_response_status(response, 201)
                    response_data = Helpers.extract_json(response)
                    assert "track" in response_data

    @allure.title("Get order by track number")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.order
    def test_get_order_by_track(self, create_order, order_api):
        """Тест получения заказа по трекингу"""
        with allure.step("Get created order data"):
            order_data, track_number, create_response = create_order

        with allure.step(f"Get order by track number: {track_number}"):
            response = order_api.get_order_by_track(track_number)
            Helpers.check_response_status(response, 200)

        with allure.step("Verify order data"):
            response_data = Helpers.extract_json(response)
            assert "order" in response_data

            order_info = response_data["order"]
            assert order_info["firstName"] == order_data["firstName"]
            assert order_info["lastName"] == order_data["lastName"]
            assert order_info["address"] == order_data["address"]

    @allure.title("Get order with non-existent track")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.order
    def test_get_order_with_nonexistent_track(self, order_api):
        """Тест получения заказа по несуществующему треку"""
        with allure.step("Try to get order with non-existent track"):
            response = order_api.get_order_by_track(999999)

        with allure.step("Check error response"):
            Helpers.check_response_status(response, 404)
            response_data = Helpers.extract_json(response)
            assert "code" in response_data
            assert response_data["code"] == 404
            assert "message" in response_data