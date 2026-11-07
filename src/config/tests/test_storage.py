import logging

import pytest

from config.storage import StaticFilesStorage, vite_prefix

FILES = {
    "eduland.css": "body { color: red }",
    "vue/assets/editor-vue-CcNCj6ev.js": "console.log('vite')",
}


@pytest.fixture
def storage(tmp_path):
    """Storage after collectstatic, which gives post_process all collected files."""
    for name, content in FILES.items():
        (tmp_path / name).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / name).write_text(content)

    storage = StaticFilesStorage(location=tmp_path, base_url="/static/")
    paths = {name: (storage, name) for name in FILES}
    processed = [name for name, _, _ in storage.post_process(paths)]
    assert processed == ["eduland.css"]
    return storage


def test_vite_prefix():
    assert vite_prefix() == "vue/"


def test_hashed_file(storage):
    assert storage.stored_name("eduland.css").startswith("eduland.")
    assert storage.stored_name("eduland.css") != "eduland.css"


def test_vite_file_not_hashed_again(storage):
    name = "vue/assets/editor-vue-CcNCj6ev.js"
    assert storage.stored_name(name) == name


def test_missing_file(storage, caplog):
    with caplog.at_level(logging.WARNING, logger="config.storage"):
        assert storage.stored_name("missing.css") == "missing.css"
    assert "Static file not found: missing.css" in caplog.text
