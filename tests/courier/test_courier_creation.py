import pytest
import allure
from data.test_data import TestData
from utils.helpers import Helpers


@allure.epic("Courier API")
@allure.feature("Courier Creation")
class TestCourierCreation:

    @allure.title("Successful courier creation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.courier
    def test_create_courier_success(self, courier_api, courier_data):
        with allure.step("Create courier with valid data"):
            response = courier_api.create_courier(
                courier_data["login"],
                courier_data["password"],
                courier_data["firstName"]
            )

        with allure.step("Check creation response"):
            Helpers.check_response_status(response, 201)
            response_data = Helpers.extract_json(response)
            assert response_data.get("ok") == True

    @allure.title("Create courier with missing data")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.courier
    @pytest.mark.parametrize("invalid_data", TestData.INVALID_CREATION_DATA)
    def test_create_courier_missing_data(self, courier_api, invalid_data):
        with allure.step("Try to create courier with missing data"):
            response = courier_api.create_courier(
                invalid_data.get("login", ""),
                invalid_data.get("password", ""),
                invalid_data.get("firstName", "")
            )

        with allure.step("Check error response"):
            # API возвращает 400 для недостающих данных, 409 для дубликатов
            Helpers.check_response_status_in(response, [400, 409])
            response_data = Helpers.extract_json(response)
            assert "code" in response_data
            assert response_data["code"] in [400, 409]

    @allure.title("Create duplicate courier")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.courier
    def test_create_duplicate_courier(self, create_and_delete_courier, courier_api):
        with allure.step("Get existing courier data"):
            courier_data, courier_id = create_and_delete_courier

        with allure.step("Try to create courier with same login"):
            response = courier_api.create_courier(
                courier_data["login"],
                "different_password",
                "different_name"
            )

        with allure.step("Check duplicate error response"):
            Helpers.check_response_status(response, 409)
            response_data = Helpers.extract_json(response)
            assert response_data["code"] == 409
            assert "message" in response_data