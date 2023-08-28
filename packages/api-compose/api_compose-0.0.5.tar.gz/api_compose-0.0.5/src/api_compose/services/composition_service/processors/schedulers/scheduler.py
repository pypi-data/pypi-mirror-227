import traceback
from typing import List, Tuple

from api_compose.core.events.scheduler import SchedulerEvent
from api_compose.core.jinja.core.engine import JinjaEngine
from api_compose.core.logging import get_logger
from api_compose.core.utils.base_scheduler import BaseScheduler
from api_compose.services.composition_service.events.executor import ExecutorEvent
from api_compose.services.composition_service.exceptions import ActionAlreadyExecutedException, \
    ActionsWithSameExecutionIdException
from api_compose.services.composition_service.jinja.context import ActionJinjaContext
from api_compose.services.composition_service.models.actions.actions import BaseActionModel
from api_compose.services.composition_service.models.actions.states import ActionStateEnum
from api_compose.services.composition_service.processors.actions import Action
from api_compose.services.composition_service.processors.executors.base_executor import BaseExecutor
from api_compose.services.persistence_service.processors.base_backend import BaseBackend

logger = get_logger(__name__)


def validate_action_models(actions: List[BaseActionModel]):
    # Test 1
    for action in actions:
        if action.state != ActionStateEnum.PENDING:
            raise ActionAlreadyExecutedException(action.id)

    # Test 2
    if len(set([action.uid for action in actions])) != len(actions):
        raise ActionsWithSameExecutionIdException(
            [action.uid for action in actions]
        )



class ActionScheduler(BaseScheduler):

    def __init__(self,
                 executor: BaseExecutor,
                 backend: BaseBackend,
                 jinja_engine: JinjaEngine,
                 # Graph
                 nodes: List[BaseActionModel] = None,
                 edges: List[Tuple[BaseActionModel, BaseActionModel]] = None,
                 *args,
                 **kwargs,
                 ):
        super().__int__(*args, nodes=nodes, edges=edges, **kwargs)
        self.backend = backend
        self.jinja_engine = jinja_engine
        self.executor = executor
        validate_action_models(self.nodes)

    def is_node_successful(self, node: BaseActionModel) -> bool:
        logger.debug(f"Polling node {node.uid=} - {node.state=}", SchedulerEvent())
        return node.state == ActionStateEnum.ENDED

    def is_node_done(self, node: BaseActionModel) -> bool:
        logger.debug(f"Polling node {node.uid=} - {node.state=}", SchedulerEvent())
        return node.state in [ActionStateEnum.ERROR, ActionStateEnum.ENDED, ActionStateEnum.DISCARDED]

    def execute_node(self, node: BaseActionModel, skip: bool) -> None:
        if skip:
            node.state = ActionStateEnum.DISCARDED
        else:
            logger.info(f'Executing action model {node.uid=} - {skip=}', SchedulerEvent())
            jinja_context: ActionJinjaContext = ActionJinjaContext.build(
                backend=self.backend,
                action_model=node
            )
            action = Action(action_model=node,
                            backend=self.backend,
                            jinja_engine=self.jinja_engine,
                            )
            try:
                self.executor.execute(action, jinja_context)
            except Exception as e:
                logger.error(traceback.format_exc(), ExecutorEvent())
                raise


