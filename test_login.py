from database.auth_manager import (
    register_user,
    login_user
)

print(
    register_user(
        "anshika",
        "1234"
    )
)

print(
    login_user(
        "anshika",
        "1234"
    )
)