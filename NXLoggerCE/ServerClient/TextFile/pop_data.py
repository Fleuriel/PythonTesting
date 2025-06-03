import pyautogui
import random
import time

# List of strings or commands to randomly send
commands = ['echo Hello', 'dir', 'cls', 'whoami', 'hostname', 'ping 127.0.0.1', 'echo Goodbye', 'HELLO', 'GOODBYE' ,'YOU HAVE RECEIVED A VOICEMAIL', 'HELP, SOMEBODY HELP ME!', 'GOOD MORNING', 'GOOD AFTERNOON', 'GOOD NIGHT', 'THERE IS NOTHING THERE']

# Time limit (in seconds)
duration = 900
end_time = time.time() + duration
start_time = time.time()
next_log_time = start_time + 60

print("You have 5 seconds to focus the Command Prompt window...")
time.sleep(5)

while time.time() < end_time:
    cmd = random.choice(commands)
    pyautogui.write(cmd)
    pyautogui.press('enter')
    time.sleep(random.uniform(0, 1))  # Delay between commands

    current_time = time.time()
    if current_time >= next_log_time:
        elapsed = int(current_time - start_time)
        print(f"[+] {elapsed} seconds have passed...")
        next_log_time += 60