import traceback

from server.database import init_db, db_session
from server.models import Workflows, WorkflowMessages


def get_db_workflows():
    return Workflows.query.all()


def get_db_workflows_by_id(workflow_id):
    return Workflows.query.filter(Workflows.id == workflow_id).first()



