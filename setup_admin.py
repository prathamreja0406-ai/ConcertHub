
import getpass

from app.database import initialize_database
from app.auth import register_user


def setup_admin():

    print("\n" + "=" * 60)
    print("              🔐 CONCERTHUB ADMIN SETUP")
    print("=" * 60)

    name = input("Admin Name  : ").strip()
    email = input("Admin Email : ").strip()

    password = getpass.getpass(
        "Admin Password : "
    )

    confirm_password = getpass.getpass(
        "Confirm Password : "
    )

    if password != confirm_password:
        print("\n✗ Passwords do not match.")
        return

    success, message = register_user(
        name,
        email,
        password,
        role="admin"
    )

    if success:
        print("\n✓ Admin account created successfully.")
        print("✓ You can now login through the main application.")

    else:
        print(f"\n✗ {message}")


if __name__ == "__main__":

    initialize_database()
    setup_admin()
