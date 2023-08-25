import dataclasses
import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Optional
import mentium
import logging
import requests

logger = logging.getLogger(__name__)

@dataclass
class UnixTimeStamp:
    seconds: int
    milliseconds: int

    @staticmethod
    def from_datetime(dt: datetime) -> 'UnixTimeStamp':
        timestamp = dt.timestamp()
        seconds = int(timestamp)
        milliseconds = int((timestamp - seconds) * 1000)
        return UnixTimeStamp(seconds, milliseconds)


@dataclass
class Timing:
    startTime: UnixTimeStamp
    endTime: UnixTimeStamp

    @staticmethod
    def from_datetimes(start: datetime, end: datetime) -> 'Timing':
        start_timestamp = UnixTimeStamp.from_datetime(start)
        end_timestamp = UnixTimeStamp.from_datetime(end)
        return Timing(start_timestamp, end_timestamp)


@dataclass
class OAIEvent:
    api_key: str
    timestamp: int
    request_id: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    latency: int
    user_id: Optional[str]
    organization_id: Optional[str]
    customer_id: Optional[str]



class Provider(Enum):
    OPENAI = "openai"
    AZURE_OPENAI = "azure-openai"


class MentiumAsyncLogger:
    logger = mentium.logger

    def _request(self, body: dict, url: str) -> requests.Response:
        res = requests.post(
            url=url,
            json=body,
            headers={
                "X-API-Key": mentium.api_key
            }
        )
        if (res.status_code != 200):
            logger.warn(f"Fail to send mentium event. Status code {res.status_code}")
        return res

    def log_event(self,
            provider: Provider,
            event: OAIEvent,
            ):
        data = dataclasses.asdict(
            event,
            dict_factory=lambda x: {k: v for (k, v) in x if v is not None}
        )
        if provider == Provider.OPENAI:
            self._request(
                body=data,
                url=f"{mentium.base_url}/v1/oai"
            )
        elif provider == Provider.AZURE_OPENAI:
            self._request(
                url=f"{mentium.base_url}/v1/oai",
                body=data,
            )
        else:
            raise ValueError(f"Unknown provider {provider}")
