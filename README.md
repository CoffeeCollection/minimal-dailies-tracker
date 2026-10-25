# minimal-dailies-tracker
A simple checklist for daily tasks with a daily reset written in Python.

Features:
 -Helps you keep track of those dailies
 -Resets at designated time each day

Setup:
 After the config.json is generated on initial startup, it will look like this:

```json
{
    "reset_time": "00:00",
    "dailies": [
        "Sample Daily",
        "Sample Daily 2"
    ]
}
```

 `reset_time`: Set any time in HH:MM format for dailies to reset after this time.
 `dailies`: An array of strings of any length, add the tasks you want to track daily.