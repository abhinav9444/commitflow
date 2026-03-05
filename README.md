# CommitFlow

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/github/license/abhinav9444/commitflow)
![Build](https://github.com/abhinav9444/commitflow/actions/workflows/tests.yml/badge.svg)
![Tests](https://img.shields.io/github/actions/workflow/status/abhinav9444/commitflow/tests.yml)
![PyPI](https://img.shields.io/pypi/v/commitflow)

CommitFlow is a lightweight command-line tool that helps developers maintain consistent Git commits automatically without interrupting their workflow .
It provides a simple interface to commit progress, automate daily commits and keep your GitHub contribution graph active while you focus on actual development.

## Why CommitFlow?
> ### CommitFlow is built to simplify a common developer habit: committing progress regularly.
Developers often forget to commit progress regularly while working across multiple projects. CommitFlow simplifies this by providing a clean command-line workflow that helps automate and manage daily commits. It is designed to be simple, practical and useful for everyday development workflows.
> ### If this tool helps your workflow, feel free to star the repository ! It means a lot !!

## Features
- Automatic repository detection
- Commit preview before committing
- Interactive commit workflow
- Quick commit mode for frequent commits
- Automatic daily commits (Scheduled runs)
- Windows Task Scheduler support
- Linux cron support
- Configuration file support
- Logging system
- Cross-platform terminal color support

<!--
## Usage
commitflow
commitflow --quick
commitflow --auto
commitflow --setup
commitflow --schedule
---
-->
## Installation
Install CommitFlow directly from PyPI:
```bash
pip install commitflow
```
Verify installation:
```bash
commitflow --version
```
## Quick Start
Run CommitFlow in interactive mode. This mode guides you through the commit process step by step.
```bash
commitflow
```
You will be prompted for:
- repository path
- files to add
- commit message
- push confirmation

CommitFlow shows a preview before committing.

## CLI Commands
### Interactive Mode (Default)
Run the standard interactive workflow:
```bash
commitflow
```

### Quick Mode
Use repository settings from your configuration file.
``` bash
commitflow --quick
```
Quick mode skips repository selection and speeds up the commit process.

### Auto Mode
Fully automatic commit process:
``` bash
commitflow --auto
```
This mode:
- adds files automatically
- commits with a default message
- optionally pushes to remote

Auto mode is mainly used by schedulers.

### Setup Wizard
Run the configuration wizard:
``` bash
commitflow --setup
```
The setup wizard asks for:
- repository path
- automatic push preference
- default commit message
- daily schedule time

It can also configure the system scheduler automatically.

### Scheduler Setup
Create an automated daily commit task:
```bash
commitflow --schedule
```
CommitFlow supports:
- Windows Task Scheduler
- Linux/macOS cron

Scheduler settings such as power conditions and retry behavior can be customized during setup.

### Example Workflow
Typical setup:
``` bash
commitflow --setup
```
After configuration, CommitFlow can run automatic commits daily.

Manual commits can also be executed anytime:
``` bash
commitflow --quick
```
### Configuration File
CommitFlow stores configuration in:
``` bash
~/.commitflow_config.json
```
Example configuration:
```bash
{
  "repo": "/projects/my-project",
  "auto_push": true,
  "auto_add": ".",
  "commit_message": "daily progress update"
}
```
### Logs
CommitFlow keeps logs for debugging and activity tracking.
Default log location:
``` bash
~/.commitflow.log
```
Log entries include:
- commit operations
- warnings
- errors
- scheduler events

### Supported Platforms
- Windows
- Linux
<!--
Schedulers supported:
- Windows Task Scheduler
- cron
-->
<!--
Running Tests

Install development dependencies:

pip install pytest

Run tests:

pytest

GitHub Actions automatically runs tests on each push.

Project Structure
commitflow
│
├── daily_git_assistant
│   ├── main.py
│   ├── config.py
│   ├── git_utils.py
│   ├── logger.py
│   ├── repo_scanner.py
│   ├── scheduler.py
│   ├── ui.py
│   └── modes
│
├── tests
├── setup.py
└── README.md
-->

### Contributing
Contributions are welcome. If you would like to improve CommitFlow:
- Fork the repository
- Create a feature branch
- Submit a pull request

Bug reports and feature suggestions are appreciated.

### License
This project is licensed under the MIT License.

### Author
Abhinav Kumar Singh
