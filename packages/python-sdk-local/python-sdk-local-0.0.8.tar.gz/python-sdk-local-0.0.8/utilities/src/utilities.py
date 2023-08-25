import datetime
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from dotenv import load_dotenv
load_dotenv()
from logger_local.Logger import Logger  # noqa: E402

PYTHON_SDK_LOCAL_COMPONENT_ID = 184
PYTHON_SDK_LOCAL_COMPONENT_NAME = 'python_sdk_local/src/utilities.py'

obj = {
    'component_id': PYTHON_SDK_LOCAL_COMPONENT_ID,
    'component_name': PYTHON_SDK_LOCAL_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': 'tal.g@circ.zone'
}

logger = Logger.create_logger(object=obj)


def timedelta_to_time_format(timedelta: datetime.timedelta):
    TIMEDELTA_TO_TIME_FORMAT_METHOD_NAME = "timedelta_to_time_format"
    logger.start(TIMEDELTA_TO_TIME_FORMAT_METHOD_NAME)
    # The following line will cause TypeError: Object of type timedelta is not JSON serializable
    # logger.start(TIMEDELTA_TO_TIME_FORMAT_METHOD_NAME, object={'timedelta':  timedelta})

    # Calculate the total seconds and convert to HH:MM:SS format
    total_seconds = int(timedelta.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    # Format as "HH:MM:SS"
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    logger.end(TIMEDELTA_TO_TIME_FORMAT_METHOD_NAME,
               object={'formatted_time':  formatted_time})
    return formatted_time
