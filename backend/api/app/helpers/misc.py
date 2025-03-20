"""
Helper methods for the API.
"""
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager

# Initialize Ansible components
loader = DataLoader()
inventory = InventoryManager(loader=loader, sources="localhost,")
variable_manager = VariableManager(loader=loader, inventory=inventory)
