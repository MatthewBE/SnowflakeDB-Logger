import random, string, pytest
import src.sflogger as sf

sl = sf.StreamLogger("Test Logging")
logger = sl.create_logger()

def create_random_string(length):
    letters = string.printable
    return "".join(random.choice(letters) for i in range(length))

with pytest.raises(Exception) as err:
    r= 1/0
    logger.exception(err)   

with pytest.raises(KeyError) as err:
    test_d= {}
    x = test_d["key"]
    logger.exception(err)   

with pytest.raises(IndexError) as err: 
    arr = list(range(10))
    x = arr[12] 
    logger.exception(err)

logger.info("This is an info message")
logger.error("ERROR Message")   
logger.warning("WARNING Message")
logger.info(create_random_string(30000))

data = sl.return_logs()

def test_data_columns_length():
    assert len(data["cols"]) == 5

def test_data_columns_vals():
    assert data["cols"] == ["LOG_TIMESTAMP", "LOG_LEVEL", "LOG_LEVEL_DETAIL", "LOG_PROCESS" , "ERROR_TRACE"]

def test_data_logs():
    assert len(data["logs"]) > 4

def test_data_logs_type():
    assert isinstance(data["logs"], list)

def test_data_logs_subtype():
    logs = data["logs"]
    for l in logs:
        assert isinstance(l, list)

def test_output_levels():
    assert data["logs"][0][1] in ["INFO", "ERROR", "WARNING"]
