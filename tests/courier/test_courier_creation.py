import pytest
import allure
from data.test_data import TestData
from utils.helpers import Helpers


class TestCourierCreation:

    @pytest.mark.smoke
    @pytest.mark.courier
    def test_create_courier_success(self, courier_api, courier_data):
        """Тест успешного создания курьера"""
        response = courier_api.create_courier(
            courier_data["login"],
            courier_data["password"],
            courier_data["firstName"]
        )

        Helpers.check_response_status(response, 201)
        response_data = Helpers.extract_json(response)
        assert response_data.get("ok") == True

    @pytest.mark.regression
    @pytest.mark.courier
    @pytest.mark.parametrize("invalid_data", TestData.INVALID_CREATION_DATA)
    def test_create_courier_missing_data(self, courier_api, invalid_data):
        """Тест создания курьера с недостаточными данными"""
        response = courier_api.create_courier(
            invalid_data.get("login", ""),
            invalid_data.get("password", ""),
            invalid_data.get("firstName", "")
        )

        # API возвращает 400 для недостающих данных
        Helpers.check_response_status(response, 400)
        response_data = Helpers.extract_json(response)
        assert "code" in response_data
        assert response_data["code"] == 400

    @pytest.mark.regression
    @pytest.mark.courier
    def test_create_duplicate_courier(self, create_and_delete_courier, courier_api):
        """Тест создания курьера с дублирующимся логином"""
        courier_data, courier_id = create_and_delete_courier

        # Пытаемся создать курьера с тем же логином
        response = courier_api.create_courier(
            courier_data["login"],
            "different_password",
            "different_name"
        )

        # API возвращает 409 для дубликатов
        Helpers.check_response_status(response, 409)
        response_data = Helpers.extract_json(response)
        assert "code" in response_data
        assert response_data["code"] == 409