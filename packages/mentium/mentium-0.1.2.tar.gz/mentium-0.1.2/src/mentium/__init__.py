import logging
from mentium.wrapper import wrapper

logger = logging.getLogger(__name__)


api_key = ""
base_url = "https://api.mentium.io"

openai_wrapper = wrapper.MentiumOPENAIWrapper()