import logging
import sys
from math import ceil
from io import StringIO
from dataclasses import field, dataclass, asdict


@dataclass
class LoggerSchema:

    table : str = field(init=True, default="PYTHON_LOGS")
    database : str = field(init=True, default="SF_DBNAME")
    schema : str = field(init=True, default="SF")
    _ts : str = field(init=True, default="LOG_TIMESTAMP")   
    _level : str = field(init=True, default="LOG_LEVEL")
    _level_detail : str = field(init=True, default="LOG_LEVEL_DETAIL")
    _process : str = field(init=True, default="LOG_PROCESS")
    _trace : str = field(init=True, default="ERROR_TRACE")

    def get_cols(self):
        return [v for k, v in asdict(self).items() if "_" in k]


class LogMessageFormatter:

    def __init__(self):

        self.size_limit = float(15.00)
        self.default_size = sys.getsizeof("") / (1024**2)
    

    def check_string_size(self, msg: str) -> bool:
        """
        Check if the size of the given string exceeds a predefined limit.
        Calculates the size of the input string in megabytes and
        compares it against a size limit 
        Parameters:
        -----------
        msg : str
            The input string to be checked for size.

        Returns:
        --------
        bool
            True if the string size exceeds the limit, False otherwise.
        """

        msg_size = sys.getsizeof(msg) / (1024**2)
        if msg_size > self.size_limit: return True
        else: return False


    def calc_partition_size(self, msg: str)-> int:
        """
        Calculate the size of each partition for a given message.

        This method determines the appropriate size for partitioning a message
        based on a predefined size limit and a default size buffer. It first
        calculates the total size of the message in megabytes, then determines
        the number of partitions needed, and finally computes the number of
        characters for each partition.

        Parameters:
        -----------
        msg : str
            The input message to be partitioned.

        Returns:
        --------
        int
            The number of characters for each partition.
        """

        msg_size = sys.getsizeof(msg) / (1024**2)
        partitions = ceil(msg_size / (self.size_limit - self.default_size))
        n = ceil(len(msg) / partitions)

        return n
    
    
    def create_listof_logs(self)->list[str]:
        
        logs = self.log_capture_string.getvalue()
        log_split = logs.split("||")[1:]
        log_list = [s.split("|") for s in log_split]

        return log_list
    
    
    def partition_string(self, row: list)-> list[str]:

        data = row[-1] # get the error trace from list
        n = self.calc_partition_size(data)  
        l, r = 0, n
        partitions = []

        while l < len(data):
            partition = row[0:3] + [data[l:r]]
            partitions.append(partition)
            l = r
            r = r + n

        return partitions
    
    def format_logs(self)->list[list]:

        logs = self.create_listof_logs()
        res = []
        for log in logs:
            if self.check_string_size(log[-1]):
                res.append(self.partition_string(log))
            else:
                res.append(log)
        return res


class StreamLogger(LogMessageFormatter):

    def __init__(self, name: str):

        self.name = name
        self.level = logging.INFO
        self.config = LoggerSchema()
        self.log_capture_string = StringIO()

        super().__init__()
   

    def get_stream_handler(self):

        format = logging.Formatter("||%(asctime)s|%(levelname)s|%(name)s|%(message)s", "%Y-%m-%d %H:%M:%S")        
        stream_handler = logging.StreamHandler(self.log_capture_string)
        stream_handler.setFormatter(format)
        stream_handler.setLevel(self.level)

        return stream_handler
    
    def create_logger(self) -> logging.Logger:

        logger = logging.getLogger(self.name)
        logger.addHandler(self.get_stream_handler())
        logger.setLevel(self.level)

        return logger
    
    def return_logs(self)-> list[list]:
        
        columns = self.config.get_cols()
        logs = self.format_logs()
        data = {"cols": columns, "logs": logs}

        return data

