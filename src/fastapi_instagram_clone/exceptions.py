from beartype import beartype


class StoryException(Exception):
    @beartype
    def __init__(self, name: str, /) -> None:
        super().__init__()
        self.name = name
