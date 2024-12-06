from typing import Optional
import solara
from solara.alias import rv

from ...utils import IMG_PATH


tags = ["TEMPO", "climate", "comets", "data science", "eclipse", "milky way",
        "nebula", "nova", "supernova"]


stories = [
    {
        "name": "Hubble Data Story",
        "description": """
            The Hubble Data Story (HubbleDS) is the first prototype 
            story under development by the CosmicDS team. In the 
            HubbleDS, learners will use real astronomical data to 
            answer questions like, “Has the universe always existed? 
            If not, how long ago did it form?”""",
        "image_filename": "hubbleds.avif",
        "url": "https://www.cosmicds.cfa.harvard.edu/hubbleds",
        "tags": ["data science"],
    },
    {
        "name": "Blaze Star Nova",
        "description": """
            Any day now, a new star* will appear in our night sky within the constellation Corona Borealis.
            In this Blaze Star Nova Data Story, we’ll show you just where in the sky to look for it when the time comes!
            Also learn what we expect it to look like and what causes novas.

            *Spoiler alert, novas are not actually new stars!
            A nova appears when a fainter star becomes so bright it seems like a new star has come out of nowhere.""",
        "image_filename": "blaze-star-nova.avif",
        "url": "https://projects.cosmicds.cfa.harvard.edu/blaze-star-nova/",
        "tags": ["nova"],
    },
    {
        "name": "TEMPO Lite",
        "description": """
            The TEMPO (Tropospheric Emissions: Monitoring Pollution) mission aims to monitor pollution with more regularity 
            and precision than ever before. In this interactive, we present map-based examples of TEMPO tropospheric 
            nitrogen dioxide data which highlight the satellite's capabilities. A future TEMPO DS will also allow linking 
            of map data to time graphs.
        """,
        "image_filename": "tempo-lite.avif",
        "url": "https://projects.cosmicds.cfa.harvard.edu/tempo-lite/",
        "tags": ["TEMPO", "climate"],
    },
    {
        "name": "Solar Eclipse",
        "description": """
            On April 8, 2024, North America was treated to an awe-inspiring total eclipse. This interactive lets you explore the April total eclipse from different locations!

            For educators, take a look at the [Educator Guide](https://bit.ly/cosmicds-eclipse-2024-educator-guide)

            [YouTube short intro](https://tinyurl.com/CosmicDS-eclipse-24-intro)
        """,
        "image_filename": "solar-eclipse-2024.avif",
        "url": "https://projects.cosmicds.cfa.harvard.edu/solar-eclipse-2024/",
        "tags": ["eclipse"],
    },
    {
        "name": "RadWave in Motion",
        "description": """
            The RadWave is made up of gas, dust, and stars loosely connected in a wave-like shape. 
            It is so huge and so close to us that earlier scientists did not see that these parts were all connected.
            
            Learn more about the discovery of the RadWave here!
        """,
        "image_filename": "radwave-in-motion.avif",
        "url": "https://projects.cosmicds.cfa.harvard.edu/radwave-in-motion/",
        "tags": ["milky way"],
    },
    {
        "name": "JWST Brick",
        "description": """
            “The Brick” is possibly the densest, most massive dark cloud in the Milky Way Galaxy!
            Explore what it looks like in JWST images taken by astronomer Adam Ginsburg and team, and learn how different
            infrared “colors” help scientists understand the physics within The Brick and visualize its structure.
        """,
        "image_filename": "jwst-brick.avif",
        "url": "https://projects.cosmicds.cfa.harvard.edu/jwst-brick/",
        "tags": ["milky way"],
    },
    {
        "name": "Carina Nebula",
        "description": """
            Explore where well-known HST and JWST images of the Carina Nebula are situated within a larger cloud of stars, dust, and gas. 
            Cross-fade between the two images to compare what visible vs. infrared wavelength observations can teach us about star formation.
            View a 1-minute video sharing scientific highlights!
        """,
        "image_filename": "carina-nebula.avif",
        "url": "https://projects.cosmicds.cfa.harvard.edu/carina/",
        "tags": ["nebula"],
    },
    {
        "name": "Pinwheel Supernova",
        "description": """
            See a new supernova burst onto the scene in the Pinwheel Galaxy 200 million light years away! 
            Learn how astronomers use data to determine what caused this supernova, discovered by Koichi Itagaki.

            Featuring images and data from MicroObservatory processed by Martin Fowler.
        """,
        "image_filename": "pinwheel-supernova.avif",
        "url": "https://projects.cosmicds.cfa.harvard.edu/pinwheel-supernova/",
        "tags": ["supernova"],
    },
    {
        "name": "Green Comet",
        "description": """
            Follow the path of Comet ZTF — a.k.a. the “Green Comet" — through the sky and find out why it's 
            green and discover why comet tails point where they do!

            This data story features images from astro-photographer Gerald Rehmann.
        """,
        "image_filename": "green-comet.avif",
        "url": "https://projects.cosmicds.cfa.harvard.edu/green-comet/",
        "tags": ["comets"],
    },
    {
        "name": "Annular Eclipse",
        "description": """
            On October 14, 2023, North, Central, and South America were treated to a beautiful annular eclipse.

            This interactive lets you explore the October "Ring of Fire" eclipse from different locations!
        """,
        "image_filename": "annular-eclipse-2023.avif",
        "url": "https://projects.cosmicds.cfa.harvard.edu/annular-eclipse-2023/",
        "tags": ["eclipse"],
    }
]


@solara.component
def StoryCard(
        name: str,
        description: str,
        image_filename: str,
        url: str,
        subtitle: Optional[str] = None,
        **kwargs
    ):
    image_url = str(IMG_PATH / "stories" / image_filename)
    with rv.Card(max_width=600, class_="mx-auto", style_="height: 100%") as story_card:
        link_attributes = {"href": url, "target": "_blank", "rel": "noopener noreferrer"}
        with rv.Html(tag="a", attributes=link_attributes):
            rv.Img(
                class_="white--text align-end",
                height="275px",
                src=image_url,
            )

        with rv.CardTitle():
            solara.Text(name)

        if subtitle:
            with rv.CardSubtitle():
                solara.Text(subtitle)

        # The card actions + button has a fixed height
        with rv.CardText(style_="padding-bottom: 52px"):
            solara.Markdown(description)
        
        with rv.CardActions():
            rv.Btn(
                children=["View"],
                elevation=0,
                color="primary",
                attributes=link_attributes,
                absolute=True,
                bottom=True,
            )
            # rv.Btn(children=["Details"], color="orange")
            # rv.Spacer()
            # solara.HTML("div",
            #             unsafe_innerHTML="<a href='https://cosmicds.2i2c.cloud/hub/user-redirect/hubble/'>Create</a>")

    return story_card


@solara.component
def Page():

    selected, set_selected = solara.use_state([])

    with rv.ItemGroup() as main:
        solara.Div("Data Stories", classes=["display-1", "mb-8"])
        with rv.ChipGroup(multiple=True,
                          v_model=selected,
                          on_v_model=set_selected,
                          active_class="primary--text"):
            for tag in tags:
                rv.Chip(value=tag, children=[tag])
        with solara.ColumnsResponsive([4]):
            for story in stories:
                if (not selected) or any(tag in selected for tag in story.get("tags", [])):
                    StoryCard(**story)

    return main
