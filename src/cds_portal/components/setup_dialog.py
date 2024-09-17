import solara

from solara.alias import rv
import ipyvuetify as v

# from ..server import manager
from ..state import GLOBAL_STATE, UserType
from solara.lab import Ref
from pathlib import Path
from ..remote import BASE_API
from ..components.join_class import JoinClass
from ..components.request_form import RequestForm

IMG_PATH = Path("static") / "public" / "images"


@solara.component
def InitialSetup():
    router = solara.use_router()
    step, set_step = solara.use_state("1")

    student_submit_count = solara.use_reactive(0)
    educator_submit_count = solara.use_reactive(0)

    class_code = solara.use_reactive("")
    student_validation_message = solara.use_reactive("")
    educator_validation_message = solara.use_reactive("")

    form_data = solara.use_reactive(
        {
            # "valid": False,
            # "verified": False,
            "first_name": "",
            "last_name": "",
            "email": "",
            "confirm_email": "",
            "institution": "",
            "age": 0,
            "gender": "undefined",
        }
    )

    def _on_finished_clicked(*args):
        Ref(GLOBAL_STATE.fields.initial_setup_finished).set(True)
        router.push("/student_classes")

    with rv.Card():
        with rv.CardTitle():
            with rv.Row(class_="pa-0 ma-0"):
                solara.Text("Choose Your Role")

                if int(step) > 1:
                    rv.Spacer()
                    solara.Button(
                        icon_name="mdi-refresh",
                        icon=True,
                        on_click=lambda: set_step("1"),
                    )

        with rv.CardText():
            with rv.Stepper(v_model=step, on_v_model=set_step):
                with rv.StepperItems():
                    with rv.StepperContent(step="1"):
                        with rv.Row():
                            with rv.Col(cols=6):
                                with rv.Card(
                                    height=200,
                                    class_="d-flex align-center justify-center",
                                    link=True,
                                    hover=True,
                                ) as student_card:
                                    with rv.Img(
                                        src=str(IMG_PATH / "student.jpg"),
                                        class_="white--text align-end",
                                        height=200,
                                        gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)",
                                    ):
                                        with rv.CardTitle():
                                            solara.Text("Student")

                                def _student_card_clicked(*args):
                                    Ref(GLOBAL_STATE.fields.user.user_type).set(
                                        UserType.student
                                    )
                                    set_step("2")

                                solara.v.use_event(
                                    student_card,
                                    "click",
                                    _student_card_clicked,
                                )

                            with rv.Col(cols=6):
                                with rv.Card(
                                    height=200,
                                    class_="d-flex align-center justify-center",
                                    link=True,
                                    hover=True,
                                ) as educator_card:
                                    with rv.Img(
                                        src=str(IMG_PATH / "educator.jpg"),
                                        class_="white--text align-end",
                                        height=200,
                                        gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)",
                                    ):
                                        with rv.CardTitle():
                                            solara.Text("Educator")

                                def _educator_card_clicked(*args):
                                    Ref(GLOBAL_STATE.fields.user.user_type).set(
                                        UserType.educator
                                    )
                                    set_step("2")

                                solara.v.use_event(
                                    educator_card,
                                    "click",
                                    _educator_card_clicked,
                                )

                    # Student steps
                    with rv.StepperContent(step="2"):
                        if (
                            Ref(GLOBAL_STATE.fields.user.user_type).value
                            == UserType.student
                        ):
                            JoinClass(
                                class_code,
                                student_validation_message,
                            )
                        elif (
                            Ref(GLOBAL_STATE.fields.user.user_type).value
                            == UserType.educator
                        ):
                            RequestForm(form_data, educator_validation_message)

                    with rv.StepperContent(step="3"):
                        with rv.Row(
                            class_="pa-0 ma-0 d-flex align-center justify-center"
                        ):
                            with rv.Col(cols=12, class_="pa-0 ma-0"):
                                rv.Img(
                                    src=str(IMG_PATH / "success.gif"),
                                    max_height=100,
                                    contain=True,
                                )

                                if (
                                    Ref(GLOBAL_STATE.fields.user.user_type).value
                                    == UserType.student
                                ):
                                    solara.Text(
                                        "You have successfully joined the class."
                                    )
                                elif (
                                    Ref(GLOBAL_STATE.fields.user.user_type).value
                                    == UserType.educator
                                ):
                                    solara.Text(
                                        "Your request has been submitted successfully."
                                    )

        if step == "2":
            rv.Divider()

            with rv.CardActions():
                rv.Spacer()

                if Ref(GLOBAL_STATE.fields.user.user_type).value == UserType.student:

                    def _on_join_clicked(*args):
                        class_exists = BASE_API.validate_class_code(class_code.value)

                        if not class_exists:
                            student_validation_message.set("Class does not exist.")
                            return

                        student_response = BASE_API.create_new_student(class_code.value)

                        if student_response.status_code != 200:
                            student_validation_message.set(student_response.reason)
                            return

                        set_step("3")

                    solara.Button(
                        "Join",
                        on_click=_on_join_clicked,
                    )
                elif Ref(GLOBAL_STATE.fields.user.user_type).value == UserType.educator:

                    def _on_submit_clicked(*args):
                        educator_response = BASE_API.create_new_educator(
                            form_data.value
                        )

                        if educator_response.status_code != 200:
                            educator_validation_message.set(educator_response.reason)
                            return

                        set_step("3")

                    solara.Button(
                        "Submit",
                        on_click=_on_submit_clicked,
                    )
        elif step == "3":
            rv.Divider()
            with rv.CardActions():
                rv.Spacer()
                solara.Button("Finish", on_click=_on_finished_clicked)


@solara.component
def UserTypeSetup():
    show = solara.use_reactive(True)

    active = (
        Ref(GLOBAL_STATE.fields.user.is_validated).value
        and not Ref(GLOBAL_STATE.fields.initial_setup_finished).value
    ) and show.value

    # @solara.lab.computed
    # def active():
    #     return (
    #         Ref(GLOBAL_STATE.fields.user.is_validated).value
    #         and not Ref(GLOBAL_STATE.fields.initial_setup_finished).value
    #     ) or show.value

    with rv.Dialog(
        v_model=active, on_v_model=show.set, max_width=600, persistent=False
    ) as user_type_setup:
        InitialSetup()
        # if not (unfinished_student or unfinished_educator):
        #     InitialSetup()
        # elif unfinished_student:
        #     UnfinishedStudent()
        # elif unfinished_educator:
        #     pass

    return user_type_setup
