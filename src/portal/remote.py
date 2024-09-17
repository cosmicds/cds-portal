import uuid

from solara_enterprise import auth
import hashlib
import os
from requests import Session, Response
from functools import cached_property

from .state import GlobalState
from solara import Reactive
from solara.lab import Ref
from .logger import setup_logger

logger = setup_logger("API")


class BaseAPI:
    # API_URL = "https://api.cosmicds.cfa.harvard.edu"
    API_URL = "http://localhost:8081"

    @cached_property
    def request_session(self):
        """
        Returns a `requests.Session` object that has the relevant authorization
        parameters to interface with the CosmicDS API server (provided that
        environment variables are set correctly).
        """
        session = Session()
        session.headers.update({"Authorization": os.getenv("CDS_API_KEY")})
        return session

    @property
    def hashed_user(self):
        if auth.user.value is None:
            logger.error("Failed to create hash: user not authenticated.")
            return "User not authenticated"

        userinfo = auth.user.value.get("userinfo")

        if not ("email" in userinfo or "name" in userinfo):
            logger.error("Failed to create hash: not authentication information.")
            return

        user_ref = userinfo.get("email", userinfo["name"])

        hashed = hashlib.sha1(
            (user_ref + os.environ["SOLARA_SESSION_SECRET_KEY"]).encode()
        ).hexdigest()

        return hashed

    @property
    def student_exists(self):
        r = self.request_session.get(f"{self.API_URL}/students/{self.hashed_user}")
        return r.json()["student"] is not None

    @property
    def educator_exists(self):
        r = self.request_session.get(f"{self.API_URL}/educators/{self.hashed_user}")
        return r.json()["educator"] is not None

    def validate_class_code(self, class_code: str) -> bool:
        r = self.request_session.get(
            f"{self.API_URL}/validate-classroom-code/{class_code}"
        )
        return r.status_code == 200

    def load_student_info(self, stu_id: str = None) -> dict:
        stu_id = self.hashed_user if stu_id is None else stu_id

        student_json = self.request_session.get(
            f"{self.API_URL}/students/{stu_id}"
        ).json()

        return student_json["student"]

    def load_educator_info(self, edu_id: str = None) -> dict:
        edu_id = self.hashed_user if edu_id is None else edu_id

        educator_json = self.request_session.get(
            f"{self.API_URL}/educators/{edu_id}"
        ).json()

        return educator_json["educator"]

    def load_student_classes(self) -> list:
        student_json = self.load_student_info()
        sid = student_json["id"]

        r = self.request_session.get(
            f"{self.API_URL}/students/{self.hashed_user}/classes"
        )

        if r.status_code != 200:
            logger.error("Failed to load student classes.")
            return []

        return r.json()["classes"]

    def create_new_student(self, class_code: str) -> Response:
        r = self.request_session.get(f"{self.API_URL}/student/{self.hashed_user}")
        student = r.json()["student"]

        if student is not None:
            logger.error(
                "Failed to create user `%s`: user already exists.", self.hashed_user
            )

            r = Response()
            r.status_code = 500
            r.reason = "User already exists"

            return r

        payload = {
            "username": self.hashed_user,
            "password": "",
            "institution": "",
            "email": f"{self.hashed_user}",
            "age": 0,
            "gender": "undefined",
            "classroom_code": class_code,
        }

        r = self.request_session.post(
            f"{self.API_URL}/student-sign-up",
            json=payload,
        )

        print(r.json())

        if r.status_code != 200:
            logger.error("Failed to create new user.")
        else:
            logger.info(
                "Created new user `%s` with class code '%s'.",
                self.hashed_user,
                class_code,
            )

        return r

    def create_new_educator(self, form_data: dict) -> Response:
        r = self.request_session.get(f"{self.API_URL}/educators/{self.hashed_user}")
        educator = r.json()["educator"]

        if educator is not None:
            logger.error(
                "Failed to create user `%s`: user already exists.", self.hashed_user
            )

            r = Response()
            r.status_code = 500
            r.reason = "User already exists"

            return r

        form_data.update({"username": self.hashed_user, "password": str(uuid.uuid4())})

        r = self.request_session.post(
            f"{self.API_URL}/educator-sign-up",
            json=form_data,
        )

        if r.status_code != 200:
            logger.error("Failed to create new user.")

            r = Response()
            r.status_code = 500
            r.reason = "Something went wrong."
        else:
            logger.info(
                "Created new educator `%s`.",
                self.hashed_user,
            )

        return r

    def create_new_class(self, name: str) -> dict:
        r = self.request_session.get(f"{self.API_URL}/educators/{self.hashed_user}")
        educator = r.json()["educator"]

        r = self.request_session.post(
            f"{self.API_URL}/create-class",
            json={"educator_id": educator["id"], "name": name},
        )

        return r.json()

    def delete_class(self, class_id: int) -> dict:
        r = self.request_session.delete(f"{self.API_URL}/classes/{class_id}")

        return r.json()

    def load_educator_classes(self):
        r = self.request_session.get(f"{self.API_URL}/educators/{self.hashed_user}")
        educator = r.json()["educator"]

        r = self.request_session.get(
            f"{self.API_URL}/educator-classes/{educator['id']}"
        )

        print(r.json())

        return r.json()

    def load_students_for_class(self, class_id: int):
        r = self.request_session.get(f"{self.API_URL}//classes/roster/{class_id}")
        return r.json()

    def add_student_to_class(self, class_code: str, username: str) -> Response:
        r = self.request_session.post(
            f"{self.API_URL}/classes/join",
            json={"class_code": class_code, "username": username},
        )

        return r

    @staticmethod
    def clear_user(state: Reactive[GlobalState]):
        Ref(state.fields.student.id).set(0)
        Ref(state.fields.classroom.class_info).set({})
        Ref(state.fields.classroom.size).set(0)


BASE_API = BaseAPI()
