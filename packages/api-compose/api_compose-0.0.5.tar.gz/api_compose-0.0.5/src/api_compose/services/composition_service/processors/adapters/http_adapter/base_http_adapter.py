import traceback
from typing import Dict, Optional
from unittest.mock import Mock

import requests
from requests import Response

from api_compose.core.logging import get_logger
from api_compose.services.common.registry.processor_registry import ProcessorRegistry, ProcessorType, ProcessorCategory
from api_compose.services.common.field.templated_text_field import BaseTemplatedTextField
from api_compose.services.composition_service.events.action import ActionEvent, ActionData
from api_compose.services.composition_service.jinja.context import ActionJinjaContext
from api_compose.services.composition_service.models.actions.states import ActionStateEnum
from api_compose.services.composition_service.models.calculated_field.calculated_field import \
    BuiltinCalculatedFieldNameEnum
from api_compose.services.composition_service.models.protocols.status_enums import HttpResponseStatusEnum, \
    OtherResponseStatusEnum
from api_compose.services.composition_service.processors.adapters.base_adapter import BaseAdapter
from api_compose.services.composition_service.registry.calculated_field_registry import CalculatedFieldRegistry

logger = get_logger(__name__)


@ProcessorRegistry.set(
    processor_type=ProcessorType.Builtin,
    processor_category=ProcessorCategory.Adapter,
    models=[]
)
class BaseHttpAdapter(BaseAdapter):
    """
    Communication over HTTP
    """

    @CalculatedFieldRegistry.set(name=BuiltinCalculatedFieldNameEnum.HTTP_METHOD.value)
    def calculate_method(self, **ctx) -> str:
        return self.method.render_to_text(jinja_engine=self.jinja_engine, jinja_context=self.jinja_context).deserialise_to_obj().obj

    @CalculatedFieldRegistry.set(name=BuiltinCalculatedFieldNameEnum.HTTP_HEADERS.value)
    def calculate_headers(self, **ctx) -> Dict:
        return self.headers.render_to_text(jinja_engine=self.jinja_engine, jinja_context=self.jinja_context).deserialise_to_obj().obj

    @CalculatedFieldRegistry.set(name=BuiltinCalculatedFieldNameEnum.HTTP_PARAMS.value)
    def calculate_params(self, **ctx) -> Dict:
        return self.params.render_to_text(jinja_engine=self.jinja_engine, jinja_context=self.jinja_context).deserialise_to_obj().obj

    def __init__(
            self,
            method: BaseTemplatedTextField,
            headers: BaseTemplatedTextField,
            params: BaseTemplatedTextField,
            *args,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.method = method
        self.required_templated_fields[BuiltinCalculatedFieldNameEnum.HTTP_METHOD.value] = self.method
        self.headers = headers
        self.required_templated_fields[BuiltinCalculatedFieldNameEnum.HTTP_HEADERS.value] = self.headers
        self.params = params
        self.required_templated_fields[BuiltinCalculatedFieldNameEnum.HTTP_PARAMS.value] = self.params

        self.response: Optional[Response] = None

    def _on_start(self, jinja_context: ActionJinjaContext):
        """
        Hook to preprocess config passed
        :return:
        """
        super()._on_start(jinja_context)

    def _on_exchange(self):
        super()._on_exchange()

        logger.info(f"Action %s is communicating over HTTP" % (self.action_model.execution_id), ActionEvent(
            data=ActionData(id=self.action_model.execution_id, state=ActionStateEnum.RUNNING,
                            input={'url': self.calculated_field_registry.get_value_by_name(
                                BuiltinCalculatedFieldNameEnum.URL.value),
                                'method': self.calculated_field_registry.get_value_by_name(
                                    BuiltinCalculatedFieldNameEnum.HTTP_METHOD.value),
                                'headers': self.calculated_field_registry.get_value_by_name(
                                    BuiltinCalculatedFieldNameEnum.HTTP_HEADERS.value),
                                'params': self.calculated_field_registry.get_value_by_name(
                                    BuiltinCalculatedFieldNameEnum.HTTP_PARAMS.value),
                                'body': self.calculated_field_registry.get_value_by_name(
                                    BuiltinCalculatedFieldNameEnum.HTTP_JSON_BODY.value),
                            })))

        body = self.calculated_field_registry.get_value_by_name(BuiltinCalculatedFieldNameEnum.HTTP_JSON_BODY.value)
        if len(body) == 0:
            body = None

        self.response = requests.request(
            method=self.calculated_field_registry.get_value_by_name(BuiltinCalculatedFieldNameEnum.HTTP_METHOD.value),
            url=self.calculated_field_registry.get_value_by_name(BuiltinCalculatedFieldNameEnum.URL.value),
            headers=self.calculated_field_registry.get_value_by_name(BuiltinCalculatedFieldNameEnum.HTTP_HEADERS.value),
            params=self.calculated_field_registry.get_value_by_name(BuiltinCalculatedFieldNameEnum.HTTP_PARAMS.value),
            json=body,
            verify=False,
        )

    def _on_error(self):
        super()._on_error()
        self.response = build_default_response(
            response_str=self.__class__.ERROR_OUTPUT_BODY,
            url=self.calculated_field_registry.get_value_by_name(BuiltinCalculatedFieldNameEnum.URL.value),
            headers=self.calculated_field_registry.get_value_by_name(BuiltinCalculatedFieldNameEnum.HTTP_HEADERS.value),
        )

    def _on_end(self):
        super()._on_end()

    def _set_response_status(self):
        status_code = self.response.status_code
        try:
            self.response_status = HttpResponseStatusEnum(status_code)
        except Exception as e:
            logger.error(f"No matching status found for status code {status_code}")
            self.response_status = OtherResponseStatusEnum.NO_MATCHING_STATUS_FOUND

    def start(self, jinja_context: ActionJinjaContext):
        try:
            # Might error on_start when rendering
            self._on_start(jinja_context=jinja_context)
            # Might error on_exchange when doing network call
            self._on_exchange()
        except Exception as e:
            self._on_error()
            logger.error(traceback.format_exc(),
                         ActionEvent(data=ActionData(id=self.action_model.execution_id, state=ActionStateEnum.ERROR)))
        else:
            self._on_end()
        finally:
            # Clean up
            self._set_input()
            self.action_model.input = self.input
            self._set_output()
            self.action_model.output = self.output
            self._set_response_status()
            self.action_model.response_status = self.response_status

    def stop(self):
        logger.debug("stop() in JsonHttpAdapter not implemented", ActionEvent(data=ActionData(id=self.action_model.execution_id)))


def build_default_response(
        response_str: str,
        headers: Dict = None,
        url: str = "",

) -> Response:
    response = Mock(spec=Response)
    response.url = url
    response.headers = headers if not headers else {}
    response.text = response_str
    response.status_code = HttpResponseStatusEnum.NOT_FOUND.value
    return response
