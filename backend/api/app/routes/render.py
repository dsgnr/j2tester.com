"""
The API routes.
"""
from typing import Annotated

import yaml
from ansible.template import Templar
from litestar import MediaType, post
from litestar.params import Body
from litestar.status_codes import HTTP_200_OK

from app.helpers.misc import loader
from app.helpers.schemas import APIResponseSchema, TemplateRequest


@post(
    "/api/render",
    media_type=MediaType.JSON,
    status_code=HTTP_200_OK,
    sync_to_thread=True,
)
def render_template(
    data: Annotated[
        TemplateRequest,
        Body(title="Parse a Jinja2 template", description="Parses a Jinja2 template"),
    ]
) -> APIResponseSchema:
    """
    A `POST` endpoint to parse a Jinja2 template using the variables and template provided.
    """
    try:
        # Convert YAML/JSON string to a dictionary
        if data.variables:  # Only parse if not empty
            try:
                variables_dict = yaml.safe_load(data.variables.strip())
                if not isinstance(variables_dict, dict):
                    raise ValueError("Variables must be a dictionary.")
            except yaml.YAMLError as e:
                return APIResponseSchema(
                    error=True, msg=f"Invalid YAML format: {str(e)}"
                )
        else:
            variables_dict = {}  # Default to empty dict

        # Use Ansible templating
        templar = Templar(loader=loader, variables=variables_dict)
        rendered_output = templar.template(data.template)

        return APIResponseSchema(error=False, msg="success", results=rendered_output)
    except Exception as e:
        return APIResponseSchema(error=True, msg=str(e))
