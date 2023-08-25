import functools
from typing import Optional
import inspect
import openai
from openai.api_resources import (
    ChatCompletion,
    Completion,
    Edit,
    Embedding,
    Image,
    Moderation,
)
from datetime import datetime, timedelta
from mentium.logger.async_logger import MentiumAsyncLogger, Provider, OAIEvent


class AttributeDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttributeDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def normalize_data_type(data_type):
    if isinstance(data_type, str):
        data_type = data_type.lower()

    if data_type in (str, "str", "string"):
        return "string"
    elif data_type in (bool, "bool", "boolean"):
        return "boolean"
    elif data_type in (float, int, "float", "int", "numerical"):
        return "numerical"
    elif data_type in (object, "object", "categorical"):
        return "categorical"
    else:
        raise ValueError(
            "Invalid data_type provided. Please use a valid data type or string.")


class MentiumOPENAIWrapper:
    def __init__(self):
        self.openai = openai
        self.apply_mentium_wrapper()
        self.logger = MentiumAsyncLogger()

    def _mask_api_key(self, api_key: Optional[str], mask_char='*') -> Optional[str]:
        if api_key is None or len(api_key) <= 2 * 12:
            return api_key  # Return the original key if it's too short to mask

        start = api_key[:8]
        end = api_key[-4:]
        masked_length = len(api_key) - 2 * 12
        masked_part = mask_char * masked_length

        return start + masked_part + end

    def _log_result(self, result: dict, timestamp: datetime, latency: timedelta,  metadata: dict = {}):
        def result_with_mentium():
            for r in result:
                yield r

        if inspect.isgenerator(result):
            return result_with_mentium()
        else:
            key = self._mask_api_key(openai.api_key)
            self.logger.log_event(Provider.OPENAI, OAIEvent(
                api_key=key,
                organization_id=openai.organization,
                request_id=result['id'],
                customer_id=metadata.get("customer", None),
                user_id=metadata.get("user", None),
                timestamp=result.get("created", timestamp),
                latency=latency.microseconds,
                completion_tokens=result["usage"]["completion_tokens"],
                prompt_tokens=result["usage"]["prompt_tokens"],
                model=result["model"]
            ))
            return result

    async def _log_result_async(self, result: dict, timestamp: datetime, latency: timedelta, 
                                metadata: dict = {}):
        async def result_with_mentium_async():
            async for r in result:
                yield r

        if inspect.isasyncgen(result):
            return result_with_mentium_async()
        else:
            key = self._mask_api_key(openai.api_key)
            self.logger.log_event(Provider.OPENAI, OAIEvent(
                api_key=key,
                organization_id=openai.organization,
                request_id=result['id'],
                customer_id=metadata.get("customer", None),
                user_id=metadata.get("user", None),
                timestamp=result.get("created", timestamp),
                latency=latency.microseconds,
                completion_tokens=result["usage"]["completion_tokens"],
                prompt_tokens=result["usage"]["prompt_tokens"],
                model=result["model"]
            ))
            return result
        
    def _filter_mentium_metadata(self, **kwargs) -> (dict, dict):
        metadata = {}
        metadata["user"] = kwargs.get("user", None)
        metadata["customer"] = kwargs.pop("customer", None)
        metadata["organization"] = kwargs.pop("organization", None)
        return kwargs, metadata

    def _with_mentium_wrapper(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            filtered_kwargs, metadata = self._filter_mentium_metadata(**kwargs)
            start = datetime.utcnow()
            result = func(*args, **filtered_kwargs)
            end = datetime.utcnow()
            latency = (end - start) // 1000
            return self._log_result(result, timestamp=start, latency=latency, metadata=metadata)

        return wrapper

    def _with_mentium_wrapper_async(self, func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            filtered_kwargs, metadata = self._filter_mentium_metadata(**kwargs)
            start = datetime.utcnow()
            result = await func(*args, **filtered_kwargs)
            end = datetime.utcnow()
            latency = (end - start) // 1000
            return await self._log_result_async(result, timestamp=start, latency=latency, metadata=metadata)

        return wrapper



    def apply_mentium_wrapper(self_parent):

        api_resources_classes = [
            (ChatCompletion, "create", "acreate"),
            # (Completion, "create", "acreate"),
            # (Edit, "create", "acreate"),
            # (Embedding, "create", "acreate"),
            # (Image, "create", "acreate"),
            # (Moderation, "create", "acreate"),
        ]

        for api_resource_class, method, async_method in api_resources_classes:
            create_method = getattr(api_resource_class, method)
            setattr(api_resource_class, method,
                    self_parent._with_mentium_wrapper(create_method))

            async_create_method = getattr(api_resource_class, async_method)
            setattr(api_resource_class, async_method,
                    self_parent._with_mentium_wrapper_async(async_create_method))
