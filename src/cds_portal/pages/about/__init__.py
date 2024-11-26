import solara


@solara.component
def Page():

    with solara.Div(classes=['fill-height', 'px-4']) as main:
        with solara.Row(classes=['fill-height', 'px-4']):
            with solara.Column():
                solara.Text("A Brief History", classes=["display-1"])
                solara.Markdown(
                    """
        The Cosmic Data Stories (CosmicDS) project started in January 2021.
        Led by Harvard University's [Dr. Alyssa Goodman](team) 
        and [Dr. Pat Udomprasert](team), the project was funded 
        by the NASA Science Activation Program (SciAct), a community-based program to connect NASA 
        science with learners of all ages. Since then, they have produced several interactive [Data 
        Stories](data-stories), along with a comprehensive prototype for classroom use."""
                )
    
        with solara.Row():
            solara.Text("Objectives")

    return main
