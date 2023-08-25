# -*- coding: utf-8 -*-
import asyncio
import logging
from datetime import datetime
from functools import cached_property
from typing import (
    Dict,
    Generic,
    List,
    Optional,
    Sequence,
    Set,
    Type,
    TypeVar,
    Union,
    get_args,
)

from pydantic import BaseModel
from pydantic.generics import GenericModel

from wyvern import request_context
from wyvern.components.component import Component
from wyvern.components.events.events import EventType, LoggedEvent
from wyvern.config import settings
from wyvern.entities.identifier import Identifier
from wyvern.entities.identifier_entities import WyvernEntity
from wyvern.entities.request import BaseWyvernRequest
from wyvern.event_logging import event_logger
from wyvern.exceptions import WyvernModelInputError
from wyvern.wyvern_typing import GENERALIZED_WYVERN_ENTITY, REQUEST_ENTITY

MODEL_OUTPUT_DATA_TYPE = TypeVar(
    "MODEL_OUTPUT_DATA_TYPE",
    bound=Union[float, str, List[float]],
)

logger = logging.getLogger(__name__)


class ModelEventData(BaseModel):
    model_name: str
    model_output: str
    entity_identifier: Optional[str] = None
    entity_identifier_type: Optional[str] = None


class ModelEvent(LoggedEvent[ModelEventData]):
    event_type: EventType = EventType.MODEL


class ModelOutput(GenericModel, Generic[MODEL_OUTPUT_DATA_TYPE]):
    data: Dict[Identifier, Optional[MODEL_OUTPUT_DATA_TYPE]]
    model_name: Optional[str] = None

    def get_entity_output(
        self,
        identifier: Identifier,
    ) -> Optional[MODEL_OUTPUT_DATA_TYPE]:
        return self.data.get(identifier)


class ModelInput(GenericModel, Generic[GENERALIZED_WYVERN_ENTITY, REQUEST_ENTITY]):
    request: REQUEST_ENTITY
    entities: List[GENERALIZED_WYVERN_ENTITY] = []

    @property
    def first_entity(self) -> GENERALIZED_WYVERN_ENTITY:
        if not self.entities:
            raise WyvernModelInputError(model_input=self)
        return self.entities[0]

    @property
    def first_identifier(self) -> Identifier:
        return self.first_entity.identifier


MODEL_INPUT = TypeVar("MODEL_INPUT", bound=ModelInput)
MODEL_OUTPUT = TypeVar("MODEL_OUTPUT", bound=ModelOutput)


class ModelComponent(
    Component[
        MODEL_INPUT,
        MODEL_OUTPUT,
    ],
):
    def __init__(
        self,
        *upstreams,
        name: Optional[str] = None,
    ):
        super().__init__(*upstreams, name=name)
        self.model_input_type = self.get_type_args_simple(0)
        self.model_output_type = self.get_type_args_simple(1)

    @classmethod
    def get_type_args_simple(cls, index: int) -> Type:
        return get_args(cls.__orig_bases__[0])[index]  # type: ignore

    @cached_property
    def manifest_feature_names(self) -> Set[str]:
        """
        This function defines which features are necessary for model evaluation

        Our system will automatically fetch the required features from the feature store
            to make this model evaluation possible
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} is a ModelComponent. "
            "The @cached_property function `manifest_feature_names` must be "
            "implemented to define features required for the model.",
        )

    async def execute(self, input: MODEL_INPUT, **kwargs) -> MODEL_OUTPUT:
        """
        The model_name and model_score will be automatically logged
        """
        api_source = request_context.ensure_current_request().url_path
        request_id = input.request.request_id
        model_output = await self.inference(input, **kwargs)

        def events_generator() -> List[ModelEvent]:
            timestamp = datetime.utcnow()
            return [
                ModelEvent(
                    request_id=request_id,
                    api_source=api_source,
                    event_timestamp=timestamp,
                    event_data=ModelEventData(
                        model_name=model_output.model_name or self.__class__.__name__,
                        model_output=str(output),
                        entity_identifier=identifier.identifier,
                        entity_identifier_type=identifier.identifier_type,
                    ),
                )
                for identifier, output in model_output.data.items()
            ]

        event_logger.log_events(events_generator)  # type: ignore

        return model_output

    async def batch_inference(
        self,
        request: BaseWyvernRequest,
        entities: List[Union[WyvernEntity, BaseWyvernRequest]],
    ) -> Sequence[Optional[Union[float, str, List[float]]]]:
        """
        Define your model inference in a batched manner so that it's easier to boost inference speed
        """
        raise NotImplementedError

    async def inference(
        self,
        input: MODEL_INPUT,
        **kwargs,
    ) -> MODEL_OUTPUT:
        """
        The inference function is the main entrance to model evaluation.

        By default, the base ModelComponent slices entities into smaller batches and call batch_inference on each batch.

        The default batch size is 30. You should be able to configure the MODEL_BATCH_SIZE env variable
        to change the batch size.

        In order to set up model inference, you only need to define a class that inherits ModelComponent and
        implement batch_inference.

        You can also override this function if you want to customize the inference logic.
        """
        target_entities: List[
            Union[WyvernEntity, BaseWyvernRequest]
        ] = input.entities or [input.request]

        # split entities into batches and parallelize the inferences
        batch_size = settings.MODEL_BATCH_SIZE
        futures = [
            self.batch_inference(
                request=input.request,
                entities=target_entities[i : i + batch_size],
            )
            for i in range(0, len(target_entities), batch_size)
        ]
        batch_outputs = await asyncio.gather(*futures)

        output_data: Dict[Identifier, Optional[Union[float, str, List[float]]]] = {}
        # map each entity.identifier to its output
        for batch_idx, batch_output in enumerate(batch_outputs):
            for entity_idx, output in enumerate(batch_output):
                entity = target_entities[batch_idx * batch_size + entity_idx]
                output_data[entity.identifier] = output

        return self.model_output_type(
            data=output_data,
            model_name=self.name,
        )
