import json
from datetime import datetime, timedelta
import tkinter as tk

CONFIG_FILE = 'config.json'
DATA_FILE = 'data.json'

#CONFIG LOADING
default_config = {
    'reset_time': '00:00',
    'dailies': [
        "Sample Daily",
        "Sample Daily 2"
    ]
}

try:
    with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
        config = json.load(file)
except (FileNotFoundError, json.JSONDecodeError ) as e:
    if isinstance(e, FileNotFoundError):
        print(f'{CONFIG_FILE} not found, creating default')
    elif isinstance(e, ValueError):
        print(f'{CONFIG_FILE} is invalid JSON, creating default')
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(default_config, f, indent=4)
    config = default_config
except Exception as e:
    print(f'{CONFIG_FILE} load error: {e}')
    config = default_config

dailies = config.get('dailies', [])
reset_time_str = config.get('reset_time', '00:00')

#DATA LOADING
now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
default_data = {
    'last_updated': now_str,
    'states': {daily: False for daily in dailies}
}

try:
    with open(DATA_FILE, 'r', encoding='utf-8') as file:
        data = json.load(file)
except FileNotFoundError as e:
    print(f'{DATA_FILE} not found, creating default')
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(default_data, f, indent=4)
    data = default_data
except Exception as e:
    print(f'{DATA_FILE} load error: {e}')
    data = default_data

#Reset
now = datetime.strptime(now_str, '%Y-%m-%d %H:%M:%S')
last_updated = datetime.strptime(data['last_updated'], '%Y-%m-%d %H:%M:%S')
reset_time = datetime.strptime(reset_time_str, '%H:%M').time()

today_reset = now.replace(hour=reset_time.hour, minute=reset_time.minute, second=0)
last_reset = today_reset if now >= today_reset else today_reset - timedelta(days=1)

if last_updated < last_reset:
    print('Resetting Dailies...')
    data['states'] = {daily: False for daily in dailies}

#Funcs
def update_daily(daily, var):
    data['states'][daily] = var.get()
    data['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

#GUI
root = tk.Tk()
root.title('Minimal Dailies Tracker')
root.minsize(200, 200)

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill='both', expand=True)

for daily in dailies:
    if daily not in data['states']:
        data['states'][daily] = False
    daily_var = tk.BooleanVar(value=data['states'][daily])

    chk = tk.Checkbutton(
        frame,
        text=daily,
        variable=daily_var,
        font=('Arial', 11),
        command=lambda d=daily, v=daily_var: update_daily(d,v)
    )

    chk.pack(anchor='w', pady=5)

reset_label = tk.Label(
    frame,
    text=f'Global Reset: {reset_time}',
    font=('Arial', 9),
)
reset_label.pack(anchor="w", pady=(20, 0))

root.mainloop()