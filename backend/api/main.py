"""
The j2tester.com app. 
"""

import pathlib

import tomli
from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.plugins import ScalarRenderPlugin
from litestar.plugins.prometheus import PrometheusConfig, PrometheusController

from app.routes.admin import health
from app.routes.render import render_template


def _get_project_meta():
    """Parse the pyproject.toml file to retrieve project information"""
    with open(
        f"{pathlib.Path(__file__).parent.resolve().parent}/pyproject.toml", mode="rb"
    ) as pyproject:
        return tomli.load(pyproject)["tool"]["poetry"]


project_meta = _get_project_meta()

prometheus_config = PrometheusConfig(
    app_name="api",
    prefix=project_meta["name"].split(".")[0].replace(" ", "_"),
    group_path=True,
    labels={
        "version": project_meta["version"],
    },
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5],
)

app = Litestar(
    route_handlers=[render_template, health, PrometheusController],
    middleware=[prometheus_config.middleware],
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
