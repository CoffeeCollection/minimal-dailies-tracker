# minimal-dailies-tracker
A simple checklist for tasks that resets daily.

## Features:
 * Helps you keep track of those dailies
 * Resets at designated times each day

## Setup:
 After the config.json is generated on initial startup, it will look like this:

```json
{
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
```

 * `default_reset_time`: Set any time in HH:MM format to reset dailies without a unique rest time.
 * `dailies`: Add a list of dailies to track. If "reset_time" is not assigned, will use default_reset_time.
