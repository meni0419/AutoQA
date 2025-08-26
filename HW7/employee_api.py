import time
from typing import Any, Dict, Optional, Tuple, Union

import requests


class EmployeeApi:
    """
    Вспомогательный класс-обёртка над API сотрудников.
    Позволяет создавать, читать и изменять данные о сотрудниках.
    """

    def __init__(self, session: requests.Session, base_url: str = "http://5.101.50.27:8000"):
        self.session = session
        self.base_url = base_url.rstrip("/")

    # -------------------- Public API methods --------------------

    def create_employee(self, payload: Dict[str, Any], timeout: int = 10) -> Dict[str, Any]:
        """
        POST /employee/create
        Body: JSON с данными сотрудника
        Returns: JSON ответа (ожидаем в нём id созданного сотрудника)
        """
        url = f"{self.base_url}/employee/create"
        resp = self.session.post(url, json=payload, timeout=timeout)
        self._ensure_success(resp, expected_statuses=(200, 201))
        return self._to_json(resp)

    def get_employee(self, employee_id: Union[int, str], timeout: int = 10) -> Dict[str, Any]:
        """
        GET /employee/info?id=<employee_id>
        Returns: JSON с данными сотрудника
        """
        url = f"{self.base_url}/employee/info"
        resp = self.session.get(url, params={"id": employee_id}, timeout=timeout)
        self._ensure_success(resp, expected_statuses=(200,))
        return self._to_json(resp)

    def patch_employee(self, employee_id: Union[int, str], patch: Dict[str, Any], timeout: int = 10) -> Dict[str, Any]:
        """
        PATCH /employee/change
        Body: JSON с id и полями для изменения
        Returns: JSON обновлённого сотрудника или подтверждение
        """
        url = f"{self.base_url}/employee/change"
        body = {"id": employee_id, **patch}
        resp = self.session.patch(url, json=body, timeout=timeout)
        self._ensure_success(resp, expected_statuses=(200,))
        return self._to_json(resp)

    # -------------------- Helpers --------------------

    @staticmethod
    def _ensure_success(resp: requests.Response, expected_statuses: Tuple[int, ...]) -> None:
        if resp.status_code not in expected_statuses:
            # Пытаемся вытащить тело в текст для удобства диагностики
            detail = ""
            try:
                detail = resp.text
            except Exception:
                pass
            raise AssertionError(
                f"Unexpected response status {resp.status_code}, expected {expected_statuses}. Body: {detail}"
            )

    @staticmethod
    def _to_json(resp: requests.Response) -> Dict[str, Any]:
        try:
            return resp.json()
        except Exception as exc:
            raise AssertionError(f"Response is not valid JSON. Error: {exc}. Body: {resp.text!r}")

    @staticmethod
    def extract_id(payload: Dict[str, Any]) -> Optional[Union[int, str]]:
        """
        Пытается извлечь id сотрудника из разных возможных форматов ответов:
        - плоский JSON: {"id": 123, ...}
        - вложенный JSON: {"data": {"id": 123, ...}}
        - альтернативные ключи: employee_id, employeeId
        """
        candidates = [
            payload.get("id"),
            payload.get("employee_id"),
            payload.get("employeeId"),
        ]
        # Вариант с "data"
        data = payload.get("data")
        if isinstance(data, dict):
            candidates.extend([data.get("id"), data.get("employee_id"), data.get("employeeId")])

        for cid in candidates:
            if cid is not None:
                return cid
        return None

    @staticmethod
    def unwrap_data(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Возвращает основное содержимое ответа:
        - если есть "data" и это dict — вернёт его
        - иначе вернёт сам payload
        """
        data = payload.get("data")
        return data if isinstance(data, dict) else payload