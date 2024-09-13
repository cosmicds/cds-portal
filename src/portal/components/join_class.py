import solara
from solara.alias import rv
from ..remote import BASE_API


@solara.component
def JoinClass(class_code: solara.Reactive, validation_message: solara.Reactive):
    with rv.Row(class_="pa-0 ma-0"):
        with rv.Col(cols=12, class_="pa-0 ma-0"):
            solara.Text(
                "Join a class by entering the class code given by your educator."
            )

            class_code_field = rv.TextField(
                label="Class Code",
                outlined=True,
                v_model=class_code.value,
                on_v_model=class_code.set,
                # value=class_code.value,
                class_="pt-2 mt-2",
                error=bool(validation_message.value),
                error_messages=(
                    [validation_message.value] if bool(validation_message.value) else []
                ),
            )

            solara.v.use_event(
                class_code_field,
                "focus",
                lambda *args: validation_message.set(""),
            )
