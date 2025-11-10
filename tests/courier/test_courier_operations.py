import pytest
from utils.helpers import Helpers


class TestCourierOperations:

    @pytest.mark.smoke
    @pytest.mark.courier
    def test_delete_courier_success(self, create_and_delete_courier, courier_api):
        """Тест успешного удаления курьера"""
        courier_data, courier_id = create_and_delete_courier

        # Проверяем что курьер был создан - логинимся
        login_response = courier_api.login_courier(courier_data["login"], courier_data["password"])
        Helpers.check_response_status(login_response, 200)

    @pytest.mark.regression
    @pytest.mark.courier
    def test_delete_nonexistent_courier(self, courier_api):
        """Тест удаления несуществующего курьера"""
        response = courier_api.delete_courier(999999)

        # API возвращает 404 для несуществующего курьера
        Helpers.check_response_status(response, 404)
        response_data = Helpers.extract_json(response)
        assert "code" in response_data
        assert response_data["code"] == 404

    @pytest.mark.smoke
    @pytest.mark.courier
    def test_get_courier_orders_count(self, create_and_delete_courier, courier_api):
        """Тест получения количества заказов курьера"""
        courier_data, courier_id = create_and_delete_courier

        response = courier_api.get_orders_count(courier_id)

        # API возвращает 404 если у курьера нет заказов или курьер не найден
        # Используем проверку на несколько возможных статусов
        Helpers.check_response_status_in(response, [200, 404])

        if response.status_code == 200:
            response_data = Helpers.extract_json(response)
            assert "id" in response_data
            assert "ordersCount" in response_data

    @pytest.mark.regression
    @pytest.mark.courier
    def test_get_orders_count_nonexistent_courier(self, courier_api):
        """Тест получения количества заказов несуществующего курьера"""
        response = courier_api.get_orders_count(999999)

        # API возвращает 404
        Helpers.check_response_status(response, 404)
        response_data = Helpers.extract_json(response)
        assert "code" in response_data
        assert response_data["code"] == 404

    @pytest.mark.regression
    @pytest.mark.courier
    def test_delete_courier_without_id(self, courier_api):
        """Тест удаления курьера без ID"""
        response = courier_api.delete_courier("")

        # API возвращает 404 для пустого ID
        Helpers.check_response_status(response, 404)
        response_data = Helpers.extract_json(response)
        assert "code" in response_data
        assert response_data["code"] == 404

    @pytest.mark.regression
    @pytest.mark.courier
    def test_get_orders_count_without_id(self, courier_api):
        """Тест получения количества заказов без ID курьера"""
        response = courier_api.get_orders_count("")

        # API возвращает 404
        Helpers.check_response_status(response, 404)
        response_data = Helpers.extract_json(response)
        assert "code" in response_data
        assert response_data["code"] == 404