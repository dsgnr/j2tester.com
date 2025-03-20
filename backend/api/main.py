"""
The j2tester.com app. 
"""

import pathlib

import tomli
from app.routes.admin import health
from app.routes.render import render_template
from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin


def _get_project_meta():
    """Parse the pyproject.toml file to retrieve project information"""
    with open(
        f"{pathlib.Path(__file__).parent.resolve().parent}/pyproject.toml", mode="rb"
    ) as pyproject:
        return tomli.load(pyproject)["tool"]["poetry"]


project_meta = _get_project_meta()

app = Litestar(
    route_handlers=[render_template, health],
    openapi_config=OpenAPIConfig(
        title=project_meta["name"],
        description=project_meta["description"],
        version=project_meta["version"],
        render_plugins=[ScalarRenderPlugin()],
        path="/docs",
        use_handler_docstrings=True,
    ),
    cors_config=CORSConfig(allow_origins=["*"]),
)

if __name__ == "__main__":
    # Third Party
    import uvicorn

    uvicorn.run(app)
