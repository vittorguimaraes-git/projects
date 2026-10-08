import json

try:
    with open("tasks.json", "r", encoding= "utf-8") as f:
        todo = json.load(f)
except FileNotFoundError:
    todo = []

while True:

    while True:
        command = input("Choose a action: (add | list | done | edit | remove | exit): ").strip().lower()
        if command not in ["list", "add", "done", "remove", "exit", "edit"]:
            print("Invalid command")
        else:
            break

    match command:
        case "add":
            while True:
                try:
                    desc = input("Enter a description: ").strip().title()
                    priority = input("Enter priority (high | medium | low): ").strip().lower()

                    if priority not in ["high", "medium", "low"] or not priority:
                        raise ValueError("Invalid priority")

                    if not desc:
                        raise ValueError("Invalid description")

                    if priority and desc:
                        break

                except ValueError:
                    print("Please enter a valid description or priority")

            todo.append({"description": desc, "status": False, "priority": priority})
            print(f"Task '{desc}' added with priority '{priority}'")

        case "list":
            priority_order = {"high": 3, "medium": 2, "low": 1}
            priority_icons = {"high": "🔴", "medium": "🟡", "low": "🟢"}
            if not todo:
                print("There are no task")
            else:
                print("=" * 50)
                for i, task in enumerate(sorted(todo, key=lambda t: priority_order[t["priority"]], reverse=True), start=1):
                    markup = "[x]" if task["status"] else "[ ]"
                    icon = priority_icons[task["priority"]]
                    print(f"{i} - | {markup} | {task['description']} {icon}")
                print("=" * 50)

        case "done":
            try:
                done = int(input("Enter the task number: "))
                todo[done - 1]["status"] = True
                task = todo[done - 1]["description"]
                print(f"✅ Task '{task}' marked as completed")
            except (ValueError, IndexError):
                print("Invalid task")

        case "edit":
            try:
                edit = int(input("Enter the task number: "))
                new_description = input("Enter a new description: ").strip().title()
                new_priority = input("Enter a new priority (high | medium | low): ").strip().lower()
                confirmation = input("Do you really want to edit the task? [y/n]: ").strip().lower()

                if new_priority not in ["high", "medium", "low"] or not new_priority:
                    print("Invalid priority")

                elif not new_description:
                    print("Description cannot be empty")
                    
                elif confirmation in ["y", "yes"]:
                    todo[edit- 1]["description"] = new_description
                    todo[edit - 1]["status"] = False
                    todo[edit - 1]["priority"] = new_priority
                    print(f"✏️ Task updated to: {new_description}")

            except (ValueError, IndexError):
                print("Invalid task")

        case "remove":
            try:
                remove = int(input("Enter the task number: "))
                confirmation = input("Do you really want to remove the task? [y/n]: ").strip().lower()
                task = todo[remove- 1]["description"]

                if confirmation in ["y", "yes"]:
                    todo.pop(remove - 1)
                    print(f"🗑️ Task '{task}' removed successfully")
            except (ValueError, IndexError):
                print("Invalid task")

        case "exit":
            print("💾 Tasks saved successfully! Goodbye.")
            break

with open("tasks.json", "w", encoding= "utf-8") as f:
    json.dump(todo, f, indent=4, ensure_ascii=False)
