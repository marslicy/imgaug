
from threading import Lock

class LazyImport(object):
    """
    Import the named module on first use.

    Use the singleton pattern to support multi-threaded environments
    """
    def __init__(self, package_name, /, globals = None, as_=None):
        """
        :param package_name: the name of a package to import. e.g. 'sklea'
        """
        super(LazyImport, self).__init__()
        self.package_name = package_name
        self.lock = Lock()
        self.mod = None
        self.globals = globals
        self.as_ = as_

    def __getattr__(self, attr):

        if self.mod is None:
            with self.lock:
                import importlib
                # throws ModuleNotFoundError on first use
                self.mod = importlib.import_module(self.package_name)

                # replace the reference from the calling global namespace
                if self.globals is None:
                    import inspect
                    self.globals = inspect.stack()[-1].frame.f_globals

                if self.globals and self.as_:
                    self.globals[self.as_] = self.mod

        return getattr(self.mod, attr)

if __name__ == '__main__':
    np = LazyImport("numpy", as_='np')
    print(np.int32) # first will lazy import
    print(np.int32) # np is now actually numpy
