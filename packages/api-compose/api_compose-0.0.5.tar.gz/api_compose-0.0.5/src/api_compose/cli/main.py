import datetime
from typing import Annotated, List, Optional

import typer

from api_compose import get_logger
from api_compose.cli.commands import config
from api_compose.cli.events import CliEvent
from api_compose.cli.utils.parser import parse_context
from api_compose.cli.utils.yaml_dumper import dump_model_as_yaml
from api_compose.core.settings import GlobalSettingsModelSingleton, CliContextSettings
from api_compose.services.common.deserialiser.deserialiser import deserialise_manifest_to_model
from api_compose.cli.session_builder.builder import build_session_from_tags, build_session_from_model
from api_compose.root import run_session_model
from api_compose.version import __version__

logger = get_logger(__name__)

DOCUMENTATION_URL = ""
EPILOG_TXT = f"Doc: {DOCUMENTATION_URL}"
HELP_TXT = "Declaratively Compose and Test and Report your API Calls"

app = typer.Typer(
    help=HELP_TXT,
    short_help=HELP_TXT,
    epilog=EPILOG_TXT,
    no_args_is_help=True
)

app.add_typer(config.app, name='cfg', help="Configuration")


@app.command(help="Scaffold Project Structure")
def version() -> None:
    typer.echo(__version__)


@app.command(help="Scaffold Project Structure")
def scaffold(project_name: str) -> None:
    pass


@app.command(help="Compile a template to a model")
def compile(
        select: Annotated[Optional[str], typer.Option(help='Relative Path to Manifest')] = None,
        ctx: Annotated[Optional[List[str]], typer.Option()] = None,
) -> None:
    """
    Render and Execute

    Usage:

    acp render --ctx key1=val1 --ctx key2=val2

    :return:
    """
    GlobalSettingsModelSingleton.get().cli_context = CliContextSettings(**parse_context(ctx))
    manifests_folder_path = GlobalSettingsModelSingleton.get().discovery.manifests_folder_path
    folder_path = GlobalSettingsModelSingleton.get().build_folder.joinpath(
        GlobalSettingsModelSingleton.get().compiled_folder
    )
    timestamp = datetime.datetime.utcnow()
    if select:
        model = deserialise_manifest_to_model(
            select,
            manifests_folder_path=manifests_folder_path,
        )
    else:
        # Run any specification with matching tags
        model = build_session_from_tags(
            target_tags=GlobalSettingsModelSingleton.get().discovery.tags,
            manifests_folder_path=manifests_folder_path,
        )

    file_path = folder_path.joinpath(f'{model.model_name}-{timestamp}.yaml')
    dump_model_as_yaml(model, file_path)



@app.command(help="Run manifests")
def run(
        select: Annotated[Optional[str], typer.Option(help='Relative Path to Manifest')] = None,
        is_interactive: Annotated[Optional[bool], typer.Option("--interactive/--no-interactive", "-i/-I")] = None,
        ctx: Annotated[Optional[List[str]], typer.Option()] = None
):
    """
    Render and Run

    acp run --ctx key1=val1 --ctx key2=val2

    :return:
    """
    GlobalSettingsModelSingleton.get().cli_context = CliContextSettings(**parse_context(ctx))
    if is_interactive is not None:
        logger.debug(f'Setting session.is_interactive to {is_interactive}', CliEvent())
        GlobalSettingsModelSingleton.get().session.is_interactive = is_interactive
    manifests_folder_path = GlobalSettingsModelSingleton.get().discovery.manifests_folder_path
    folder_path = GlobalSettingsModelSingleton.get().build_folder.joinpath(
        GlobalSettingsModelSingleton.get().run_folder
    )
    timestamp = datetime.datetime.utcnow()

    if select:
        # Run specific manifest
        model = deserialise_manifest_to_model(
            select,
            manifests_folder_path=manifests_folder_path,
        )
        session_model = build_session_from_model(model)
    else:
        # Run any specification with matching tags
        session_model = build_session_from_tags(
            target_tags=GlobalSettingsModelSingleton.get().discovery.tags,
            manifests_folder_path=manifests_folder_path,
        )
    session_model = run_session_model(session_model, timestamp)
    file_path = folder_path.joinpath(f'{session_model.model_name}-{timestamp}.yaml')
    dump_model_as_yaml(session_model, file_path)
