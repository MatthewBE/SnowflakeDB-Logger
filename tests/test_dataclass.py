from sflogger import LoggerSchema

test_dataclass = LoggerSchema()

def test_dataclass_get_cols():
    cols = ["LOG_TIMESTAMP", "LOG_LEVEL", "LOG_LEVEL_DETAIL", "LOG_PROCESS", "ERROR_TRACE"]
    assert test_dataclass.get_cols() == cols

def test_dataclass_get_cols_type():
    assert isinstance(test_dataclass.get_cols(), list)
    