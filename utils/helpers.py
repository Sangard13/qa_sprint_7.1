import json


class Helpers:

    @staticmethod
    def extract_json(response):
        """Извлечение JSON из ответа"""
        try:
            return response.json()
        except json.JSONDecodeError:
            return {}

    @staticmethod
    def check_response_status(response, expected_status):
        """Проверка статуса ответа"""
        assert response.status_code == expected_status, \
            f"Expected status {expected_status}, but got {response.status_code}. " \
            f"Response: {response.text}"

    @staticmethod
    def check_response_status_in(response, expected_statuses):
        """Проверка что статус ответа находится в списке ожидаемых"""
        assert response.status_code in expected_statuses, \
            f"Expected status in {expected_statuses}, but got {response.status_code}. " \
            f"Response: {response.text}"

    @staticmethod
    def check_error_message(response, expected_message=None):
        """Проверка сообщения об ошибке (теперь опционально)"""
        response_data = Helpers.extract_json(response)
        if expected_message:
            assert "message" in response_data, f"No error message in response. Response: {response_data}"
            assert response_data["message"] == expected_message, \
                f"Expected message '{expected_message}', but got '{response_data.get('message')}'"
        return response_data