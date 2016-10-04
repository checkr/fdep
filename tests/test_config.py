from fdep.config import FdepConfig


def test_read_config(fdep_yml):
    fdep = FdepConfig.load(fdep_yml)
    assert isinstance(fdep.config['default'], dict)
    assert isinstance(fdep.config['production'], dict)


def test_write_config(empty_fdep_yml):
    fdep = FdepConfig({
        "default": {
            "write_test.txt": "http://example.com/write_test.txt"
        }
    })
    fdep.save(empty_fdep_yml)

    loaded_fdep = FdepConfig.load(empty_fdep_yml)
    assert loaded_fdep.config["default"].get("write_test.txt") is not None


def test_find_local_path(fdep_yml, test_project_path):
    assert FdepConfig.find_local_config(test_project_path) == fdep_yml
