# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

import pydantic

from ....core.datetime_utils import serialize_datetime
from ...commons.types.llm_usage import LlmUsage
from ...commons.types.map_value import MapValue
from ...commons.types.observation_level import ObservationLevel


class UpdateGenerationRequest(pydantic.BaseModel):
    generation_id: str = pydantic.Field(alias="generationId")
    trace_id: typing.Optional[str] = pydantic.Field(alias="traceId")
    name: typing.Optional[str]
    end_time: typing.Optional[dt.datetime] = pydantic.Field(alias="endTime")
    completion_start_time: typing.Optional[dt.datetime] = pydantic.Field(alias="completionStartTime")
    model: typing.Optional[str]
    model_parameters: typing.Optional[typing.Dict[str, MapValue]] = pydantic.Field(alias="modelParameters")
    prompt: typing.Optional[typing.Any]
    version: typing.Optional[str]
    metadata: typing.Optional[typing.Any]
    completion: typing.Optional[str]
    usage: typing.Optional[LlmUsage]
    level: typing.Optional[ObservationLevel]
    status_message: typing.Optional[str] = pydantic.Field(alias="statusMessage")

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        allow_population_by_field_name = True
        json_encoders = {dt.datetime: serialize_datetime}
