import pytest
import allure
from utils.helpers import Helpers


@allure.epic("Order API")
@allure.feature("Order List")
class TestOrderList:

    @allure.title("Get orders list with default parameters")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.order
    def test_get_orders_list_default(self, order_api):
        """Тест получения списка заказов с параметрами по умолчанию"""
        with allure.step("Get orders list with default parameters"):
            response = order_api.get_orders_list()

        with allure.step("Check response structure"):
            Helpers.check_response_status(response, 200)
            response_data = Helpers.extract_json(response)

            assert "orders" in response_data
            assert "pageInfo" in response_data
            assert "availableStations" in response_data

            page_info = response_data["pageInfo"]
            assert page_info["page"] == 0
            assert page_info["limit"] == 30

    @allure.title("Get orders list with courier ID")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.order
    def test_get_orders_list_with_courier_id(self, create_and_delete_courier, order_api):
        """Тест получения списка заказов с courierId"""
        with allure.step("Get test courier"):
            courier_data, courier_id = create_and_delete_courier

        with allure.step("Get orders list for courier"):
            response = order_api.get_orders_list(courier_id=courier_id)

        with allure.step("Check response"):
            Helpers.check_response_status(response, 200)
            response_data = Helpers.extract_json(response)
            assert "orders" in response_data

    @allure.title("Get orders list with limit")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.order
    def test_get_orders_list_with_limit(self, order_api):
        """Тест получения списка заказов с ограничением количества"""
        with allure.step("Get orders list with limit=5"):
            response = order_api.get_orders_list(limit=5)

        with allure.step("Check response with limit"):
            Helpers.check_response_status(response, 200)
            response_data = Helpers.extract_json(response)

            page_info = response_data["pageInfo"]
            assert page_info["limit"] == 5
            assert len(response_data["orders"]) <= 5

    @allure.title("Get orders list with pagination")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.order
    def test_get_orders_list_with_pagination(self, order_api):
        """Тест пагинации списка заказов"""
        with allure.step("Get first page of orders"):
            response_page_0 = order_api.get_orders_list(limit=5, page=0)
            Helpers.check_response_status(response_page_0, 200)

        with allure.step("Get second page of orders"):
            response_page_1 = order_api.get_orders_list(limit=5, page=1)
            Helpers.check_response_status(response_page_1, 200)

        with allure.step("Verify pages are different"):
            orders_page_0 = response_page_0.json()["orders"]
            orders_page_1 = response_page_1.json()["orders"]
            assert isinstance(orders_page_0, list)
            assert isinstance(orders_page_1, list)

            # Если на обеих страницах есть заказы, проверяем что они разные
            order_ids_page_0 = [order["id"] for order in orders_page_0]
            order_ids_page_1 = [order["id"] for order in orders_page_1]

            # Проверяем что нет пересечений ID между страницами
            common_ids = set(order_ids_page_0).intersection(order_ids_page_1)
            assert len(common_ids) == 0, f"Found common order IDs between pages: {common_ids}"

    @allure.title("Get orders list with non-existent courier")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.order
    def test_get_orders_list_nonexistent_courier(self, order_api):
        """Тест получения списка заказов с несуществующим courierId"""
        with allure.step("Try to get orders for non-existent courier"):
            response = order_api.get_orders_list(courier_id=999999)

        with allure.step("Check error response"):
            Helpers.check_response_status(response, 404)
            response_data = Helpers.extract_json(response)
            assert "message" in response_data
            assert "не найден" in response_data["message"]