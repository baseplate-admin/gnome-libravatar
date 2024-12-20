# Gnome-Libravatar

This project allows you to automatically download a user's avatar from Libravatar and set it as their GNOME profile icon. The script downloads the avatar using the email address provided, then updates the user's GNOME profile to set the downloaded image as their profile picture.

Additionally, this project configures a `systemd` service to automatically change the profile icon once after a reboot.

## Features

-   Downloads a user's avatar from Libravatar based on their email address.
-   Changes the GNOME profile icon to the downloaded avatar.
-   Automatically sets up a `systemd` service that runs the script once after every system reboot.
-   The script runs as the currently logged-in user.

## Prerequisites

-   **GNOME-based system**
-   **Python 3** installed.
-   **sudo/root permissions** to install and enable the systemd service.

## Installation

1.  **Clone or Download the Project**

    Clone this repository or download the files to your local machine.

    ```bash

    git clone https://github.com/baseplate-admin/gnome-libravatar.git
    cd gnome-libravatar

    ```

2.  **Usage**

    Run:

    ```bash
    sudo python install.py
    ```

    After you run the install.py script, the systemd service will be set up to automatically run the `gnome-libravatar.py` script once after each reboot.

    To disable the service from running on reboot, you can stop and disable it using:

    ```bash
    sudo systemctl stop gnome-libravatar.service
    sudo systemctl disable gnome-libravatar.service
    ```

## Uninstall

To undo any changes made by this project run

```bash
sudo python uninstall.py
```

## How It Works

-   **Downloading the Avatar:** The main script uses the email address to generate a hash and fetch the avatar from Libravatar. The avatar is then stored in memory as a temporary file.

-   **Changing the Profile Icon:** The script updates the GNOME profile icon for the user, by copying the avatar image to the appropriate location and modifying the AccountsService user file to point to the new icon.

-   **Systemd Service:** The script creates a systemd service that is configured to run once after a system reboot. The service is set up with the current logged-in user, ensuring the script runs with the user's environment.

## License

This project is licensed under the AGPL-v3 License - see the LICENSE file for details.

## Contributing

Feel free to fork the repository, submit issues, and create pull requests. Contributions are welcome!
