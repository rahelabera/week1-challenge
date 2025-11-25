import os
import importlib


def test_project_files_exist():
    root = os.path.dirname(os.path.dirname(__file__))
    assert os.path.exists(os.path.join(root, "requirements.txt"))
    assert os.path.exists(os.path.join(root, "src"))
    assert os.path.exists(os.path.join(root, "notebooks"))


def test_import_src_package():
    # ensure src can be imported as a package
    spec = importlib.util.find_spec("src") # type: ignore
    assert spec is not None
