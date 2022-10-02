from fastapi_instagram_clone import __version__


def test_main() -> None:
    assert isinstance(__version__, str)
