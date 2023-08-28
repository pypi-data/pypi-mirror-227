import datetime
from pathlib import Path

from pydantic import BaseModel

from api_compose import GlobalSettingsModelSingleton
from api_compose.cli.utils.yaml_dumper import dump_model_as_yaml
from api_compose.root import SessionModel



def dump_session_model(
        session: SessionModel,
        timestamp: datetime.datetime,
):
    folder_path = GlobalSettingsModelSingleton.get().build_folder.joinpath(
        GlobalSettingsModelSingleton.get().session.run_folder
    )
    file_path = folder_path.joinpath(f"{timestamp}.yaml")
    dump_model_as_yaml(session, file_path)


