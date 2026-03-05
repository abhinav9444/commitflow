import os
import platform
import subprocess
import tempfile


def detect_os():
    return platform.system()


def validate_time_format(time_str):

    try:
        hour, minute = time_str.split(":")
        hour = int(hour)
        minute = int(minute)

        return 0 <= hour <= 23 and 0 <= minute <= 59

    except Exception:
        return False


# -------------------------------------------
# USER SETTINGS PROMPT
# -------------------------------------------

def ask_boolean(question, default="n"):

    value = input(f"{question} (y/n) [default {default}] ➤ ").strip().lower()

    if not value:
        value = default

    return value == "y"


def ask_scheduler_settings():

    print("\n--- Scheduler Conditions ---")

    idle = ask_boolean("Start only if computer is idle?", "n")
    ac_power = ask_boolean("Start only if computer is on AC power?", "n")
    stop_battery = ask_boolean("Stop task if switching to battery?", "n")
    wake = ask_boolean("Wake computer to run task?", "y")
    network = ask_boolean("Require network connection?", "n")

    print("\n--- Scheduler Settings ---")

    run_on_demand = ask_boolean("Allow task to run on demand?", "y")
    run_missed = ask_boolean("Run task ASAP if missed?", "y")
    restart = ask_boolean("Restart task if it fails?", "y")

    restart_interval = "PT5M"
    restart_count = "100"

    stop_time = "P1D"

    force_stop = ask_boolean("Force stop if task does not end?", "y")

    delete_after = "PT0S"

    return {
        "idle": idle,
        "ac_power": ac_power,
        "stop_battery": stop_battery,
        "wake": wake,
        "network": network,
        "run_on_demand": run_on_demand,
        "run_missed": run_missed,
        "restart": restart,
        "restart_interval": restart_interval,
        "restart_count": restart_count,
        "stop_time": stop_time,
        "force_stop": force_stop,
        "delete_after": delete_after
    }


# -------------------------------------------
# WINDOWS TASK CREATION
# -------------------------------------------

def create_windows_task(time_str, settings):

    hour, minute = time_str.split(":")

    restart_xml = ""
    if settings["restart"]:
        restart_xml = f"""
        <RestartOnFailure>
            <Interval>{settings['restart_interval']}</Interval>
            <Count>{settings['restart_count']}</Count>
        </RestartOnFailure>
        """

    xml_content = f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">

  <Triggers>
    <CalendarTrigger>
      <StartBoundary>2026-01-01T{hour}:{minute}:00</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByDay>
        <DaysInterval>1</DaysInterval>
      </ScheduleByDay>
    </CalendarTrigger>
  </Triggers>

  <Principals>
    <Principal id="Author">
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>

  <Settings>

    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>

    <DisallowStartIfOnBatteries>{str(settings['ac_power']).lower()}</DisallowStartIfOnBatteries>

    <StopIfGoingOnBatteries>{str(settings['stop_battery']).lower()}</StopIfGoingOnBatteries>

    <AllowHardTerminate>{str(settings['force_stop']).lower()}</AllowHardTerminate>

    <StartWhenAvailable>{str(settings['run_missed']).lower()}</StartWhenAvailable>

    <RunOnlyIfNetworkAvailable>{str(settings['network']).lower()}</RunOnlyIfNetworkAvailable>

    <WakeToRun>{str(settings['wake']).lower()}</WakeToRun>

    <ExecutionTimeLimit>{settings['stop_time']}</ExecutionTimeLimit>

    {restart_xml}

    <AllowStartOnDemand>{str(settings['run_on_demand']).lower()}</AllowStartOnDemand>

    <Enabled>true</Enabled>

  </Settings>

#   <Actions Context="Author">
#     <Exec>
#       <Command>commitflow</Command>
#       <Arguments>--auto</Arguments>
#     </Exec>
#   </Actions>

  <Actions Context="Author">
    <Exec>
      <Command>python</Command>
      <Arguments>-m daily_git_assistant.main --auto</Arguments>
    </Exec>
  </Actions>

</Task>
"""

    try:

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as f:

            f.write(xml_content.encode("utf-16"))
            xml_path = f.name

        subprocess.run(
            [
                "schtasks",
                "/create",
                "/tn",
                "CommitFlowDaily",
                "/xml",
                xml_path,
                "/f"
            ],
            check=True
        )

        os.remove(xml_path)

        print("\n[SUCCESS] Windows scheduled task created.")

    except Exception as e:

        print("[ERROR] Failed to create Windows scheduled task:", e)


# -------------------------------------------
# LINUX CRON
# -------------------------------------------

def create_linux_cron(time_str):

    hour, minute = time_str.split(":")

    cron_line = f"{minute} {hour} * * * commitflow --auto"

    try:

        result = subprocess.run(
            ["crontab", "-l"],
            capture_output=True,
            text=True
        )

        existing = result.stdout

        if cron_line in existing:
            print("[INFO] Cron already exists.")
            return

        new_cron = existing + "\n" + cron_line + "\n"

        p = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE, text=True)
        p.communicate(new_cron)

        print("\n[SUCCESS] Cron job created.")

    except Exception:

        print("[ERROR] Failed to create cron job.")


# -------------------------------------------
# INTERACTIVE SCHEDULER
# -------------------------------------------

def schedule_interactive():

    print("\nSelect Scheduler Type")

    print("1. Windows Task Scheduler")
    print("2. Linux Cron")

    choice = input("Enter choice ➤ ").strip()

    time_str = input("Run time (HH:MM) ➤ ").strip()

    if not validate_time_format(time_str):

        print("[ERROR] Invalid time format.")
        return

    os_type = detect_os()

    if choice == "1" and os_type == "Windows":

        settings = ask_scheduler_settings()

        create_windows_task(time_str, settings)

    elif choice == "2" and os_type != "Windows":

        create_linux_cron(time_str)

    else:

        print("[WARNING] Scheduler type does not match OS.")