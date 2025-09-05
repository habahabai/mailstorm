# Deployment

## Introduction

This document provides a comprehensive guide to building and deploying the mailstorm Desktop application. It covers the entire process, from setting up the build environment to packaging the application for distribution. This document is intended for developers who want to create a distributable version of the application.

## Prerequisites

Before you can build the application, you need to have the following software installed on your system:

*   **Python:** The application is written in Python, so you need to have Python installed. You can download Python from the official website: [https://www.python.org/](https://www.python.org/)
*   **pip:** You also need to have `pip`, the Python package installer, installed. `pip` is usually installed automatically with Python.

## Building the Application

The application is built using the `pyinstaller` library, which is a popular tool for packaging Python applications as standalone executables. The `build.bat` script in the root of the project automates the build process.

### The `build.bat` Script

The `build.bat` script performs the following steps:

1.  **Installs PyInstaller:** It first ensures that `pyinstaller` is installed by running `pip install pyinstaller`.
2.  **Runs PyInstaller:** It then runs the `pyinstaller` command with the following options:
    *   `--onefile`: This option tells `pyinstaller` to create a single executable file that contains all of the application's code and dependencies.
    *   `--add-data "tor-expert-bundle-windows-i686-13.5.3;tor-expert-bundle-windows-i686-13.5.3"`: This option tells `pyinstaller` to include the `tor-expert-bundle-windows-i686-13.5.3` directory in the executable. This is necessary because the application needs the Tor client to be available at runtime.
    *   `main.py`: This is the entry point of the application.

To build the application, simply run the `build.bat` script from the command line.

### The `dist` Folder

After the build process is complete, you will find the executable file in the `dist` folder. The `dist` folder will contain a single file named `main.exe`. This is the standalone executable file that you can distribute to users.

## Packaging for Distribution

Once you have built the application, you need to package it for distribution. There are several ways to do this:

### ZIP Archive

The simplest way to package the application is to create a ZIP archive of the `main.exe` file. You can then distribute the ZIP archive to users, and they can extract the executable and run it.

### Installer

A more professional way to package the application is to create an installer. An installer is a program that guides the user through the process of installing the application on their system. An installer can:

*   Create a shortcut to the application on the user's desktop or in the Start menu.
*   Associate the application with certain file types.
*   Add an entry for the application in the "Add or Remove Programs" list.

There are several tools available for creating installers for Windows applications, such as Inno Setup and NSIS.

## Code Signing

Code signing is the process of digitally signing an executable file to verify its authenticity and integrity. When you sign an executable, you are essentially saying that you are the author of the executable and that it has not been tampered with since you signed it.

Code signing is important for Windows applications because it helps to build trust with users. When a user runs an unsigned executable, Windows will display a security warning, which may discourage the user from running the application. When a user runs a signed executable, Windows will display the name of the publisher, which can help to reassure the user that the application is legitimate.

To sign an executable, you need to obtain a code signing certificate from a certificate authority (CA). Once you have a certificate, you can use a tool like Microsoft's SignTool to sign your executable.

## Distribution Methods

There are several ways to distribute the application to users:

### GitHub Releases

If your project is hosted on GitHub, you can use GitHub Releases to distribute your application. GitHub Releases allows you to create a new release, upload your packaged application, and write release notes.

### Website Download

You can also distribute the application from your own website. You can create a download page where users can download the packaged application.

## Conclusion

This document has provided a comprehensive overview of the deployment process for the mailstorm Desktop application. By following the steps outlined in this document, you can build and deploy a professional-quality application that is easy for users to install and run. This document has covered the entire process, from setting up the build environment to packaging the application for distribution.
