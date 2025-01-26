import solara
from ...remote import BASE_API
from solara.alias import rv
from ...components.educator_dashboard import EducatorDashboard


@solara.component
def Page():
    router = solara.use_router()
    url_params = {x.split("=")[0]: x.split("=")[1] for x in router.search.split("&")}

    classes_dict = BASE_API.load_educator_classes()
    educator_class_ids = [str(cls["id"]) for cls in classes_dict["classes"]]

    with solara.Row(classes=["fill-height"]):
        with rv.Col(cols=12):
            solara.Div("Educator Dashboard", classes=["display-1", "mb-8"])

            if url_params.get("id") not in educator_class_ids:
                solara.Markdown("You do not have access to this class.")
                return
            else:
                EducatorDashboard(url_params)
