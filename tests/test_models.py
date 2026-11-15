import importlib
import sys
import typing

import typing_extensions  # noqa: F401  loaded before sys.version_info is faked


def test_models_import_on_python_before_3_11(monkeypatch):
    monkeypatch.delattr(typing, "NotRequired", raising=False)
    monkeypatch.setattr(sys, "version_info", (3, 8, 20, "final", 0))
    monkeypatch.delitem(sys.modules, "scoop.models", raising=False)
    models = importlib.import_module("scoop.models")
    assert "url" in models.AppManifest.__optional_keys__
