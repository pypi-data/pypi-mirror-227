import tempfile

from trendup_utils.temp_file import TempFile


class TempFileImpl(TempFile):

    def make_temp_file_path(self) -> str:
        return tempfile.mktemp()
