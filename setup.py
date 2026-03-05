from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import sys

class PostInstallCommand(install):

    def run(self):
        install.run(self)
        self.add_scripts_to_path()

    def add_scripts_to_path(self):

        if os.name != "nt":
            return

        try:
            import winreg

            scripts_path = os.path.join(
                os.path.expanduser("~"),
                "AppData",
                "Roaming",
                "Python",
                f"Python{sys.version_info.major}{sys.version_info.minor}",
                "Scripts"
            )

            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Environment",
                0,
                winreg.KEY_ALL_ACCESS
            )

            current_path, _ = winreg.QueryValueEx(key, "PATH")

            if scripts_path.lower() in current_path.lower():
                print("[CommitFlow] Scripts path already in PATH")
                return

            new_path = current_path + ";" + scripts_path

            winreg.SetValueEx(
                key,
                "PATH",
                0,
                winreg.REG_EXPAND_SZ,
                new_path
            )

            winreg.CloseKey(key)

            print("\n[CommitFlow] PATH updated automatically.")
            print("[CommitFlow] Restart terminal to use 'commitflow' command.\n")

        except Exception as e:
            print("\n[CommitFlow] Could not modify PATH automatically.")
            print(e)


setup(
    name="commitflow",
    version="1.0.0",
    description="Daily Git commit assistant for developers",
    author="Abhinav Kr Singh",
    packages=find_packages(),
    install_requires=[
        "colorama"
    ],
    entry_points={
        "console_scripts": [
            "commitflow=daily_git_assistant.main:main"
        ]
    },
    cmdclass={
        "install": PostInstallCommand
    }
)