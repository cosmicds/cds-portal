import solara
from .components.TeacherCodeInput import TeacherCodeEntry
from .components.Dashboard import Dashboard
from .components.SetClass import SetClass
from .components.StudentDataLoad import StudentNameLoad
from .components.ReportDownload import DownloadReport
import reacton.ipyvuetify as rv

from .database.class_report import Roster
from typing import cast

from .database.Query import QueryCosmicDSApi


from .components.RefreshClass import RefreshClass

from solara.lab import theme, ThemeToggle


@solara.component
def EducatorDashboard(url_params):
    query = QueryCosmicDSApi()
    show_dashboard, set_show_dashboard = solara.use_state(False)
    class_id_list = solara.use_reactive([int(url_params["id"])])
    class_id = solara.use_reactive(int(url_params["id"]))  # add class id here
    # if not show_dashboard:
    #     def callback():
    #         set_show_dashboard(True)
    #     TeacherCodeEntry(class_id_list, class_id, callback, query = query)
    #     return

    # print(" ================== main page ================== ")
    # for testing use
    # - 199 (test class for dashboard refresh)
    # - 195 (a full current class)
    # - 192 (an empty class)
    # - 188 (real spring beta class)
    # - 185 (testing spring beta class)
    # - 172 (old outdated class - should show stuff but probably incorrect)
    # - 170 (outdated class - should show nothing)

    roster = solara.use_reactive(
        cast(Roster, None), on_change=lambda x: print("roster changed")
    )
    student_names = solara.use_reactive(None)
    dashboard_names = solara.use_reactive(None)  # , on_change=on_change_names)
    first_run = solara.use_reactive(True)
    are_names_set = solara.use_reactive(False)

    story_name = "HubbleDS"

    # with solara.Columns([6, 3, 3], classes=["my-column"]):
    with rv.Row():
        with rv.Col(cols=8):
            SetClass(class_id, roster, first_run, class_id_list, query)

        with rv.Col(cols=2):
            StudentNameLoad(
                roster,
                student_names,
                names_set=are_names_set,
                on_update=dashboard_names.set,
            )

        with rv.Col(cols=2):
            DownloadReport(roster)

        RefreshClass(
            rate_minutes=20.0 / 60.0,
            roster=roster,
            student_names=dashboard_names.value,
            show_refresh_button=False,
            stop_start_button=False,
            refresh_button_text=None,
            # show button to manually refresh and to start/stop autorefresh. no text cuz icon_only is set
            refresh_button_color="primary",
            start_button_color="#777",
            stop_button_color="#ccc",
            icon_only=True,
        )

    Dashboard(roster, dashboard_names, add_names=dashboard_names.value is not None)

    # solara.DataFrame(df.value)
