import json
import tkinter as tk

default_config = {
    'reset_time': '02:00',
    'dailies': []
}

try:
    with open('config.json', 'r', encoding='utf-8') as file:
        config = json.load(file)
except Exception as e:
    print(f'Error: {e}')
    config = default_config

dailies = config.get('dailies', [])
reset_time = config.get('reset_time', '00:00')

root = tk.Tk()
root.title('Minimal Dailies Tracker')
root.geometry('250x400')

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill='both', expand=True)

for daily in dailies:
    daily_var = tk.BooleanVar(value=False)

    chk = tk.Checkbutton(
        frame,
        text=daily,
        variable=daily_var,
        font=('Arial', 11)
    )

    chk.pack(anchor='w', pady=5)

reset_label = tk.Label(
    frame,
    text=f'Global Reset: {reset_time}',
    font=('Arial', 9),
)
reset_label.pack(anchor="w", pady=(20, 0))

root.mainloop()