from pathlib import Path

import ipyvuetify as v
import solara
from solara.alias import rv
from solara_enterprise import auth
import httpx
from solara.lab import Ref

from .state import GLOBAL_STATE, UserType
from .remote import BASE_API
from .components.hero import Hero
from .components.setup_dialog import UserTypeSetup


@solara.component
def Layout(children=[]):
    router = solara.use_router()
    snackbar, set_snackbar = solara.use_state(True)
    route_current, routes = solara.use_route()
    show_menu = solara.use_reactive(False)

    def _check_user_status():
        if BASE_API.student_exists:
            Ref(GLOBAL_STATE.fields.user.user_type).set(UserType.student)
        elif BASE_API.educator_exists:
            Ref(GLOBAL_STATE.fields.user.user_type).set(UserType.educator)

    solara.use_effect(_check_user_status, [])

    with rv.App(dark=True) as main:
        solara.Title("Cosmic Data Stories")

        with rv.AppBar(elevate_on_scroll=True, app=True):
            with rv.Container(class_="py-0 fill-height"):
                with solara.Link(solara.resolve_path("/")):
                    rv.Avatar(class_="me-10 ms-4", color="#cccccc", size="32")

                solara.Button(
                    "Data Stories",
                    text=True,
                    on_click=lambda: router.push("/data_stories"),
                )
                solara.Button(
                    "Mini Stories", text=True, on_click=lambda: router.push("/")
                )

                rv.Spacer()

                # solara.Text(f"User Type: {BASE_API.hashed_user}")

                if not Ref(GLOBAL_STATE.fields.user.is_validated).value:
                    solara.Button(
                        "Sign in", href=auth.get_login_url(), text=True, outlined=True
                    )
                else:
                    # if (
                    #     Ref(GLOBAL_STATE.fields.user.is_undefined).value
                    #     or not Ref(GLOBAL_STATE.fields.initial_setup_finished).value
                    # ):
                    if not (BASE_API.student_exists or BASE_API.educator_exists):
                        UserTypeSetup()

                    # if not Ref(GLOBAL_STATE.fields.user.is_undefined).value:
                    #     solara.Button("Manage Classes")

                    # rv.Divider(vertical=True)
                    rv.Btn(
                        icon=True,
                        children=[rv.Icon(children=["mdi-brightness-6"])],
                    )
                    rv.Btn(icon=True, children=[rv.Icon(children=["mdi-bell"])])

                    with rv.Menu(
                        offset_y=True,
                        offset_x=True,
                        v_model=show_menu.value,
                        on_v_model=show_menu.set,
                        v_slots=[
                            {
                                "name": "activator",
                                "variable": "x",
                                "children": rv.Btn(
                                    icon=True,
                                    class_="ml-2",
                                    children=[
                                        rv.Avatar(
                                            children=[
                                                rv.Img(
                                                    src="https://randomuser.me/api/portraits/women/85.jpg"
                                                )
                                            ]
                                        )
                                    ],
                                    text=True,
                                    outlined=True,
                                    v_on="x.on",
                                ),
                            }
                        ],
                    ):
                        with rv.List(dense=True, nav=True):
                            with rv.ListItem():
                                rv.ListItemAvatar(
                                    children=[
                                        rv.Img(
                                            src=f"https://randomuser.me/api/portraits/women/85.jpg"
                                        )
                                    ]
                                ),
                                rv.ListItemContent(
                                    children=[
                                        rv.ListItemTitle(
                                            children=[
                                                f"{auth.user.value['userinfo'].get("name", "email")}"
                                            ]
                                        ),
                                        rv.ListItemSubtitle(
                                            children=[
                                                f"{auth.user.value['userinfo'].get("email", "")}"
                                            ]
                                        ),
                                    ]
                                )

                            rv.Divider(class_="pb-1")

                            if (
                                Ref(GLOBAL_STATE.fields.user.user_type).value
                                == UserType.student
                            ):
                                with rv.ListItem(link=True) as classes_item:
                                    with rv.ListItemIcon():
                                        rv.Icon(children=["mdi-account"])

                                    rv.ListItemTitle(children=["My Classes"])

                                solara.v.use_event(
                                    classes_item,
                                    "click",
                                    lambda *args: router.push("/student_classes"),
                                )

                                rv.Divider(class_="pb-1")
                            elif (
                                Ref(GLOBAL_STATE.fields.user.user_type).value
                                == UserType.educator
                            ):
                                with rv.ListItem(link=True) as classes_item:
                                    with rv.ListItemIcon():
                                        rv.Icon(children=["mdi-account"])

                                    rv.ListItemTitle(children=["Manage Classes"])

                                solara.v.use_event(
                                    classes_item,
                                    "click",
                                    lambda *args: router.push("/manage_classes"),
                                )

                            with rv.ListItem(link=True):
                                with rv.ListItemIcon():
                                    rv.Icon(children=["mdi-settings"])

                                rv.ListItemTitle(children=["Settings"])

                            rv.Divider(class_="pb-1")

                            solara.Button(
                                "Logout",
                                style="width:100%",
                                icon_name="mdi-logout",
                                color="error",
                                text=False,
                                on_click=lambda: router.push("/"),
                                href=auth.get_logout_url(),
                            )

        with rv.Content():
            if route_current.path == "/":
                Hero()

            with rv.Container(
                children=children,
                style_="max-width: 1200px",
            ):
                pass

        with rv.Footer(app=False, padless=True):
            with rv.Container():
                with rv.Row(class_="d-flex justify-center"):
                    with rv.Col(class_="d-flex justify-center"):
                        rv.Btn(children=["About"], text=True)
                        rv.Btn(children=["Team"], text=True)
                        rv.Btn(children=["Contact"], text=True)
                        rv.Btn(children=["Privacy"], text=True)
                        rv.Btn(children=["Digital Accessibility"], text=True)

                rv.Divider()

                with rv.Row():
                    with rv.Col(class_="d-flex justify-center"):
                        solara.Text(
                            "Copyright © 2024 The President and Fellows of Harvard College"
                        )

    return main
