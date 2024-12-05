import solara
from solara.alias import rv

from ..utils import IMG_PATH


@solara.component
def Hero():
    with rv.Parallax(src=str(IMG_PATH / "opo0006a.jpg")) as hero:
        with rv.Container(style_="max-width: 1200px"):
            with rv.Row():
                with rv.Col(cols=9):
                    # with rv.Container():
                    rv.Html(tag="div", children=["Cosmic Data Stories"],
                            class_="display-4",
                            style_="text-shadow: 1px 1px 8px black")
                    rv.Html(tag="div", children=[
                        "Interactive data stories designed by NASA "
                        "astronomers to inspire learners of all ages "
                        "to explore the universe."], class_="display-1",
                            style_="text-shadow: 1px 1px 8px black")

    return hero
