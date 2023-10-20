import json
import pytest
import allure
from jsonschema import validate



@pytest.fixture(params=json.load(open("requests.json")), ids=lambda r: r["name"])
def api_request(request):
    return request.param


@allure.epic("Проверка API МАРМ4")
def test_api(marm_api, api_request):
    service = api_request["service"]
    url = service + api_request["url"]
    allure.dynamic.feature(f'Проверка сервиса "{api_request["service"]}"')  # Динамическое определение feature
    allure.dynamic.title(api_request["name"])
    response = marm_api.get(url)
    with allure.step('Статус-код запроса'):
        assert response.status_code == 200, f"Неверный код ответа, получен {response.status_code}. URL запроса: {response.url}"
    response_data = response.json()

    # Загрузка схемы запроса из файла
    schema = json.load(open(api_request["schema_path"]))
    # Проверка схемы для каждого объекта в массиве
    with allure.step('Валидация ответа (проверка схемы и типов данных полей)'):
        for data_object in response_data:
            with allure.step('Проверка типов данных'):
                # Проверка типов данных для каждого поля в объекте
                for field, value in data_object.items():
                    field_schema = schema["properties"].get(field)
                    if field_schema:
                        field_type = field_schema.get("type")
                        if field_type:
                            assert isinstance(value,
                                              field_type), f"Неверный тип данных для поля '{field}', ожидается '{field_type}', получено '{type(value)}'"
                    else:
                        allure.attach(f"Поле '{field}' не найдено в схеме запроса")
            # Дополнительная логика для валидации других вещей
            # ...
            # ...
            # ...
            # ...
            validate(data_object, schema=schema)
