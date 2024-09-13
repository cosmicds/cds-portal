from datetime import date, datetime

import shortuuid
import solara
from solara.alias import rv
import httpx

from ...state import GLOBAL_STATE
from ...remote import BASE_API


@solara.component
def AddClassDialog(callback, **btn_kwargs):
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
                    children=["Add"],
                    elevation=0,
                    **btn_kwargs,
                ),
            }
        ],
        max_width=600,
    ) as dialog:
        with rv.Card(outlined=True):
            with rv.CardTitle():
                rv.Html(tag="text-h5", children=["Add Class"])

            with rv.CardText():
                rv.TextField(
                    label="Class name",
                    outlined=True,
                    required=True,
                    v_model=text,
                    on_v_model=set_text,
                )

                rv.Select(
                    v_model=stories,
                    outlined=True,
                    on_v_model=set_stories,
                    label="Data Stories",
                    items=["Hubble"],
                    multiple=True,
                )

            rv.Divider()

            with rv.CardActions():

                def _add_button_clicked(*args):
                    callback(
                        {
                            "name": f"{text}",
                            "date": f"{date.today()}",
                            "stories": f"{', '.join(stories)}",
                            "code": f"{shortuuid.uuid()}",
                        }
                    )
                    set_active(False)

                rv.Spacer()

                solara.Button("Cancel", on_click=lambda: set_active(False), elevation=0)
                solara.Button(
                    "Add", color="success", on_click=_add_button_clicked, elevation=0
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
        print(students)

    def _create_class_callback():
        BASE_API.create_new_class("Test Class Creation")
        _retrieve_classes()

    with solara.Row(classes=["fill-height"]):
        with rv.Col(cols=12):
            with rv.Row(class_="pa-0 mb-8 mx-0"):
                solara.Text("Manage Classes", classes=["display-1"])
                rv.Spacer()

                solara.Button(
                    "Create",
                    elevation=0,
                    on_click=_create_class_callback,
                    color="success",
                ),

            classes_table = rv.DataTable(
                items=data,
                # single_select=False,
                # show_select=True,
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
                        "variable": "y",
                        "children": [
                            rv.Html(
                                tag="td",
                                attributes={"colspan": 5},
                                children=[
                                    rv.DataTable(
                                        items=stu_data,
                                        headers=[
                                            {
                                                "text": "Name",
                                                "align": "start",
                                                "value": "name",
                                            },
                                            {"text": "Email", "value": "email"},
                                        ],
                                    ),
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
