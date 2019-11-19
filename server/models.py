from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from server.database import Base
from sqlalchemy.orm import relationship
from datetime import  datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)


class Workflows(Base):
    __tablename__ = 'workflows'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    status = Column(String(30), unique=False)
    date = Column(DateTime)

    def __init__(self, name=None, status=None):
        self.name = name
        self.status = status
        self.date = datetime.now()

    def __repr__(self):
        return self

    def get_workflow(self):
        return {"id": self.id,
                "name": self.name,
                "date": self.date,
                "status": self.status
                }


class WorkflowMessages(Base):
    __tablename__ = 'workflow_messages'
    id = Column(Integer, primary_key=True)
    wf_id = Column(Integer, ForeignKey('workflows.id'))
    msg = Column(String(100), unique=False)
    status = Column(String(30), unique=False)

    wf = relationship("Workflows", foreign_keys=[wf_id])

    def __init__(self, msg=None, status=None, wf_id=1):
        self.wf_id = wf_id
        self.msg = msg
        self.status = status

    def __repr__(self):
        return self

    def get_workflow_json(self):
        return {"id": self.id,
                "workflow": self.name,
                "date": self.date,
                "status": self.status
                }


class WorkflowJobs(Base):
    __tablename__ = 'workflow_jobs'
    id = Column(Integer, primary_key=True)
    wf_id = Column(Integer, ForeignKey('workflows.id'))
    msg = Column(String(100), unique=False)
    name = Column(String(30), unique=False)
    input = Column(String(500), unique=False)
    output = Column(String(500), unique=False)
    log = Column(String(100), unique=False)
    wildcards = Column(String(100), unique=False)
    is_checkpoint = Column(Boolean, unique=False)
    shel_command = Column(String(100), unique=False)
    status = Column(String(30), unique=False)

    wf = relationship("Workflows", foreign_keys=[wf_id])

    def __init__(self, ids, wf_id, msg, name, input, output, log, wildcards, is_checkpoint, shel_command=None,
                 status=None):
        self.id = ids
        self.wf_id = wf_id
        self.msg = msg
        self.name = name
        self.input = input
        self.output = output
        self.log = log
        self.wildcards = wildcards
        self.is_checkpoint = is_checkpoint
        self.shel_command = shel_command
        self.status = status

    def __repr__(self):
        return self

    def get_job_json(self):
        return {"id": self.id,
                "workflow_id": self.wf_id,
                "msg": self.msg,
                "name": self.name,
                "input": eval(self.input),
                "output": eval(self.output),
                "log": eval(self.log),
                "wildcards": eval(self.wildcards),
                "is_checkpoint":  self.is_checkpoint,
                "shel_command": self.shel_command,
                "status": self.status
                }

