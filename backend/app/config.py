from __future__ import annotations

from importlib import import_module
from types import ModuleType

from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'app'
    _models_module_path = 'app.models'

    @property
    def models_module(self) -> ModuleType | None:
        return import_module(self._models_module_path)

    @models_module.setter
    def models_module(self, value: ModuleType | None) -> None:
        pass
