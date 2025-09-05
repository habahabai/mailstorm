# Backend Integration

## Introduction

This document provides a detailed overview of the backend integration of the mailstorm Desktop application. The application is designed to be a client for the mailstorm web application, which is hosted on the Tor network. This document will explore the nature of this client-server relationship, the specifics of the backend, and the technical details of the integration.

Unlike many desktop applications that have a dedicated backend API (e.g., a REST API), the mailstorm Desktop application does not have a traditional backend in this sense. Instead, its "backend" is a full-fledged web application that is designed to be interacted with through a web browser. The desktop application, therefore, acts as a specialized web browser, providing a secure and convenient way to access the web application.

## The .onion Backend

The backend of the mailstorm service is a web application that is hosted as a Tor hidden service. This means that it is only accessible through the Tor network, and its IP address is not publicly known. The address of the backend is `http://imux3xyaclb655flrnkmvudyt4k3m37tw437geyvhlrg4e75flhvb5yd.onion`.

### What is a Tor Hidden Service?

A Tor hidden service is a service that can be accessed only through the Tor network. The main advantage of a hidden service is that it is difficult to determine who is running the service and where it is located. This is because all traffic to and from the hidden service is routed through the Tor network, which is designed to anonymize the source and destination of the traffic.

This is a crucial aspect of the mailstorm service, as it provides a layer of anonymity for both the users of the service and the operators of the service. It also makes the service more resilient to censorship and takedown attempts.

### The Web Application

The web application itself is a standard web application, likely built with a common web framework (e.g., Python/Django, Node.js/Express, etc.). It is responsible for all the core logic of the mailstorm service, including:

*   **User Interface:** The web application provides the user interface that is displayed in the desktop application's webview window. This includes the forms for entering the access key, the target email address, and the number of emails to send.
*   **User Authentication:** The web application may have a system for user authentication, although the user's description suggests a simple access key system.
*   **Email Bombing Logic:** The core logic for sending the emails resides on the server. When a user submits the form, the web application's backend code is responsible for initiating the email sending process.
*   **Status Updates:** The web application provides real-time status updates on the progress of the email bombing. This is likely implemented using WebSockets or a similar technology that allows the server to push updates to the client.

## Webview Integration

The desktop application uses a webview component to display the web application. The webview component is essentially an embedded web browser. It is a native GUI component that can be embedded in a desktop application, and it is capable of rendering web content (HTML, CSS, JavaScript) just like a regular web browser.

### The Role of `pywebview`

The `pywebview` library is a Python wrapper around the native webview components of the underlying operating system. On Windows, it uses the WebView2 runtime, which is based on the Microsoft Edge (Chromium) rendering engine.

The desktop application uses `pywebview` to:

1.  Create a window to host the webview component.
2.  Load the .onion URL into the webview.
3.  Configure the webview to use the Tor proxy.

### Sandboxing and Isolation

The webview component provides a degree of sandboxing and isolation. The web content is rendered in a separate process from the main application process. This helps to prevent malicious web content from compromising the desktop application itself.

However, the level of sandboxing is not as strong as in a modern web browser like Chrome or Firefox. Therefore, it is still important to be cautious about the websites that are loaded into the webview.

In the case of the mailstorm application, the webview is only used to load a single, known .onion site. This significantly reduces the risk of loading malicious content.

## Communication Protocol

The communication between the desktop application and the backend web application is done using the standard HTTP protocol. However, all of this traffic is routed through the Tor network.

Here is a breakdown of the communication flow:

1.  The webview component in the desktop application makes an HTTP request to the .onion address.
2.  The request is sent to the local Tor client, which is listening on a SOCKS5 proxy.
3.  The Tor client encrypts the request and sends it into the Tor network.
4.  The request is routed through a series of Tor relays until it reaches the hidden service.
5.  The web application receives the request, processes it, and sends an HTTP response back.
6.  The response is sent back through the Tor network to the desktop application's Tor client.
7.  The Tor client forwards the response to the webview component.
8.  The webview component renders the response and displays it to the user.

## Limitations of the Integration

The current integration model has some limitations:

*   **No Direct API Access:** The desktop application does not have direct access to the backend's functionality through a structured API. It can only interact with the backend by rendering the web interface and simulating user input (although the current implementation does not do this).
*   **Limited Control over the Backend:** The desktop application has no control over the backend. It is simply a client that accesses the backend. If the backend is down or changes its URL, the desktop application will no longer work.
*   **Dependency on the Web Interface:** The desktop application is tightly coupled to the web interface of the backend. If the web interface changes, the desktop application may no longer be able to interact with it correctly.

Despite these limitations, this architecture is a simple and effective way to provide a desktop experience for a web application, especially when the web application is a hidden service that requires a Tor connection.

This concludes the detailed overview of the backend integration. For more information on the other components of the application, please refer to the other documents in this documentation.
