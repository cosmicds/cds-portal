import solara
from solara.alias import rv
from cds_portal.components.educator_dashboard import EducatorDashboard


@solara.component
def Page():
    with solara.Row(classes=["fill-height"]):
        with rv.Col(cols=12):
            solara.Div("Educator Dashboard", classes=["display-1", "mb-8"])

            EducatorDashboard()
