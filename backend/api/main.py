"""
The j2tester.com app. 
"""
from litestar import Litestar
from litestar.config.cors import CORSConfig

from app.routes.render import render_template
from app.routes.admin import health 

app = Litestar([render_template, health], cors_config=CORSConfig(allow_origins=["*"]))

if __name__ == "__main__":
    # Third Party
    import uvicorn

    uvicorn.run(app)
