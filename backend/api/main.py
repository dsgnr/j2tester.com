from litestar import Litestar, post
from litestar.config.cors import CORSConfig
from pydantic import BaseModel, Field
from typing import Optional
import yaml
from ansible.template import Templar
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader

# Define request model with variables as an optional string (YAML or JSON)
class TemplateRequest(BaseModel):
    template: str
    variables: Optional[str] = Field(default="")  # Can be empty, YAML, or JSON string

# Initialize Ansible components
loader = DataLoader()
inventory = InventoryManager(loader=loader, sources=[])
variable_manager = VariableManager(loader=loader, inventory=inventory)

@post("/render")
async def render_template(data: TemplateRequest) -> dict:
    try:
        # Convert YAML/JSON string to a dictionary
        if data.variables.strip():  # Only parse if not empty
            try:
                variables_dict = yaml.safe_load(data.variables)
                if not isinstance(variables_dict, dict):
                    raise ValueError("Variables must be a dictionary.")
            except yaml.YAMLError as e:
                return {"error": f"Invalid YAML format: {str(e)}"}
        else:
            variables_dict = {}  # Default to empty dict

        # Use Ansible templating
        templar = Templar(loader=loader, variables=variables_dict)
        rendered_output = templar.template(data.template)

        return {"rendered": rendered_output}
    except Exception as e:
        return {"error": str(e)}

# Enable CORS to allow frontend requests
cors_config = CORSConfig(allow_origins=["*"])  # Allow all origins

# Create the Litestar app with CORS middleware
app = Litestar([render_template], cors_config=cors_config)

if __name__ == "__main__":
    # Third Party
    import uvicorn

    uvicorn.run(app)
