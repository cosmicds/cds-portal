from pydantic import BaseModel
from enum import IntEnum
import solara
from solara_enterprise import auth
from solara.server import settings
import os


if "AWS_EBS_URL" in os.environ:
    settings.main.base_url = os.environ["AWS_EBS_URL"]


class BaseState(BaseModel):
    def as_dict(self):
        return self.model_dump()

    def update(self, new):
        return self.model_copy(update=new)


class UserType(IntEnum):
    none = 0
    student = 1
    educator = 2
    admin = 3


class User(BaseModel):
    id: int = None
    user_type: UserType = UserType.none
    verified: bool = False
    verification_code: str = None

    @property
    def is_educator(self):
        return self.user_type == UserType.educator

    @property
    def is_student(self):
        return self.user_type == UserType.student

    @property
    def is_admin(self):
        return self.user_type == UserType.admin

    @property
    def is_undefined(self):
        return self.user_type == UserType.none

    @property
    def is_validated(self):
        return auth.user.value is not None

    @property
    def exists_in_db(self):
        return self.id is not None


class GlobalState(BaseState):
    user: User = User()
    initial_setup_finished: bool = False


GLOBAL_STATE = solara.reactive(GlobalState())
