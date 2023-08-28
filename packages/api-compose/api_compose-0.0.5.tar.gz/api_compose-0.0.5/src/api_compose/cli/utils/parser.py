from typing import Optional, List, Dict, Tuple

from api_compose.core.logging import get_logger
from api_compose.services.common.events.deserialisation import DeserialisationEvent

logger = get_logger(__name__)


def parse_context(context: Optional[List[str]]) -> Dict[str, str]:
    dict_ = {}
    if context is not None and type(context) == list:
        for val in context:
            key, val = validate_context_kv_pair(val)
            dict_[key] = val
        logger.info('Parsed CLI context \n' f'{dict_=}', DeserialisationEvent())
    else:
        logger.warning('Cannot parse CLI context as it is not a list a strings \n' f'{context=}', DeserialisationEvent())

    return dict_


def validate_context_kv_pair(kv_pair: str) -> Tuple[str, str]:
    kv_pair = kv_pair.strip()
    assert '=' in kv_pair, f'{kv_pair} does not follow the syntax key=kv_pairue pair.'
    parts = kv_pair.split('=')
    if len(parts) > 2:
        raise ValueError(f'{kv_pair} does not follow the syntax key=kv_pairue pair.')
    key, val = parts
    return key, val
