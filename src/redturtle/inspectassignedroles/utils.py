from zope.interface.interfaces import IInterface
from ZPublisher.Iterators import IStreamIterator
from zope.interface import implements
import shutil
import os


class FileStreamIterator(object):
    """Simple stream iterator to allow efficient data streaming.
    """

    # Stupid workaround for the fact that on Zope < 2.12, we don't have
    # a real interface
    if IInterface.providedBy(IStreamIterator):
        implements(IStreamIterator)
    else:
        __implements__ = (IStreamIterator,)

    def __init__(self, path, size=None, chunk=1 << 16):
        """Consume data (a str) into a temporary file and prepare streaming.
        size is the length of the data. If not given, the length of the data
        string is used.
        chunk is the chunk size for the iterator
        """
        self.path = path
        self.file = open(path)
        self.file.seek(0)
        self.size = os.stat(path).st_size
        self.chunk = chunk

    def __iter__(self):
        return self

    def next(self):
        data = self.file.read(self.chunk)
        if not data:
            self.file.close()
            raise StopIteration
        return data

    def __len__(self):
        return self.size


class EphemeralStreamIterator(FileStreamIterator):
    """File and maybe its parent directory is deleted when readed"""

    def __init__(self, path, size=None, chunk=1 << 16,
                 delete_parent=False, delete_grand_parent=False):
        FileStreamIterator.__init__(self, path, size, chunk)
        self.delete_parent = delete_parent
        self.delete_grand_parent = delete_grand_parent

    def next(self):
        try:
            return FileStreamIterator.next(self)
        except:
            #  os.unlink(self.path)
            if self.delete_parent:
                shutil.rmtree(os.path.dirname(self.path))
            if self.delete_grand_parent:
                shutil.rmtree(os.path.dirname(os.path.dirname(self.path)))
            raise
