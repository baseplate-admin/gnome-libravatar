#!/usr/bin/python3

import os
import shutil
import subprocess
import sys
import getpass


if os.geteuid() != 0:
    print("This script must be run with root privileges. Please run with 'sudo'.")
    sys.exit(1)

script_name = "./src/__init__.py"
script_source_path = os.path.join(os.getcwd(), script_name)
script_dest_path = "/usr/local/bin/gnome-libravatar.py"
service_file_path = "/etc/systemd/system/gnome-libravatar.service"
while True:
    email = input("What is your Email: ")
    if email:
        break


def get_logged_in_username():
    """
    Get the logged-in GNOME user from the system.

    :return: The logged-in username.
    """
    if "SUDO_USER" in os.environ:
        return os.environ["SUDO_USER"]
    else:
        return getpass.getuser()


def move_script_to_bin():
    """Move the Python script to /usr/local/bin/."""
    try:
        if not os.path.exists("/usr/local/bin"):
            os.makedirs("/usr/local/bin")

        shutil.copy(script_source_path, script_dest_path)
        print(f"Moved {script_name} to {script_dest_path}")
        os.chmod(script_dest_path, 0o755)
    except Exception as e:
        print(f"Error moving the script: {e}")
        raise


def create_systemd_service():
    """Create the systemd service file."""
    service_content = f"""
[Unit]
Description=Change GNOME Profile Icon
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/bin/python3 {script_dest_path}
Type=oneshot
RemainAfterExit=true
Environment=DISPLAY=:0
User=root
Restart=on-failure
RestartSec=30s
ExecStartPre=/bin/rm -f /var/run/change_gnome_icon.done
ExecCondition=/bin/bash -c '! [ -e /var/run/change_gnome_icon.done ]'
ExecStartPost=/bin/touch /var/run/change_gnome_icon.done

[Install]
WantedBy=multi-user.target
"""
    try:
        with open(service_file_path, "w") as service_file:
            service_file.write(service_content)
        print(f"Created systemd service file at {service_file_path}")
    except Exception as e:
        print(f"Error creating systemd service file: {e}")
        raise


def enable_and_start_service():
    """Enable and start the systemd service."""
    try:
        subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
        subprocess.run(
            ["sudo", "systemctl", "enable", "gnome-libravatar.service"], check=True
        )
        subprocess.run(
            ["sudo", "systemctl", "start", "gnome-libravatar.service"], check=True
        )
        print("Systemd service enabled and started.")
    except subprocess.CalledProcessError as e:
        print(f"Error enabling or starting systemd service: {e}")
        raise


if __name__ == "__main__":
    try:
        move_script_to_bin()
        create_systemd_service()
        enable_and_start_service()
        print("Build process completed successfully.")
    except Exception as e:
        print(f"Build process failed: {e}")
