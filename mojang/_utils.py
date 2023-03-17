def _assert_valid_username(username: str) -> None:
    """Raises a ValueError if a username is considered invalid"""

    if len(username) < 3 or len(username) > 16:
        raise ValueError(
            "Invalid username. Username size must be between 3 and 16 characters"
        )

    if not username.isascii():
        raise ValueError("Invalid username. Username contains invalid characters")
