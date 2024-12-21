#!/usr/bin/python3

import os
import subprocess
import sys
import re
import getpass

script_dest_path = "/usr/local/bin/gnome-libravatar.py"
service_file_path = "/etc/systemd/system/gnome-libravatar.service"
if os.geteuid() != 0:
    print("This script must be run with root privileges. Please run with 'sudo'.")
    sys.exit(1)


def get_logged_in_username():
    """
    Get the logged-in GNOME user from the system.

    :return: The logged-in username.
    """
    if "SUDO_USER" in os.environ:
        return os.environ["SUDO_USER"]
    else:
        return getpass.getuser()


username = get_logged_in_username()
icon_dest_path = f"/var/lib/AccountsService/icons/{username}"
user_data_path = f"/var/lib/AccountsService/users/{username}"


def remove_script():
    """Remove the script from /usr/local/bin/."""
    try:
        if os.path.exists(script_dest_path):
            os.remove(script_dest_path)
            print(f"Removed the script from {script_dest_path}")
        else:
            print(f"The script does not exist at {script_dest_path}.")
    except Exception as e:
        print(f"Error removing the script: {e}")
        raise


def remove_systemd_service():
    """Remove the systemd service file and disable it."""
    try:
        if os.path.exists(service_file_path):
            # Disable and stop the service before removing it
            subprocess.run(
                ["sudo", "systemctl", "stop", "gnome-libravatar.service"], check=True
            )
            subprocess.run(
                ["sudo", "systemctl", "disable", "gnome-libravatar.service"],
                check=True,
            )

            # Remove the systemd service file
            os.remove(service_file_path)
            print(f"Removed the systemd service file at {service_file_path}")
        else:
            print(f"The systemd service file does not exist at {service_file_path}.")
    except subprocess.CalledProcessError as e:
        print(f"Error stopping or disabling systemd service: {e}")
        raise e
    except Exception as e:
        print(f"Error removing systemd service: {e}")
        raise e


def remove_profile_icon():
    """Remove the GNOME profile icon and update the user profile file."""
    try:
        # Remove the icon file
        if os.path.exists(icon_dest_path):
            os.remove(icon_dest_path)
            print(f"Removed the profile icon from {icon_dest_path}")
        else:
            print(f"No profile icon found at {icon_dest_path}.")

        # Update the user profile file to remove the Icon entry
        if os.path.exists(user_data_path):
            with open(user_data_path, "rb") as user_file:
                content = user_file.read().decode()
                content_updated = re.sub(r"^Icon=.*\n", "", content, flags=re.M)

            with open(user_data_path, "wb") as user_file:
                user_file.write(content_updated.encode())
                print(f"Removed the Icon entry from {user_data_path}")
        else:
            print(f"No user data file found at {user_data_path}.")
    except Exception as e:
        print(f"Error removing profile icon: {e}")
        raise


if __name__ == "__main__":
    try:
        remove_profile_icon()
        remove_script()
        remove_systemd_service()
        print("Uninstallation completed successfully.")
    except Exception as e:
        print(f"Uninstallation failed: {e}")
