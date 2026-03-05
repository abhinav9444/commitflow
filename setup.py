from setuptools import setup, find_packages
from pathlib import Path
import site
import sys
import os


# -----------------------------
# Read README for PyPI
# -----------------------------

this_directory = Path(__file__).parent
readme_path = this_directory / "README.md"

if readme_path.exists():
    long_description = readme_path.read_text(encoding="utf-8")
else:
    long_description = ""


# -----------------------------
# Add Scripts folder to PATH
# -----------------------------

def add_scripts_to_path():

    try:

        user_base = site.USER_BASE
        scripts_path = os.path.join(user_base, "Scripts")

        if os.name != "nt":
            scripts_path = os.path.join(user_base, "bin")

        path_env = os.environ.get("PATH", "")

        if scripts_path not in path_env:

            if os.name == "nt":

                os.system(f'setx PATH "%PATH%;{scripts_path}"')

            else:

                shell_profile = os.path.expanduser("~/.bashrc")

                with open(shell_profile, "a") as f:
                    f.write(f'\nexport PATH="$PATH:{scripts_path}"\n')

    except Exception:
        pass


add_scripts_to_path()


# -----------------------------
# Setup configuration
# -----------------------------

setup(

    name="commitflow",

    version="1.0.1",   # version bumped for PyPI update

    description="CLI tool for maintaining consistent Git commits automatically",

    long_description=long_description,

    long_description_content_type="text/markdown",

    author="Abhinav Kumar Singh",

    author_email="abhinavksinghofc@gmail.com",

    url="https://github.com/abhinav9444/commitflow",

    license="MIT",

    packages=find_packages(),

    install_requires=[
        "colorama"
    ],

    entry_points={
        "console_scripts": [
            "commitflow=daily_git_assistant.main:main"
        ]
    },

    python_requires=">=3.8",

    project_urls={
        "Source": "https://github.com/abhinav9444/commitflow",
        "Issues": "https://github.com/abhinav9444/commitflow/issues",
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
    ],

)