from pathlib import Path

import yaml

from api_compose import GlobalSettingsModelSingleton
from api_compose.core.jinja.core.context import BaseJinjaContext
from api_compose.core.jinja.core.engine import JinjaEngine, logger, JinjaTemplateSyntax
from api_compose.services.common.deserialiser.deserialiser import build_compile_time_jinja_engine, \
    deserialise_manifest_to_model
from api_compose.services.common.events.deserialisation import DeserialisationEvent
from api_compose.services.common.models.base import BaseModel
from api_compose.services.common.models.ref import RefResolverModel
from api_compose.services.common.processors.base import BaseProcessor
from api_compose.services.common.registry.processor_registry import ProcessorRegistry, ProcessorType, ProcessorCategory


@ProcessorRegistry.set(
    processor_type=ProcessorType.Builtin,
    processor_category=ProcessorCategory.Ref,
    models=[
        RefResolverModel(
            id='',
            description='',
            ref='actions/action_one.yaml',
            context=dict(
                execution_id='action_one_exec_one',
                url='http://abc.com',
                limit='12',
            ),
        ),
    ]
)
class RefResolver(BaseProcessor):
    """Resolve the reference"""
    

    def __init__(
            self,
            ref_resolver_model: RefResolverModel,
    ):
        super().__init__()
        self.ref_resolver_model = ref_resolver_model

    def resolve(
            self,
            manifests_folder_path: Path,
    ) -> BaseModel:
        return deserialise_manifest_to_model(
            manifest_file_path=self.ref_resolver_model.ref,
            manifests_folder_path=manifests_folder_path,
            context=self.ref_resolver_model.context,
            json_dump=False,
            is_rendering_strict=True
        )
        #
        # id = Path(self.ref_resolver_model.ref).parts[-1].split('.')[0]
        # str_, is_success, exec = (self.jinja_engine.set_template_by_file_path(
        #     template_file_path=self.ref_resolver_model.ref,
        #     can_strip=True).
        # render_to_str(
        #     jinja_context=BaseJinjaContext(**self.ref_resolver_model.context)))
        #
        # if not is_success:
        #     raise exec
        #
        # dict_ = yaml.safe_load(str_)
        # if dict_.get('id'):
        #     logger.warning(f'Id field is already set in the file. Will be overridden by the file name {id=}',
        #                    DeserialisationEvent())
        #
        # dict_['id'] = id
        # model_name = dict_.get('model_name')
        # model = ProcessorRegistry.create_model_by_name(model_name, dict_)
        # return model
