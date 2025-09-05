# Application Architecture

## Introduction

This document provides a detailed overview of the architecture of the mailstorm Desktop application. The application is designed to be a simple and lightweight wrapper around the mailstorm web application, which is hosted on the Tor network. The primary goal of the architecture is to provide a secure and isolated environment for accessing the web application, without requiring the user to manually configure a Tor client or a special browser.

The architecture is based on a client-server model, where the mailstorm Desktop application acts as the client and the mailstorm web application acts as the server. However, the client itself is a self-contained desktop application that bundles a Tor client and a webview component. This allows the application to be distributed as a single executable file, without any external dependencies other than the WebView2 runtime on Windows.

## Component Breakdown

The application is composed of the following key components:

*   **Main Application (`main.py`):** This is the entry point of the application. It is a Python script that is responsible for orchestrating the other components of the application. It is responsible for:
    *   Checking for the presence of the WebView2 runtime and triggering the installation if it is missing.
    *   Launching and managing the Tor client process.
    *   Creating and managing the webview window.
    *   Configuring the webview to use the Tor proxy.
    *   Terminating the Tor client process when the application exits.

*   **Tor Client:** The application bundles a pre-configured Tor client. The Tor client is responsible for connecting to the Tor network and providing a SOCKS5 proxy that can be used by the webview component to access the .onion website. The Tor client is launched as a background process by the main application, and it is automatically terminated when the application exits.

*   **Webview Component (`pywebview`):** The application uses the `pywebview` library to create a lightweight, cross-platform webview window. The webview window is used to display the mailstorm web application. The webview component is configured to use the Tor SOCKS5 proxy, which ensures that all traffic to and from the web application is routed through the Tor network.

*   **WebView2 Runtime (Windows only):** On Windows, `pywebview` uses the Microsoft Edge WebView2 runtime to render web content. The WebView2 runtime is a prerequisite for the application to run on Windows. The main application includes logic to automatically download and install the WebView2 runtime if it is not already present on the system.

*   **mailstorm Web Application (.onion site):** This is the backend component of the system. It is a web application that is hosted on the Tor network and is accessible via a .onion address. The web application is responsible for the core functionality of the mailstorm service, including user authentication, email bombing, and status reporting. The desktop application is simply a client for this web application.

## Architectural Diagram

```
+----------------------------------------------------+
|                 User's Desktop                     |
|                                                    |
|  +-----------------------------------------------+ |
|  |           mailstorm Desktop App               | |
|  |                                               | |
|  |  +-----------------+      +-----------------+ | |
|  |  |   main.py       |----->|   Tor Client    | | |
|  |  | (Orchestrator)  |      | (Background     | | |
|  |  +-----------------+      |  Process)       | | |
|  |          |                +-----------------+ | |
|  |          |                        ^             | |
|  |          |                        |             | |
|  |          v                        | SOCKS5      | |
|  |  +-----------------+      +-------+-------+ | |
|  |  | pywebview       |----->| WebView2      | | |
|  |  | (Window)        |      | (Renderer)    | | |
|  |  +-----------------+      +---------------+ | |
|  |          |                                  | |
|  +----------|----------------------------------+ |
|             |                                    |
+-------------|------------------------------------+
              | HTTP over Tor
              v
+----------------------------------------------------+
|                 Tor Network                        |
+----------------------------------------------------+
              |
              v
+----------------------------------------------------+
|          mailstorm Web Application                 |
|             (.onion site)                          |
+----------------------------------------------------+
```

## Execution Flow

The following steps describe the execution flow of the application:

1.  The user launches the mailstorm Desktop application.
2.  The `main.py` script is executed.
3.  The script checks if the WebView2 runtime is installed (on Windows). If not, it downloads and installs it, and then prompts the user to relaunch the application.
4.  The `main.py` script launches the bundled Tor client as a background process.
5.  The script waits for the Tor client to bootstrap and establish a connection to the Tor network.
6.  Once the Tor client is ready, the `main.py` script creates a `pywebview` window.
7.  The script configures the webview to use the Tor SOCKS5 proxy (at `socks5://127.0.0.1:9050`).
8.  The webview window loads the mailstorm .onion website.
9.  The user interacts with the mailstorm web application through the webview window.
10. When the user closes the webview window, the `main.py` script terminates the Tor client process.
11. The application exits.

## Security Considerations

The architecture is designed with security in mind. The following are some of the key security features of the application:

*   **Tor-only Traffic:** All traffic to and from the web application is routed through the Tor network. This helps to anonymize the user's IP address and to protect their privacy.
*   **Process Isolation:** The Tor client runs as a separate process from the main application. This helps to isolate the Tor client from the rest of the application and to prevent it from being compromised.
*   **No Data Storage:** The desktop application does not store any user data locally. All data is stored on the mailstorm web application.

This architecture provides a reasonably secure environment for accessing the mailstorm web application. However, it is important to note that no system is 100% secure. Users should still be cautious when using the application and should not enter any sensitive information into the web application.
