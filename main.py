import subprocess
import time
import os
import sys
import webview
import platform
import tempfile
import requests

# Platform-specific imports
if platform.system() == 'Windows':
    import winreg

# Platform-specific Tor path
if platform.system() == 'Windows':
    TOR_PATH_RELATIVE = "tor-expert-bundle-windows-i686-13.5.3/tor-expert-bundle-windows-i686-13.5.3/tor/tor.exe"
else:
    TOR_PATH_RELATIVE = "tor/tor"

def get_webview2_version():
    """
    Detects if the WebView2 runtime is installed and returns its version.
    Checks the Windows Registry for both machine-wide and user-specific installations.
    Only runs on Windows.
    """
    if platform.system() != 'Windows':
        # On Linux, webview uses GTK and doesn't need WebView2
        return "N/A (Linux)"

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

def install_webview2_and_relaunch():
    """
    Downloads, silently installs the WebView2 runtime, and prompts the user to relaunch.
    Only runs on Windows.
    """
    if platform.system() != 'Windows':
        print("WebView2 installation not needed on Linux.")
        return

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


def get_absolute_path(relative_path):
    """Get the absolute path for a given relative path."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def launch_tor():
    """Launches Tor and waits for it to bootstrap."""
    tor_exe_path = get_absolute_path(TOR_PATH_RELATIVE)
    print(f"Attempting to launch Tor from: {tor_exe_path}")

    if not os.path.exists(tor_exe_path):
        print(f"Error: Tor executable not found at {tor_exe_path}")
        sys.exit(1)

    # Platform-specific process creation
    if platform.system() == 'Windows':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        tor_process = subprocess.Popen([tor_exe_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, startupinfo=startupinfo)
    else:
        # Linux doesn't need startupinfo
        tor_process = subprocess.Popen([tor_exe_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

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

def main():
    """Main application logic."""
    tor_process = None
    try:
        tor_process = launch_tor()
        onion_url = "http://snzjnzdgfel2h2z3kfd34cvv6szdjfwboynqctjln7ze4ythgrllixyd.onion"

        # Set proxy for webview
        if platform.system() == 'Windows':
            os.environ['WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS'] = "--proxy-server=socks5://127.0.0.1:9050"
        else:
            # On Linux, we may need to set environment variables for GTK webkit
            os.environ['http_proxy'] = 'socks5://127.0.0.1:9050'
            os.environ['https_proxy'] = 'socks5://127.0.0.1:9050'

        print(f"Opening webview for: {onion_url}")
        webview.create_window(title="mailstorm desktop", fullscreen=False, maximized=True, url=onion_url)
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

if __name__ == "__main__":
    version = get_webview2_version()
    if platform.system() == 'Windows' and not version:
        install_webview2_and_relaunch()
    else:
        if platform.system() == 'Windows':
            print("Microsoft Edge WebView2 runtime is already installed.")
        else:
            print(f"Running on {platform.system()}. Using native webview.")
        main()
