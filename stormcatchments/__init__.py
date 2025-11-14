__version__ = "0.4.1"

# Lazy imports - only import when actually used
def __getattr__(name):
    if name == "constants":
        from . import constants
        return constants
    elif name == "delineate":
        from . import delineate
        return delineate
    elif name == "network":
        from . import network
        return network
    elif name == "terrain":
        from . import terrain
        return terrain
    elif name == "topology":
        from . import topology
        return topology
    elif name == "Network":
        from .network import Network
        return Network
    elif name == "Delineate":
        from .delineate import Delineate
        return Delineate
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
