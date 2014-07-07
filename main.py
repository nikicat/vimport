import threading
import sys
import collections
import time

def test():
    import pkg
    print(pkg.__path__, threading.current_thread().name, pkg.value)

def run(version):
    sys.path.append('rules/{}'.format(version))
    test()


class VersionedPath(collections.UserList):
    def __init__(self):
        self._orig = sys.path
        self._local = threading.local()

    @property
    def data(self):
        if not hasattr(self._local, 'data'):
            self._local.data = list(self._orig)
        return self._local.data


class VersionedModules(collections.UserDict):
    def __init__(self):
        self._local = threading.local()
        self._orig = sys.modules

    @property
    def data(self):
        if not hasattr(self._local, 'data'):
            self._local.data = dict(self._orig)
        return self._local.data


if __name__ == '__main__':
    sys.path = VersionedPath()
    sys.modules = VersionedModules()

    for v in ['v1', 'v2', 'v3']:
        thread = threading.Thread(target=run, args=(v,))
        thread.daemon = True
        thread.start()
    sys.path.append('rules/head')
    import pkg
    print(pkg.__path__, threading.current_thread().name, pkg.value)
    time.sleep(100)
