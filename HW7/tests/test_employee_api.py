import uuid
import pytest

from employee_api import EmployeeApi


@pytest.mark.api
def test_employee_crud_flow(api: EmployeeApi):
    """
    Полный поток:
    1) Создать сотрудника
    2) Получить по id и сравнить ключевые поля
    3) Изменить часть данных (PATCH)
    4) Снова получить по id и проверить, что изменения применены, а остальные поля не сломаны
    """
    # Уникальные данные, чтобы не конфликтовать с уже существующими записями
    uniq = uuid.uuid4().hex[:8]
    initial_payload = {
        "first_name": f"Max-{uniq}",
        "last_name": "Melnychuk",
        "age": 28,
        "department": "QA",
        "position": "Automation QA",
    }

    # 1) Create
    create_resp = api.create_employee(initial_payload)
    created_id = EmployeeApi.extract_id(create_resp)
    assert created_id is not None, f"В ответе на создание не найден id. Ответ: {create_resp}"

    # 2) Get by id
    get_resp = api.get_employee(created_id)
    get_data = EmployeeApi.unwrap_data(get_resp)
    # Проверим, что хотя бы некоторые ключевые поля сохранились
    for k in ("first_name", "last_name", "age"):
        assert k in get_data, f"В ответе /employee/info отсутствует поле {k}. Ответ: {get_data}"
        assert str(get_data[k]) == str(initial_payload[k]), f"Поле {k} не совпадает. Ожидалось: {initial_payload[k]!r}, получено: {get_data[k]!r}"

    # 3) Patch
    patch_payload = {
        "age": 29,
        "position": "Senior Automation QA",
    }
    patch_resp = api.patch_employee(created_id, patch_payload)

    # Возможные варианты ответа: сразу обновлённые данные или просто статус/сообщение.
    # Поэтому повторно читаем по id.
    get_after_patch = api.get_employee(created_id)
    data_after = EmployeeApi.unwrap_data(get_after_patch)

    # 4) Проверки после обновления
    assert str(data_after.get("age")) == str(patch_payload["age"]), f"Возраст не обновился. Ответ: {data_after}"
    assert data_after.get("position") == patch_payload["position"], f"Должность не обновилась. Ответ: {data_after}"
    # Проверим, что другие поля сохранились
    assert data_after.get("first_name") == initial_payload["first_name"]
    assert data_after.get("last_name") == initial_payload["last_name"]