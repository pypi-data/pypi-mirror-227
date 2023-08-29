try:
    import __builtin__ as builtins
except ImportError:
    import builtins
import sys
import importlib.util
import logging

logger = logging.getLogger("minium")

_origimport = __import__


def lazy_import(name):
    """lazy import module"""
    spec = importlib.util.find_spec(name)
    if spec is None:
        logger.warning(f"can't find the {name!r} module")
        return None
    loader = importlib.util.LazyLoader(spec.loader)
    spec.loader = loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    loader.exec_module(module)
    return module

def _lazyimport(name, globals=None, locals=None, fromlist=None, level=0):
    logger.warning(f"_lazyimport({name}, {globals is None}, {locals is None}, {fromlist}, {level})")
    if fromlist or name == "_io":
        return _origimport(name, globals, locals, fromlist, level)
    return lazy_import(name)

def enable():
    "enable global demand-loading of modules"
    global is_enabled
    if not is_enabled:
        builtins.__import__ = _lazyimport
        is_enabled = True

def disable():
    "disable global demand-loading of modules"
    global is_enabled
    if is_enabled:
        builtins.__import__ = _origimport
        is_enabled = False

is_enabled = False
class enabled(object):
    def __enter__(self):
        global is_enabled
        self.old = is_enabled
        if not is_enabled:
            enable()
    def __exit__(self, *args):
        if not self.old:
            disable()

if __name__ == "__main__":
    pass