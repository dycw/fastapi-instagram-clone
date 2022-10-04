from beartype import beartype


@beartype
def log(*, tag: str = "", message: str = "") -> None:
    with open("log.txt", mode="w+") as fh:
        _ = fh.write(f"{tag}: {message}\n")
