import subprocess
import time
import os
import sys
import webview

TOR_PATH_RELATIVE = "tor-expert-bundle-windows-i686-13.5.3/tor-expert-bundle-windows-i686-13.5.3/tor/tor.exe"

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

    # Command to launch Tor. We redirect stdout/stderr to capture output for bootstrapping check.
    # Using a list for the command is generally safer than a single string.
    # Hide the console window for the Tor process
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
        time.sleep(0.1) # Small delay to prevent busy-waiting
    return tor_process

def main():
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

if __name__ == "__main__":
    main()
