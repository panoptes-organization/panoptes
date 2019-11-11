from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
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
        return '<Workflow %r>' % (self.name)

    def get_workflow(self):
        return {"id": self.id,
                "name":self.name}


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
        return '<Workflow %r>' % (self.id)

