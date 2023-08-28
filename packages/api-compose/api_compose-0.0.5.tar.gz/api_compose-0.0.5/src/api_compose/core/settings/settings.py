"""
Programme's Global Settings.

Cannot use logger. That would cause Cyclical Dependency OR double or triple logging of the same message
"""

__all__ = ['GlobalSettingsModelSingleton', 'GlobalSettingsModel']

import logging
from pathlib import Path
from typing import List, Optional, Dict, Set, Any

import yaml
from pydantic import Field

from api_compose.core.events.base import EventType
from api_compose.core.settings.yaml_settings import YamlBaseSettings, BaseSettings, SettingsConfigDict
from api_compose.services.persistence_service.models.enum import BackendProcessorEnum
from api_compose.services.reporting_service.models.enum import ReportProcessorEnum


class ActionSettings(BaseSettings):
    pass


class BackendSettings(BaseSettings):
    processor: BackendProcessorEnum = BackendProcessorEnum.SimpleBackend


class CliContextSettings(BaseSettings):
    model_config = SettingsConfigDict(extra='allow')


class DiscoverySettings(BaseSettings):
    env_file_path: Optional[Path] = Path('env.yaml')
    manifests_folder_path: Path = Path.cwd().joinpath('manifests')
    calculated_fields_folder_path: Path = Path.cwd().joinpath('calculated_fields')
    tags: Set[str] = set()


class LoggingSettings(BaseSettings):
    logging_level: int = logging.INFO
    log_file_path: Optional[Path] = Path.cwd().joinpath('log.jsonl')
    event_filters: List[EventType] = []


class SessionSettings(BaseSettings):
    description: str = 'Default Session Description'
    id: str = 'default_session_id'
    is_interactive: bool = Field(False, description='When True, users will be prompted to create assertions dynamically at the end of each Scenario Run')


class ReportingSettings(BaseSettings):
    processor: ReportProcessorEnum = ReportProcessorEnum.HtmlReport
    reports_folder: Path = Path('reports')


class GlobalSettingsModel(YamlBaseSettings):
    action: ActionSettings = ActionSettings()
    backend: BackendSettings = BackendSettings()
    build_folder: Path = Path().cwd().joinpath('build')
    compiled_folder: Path = Path('compiled')
    run_folder: Path = Path('run')
    cli_context: CliContextSettings = Field(CliContextSettings(), exclude=True)
    discovery: DiscoverySettings = DiscoverySettings()
    logging: LoggingSettings = LoggingSettings()
    session: SessionSettings = SessionSettings()
    reporting: ReportingSettings = ReportingSettings()

    model_config = SettingsConfigDict(
        env_nested_delimiter='__',
        yaml_file="config.yaml",
        env_prefix='acp__'
    )

    @property
    def env_vars(self) -> Dict[str, Any]:
        if self.discovery.env_file_path.exists():
            with open(self.discovery.env_file_path, 'r') as f:
                return yaml.load(f, Loader=yaml.FullLoader)
        else:
            return {}


class GlobalSettingsModelSingleton():
    _GLOBAL_SETTINGS_MODEL: Optional[GlobalSettingsModel] = None

    @classmethod
    def set(cls):
        cls._GLOBAL_SETTINGS_MODEL = GlobalSettingsModel()

    @classmethod
    def get(cls) -> GlobalSettingsModel:
        if cls._GLOBAL_SETTINGS_MODEL is None:
            raise ValueError('Global Settings Model not yet created!')
        return cls._GLOBAL_SETTINGS_MODEL
