from interfaces.itransform import ITransform
from load.main import Load


class Transform(ITransform):
    def __init__(self):
        self._load = Load()

    def _validate_transformers(self) -> None:
        ...

    def transform(self) -> None:
        ...

    def flush(self) -> None:
        ...
