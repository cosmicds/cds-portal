from collections import defaultdict
from datetime import datetime

import solara
from solara.alias import rv

from cds_portal.components.input import IntegerInput

from ...remote import BASE_API


# If we want to remove more characters in the future
# (or replace more with underscores)
# switch to using re.sub
def format_story_name(name: str):
    return name.lower().replace("'", "").replace(" ", "_")


@solara.component
def CreateClassDialog(on_create_clicked: callable = None):
    active, set_active = solara.use_state(False)  #
    text, set_text = solara.use_state("")
    stories, set_stories = solara.use_state("")
    expected_size, set_expected_size = solara.use_state(20)
    asynchronous, set_asynchronous = solara.use_state(False)
    expected_size_error = solara.use_reactive(False)

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
                    text=True,
                    children=["New"],
                    elevation=0,
                ),
            }
        ],
        max_width=600,
    ) as dialog:
        with rv.Card(outlined=True):
            rv.CardTitle(children=["Create a New Class"])

            with rv.CardText():
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

                IntegerInput(
                    label="Expected size",
                    value=expected_size,
                    on_value=set_expected_size,
                    on_error_change=expected_size_error.set,
                    continuous_update=True,
                    outlined=True,
                    hide_details="auto",
                    classes=["pt-2"],
                )

                solara.Checkbox(
                    label="Asynchronous class",
                    value=asynchronous,
                    on_value=set_asynchronous,
                )

            rv.Divider()

            with rv.CardActions():

                @solara.lab.computed
                def create_button_disabled():
                    print(expected_size_error)
                    return expected_size_error.value or (not (text and stories))

                def _add_button_clicked(*args):
                    on_create_clicked(
                        {
                            "name": f"{text}",
                            "stories": f"{', '.join(stories)}",
                            "expected_size": expected_size,
                            "asynchronous": asynchronous,
                            "story_name": format_story_name(stories),
                        }
                    )
                    set_active(False)

                rv.Spacer()

                solara.Button("Cancel", on_click=lambda: set_active(False), elevation=0)
                solara.Button(
                    "Create",
                    color="info",
                    on_click=_add_button_clicked,
                    elevation=0,
                    disabled=create_button_disabled.value,
                )

    return dialog


@solara.component
def DeleteClassDialog(disabled: bool, on_delete_clicked: callable = None):
    active, set_active = solara.use_state(False)

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
                    color="error",
                    disabled=disabled,
                    text=True,
                    children=[
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

            with rv.CardText():
                solara.Div("Are you sure you want to delete the selected class(es)?")

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
def ClassActionsDialog(disabled: bool, class_data: list[dict]):
    active, set_active = solara.use_state(False)
    message, set_message = solara.use_state("")
    message_color, set_message_color = solara.use_state("")

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
                    disabled=disabled,
                    text=True,
                    children=["Modify class"],
                    elevation=0,
                )
            }
        ],
        max_width=600,
    ):

        def _update_snackbar(message: str, color: str):
            set_message_color(color)
            set_message(message)

        def _reset_snackbar():
            set_message("")

        def close_dialog():
            set_active(False)
            _reset_snackbar()

        classes_by_story = defaultdict(list)
        for data in class_data:
            classes_by_story[data["story"]].append(data)

        with rv.Card(outlined=True):
            rv.CardTitle(children=["Modify Class"])

            with rv.CardText():
                solara.Div("From this dialog you can make any necessary changes to the selected classes")

            if "Hubble's Law" in classes_by_story:

                hubble_classes = classes_by_story["Hubble's Law"]

                override_statuses = [BASE_API.get_hubble_waiting_room_override(data["id"])["override_status"] for data in hubble_classes]
                all_overridden = all(override_statuses)

                def _on_override_button_pressed(*args):
                    failures = []
                    for data in hubble_classes:
                        class_id = data["id"]
                        response = BASE_API.set_hubble_waiting_room_override(class_id, True)
                        success = response.status_code in (200, 201)
                        if not success:
                            failures.append(class_id)

                    relevant_ids = failures if failures else [data["id"] for data in hubble_classes]
                    classes_string = "class" if len(relevant_ids) == 1 else "classes"
                    ids_string = ", ".join(str(cid) for cid in relevant_ids)
                    message = f"There was an error updating the waiting room status for {classes_string} {ids_string}" if failures else \
                              f"Updated waiting room status for {classes_string} {ids_string}"
                    color = "error" if failures else "success"

                    _update_snackbar(message=message, color=color)

                with rv.Container():
                    with rv.CardText():
                        solara.Text("Set the small class override for the selected classes. If a class already has the override set, there will be no effect.")
                    with solara.Row():
                        no_override_count = len(hubble_classes) - sum(override_statuses)
                        no_override_classes = "class" if no_override_count == 1 else "classes"
                        solara.Button(label=f"Set override",
                                      on_click=_on_override_button_pressed,
                                      disabled=all_overridden)
                        rv.Alert(children=[f"This will affect {no_override_count} {no_override_classes}"],
                                 color="info",
                                 outlined=True,
                                 dense=True)

                rv.Spacer()

                with rv.CardActions():
                    solara.Button("Cancel", on_click=close_dialog, elevation=0)

        rv.Snackbar(v_model=bool(message),
                    on_v_model=lambda *args: _reset_snackbar(),
                    color=message_color,
                    timeout=5000,
                    children=[message])


@solara.component
def Page():
    data = solara.use_reactive([])
    selected_rows = solara.use_reactive([])

    def _retrieve_classes():
        classes_dict = BASE_API.load_educator_classes()

        new_classes = [
            {
                "name": cls["name"],
                "date": datetime.fromisoformat(cls["created"].removesuffix("Z")).strftime("%m/%d/%Y"),
                "story": "Hubble's Law",
                "code": cls["code"],
                "id": cls["id"],
                "expected_size": cls["expected_size"],
                "small_class": cls["small_class"],
                "asynchronous": cls["asynchronous"],
            }
            for cls in classes_dict["classes"]
        ]

        data.set(new_classes)

    solara.use_effect(_retrieve_classes, [])

    def _create_class_callback(class_info):
        BASE_API.create_new_class(class_info)
        _retrieve_classes()

    def _delete_class_callback():
        for row in selected_rows.value:
            BASE_API.delete_class(row["code"])
        _retrieve_classes()

    with solara.Row(classes=["fill-height"]):
        with rv.Col(cols=12):
            solara.Div("Manage Classes", classes=["display-1", "mb-8"])

            with rv.Card(outlined=True, flat=True):
                with rv.Toolbar(flat=True, dense=True, class_="pa-0"):
                    with rv.ToolbarItems():
                        CreateClassDialog(_create_class_callback)
                        rv.Divider(vertical=True)
                        DeleteClassDialog(
                            len(selected_rows.value) == 0, _delete_class_callback
                        )
                        rv.Divider(vertical=True)
                        solara.Button(
                            "Dashboard",
                            color="info",
                            href=(
                                f"/educator-dashboard?id={selected_rows.value[0]['id']}"
                                if len(selected_rows.value) == 1
                                else "/educator-dashboard"
                            ),
                            elevation=0,
                            disabled=len(selected_rows.value) != 1,
                        )
                        ClassActionsDialog(
                            len(selected_rows.value) == 0, selected_rows.value
                        )

                rv.DataTable(
                    items=data.value,
                    single_select=False,
                    show_select=True,
                    v_model=selected_rows.value,
                    on_v_model=selected_rows.set,
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
                        {"text": "Expected size", "value": "expected_size"},
                        {"text": "Asynchronous", "value": "asynchronous"},
                    ]
                )
