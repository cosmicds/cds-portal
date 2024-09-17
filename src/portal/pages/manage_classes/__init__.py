from datetime import date, datetime

import shortuuid
import solara
from solara.alias import rv
import httpx

from ...state import GLOBAL_STATE
from ...remote import BASE_API


@solara.component
def CreateClassDialog(on_create_clicked: callable = None):
    active, set_active = solara.use_state(False)  #
    text, set_text = solara.use_state("")
    stories, set_stories = solara.use_state([])

    with rv.Dialog(
        v_model=active,
        on_v_model=set_active,
        v_slots=[
            {
                "name": "activator",
                "variable": "x",
                "children": rv.Btn(
                    v_on="x.on",
                    v_bind="x.attrs",
                    class_="ml-2",
                    children=[rv.Icon(children=["mdi-plus"], class_="mr-2"), "New"],
                    elevation=0,
                ),
            }
        ],
        max_width=600,
    ) as dialog:
        with rv.Card(outlined=True):
            with rv.CardTitle():
                # rv.Html(tag="text-h5", children=["Create a New Class"])
                solara.Text("Create a New Class", classes=["text-h5"])

            rv.Divider()

            with rv.CardText(class_="px-4 py-2"):
                with rv.Row():
                    with rv.Col():
                        rv.TextField(
                            label="Class name",
                            outlined=True,
                            required=True,
                            hide_details="auto",
                            v_model=text,
                            on_v_model=set_text,
                        )

                        rv.Select(
                            v_model=stories,
                            outlined=True,
                            on_v_model=set_stories,
                            class_="pt-2",
                            hide_details="auto",
                            label="Data Story",
                            items=["Hubble's Law"],
                            multiple=False,
                        )

            rv.Divider()

            with rv.CardActions():

                def _add_button_clicked(*args):
                    on_create_clicked(
                        {
                            "name": f"{text}",
                            "stories": f"{', '.join(stories)}",
                        }
                    )
                    set_active(False)

                rv.Spacer()

                solara.Button("Cancel", on_click=lambda: set_active(False), elevation=0)
                solara.Button(
                    "Create", color="info", on_click=_add_button_clicked, elevation=0
                )

    return dialog


@solara.component
def DeleteClassDialog(on_delete_clicked: callable = None):
    active, set_active = solara.use_state(False)
    text, set_text = solara.use_state("")
    stories, set_stories = solara.use_state([])

    with rv.Dialog(
        v_model=active,
        on_v_model=set_active,
        v_slots=[
            {
                "name": "activator",
                "variable": "x",
                "children": rv.Btn(
                    v_on="x.on",
                    v_bind="x.attrs",
                    class_="ml-2",
                    children=[
                        rv.Icon(children=["mdi-delete"], class_="mr-2"),
                        "Delete",
                    ],
                    elevation=0,
                ),
            }
        ],
        max_width=600,
    ) as dialog:
        with rv.Card(outlined=True, style_=f"border-color: dark-red;"):
            rv.CardTitle(children=["Delete Class"])

            rv.Divider()

            with rv.CardText():
                solara.Text("Are you sure you want to delete this class?")

            rv.Divider()

            with rv.CardActions():

                def _delete_button_clicked(*args):
                    on_delete_clicked()
                    set_active(False)

                rv.Spacer()

                solara.Button("Cancel", on_click=lambda: set_active(False), elevation=0)
                solara.Button(
                    "Delete",
                    color="error",
                    on_click=_delete_button_clicked,
                    elevation=0,
                )

    return dialog


@solara.component
def Page():
    data, set_data = solara.use_state([])
    stu_data, set_stu_data = solara.use_state([])

    selected_rows, set_selected_rows = solara.use_state([])
    expanded_rows = solara.use_reactive([])

    def _retrieve_classes():
        classes_dict = BASE_API.load_educator_classes()

        new_classes = []

        for cls in classes_dict["classes"]:
            new_class = {
                "name": cls["name"],
                "date": datetime.fromisoformat(cls["created"]).strftime("%Y-%m-%d"),
                "story": "Hubble's Law",
                "code": cls["code"],
                "id": cls["id"],
            }

            new_classes.append(new_class)

        set_data(new_classes)

    solara.use_effect(_retrieve_classes, [])

    def _on_row_expanded(class_id: int):
        students = BASE_API.load_students_for_class(class_id)

        set_stu_data(
            [
                {
                    "username": student["username"],
                    "created": student["profile_created"],
                    "last_visit": student["last_visit"],
                }
                for student in students
            ]
        )

    def _create_class_callback(class_info):
        BASE_API.create_new_class(class_info["name"])
        _retrieve_classes()

    def _delete_class_callback():
        for row in selected_rows:
            BASE_API.delete_class(row["code"])

        _retrieve_classes()

    with solara.Row(classes=["fill-height"]):
        with rv.Col(cols=12):
            with rv.Row(class_="pa-0 mb-8 mx-0"):
                solara.Text("Manage Classes", classes=["headline"])
                rv.Spacer()

            with rv.Card(outlined=True, flat=True):
                with rv.Toolbar(flat=True, dense=True, class_="pa-0"):
                    CreateClassDialog(_create_class_callback)
                    rv.Spacer()
                    DeleteClassDialog(_delete_class_callback)

                classes_table = rv.DataTable(
                    items=data,
                    single_select=False,
                    show_select=True,
                    v_model=selected_rows,
                    on_v_model=set_selected_rows,
                    expanded=expanded_rows.value,
                    show_expand=True,
                    single_expand=False,
                    headers=[
                        {
                            "text": "Name",
                            "align": "start",
                            "sortable": True,
                            "value": "name",
                        },
                        {"text": "Date", "value": "date"},
                        {"text": "Story", "value": "story"},
                        {"text": "Code", "value": "code"},
                        {"text": "ID", "value": "id", "align": " d-none"},
                        # {"text": "Actions", "value": "actions", "align": "end"},
                    ],
                    v_slots=[
                        {
                            "name": "expanded-item",
                            "variable": "x",
                            "children": [
                                rv.Html(
                                    tag="td",
                                    attributes={"colspan": 6},
                                    children=[
                                        rv.Card(
                                            class_="d-flex justify-center pa-8",
                                            children=[
                                                rv.DataTable(
                                                    items=stu_data,
                                                    headers=[
                                                        {
                                                            "text": "Username",
                                                            "align": "start",
                                                            "value": "username",
                                                        },
                                                        {
                                                            "text": "Created",
                                                            "value": "created",
                                                        },
                                                        {
                                                            "text": "Last Visit",
                                                            "value": "last_visit",
                                                        },
                                                    ],
                                                ),
                                            ],
                                        )
                                    ],
                                )
                            ],
                        },
                    ],
                )

                solara.v.use_event(
                    classes_table,
                    "item-expanded",
                    lambda inst, evt, item: _on_row_expanded(item["item"]["id"]),
                )
