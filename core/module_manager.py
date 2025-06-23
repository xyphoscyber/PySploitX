import os
import importlib.util
from core.base_module import BaseModule

class ModuleManager:
    """
    Manages the discovery, loading, and interaction with modules.
    """
    def __init__(self, module_path='modules'):
        self.module_path = module_path
        self.modules = self._discover_modules()

    def _discover_modules(self):
        """
        Discovers all available modules in the specified path.
        """
        discovered_modules = {}
        for root, _, files in os.walk(self.module_path):
            for file in files:
                if file.endswith('.py') and not file.startswith('__'):
                    module_name = os.path.splitext(file)[0]
                    module_path = os.path.join(root, file)
                    
                    # Construct a unique module name for importlib
                    import_name = os.path.relpath(module_path, '.').replace(os.sep, '.')[:-3]

                    spec = importlib.util.spec_from_file_location(import_name, module_path)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        
                        for item in dir(module):
                            obj = getattr(module, item)
                            if isinstance(obj, type) and issubclass(obj, BaseModule) and obj is not BaseModule:
                                category = os.path.basename(root)
                                module_key = f"{category}/{module_name}"
                                discovered_modules[module_key] = obj()
        return discovered_modules

    def get_all_modules(self):
        """
        Returns a dictionary of all discovered modules.
        """
        return self.modules

    def get_module(self, name):
        """
        Retrieves a specific module by its name (e.g., 'recon/dns_lookup').
        """
        return self.modules.get(name)
