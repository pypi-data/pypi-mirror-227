from abc import abstractmethod


class TempFile:

    @abstractmethod
    def make_temp_file_path(self) -> str:
        pass
