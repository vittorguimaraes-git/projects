import json

try:
    with open("tasks.json", "r", encoding="utf-8") as f:
        todo = json.load(f)
except FileNotFoundError:
    todo = []

while True:

    while True:
        command = input("Choose an action: (add | list | complete | edit | remove | exit | done | pending): ").strip().lower()
        print()
        if command not in ["list", "add", "complete", "remove", "exit", "edit", "done", "pending"]:
            print("=" * 50)
            print("Invalid command".center(45))
            print("=" * 50)
        else:
            break

    match command:

        case "add":
            while True:
                try:
                    desc = input("Enter a description: ").strip().title()
                    priority = input("Enter priority (high | medium | low): ").strip().lower()

                    if priority not in ["high", "medium", "low"] or not priority:
                        raise ValueError
                    if not desc:
                        raise ValueError
                    break
                except ValueError:
                    print("=" * 50)
                    print("Please enter a valid description or priority".center(45))
                    print("=" * 50)

            todo.append({"description": desc, "status": False, "priority": priority})
            print(f"➕ Task '{desc}' added with priority '{priority}'")
            print()

        case "list":
            priority_order = {"high": 3, "medium": 2, "low": 1}
            priority_icons = {"high": "🔴", "medium": "🟡", "low": "🟢"}
            done = sum(1 for t in todo if t["status"])
            undone = len(todo) - done
            if not todo:
                print("=" * 50)
                print("There are no tasks".center(45))
                print("=" * 50)
            else:
                print("=" * 50)
                for i, task in enumerate(sorted(todo, key=lambda t: priority_order[t["priority"]], reverse=True), start=1):
                    markup = "[x]" if task["status"] else "[ ]"
                    icon = priority_icons[task["priority"]]
                    print(f"{i} - | {markup} | {task['description']} {icon}")
                print("=" * 50)
                print(f"\n✅ {done} Completed tasks | ⏳ {undone} Pending tasks\n")

        case "complete":
            try:
                count = 0
                for task in todo:
                    if task["status"]:
                        count += 1

                if count == len(todo) and todo:
                    print("=" * 50)
                    print("All tasks are completed, good job!".center(45))
                    print("=" * 50)
                    print()
                else:
                    done = int(input("Enter the task number: "))
                    todo[done - 1]["status"] = True
                    desc = todo[done - 1]["description"]
                    print(f"✅ Task '{desc}' marked as completed\n")
            except (ValueError, IndexError):
                print("=" * 50)
                print("Invalid task".center(45))
                print("=" * 50)

        case "edit":
            try:
                edit = int(input("Enter the task number: "))
                new_description = input("Enter a new description: ").strip().title()
                new_priority = input("Enter a new priority (high | medium | low): ").strip().lower()
                confirmation = input("Do you really want to edit the task? [y/n]: ").strip().lower()

                if new_priority not in ["high", "medium", "low"] or not new_priority:
                    print("=" * 50)
                    print("Invalid priority".center(45))
                    print("=" * 50)
                elif not new_description:
                    print("=" * 50)
                    print("Description cannot be empty".center(45))
                    print("=" * 50)
                elif confirmation in ["y", "yes"]:
                    todo[edit - 1]["description"] = new_description
                    todo[edit - 1]["status"] = False
                    todo[edit - 1]["priority"] = new_priority
                    print(f"✏️ Task updated to: {new_description}\n")
                elif confirmation in ["n", "no"]:
                    print("=" * 50)
                    print("Task not edited".center(45))
                    print("=" * 50)
                else:
                    print("=" * 50)
                    print("Invalid option".center(45))
                    print("=" * 50)
            except (ValueError, IndexError):
                print("=" * 50)
                print("Invalid task".center(45))
                print("=" * 50)

        case "remove":
            try:
                if not todo:
                    print("=" * 50)
                    print("There are no tasks".center(45))
                    print("=" * 50)
                else:
                    remove = int(input("Enter the task number: "))
                    confirmation = input("Do you really want to remove the task? [y/n]: ").strip().lower()
                    task = todo[remove - 1]["description"]

                    if confirmation in ["y", "yes"]:
                        todo.pop(remove - 1)
                        print(f"🗑️ Task '{task}' removed successfully\n")
                    elif confirmation in ["n", "no"]:
                        print("=" * 50)
                        print("Task not removed".center(45))
                        print("=" * 50)
                    else:
                        print("=" * 50)
                        print("Invalid option".center(45))
                        print("=" * 50)
            except (ValueError, IndexError):
                print("=" * 50)
                print("Invalid task".center(45))
                print("=" * 50)

        case "done":
            priority_icons = {"high": "🔴", "medium": "🟡", "low": "🟢"}
            if not todo:
                print("=" * 50)
                print("There are no tasks".center(45))
                print("=" * 50)
            else:
                count = 0
                print("=" * 50)
                for i, task in enumerate(todo, start=1):
                    if task["status"]:
                        icon = priority_icons[task["priority"]]
                        print(f"{i - count} - | [x] | {task['description']} {icon}")
                    else:
                        count += 1
                if count == len(todo):
                    print("There are no completed tasks".center(45))
                print("=" * 50)
                print(f"\n✅ {len(todo) - count} Completed tasks\n")

        case "pending":
            priority_icons = {"high": "🔴", "medium": "🟡", "low": "🟢"}
            if not todo:
                print("=" * 50)
                print("There are no tasks".center(45))
                print("=" * 50)
            else:
                count = 0
                print("=" * 50)
                for i, task in enumerate(todo, start=1):
                    if not task["status"]:
                        icon = priority_icons[task["priority"]]
                        print(f"{i - count} - | [ ] | {task['description']} {icon}")
                    else:
                        count += 1
                if count == len(todo):
                    print("There are no pending tasks".center(45))
                print("=" * 50)
                print(f"\n⏳ {len(todo) - count} Pending tasks\n")

        case "exit":
            print("💾 Tasks saved successfully! Goodbye.")
            break

with open("tasks.json", "w", encoding="utf-8") as f:
    json.dump(todo, f, indent=4, ensure_ascii=False)
