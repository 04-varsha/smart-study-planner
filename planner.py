def generate_schedule(tasks):
    tasks = sorted(tasks, key=lambda x: x[2], reverse=True)

    schedule = []
    time_slot = 1

    for task in tasks:
        name, hours, priority = task
        for i in range(hours):
            schedule.append(f"Hour {time_slot}: {name}")
            time_slot += 1

    return schedule