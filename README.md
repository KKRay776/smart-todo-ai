Started this as a basic Python project and kept adding stuff to it. It's a command line to-do app that does more than just add and delete tasks.

## What it does

- Automatically detects task category (Work, Personal, Shopping, etc.)
- Gives each task a priority — High, Medium, or Low
- Reads due dates from your text, so if you type "submit report by friday" it actually picks that up
- Saves tasks in a JSON file so they stay even after you close the app
- Can summarize long task descriptions if you have transformers installed

## How to run it

```
pip install -r requirements.txt
```

```
python todo_app.py
```

## Menu

```
1. Add Task
2. View Tasks
3. Mark Task as Complete
4. Delete Task
5. Exit
```

## Libraries

- `dateparser` — reads dates from plain text
- `transformers` — for summarizing tasks (optional, app works without it)

## Acknowledgements

The idea and logic behind this whole project is fully mine. I wanted to build something that actually feels useful and smart, not just a boring add and delete list. I used **Claude**, **Gemini**, and **GitHub Copilot** only to help me add specific lines and understand how certain libraries work — but the structure, the thinking, and everything you see here I figured out myself.

Honestly I got really excited building this. It started as like 20 lines and kept growing. Every time I added a new feature it felt amazing. Still learning Python but this project made me love it even more 😄


## Demo

Here’s what the app looks like when running:

=================Main Menu=================
1. Add Task
2. View Tasks
3. Mark Task as Complete
4. Delete Task
5. Exit

Enter your choice: 1
Enter the task: submit report by Friday
Task "submit report by Friday" added successfully!✅
Category: Work | Priority: Medium | Due: 2026-06-19 17:00

