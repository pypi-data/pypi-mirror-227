__all__ = []

import sys
from pathlib import Path

from api_compose.core.settings.settings import GlobalSettingsModelSingleton
from api_compose.cli.events import DiscoveryEvent
from api_compose.services.composition_service.events.calculated_field import CalculatedFieldRegistrationEvent

# read into global settings
GlobalSettingsModelSingleton.set()

# Get logger after settings are set
import importlib

# Help with import from CLI
sys.path.append(str(Path.cwd()))
from api_compose.core.logging import get_logger

logger = get_logger(__name__)

# Display Configurations
logger.debug(
    'Display Configurations: \n'
    + GlobalSettingsModelSingleton.get().model_dump_json(indent=4)
)

# Display Env var
if GlobalSettingsModelSingleton.get().discovery.env_file_path.exists():
    logger.debug('Display Environment Variables: \n' + '\n'.join(
        [f"{idx}: {key}={value}" for idx, (key, value) in
         enumerate(GlobalSettingsModelSingleton.get().env_vars.items())]), DiscoveryEvent())
else:
    logger.warning(
        f'Failed to find environment variables file  at {GlobalSettingsModelSingleton.get().discovery.env_file_path}')

# Import Calculated Fields
calculated_field_folder_path = GlobalSettingsModelSingleton.get().discovery.calculated_fields_folder_path
if calculated_field_folder_path.exists():
    # Extract the module name from the file path
    module_name = calculated_field_folder_path.stem
    # Import the module dynamically
    module = importlib.import_module(module_name)
else:
    logger.debug(f"Failed to Import Custom Calculated Fields. Folder {calculated_field_folder_path} does not exist",
                 DiscoveryEvent())

# Import manifests
if not GlobalSettingsModelSingleton.get().discovery.manifests_folder_path.exists():
    logger.warning(
        f'Failed to find manifest folder at {GlobalSettingsModelSingleton.get().discovery.manifests_folder_path}')

# Import for side effect (Controller Registration)
from api_compose.services.common.processors.ref import RefResolver # noqa - register ref processor to Registry

from api_compose.services.persistence_service.processors.base_backend import \
    BaseBackend  # noqa - register backend to Registry
from api_compose.services.persistence_service.processors.simple_backend import \
    SimpleBackend  # noqa - register backend to Registry

from api_compose.services.composition_service.processors.actions import Action  # noqa - register action to Registry
from api_compose.services.composition_service.processors.adapters.http_adapter.json_http_adapter import \
    JsonHttpAdapter  # noqa - register adapter to Registry
from api_compose.services.composition_service.processors.adapters.http_adapter.xml_http_adapter import \
    XmlHttpAdapter  # noqa - register adapter to Registry
from api_compose.services.composition_service.processors.adapters.websocket_adapter import \
    JsonRpcWebSocketAdapter  # noqa - register adapter to Registry
from api_compose.services.composition_service.processors.executors.local_executor import \
    LocalExecutor  # noqa - register executors to Registry

from api_compose.services.composition_service.processors.schema_validators.json_schema_validator import \
    JsonSchemaValidator  # noqa - register Schema Validator to Registry
from api_compose.services.composition_service.processors.schema_validators.xml_schema_validator import \
    XmlSchemaValidator  # noqa - register executors to Registry

from api_compose.services.reporting_service.processors.html_report import \
    HtmlReport  # noqa - register report_renderers to Registry

