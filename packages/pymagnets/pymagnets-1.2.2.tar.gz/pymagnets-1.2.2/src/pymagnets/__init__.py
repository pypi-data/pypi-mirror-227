
try:
    from ._version import version as __version__
    from ._version import version_tuple as __version_tuple__
except ImportError:
    __version__ = "unknown version"
    __version_tuple__ = (0, 0, "unknown version")


from . import model # imports the model library from the pymagnets package
from . import material # imports the material library from the pymagnets package
from . import magnet # imports the magnet library from the pymagnets package