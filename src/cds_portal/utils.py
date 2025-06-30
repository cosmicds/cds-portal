from pathlib import Path


IMG_PATH = Path("static") / "public" / "images"

import solara
def use_router_search_params():
    router = solara.use_router()
    def get_param(param):
        return param.partition("=")[0], param.partition("=")[2]
    if router.search:
        search_params = router.search.split("&")
        if len(search_params) > 0:
            return {get_param(param)[0]: get_param(param)[1] for param in search_params}
    return {}