import json
from datetime import datetime, timedelta
import tkinter as tk

CONFIG_FILE = 'config.json'
DATA_FILE = 'data.json'

default_config = {
    'default_reset_time': '00:00',
    'dailies': [
        {
            "name": "Sample Daily",
            "reset_time": "02:00"
        },
        {
            "name": "Sample Daily 2"
        }
    ]
}

def load_config(default_config):
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

    return config

def load_data(dailies):
    default_data = {
        'last_updated': now_str,
        'states': {daily['name']: False for daily in dailies}
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

    return data

#Loading config and data
config = load_config(default_config)

dailies = config.get('dailies', [])
default_reset_time_str = config.get('default_reset_time', '00:00')
now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

data = load_data(dailies)

#Reset
now = datetime.strptime(now_str, '%Y-%m-%d %H:%M:%S')
last_updated = datetime.strptime(data['last_updated'], '%Y-%m-%d %H:%M:%S')
default_reset_time = datetime.strptime(default_reset_time_str, '%H:%M').time()

#Individual Daily Reset
for daily in dailies:
    daily_name = daily['name']

    daily_reset_str = daily.get('reset_time', default_reset_time_str)
    daily_reset_time = datetime.strptime(daily_reset_str, '%H:%M').time()

    today_reset = now.replace(hour=daily_reset_time.hour, minute=daily_reset_time.minute, second=0)
    last_reset = today_reset if now >= today_reset else today_reset - timedelta(days=1)

    if last_updated <= last_reset:
        data['states'][daily_name] = False

#Orphaned tasks cleanup on global default reset
    today_default_reset = now.replace(hour=default_reset_time.hour, minute=default_reset_time.minute, second=0)
    last_default_reset = today_default_reset if now >= today_default_reset else today_default_reset - timedelta(days=1)
    if last_updated <= last_default_reset:
        valid_tasks = {daily['name'] for daily in dailies}
        print(valid_tasks)
        data['states'] = {k: v for k, v in data['states'].items() if k in valid_tasks}

#Funcs
def update_daily(daily_name, var):
    data['states'][daily_name] = var.get()
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
    daily_name = daily['name']
    if daily_name not in data['states']:
        data['states'][daily_name] = False
    daily_var = tk.BooleanVar(value=data['states'][daily_name])

    chk = tk.Checkbutton(
        frame,
        text=daily_name,
        variable=daily_var,
        font=('Arial', 11),
        command=lambda d=daily_name, v=daily_var: update_daily(d,v)
    )

    chk.pack(anchor='w', pady=5)

'''
reset_label = tk.Label(
    frame,
    text=f'Global Reset: {reset_time}',
    font=('Arial', 9),
)
reset_label.pack(anchor="w", pady=(20, 0))
'''

root.mainloop()