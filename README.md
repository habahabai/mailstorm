# mailstorm Service

![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/habahabai/mailstorm/total?style=plastic)

**mailstorm** is a service designed for educational purposes, providing tools for email bombing and related functionalities. It is intended for security researchers and penetration testers to understand email server resilience and perform stress tests on email infrastructure.

## Access Methods

The mailstorm service can be accessed through various interfaces, offering flexibility and convenience:

### 1. Telegram Bot

Access the mailstorm service directly through our Telegram bot. This provides a convenient way to interact with the service from your mobile device or any Telegram client.

**Telegram Bot Username:** [@mailstorm_emailbomber_bot](https://t.me/mailstorm_emailbomber_bot)

### 2. Discord Server

Join our community on Discord to connect with other users, get support.

**Discord Invite Link:** [https://discord.gg/TNeDd7jsuh](https://discord.gg/TNeDd7jsuh)

### 3. mailstorm Desktop Application

This is a desktop application that provides a secure and isolated environment for accessing the mailstorm web application, which is hosted on the Tor network. It bundles a Tor client to ensure all traffic to the service is routed anonymously.

**Features of the Desktop Application:**
*   Direct access to the "mailstorm" service via a dedicated webview.
*   Built-in Tor integration for anonymous access.
*   User-friendly interface for specifying target email addresses and the number of emails to send.
*   Real-time display of email sending progress.

**Prerequisites (for Desktop Application):**
*   Windows operating system.
*   The application will automatically attempt to install the "Microsoft Edge WebView2 runtime" if it is not already installed.

### Download

You can download the compiled executable for Windows from the following link:

[Download main.exe](https://github.com/habahabai/mailstorm/releases/download/v0.1/main.exe)

### Building from Source

To build the application from source, follow these steps:

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/habahabai/mailstorm.git
    cd mailstorm
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    # source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Run the build script:**
    ```sh
    build.bat
    ```
    This will create a standalone executable file in the `dist` directory.

### Running from Source (Without Building)

If you want to run the application directly from the source code without compiling it, follow steps 1-3 from the "Building from Source" section and then run:
```sh
python main.py
```

## Disclaimer

This tool is for educational purposes only. The developers of this tool are not responsible for any misuse of this tool. It is the user's responsibility to use this tool in a responsible and ethical manner.
