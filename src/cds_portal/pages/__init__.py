from pathlib import Path

import solara
from solara.alias import rv
from ..layout import Layout

IMG_PATH = Path("static") / "public" / "images"


@solara.component
def Page():

    with solara.Row(classes=['fill-height', 'px-4']) as main:
        with solara.Columns([8, 4]):
            with solara.Column():
                solara.Text("Our Mission", classes=["display-1"])
                solara.Markdown(
                    """
    The world is fast-becoming a place driven by data.  To address dire shortages 
    of data-competency in the workforce, industry leaders are calling for 
    educational pathways that teach people how to interact with data.  The Cosmic 
    Data Stories (CosmicDS) project promotes public understanding of data science 
    through engaging, interactive data stories.

    The project facilitates connections between astronomers who want to tell the 
    story of a discovery and learners who can interrogate the data behind the 
    story on their own, using easy-to-use but powerful data science and 
    visualization techniques."""
                )

            with solara.Column():
                with rv.Card(flat=True, outlined=True):
                    with rv.CardTitle():
                        solara.Text("Getting Started")

                    with rv.ExpansionPanels(flat=True):
                        with rv.ExpansionPanel():
                            with rv.ExpansionPanelHeader():
                                solara.Text("Why create an account?")

                            with rv.ExpansionPanelContent():
                                solara.Markdown("""
In Cosmic Data Stories, students collect and analyze their own astronomy data. 
Students’ measurements are stored anonymously in the CosmicDS database. Creating an account will:

- Associate student data with their class cohort.
- Allow students to view their results within the context of their class’s dataset and the full participant dataset.
- Keep track of students’ place within the data story if they aren’t able to finish the story within one class period
""")
                        with rv.ExpansionPanel():
                            with rv.ExpansionPanelHeader():
                                solara.Text("How do accounts work?")

                            with rv.ExpansionPanelContent():
                                solara.Markdown("""
Educators complete a brief form to receive a CosmicDS educator key by email.

Educators and Students access the CosmicDS portal and Data Story app by logging 
on through the OAuth authentication service. You can use credentials from 
common services like gmail or microsoft.

Educators enter their educator key to create classroom keys that associates 
students’ accounts with you and their classmates.

""")
                        with rv.ExpansionPanel():
                            with rv.ExpansionPanelHeader():
                                solara.Text("Privacy Policy")

                            with rv.ExpansionPanelContent():
                                solara.Markdown("""
Educator contact information is stored according to 
<link to Harvard privacy policy>. Used for …

Student contact information is anonymized by …
""")

    return main