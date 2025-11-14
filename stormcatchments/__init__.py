__version__ = "0.4.1"

# Lazy imports - only import when actually used
def __getattr__(name):
    """Lazy import modules on first access to speed up import time."""
    import importlib
    
    # Map of attribute names to module/class paths
    _lazy_imports = {
        "constants": "stormcatchments.constants",
        "delineate": "stormcatchments.delineate",
        "network": "stormcatchments.network",
        "terrain": "stormcatchments.terrain",
        "topology": "stormcatchments.topology",
        "Network": ("stormcatchments.network", "Network"),
        "Delineate": ("stormcatchments.delineate", "Delineate"),
    }
    
    if name in _lazy_imports:
        import_info = _lazy_imports[name]
        
        # Handle module imports
        if isinstance(import_info, str):
            module = importlib.import_module(import_info)
            # Cache it in globals to avoid reimporting
            globals()[name] = module
            return module
        
        # Handle class imports (tuple of module_path, class_name)
        else:
            module_path, class_name = import_info
            module = importlib.import_module(module_path)
            cls = getattr(module, class_name)
            # Cache it in globals
            globals()[name] = cls
            return cls
    
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
