from typing import Optional

import solara
from solara.alias import rv

from ...utils import IMG_PATH


def team_member_image_url(filename: str) -> str:
    return str(IMG_PATH / "team" / filename)


DEFAULT_IMAGE = "default.avif"


@solara.component
def TeamMember(
    name: str,
    title: str,
    image_filename: Optional[str],
):
    image_url = team_member_image_url(image_filename or DEFAULT_IMAGE)
    with rv.Card(class_="pb-2 ma-0", color="rgb(16, 42, 82)"):
        rv.Img(src=image_url, width="275px")
        solara.Div(children=[rv.Html(tag="h3", children=[name])])
        solara.Div(children=[title])


team_members = [
    {"name": "Alyssa Goodman", "title": "Principal Investigator", "image_filename": "Alyssa.avif"},
    {"name": "Patricia Udomprasert", "title": "Science Principal Investigator", "image_filename": "Pat.avif"},
    {"name": "Mary Dussault", "title": "Education Lead", "image_filename": "Mary.avif"},
    {"name": "Erika Wright", "title": "Education Specialist", "image_filename": "Erika.avif"},
    {"name": "John Lewis", "title": "Education & Software Engineer", "image_filename": "JohnL.avif"},
    {"name": "Jon Carifio", "title": "Software Engineer", "image_filename": "JonC.avif"},
    {"name": "Nick Earl", "title": "Software Engineer", "image_filename": "Nick.avif"},
    {"name": "Jonathan Foster", "title": "Software Engineer", "image_filename": "JonathanF.avif"},
    {"name": "Harry Houghton", "title": "Front End Developer", "image_filename": "Harry.avif"},
]

evaluation_members = [
    {"name": "Susan Sunbury", "title": "Evaluator", "image_filename": "Sue.avif"},
]

past_members = [
    {"name": "Anna Nolin", "title": "Web Admin & Graphics", "image_filename": "Anna.avif"},
    {"name": "Jack Hayes", "title": "2024 Intern", "image_filename": None},
    {"name": "Lily Nguyen", "title": "2023 Intern", "image_filename": "Lily.avif"},
    {"name": "Jody Blackwell", "title": "Web Admin", "image_filename": "Jody.avif"},
]

sections = [
    {"title": "Meet Our Team", "members": team_members},
    {"title": "Evaluation", "members": evaluation_members},
    {"title": "Past Members", "members": past_members},
]


@solara.component
def Page():
    with solara.Div() as main:
        for section in sections:
            rv.Html(tag="h2", children=[section["title"]])
            with solara.Row(
                    style="""
                        width: 100%;
                        flex-wrap: wrap;
                        background-color: transparent;
                        padding: 10px 0px;
                        row-gap: 25px;
                    """,
                gap="25px",
            ):
                for member in section["members"]:
                    TeamMember(**member)

    return main
