import random, string, pytest, sys
from io import StringIO
import sflogger as sf

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


def test_stream_hanlder_format():
    handler = sl.get_stream_handler()
    assert handler.formatter._fmt == "||%(asctime)s|%(levelname)s|%(name)s|%(message)s"

def test_stream_handler_io_object():
    handler = sl.get_stream_handler()
    assert handler.stream.__class__ == StringIO().__class__

def test_stream_handler_level():
    handler = sl.get_stream_handler()
    assert handler.level == 20

def test_formatted_log_type():
    logs = sl.create_listof_logs()
    assert isinstance(logs, list)

def test_formatted_sublog_type():
    logs = sl.create_listof_logs()
    assert all(isinstance(log, list) for log in logs)

def test_partitioned_large_log():
    logger.info(create_random_string(30000))
    logs = sl.create_listof_logs()
    partition = sl.partition_string(logs[-1])

    assert isinstance(partition, list)  

def test_partitioned_large_log_size():
    logger.info(create_random_string(30000))
    logs = sl.create_listof_logs()
    partition = sl.partition_string(logs[-1])

    for p in partition:
        assert sys.getsizeof(p) / (1024**2) < 15

def test_partition_large_log_output_length():
    logger.info(create_random_string(30000))
    logs = sl.create_listof_logs()
    partition = sl.partition_string(logs[-1])

    assert all(len(p) == 4 for p in partition)

