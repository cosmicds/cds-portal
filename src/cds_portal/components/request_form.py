import solara
from solara.alias import rv


@solara.component
def RequestForm(form_data: solara.Reactive, validation_message: solara.Reactive):
    def _update_form_data(new_data):
        form_data.set(
            {**new_data, "valid": all([x is True for y in rules.values() for x in y])}
        )

    rules = {
        "first_name": [
            len(form_data.value["first_name"]) > 2 or "Must be more than 2 characters"
        ],
        "last_name": [
            len(form_data.value["last_name"]) > 2 or "Must be more than 2 characters"
        ],
        "email": [
            (len(form_data.value["email"]) > 0 and "@" in form_data.value["email"])
            or "Must enter an email"
        ],
        "confirm_email": [
            form_data.value["email"] == form_data.value["confirm_email"]
            or "Emails must match"
        ],
        "institution": [
            len(form_data.value["institution"]) > 0 or "Must enter an school name"
        ],
    }

    with rv.Row(class_="pa-0 ma-0"):
        with rv.Col(cols=12, class_="pa-0 ma-0"):
            rv.TextField(
                v_model=form_data.value["first_name"],
                on_v_model=lambda x: _update_form_data(
                    {**form_data.value, "first_name": x}
                ),
                label="First name",
                rules=rules.get("first_name"),
                outlined=True,
                required=True,
            )
            rv.TextField(
                v_model=form_data.value["last_name"],
                on_v_model=lambda x: _update_form_data(
                    {**form_data.value, "last_name": x}
                ),
                label="Last name",
                rules=rules.get("last_name"),
                outlined=True,
                required=True,
            )
            rv.TextField(
                v_model=form_data.value["email"],
                on_v_model=lambda x: _update_form_data({**form_data.value, "email": x}),
                label="Email",
                rules=rules.get("email"),
                outlined=True,
                required=True,
            )
            rv.TextField(
                v_model=form_data.value["confirm_email"],
                on_v_model=lambda x: _update_form_data(
                    {**form_data.value, "confirm_email": x}
                ),
                label="Confirm email",
                rules=rules.get("confirm_email"),
                outlined=True,
                required=True,
            )
            rv.TextField(
                v_model=form_data.value["institution"],
                on_v_model=lambda x: _update_form_data(
                    {**form_data.value, "institution": x}
                ),
                label="Institution",
                rules=rules.get("institution"),
                outlined=True,
                required=True,
            )

            if validation_message.value:
                rv.Alert(
                    outlined=True,
                    dense=True,
                    type="error",
                    children=[f"{validation_message.value}"],
                )
