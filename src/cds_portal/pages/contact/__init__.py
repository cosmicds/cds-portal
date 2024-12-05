from email.mime.text import MIMEText
from os import getenv
from smtplib import SMTP_SSL, SMTPException

import solara
from solara.alias import rv


@solara.component
def ContactUsForm():

    name, set_name = solara.use_state("")
    email, set_email = solara.use_state("")
    message, set_message = solara.use_state("")
    sending, set_sending = solara.use_state(False)

    def _clear_inputs():
        set_name("")
        set_email("")
        set_message("")

    def _on_submit_clicked():
        from_email = getenv("EMAIL_USERNAME")
        from_password = getenv("EMAIL_PASSWORD")
        email_service = getenv("EMAIL_SERVICE")
        if not all((from_email, from_password, email_service)):
            return

        to_email = "cosmicds@cfa.harvard.edu"
        msg = MIMEText(message)
        msg["Subject"] = f"Message from {name}: {email}"
        msg["From"] = from_email
        msg["To"] = to_email

        with SMTP_SSL("smtp.gmail.com") as server:
            try:
                set_sending(True)
                server.login(from_email, from_password)
                server.sendmail(from_email, [to_email], msg.as_string())
            except SMTPException:
                return
            else:
                _clear_inputs()
            finally:
                set_sending(False)


    with solara.Card(style="width: 800px") as form:
        with solara.Column(gap="20px"):
            rv.Html(tag="h1", children=["Contact Us"])

            solara.InputTextArea(label="Name", value=name, on_value=set_name, rows=1, continuous_update=True)
            solara.InputTextArea(label="Email", value=email, on_value=set_email, rows=1, continuous_update=True)
            solara.InputTextArea(label="Type your message", value=message, on_value=set_message, continuous_update=True)

            solara.Button(label="Submit",
                          on_click=_on_submit_clicked,
                          disabled=not all((name, email, message, not sending)),
                          style_="width: 200px")

    return form 


@solara.component
def Page():
    with solara.Div(style="display: flex; justify-content: center;"):
        ContactUsForm()
