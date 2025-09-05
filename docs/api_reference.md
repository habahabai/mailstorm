# API Reference

## Introduction

This document provides a detailed reference for the functions in the `main.py` file. The `main.py` file is the entry point of the mailstorm Desktop application, and it contains the core logic of the application. This document is intended for developers who want to understand how the application works and how to extend its functionality.

## Functions

### `get_webview2_version()`

This function detects if the WebView2 runtime is installed and returns its version.

**Parameters:**

None

**Returns:**

The version of the WebView2 runtime as a string, or `None` if the runtime is not installed.

**Implementation Details:**

The function checks the Windows Registry for the presence of the WebView2 runtime. It checks both the machine-wide and user-specific installation locations.

Here is the code for the function:

```python
def get_webview2_version():
    """
    Detects if the WebView2 runtime is installed and returns its version.
    Checks the Windows Registry for both machine-wide and user-specific installations.
    """
    webview2_guid = "{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"
    
    is_64bit = platform.machine().endswith('64')
    base_paths = [r"SOFTWARE\Microsoft\EdgeUpdate\Clients"]
    if is_64bit:
        base_paths.append(r"SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients")

    registry_hives = [winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE]

    for hive in registry_hives:
        for base_path in base_paths:
            full_path = f"{base_path}\\{webview2_guid}"
            try:
                with winreg.OpenKey(hive, full_path) as key:
                    version, _ = winreg.QueryValueEx(key, "pv")
                    if version and version != "0.0.0.0":
                        return version
            except FileNotFoundError:
                continue
            except Exception as e:
                print(f"Error accessing registry: {e}")
                continue
    return None
```

### `install_webview2_and_relaunch()`

This function downloads, silently installs the WebView2 runtime, and prompts the user to relaunch.

**Parameters:**

None

**Returns:**

None

**Implementation Details:**

The function downloads the WebView2 installer from Microsoft's servers, runs the installer silently in the background, and then prompts the user to relaunch the application.

Here is the code for the function:

```python
def install_webview2_and_relaunch():
    """
    Downloads, silently installs the WebView2 runtime, and prompts the user to relaunch.
    """
    print("Microsoft Edge WebView2 runtime is required. It will be downloaded and installed now.")
    
    installer_url = "https://go.microsoft.com/fwlink/p/?LinkId=2124703"
    temp_dir = tempfile.gettempdir()
    installer_path = os.path.join(temp_dir, "MicrosoftEdgeWebview2Setup.exe")

    try:
        print(f"Downloading WebView2 installer from {installer_url}...")
        response = requests.get(installer_url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        with open(installer_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print("Download complete. Starting silent installation...")
        print("Please close this window and relaunch the application after the installation is complete.")
        # Run the installer silently and wait for it to complete
        subprocess.run(
            [installer_path, '/silent', '/install'],
            check=True
        )
        
        print("WebView2 installation complete.")

    except Exception as e:
        print(f"An error occurred during installation: {e}")
        print("Please close this window and try again.")
        # Keep the window open until the user closes it
        while True:
            time.sleep(1)

    finally:
        # Clean up the installer
        if os.path.exists(installer_path):
            os.remove(installer_path)
            print("Installer cleaned up.")
    # Keep the window open until the user closes it
    while True:
        time.sleep(1)
```

### `get_absolute_path()`

This function gets the absolute path for a given relative path.

**Parameters:**

*   `relative_path`: The relative path to convert to an absolute path.

**Returns:**

The absolute path.

**Implementation Details:**

The function uses the `os.path.join()` function to join the base path of the script with the relative path.

Here is the code for the function:

```python
def get_absolute_path(relative_path):
    """Get the absolute path for a given relative path."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)
```

### `launch_tor()`

This function launches Tor and waits for it to bootstrap.

**Parameters:**

None

**Returns:**

The Tor process object.

**Implementation Details:**

The function launches the `tor.exe` executable as a background process and then monitors its output to wait for it to bootstrap.

Here is the code for the function:

```python
def launch_tor():
    """Launches Tor and waits for it to bootstrap."""
    tor_exe_path = get_absolute_path(TOR_PATH_RELATIVE)
    print(f"Attempting to launch Tor from: {tor_exe_path}")

    if not os.path.exists(tor_exe_path):
        print(f"Error: Tor executable not found at {tor_exe_path}")
        sys.exit(1)

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE

    tor_process = subprocess.Popen([tor_exe_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, startupinfo=startupinfo)

    print("Waiting for Tor to bootstrap...")
    while True:
        line = tor_process.stdout.readline()
        if "Bootstrapped 100%" in line:
            print("Tor has successfully bootstrapped!")
            break
        if tor_process.poll() is not None:
            print("Tor process exited prematurely.")
            print(f"Tor stdout: {tor_process.stdout.read()}")
            print(f"Tor stderr: {tor_process.stderr.read()}")
            sys.exit(1)
        time.sleep(0.1)
    return tor_process
```

### `main()`

This is the main function of the application.

**Parameters:**

None

**Returns:**

None

**Implementation Details:**

The function launches the Tor client, creates the webview window, and then enters the main event loop.

Here is the code for the function:

```python
def main():
    """Main application logic."""
    tor_process = None
    try:
        tor_process = launch_tor()
        onion_url = "http://imux3xyaclb655flrnkmvudyt4k3m37tw437geyvhlrg4e75flhvb5yd.onion"

        os.environ['WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS'] = "--proxy-server=socks5://127.0.0.1:9050"

        print(f"Opening webview for: {onion_url}")
        webview.create_window(title="email tnt desktop",fullscreen=False,maximized=True , url=onion_url)
        webview.start(private_mode=False)

    except KeyboardInterrupt:
        print("Application interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if tor_process:
            print("Terminating Tor process...")
            tor_process.terminate()
            tor_process.wait()
            print("Tor process terminated.")
```

## Conclusion

This document has provided a detailed reference for the functions in the `main.py` file. By understanding how these functions work, you can extend the functionality of the application and contribute to its development.
