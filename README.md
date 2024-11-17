
![example workflow](https://github.com/MatthewBE/SnowflakeDB-Logger/actions/workflows/python-app.yml/badge.svg)

https://github.com/MatthewBE/SnowflakeDB-Logger/blob/main/.github/workflows/python-app.yml

# Simple Snowflake Python Logger

## Purpose

Often organizations will have stringent role isolation levels within a Snowflake mesh like deployment. When the admin roles prevents access or creation of event tables in the current warehouse, it's often necessary to stream the logs in memory and collect the formatted data into defined schem to load post process into a custom python logging table. 

## Implementation

This requires an [Snowflake integration](https://docs.snowflake.com/en/user-guide/ecosystem-etl) and [Snowflake Stage](https://docs.snowflake.com/en/user-guide/data-load-considerations-stage) in the Cloud provider of choice. 

Logging in Python Stored Procedure in Snowflake 

```SQL
CREATE OR REPLACE DW.SCHEMA.PROCEDURE_NAME()
RETURNS VARCHAR(10)
LANGUAGE = PYTHON
RUNTIME_VERSION = '3.8'
PACKAGES = ()
HANDLER = 'main'
IMPORTS = ('@<YOUR_STAGE_NAME>/<PATH_TO_FILE>/sflogger.py')
EXECUTE AS CALLER
AS '
```
```Python

from sflogger import StreamLogger
import snowflake.snowpark as snowpark

sl = StreamLogger("PROCEDURE_NAME")
logger = sl.get_logger()

def failed_function():
  try:
    x = 1/0
  except Exception as e:
    logger.exception(e)

def main(session: snowpark.Session):

  logger.critical("CRITICAL MESSAGE!!")
  logger.info("INFORMATIONAL LOG MESSAGE")

  failed_function()

  log_data = sl.return_logs()

  log_df = session.createDataFrame(log_data["logs"],log_data["cols])
  session.write_pandas(log_df, sl.config.table, sl.config.databsde, sl.config.schema)

  return "logged"
  
```
