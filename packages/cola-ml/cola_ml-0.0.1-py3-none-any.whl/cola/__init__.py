__version__ = '0.1.0'
from cola.utils import import_from_all
from .ops import LinearOperator

__all__ = []
# for loader, module_name, is_pkg in  pkgutil.walk_packages(__path__):
import_from_all("fns", globals(), __all__, __name__)
import_from_all("annotations", globals(), __all__, __name__)
import_from_all("linalg", globals(), __all__, __name__)
import_from_all("utils", globals(), __all__, __name__)
import_from_all("decompositions", globals(), __all__, __name__)

__all__.append("LinearOperator")
# import_from_all("ops", globals(), __all__,__name__)
