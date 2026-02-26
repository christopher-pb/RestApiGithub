"""
JSON-file backed repository implementation.
"""
import json
import os
import threading
from typing import TypeVar, Type, Optional, List

from app.repositories.base_repository import BaseRepository

T = TypeVar("T")


class JsonRepository(BaseRepository[T]):

    def __init__(self, filepath: str, model_cls: Type[T]):
        self.filepath = filepath
        self.model_cls = model_cls
        self.lock = threading.Lock()

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                json.dump([], f)

    # ---------- helpers ----------

    def _read(self) -> List[dict]:
        with open(self.filepath, "r") as f:
            return json.load(f)

    def _write(self, data: List[dict]):
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=2)

    def _to_model(self, data: dict) -> T:
        return self.model_cls.from_dict(data)

    def _to_dict(self, entity: T) -> dict:
        return entity.to_dict()

    # ---------- CRUD ----------

    def get_all(self) -> List[T]:
        with self.lock:
            return [self._to_model(d) for d in self._read()]

    def get_by_id(self, entity_id: str) -> Optional[T]:
        with self.lock:
            for item in self._read():
                # Try common ID fields dynamically
                for key in item.keys():
                    if key.endswith("_id") or key == "id":
                        if item.get(key) == entity_id:
                            return self._to_model(item)
        return None

    def get_by_field(self, field_name: str, value) -> Optional[T]:
        """
        Generic search by any field (used for login: username lookup)
        """
        with self.lock:
            for item in self._read():
                if item.get(field_name) == value:
                    return self._to_model(item)
        return None

    def create(self, entity: T) -> T:
        with self.lock:
            data = self._read()
            data.append(self._to_dict(entity))
            self._write(data)
        return entity

    def update(self, entity_id: str, entity: T) -> Optional[T]:
        with self.lock:
            data = self._read()

            for i, item in enumerate(data):
                for key in item.keys():
                    if key.endswith("_id") or key == "id":
                        if item.get(key) == entity_id:
                            data[i] = self._to_dict(entity)
                            self._write(data)
                            return entity

        return None

    def delete(self, entity_id: str) -> bool:
        with self.lock:
            data = self._read()

            new_data = []
            found = False

            for item in data:
                matched = False
                for key in item.keys():
                    if key.endswith("_id") or key == "id":
                        if item.get(key) == entity_id:
                            matched = True
                            found = True
                            break
                if not matched:
                    new_data.append(item)

            if not found:
                return False

            self._write(new_data)
            return True