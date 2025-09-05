# Tor Integration

## Introduction

This document provides a comprehensive overview of the integration of The Onion Router (Tor) within the mailstorm Desktop application. The use of Tor is a fundamental aspect of this project, as it provides the necessary infrastructure to access the backend web application, which is hosted as a Tor hidden service. This document will delve into the technical details of how Tor is used, why it is essential, and the underlying principles of the Tor network.

## What is Tor?

Tor, which stands for "The Onion Router," is a free and open-source software that enables anonymous communication. It directs internet traffic through a free, worldwide, volunteer overlay network consisting of more than seven thousand relays to conceal a user's location and usage from anyone conducting network surveillance or traffic analysis. Using Tor makes it more difficult to trace internet activity to the user: this includes "visits to Web sites, online posts, instant messages, and other communication forms". Tor's intended use is to protect the personal privacy of its users, as well as their freedom and ability to conduct confidential communication by keeping their internet activities from being monitored.

### Onion Routing

Tor's name is an acronym for "The Onion Router", which refers to the layered nature of its encryption protocol. Tor encrypts the data, including the destination IP address, multiple times and sends it through a virtual circuit comprising successive, randomly selected Tor relays. Each relay decrypts a "layer" of encryption to reveal the next relay in the circuit in order to pass the remaining encrypted data on to it. The final relay decrypts the innermost layer of encryption and sends the original data to its destination without revealing, or even knowing, the source IP address.

This layered approach is what gives Tor its name, as it is analogous to the layers of an onion.

## Tor Architecture

The Tor network is a network of volunteer-run servers that allows people to improve their privacy and security on the internet. The network is composed of three types of relays:

*   **Entry/Guard Relays:** These are the first relays that a Tor user connects to. They know the user's real IP address, but they do not know the final destination of the traffic.
*   **Middle Relays:** These relays receive traffic from the entry relays and pass it on to the exit relays. They do not know the user's real IP address, nor do they know the final destination of the traffic. This is a crucial layer of separation that helps to ensure the user's anonymity.
*   **Exit Relays:** These are the final relays in the Tor circuit. They are responsible for sending the user's traffic to its final destination on the public internet. They know the destination of the traffic, but they do not know the user's real IP address.

### The Tor Circuit

When a user connects to the Tor network, their Tor client builds a circuit of three relays. This circuit is used to route all of their traffic. The circuit is periodically torn down and rebuilt with new relays to prevent a single relay from being able to track the user's activity over time.

Here is a diagram illustrating the Tor circuit:

```
+-----------------+      +-----------------+      +-----------------+
|   Your Device   |----->|   Entry Relay   |----->|   Middle Relay  |----->|   Exit Relay    |----->|   Destination   |
+-----------------+      +-----------------+      +-----------------+      +-----------------+      +-----------------+
      (You)                                                                                             (Website)
```

## Tor in the mailstorm Application

The mailstorm Desktop application uses a bundled Tor client to connect to the Tor network. The application is responsible for launching and managing the Tor client process, and for configuring the webview component to use the Tor proxy.

### Bundling Tor

The application includes a pre-configured Tor expert bundle for Windows. This bundle contains the `tor.exe` executable and all the necessary configuration files. By bundling Tor, the application can be distributed as a self-contained package that does not require the user to install Tor separately.

### Launching and Managing the Tor Process

The `main.py` script is responsible for launching the `tor.exe` process as a background process. The script uses the `subprocess` module to launch the process and to monitor its output.

The script waits for the Tor client to bootstrap and establish a connection to the Tor network. It does this by monitoring the stdout of the `tor.exe` process for the message "Bootstrapped 100%".

### Configuring the Webview

Once the Tor client is ready, the `main.py` script configures the `pywebview` component to use the Tor SOCKS5 proxy. The Tor client provides a SOCKS5 proxy on port 9050 of the local machine. The script sets the `WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS` environment variable to `--proxy-server=socks5://127.0.0.1:9050`. This tells the underlying WebView2 runtime to route all of its traffic through the Tor proxy.

### Terminating the Tor Process

When the user closes the application, the `main.py` script is responsible for terminating the `tor.exe` process. This is important to ensure that the Tor client does not continue to run in the background after the application has been closed.

## Security and Privacy Considerations

The use of Tor in the mailstorm application provides several security and privacy benefits:

*   **Anonymity:** Tor helps to anonymize the user's IP address, which makes it more difficult for the operator of the .onion service or any other party to determine the user's identity.
*   **Circumvention of Censorship:** Tor can be used to bypass censorship and to access websites that are blocked in the user's country.
*   **Access to Hidden Services:** Tor is the only way to access .onion hidden services, which are not accessible through the regular internet.

However, it is important to be aware of the limitations of Tor:

*   **Exit Node Vulnerabilities:** When accessing websites on the public internet (not .onion services), the traffic between the exit relay and the destination website is not encrypted by Tor. This means that a malicious exit relay operator could potentially monitor or modify the traffic. This is not a concern for the mailstorm application, as it only connects to a .onion service.
*   **Traffic Analysis:** While Tor makes it difficult to trace traffic, it is not impossible. A powerful adversary who can monitor a large portion of the internet could potentially de-anonymize Tor users.

## Performance Considerations

Because traffic is routed through multiple relays, using Tor is typically slower than a direct internet connection. This can result in slower page load times and a less responsive user experience. However, for the mailstorm application, the performance impact is acceptable, as the application is not designed for high-performance browsing.

## Conclusion

The integration of Tor is a critical component of the mailstorm Desktop application. It provides a secure and anonymous way to access the backend web application, and it is essential for the overall functionality of the project. This document has provided a detailed overview of the Tor integration, from the underlying principles of the Tor network to the specific implementation details in the mailstorm application.
