from enum import Enum


class Role(Enum):
    USER = 'user'
    QA_MANAGER = 'qa_manager'
    MANAGER = 'manager'
    ADMIN = 'admin'


class Status(Enum):
    SUCCEEDED = 'Succeeded'
    FAILED = 'Failed'
    ABORTED = 'Aborted'
