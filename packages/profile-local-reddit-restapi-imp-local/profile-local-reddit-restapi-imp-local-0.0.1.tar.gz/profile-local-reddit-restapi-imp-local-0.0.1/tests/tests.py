import praw
from unittest.mock import patch, Mock
from io import StringIO
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
import pytest
import sys
import os

PROFILE_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = 190
PROFILE_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME = 'reddit/tests/tests.py'
EMAIL = os.environ.get('EMAIL')

object_to_insert = {
        'component_id': PROFILE_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
        'component_name': PROFILE_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
        'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
        'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
        'developer_email': EMAIL
    }

logger = Logger.create_logger(object=object_to_insert)

# Add the parent directory to the path so we can import the script
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the script
import reddit.src.search_reddit as reddit_script

def test_authenticate_reddit():
    logger.start("test_authenticate_reddit")
    reddit = reddit_script.Reddit().authenticate_reddit()
    assert isinstance(reddit, praw.Reddit)
    logger.end("test_authenticate_reddit")

@patch("builtins.input", side_effect=["funny", "id,name,created_utc", "10"])
def test_get_subreddit_and_query():
    logger.start("test_get_subreddit_and_query")
    subreddit_name, query, num = reddit_script.Reddit().get_subreddit_and_query()
    assert subreddit_name == "funny"
    assert query == ["id", "name", "created_utc"]
    assert num == 10
    logger.end("test_get_subreddit_and_query")
    


# Run the tests
if __name__ == "__main__":
    pytest.main()
