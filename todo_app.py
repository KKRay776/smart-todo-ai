# my to do list project - started simple then kept adding stuff to it

# need these for file saving, system exit, and json
import os
import sys
import json

# dateparser reads dates from normal text like "tomorrow" or "next friday"
# using try/except so app still runs even if someone hasnt installed it
try:
    import dateparser
    from dateparser.search import search_dates
except ImportError:
    dateparser = None
    search_dates = None

# this is the ai part - summarizes long task descriptions
# totally optional, everything works fine without it too
try:
    from transformers import pipeline
    summarizer = pipeline('summarization')
except Exception:
    summarizer = None


DATA_FOLDER = 'data'
DATA_FILE = os.path.join(DATA_FOLDER, 'tasks.json')

tasks_list = []

CATEGORY_KEYWORDS = {
    'Work': ['meeting', 'project', 'email', 'client', 'report', 'deadline', 'presentation', 'call'],
    'Personal': ['doctor', 'gym', 'family', 'friend', 'birthday', 'anniversary', 'self-care', 'exercise'],
    'Shopping': ['buy', 'purchase', 'groceries', 'milk', 'shopping', 'order', 'deliver', 'amazon'],
}
URGENCY_KEYWORDS = ['urgent', 'asap', 'today', 'now', 'immediately', 'important', 'deadline', 'soon']


def load_tasks():
    """Load saved tasks from JSON file when app starts."""
    from datetime import datetime
    global tasks_list
    if not os.path.exists(DATA_FILE):
        tasks_list = []
        return
    try:
        with open(DATA_FILE, 'r') as f:
            loaded = json.load(f)
            for task in loaded:
                if task.get('due_date'):
                    task['due_date'] = datetime.fromisoformat(task['due_date'])
            tasks_list = loaded
        print(f'Welcome back! Loaded {len(tasks_list)} saved task(s).✅')
    except Exception:
        tasks_list = []


def save_tasks():
    """Save current tasks to JSON file."""
    os.makedirs(DATA_FOLDER, exist_ok=True)
    serializable = []
    for task in tasks_list:
        t = task.copy()
        if t.get('due_date') and t['due_date'] is not None:
            t['due_date'] = t['due_date'].isoformat()
        serializable.append(t)
    with open(DATA_FILE, 'w') as f:
        json.dump(serializable, f, indent=4)


def summarize_text(text):
    """Summarize a long task description into a concise phrase."""
    if not text or len(text.split()) <= 20:
        return text.strip()

    if summarizer:
        try:
            result = summarizer(text, max_length=30, min_length=10, do_sample=False)
            return result[0]['summary_text'].strip()
        except Exception:
            pass

    return ' '.join(text.split()[:20]).strip() + '...'


def detect_category(text):
    """Determine a reasonable category from the task text."""
    normalized = text.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            return category
    return 'General'


def parse_due_date(text):
    """Extract a date/time from the task description if possible."""
    if not dateparser or not search_dates:
        return None

    parsed = search_dates(text, settings={'PREFER_DATES_FROM': 'future'})
    if parsed:
        return parsed[-1][1]
    return None


def compute_priority(text, due_date):
    """Score a task by urgency keywords and due date proximity."""
    from datetime import datetime, timedelta
    score = 0
    normalized = text.lower()

    if due_date:
        now = datetime.now()
        delta = due_date - now
        if delta.total_seconds() <= 0:
            score += 30
        elif delta <= timedelta(hours=6):
            score += 25
        elif delta <= timedelta(days=1):
            score += 15
        elif delta <= timedelta(days=3):
            score += 8

    score += sum(5 for keyword in URGENCY_KEYWORDS if keyword in normalized)
    if 'shopping' in normalized or 'buy' in normalized:
        score += 2

    if score >= 30:
        label = 'High'
    elif score >= 15:
        label = 'Medium'
    else:
        label = 'Low'

    return {'priority_score': min(max(score, 0), 100), 'priority_label': label}


def format_due_date(due_date):
    """Format a parsed due date for printing."""
    if due_date is None:
        return 'No due date'
    return due_date.strftime('%Y-%m-%d %H:%M')


def add_task():
    task = input('Enter the task: ')
    due_date = parse_due_date(task)
    summary = summarize_text(task)
    category = detect_category(task)
    priority = compute_priority(task, due_date)
    tasks_list.append({
        'task': task,
        'status': 'Incomplete',
        'summary': summary,
        'category': category,
        'due_date': due_date,
        'priority': priority,
    })
    save_tasks()
    print(f'Task "{task}" added successfully!✅')
    print(f'Category: {category} | Priority: {priority["priority_label"]} | Due: {format_due_date(due_date)}')
    if summary != task:
        print(f'Summary: {summary}')


def view_tasks():
    if not tasks_list:
        print('No tasks found. Please add a task first.😒')
    else:
        print('=================Task List=================')
        for index, task in enumerate(tasks_list):
            print(f"{index + 1}. {task['task']} - {task['status']}")
            if task.get('category'):
                print(f"   Category: {task['category']} | Priority: {task['priority']['priority_label']} | Due: {format_due_date(task['due_date'])}")
            if task.get('summary') and task['summary'] != task['task']:
                print(f"   Summary: {task['summary']}")
        print('===========================================')


def mark_task_complete():
    if not tasks_list:
        print('No tasks found. Please add a task first.😒')
    else:
        view_tasks()
        try:
            task_number = int(input('Enter the task number to mark as complete: '))
        except ValueError:
            print('Please enter a number, not a letter.😒')
            return
        if 1 <= task_number <= len(tasks_list):
            tasks_list[task_number - 1]['status'] = 'Complete'
            save_tasks()
            print(f'Task "{tasks_list[task_number - 1]["task"]}" marked as complete!✅')
        else:
            print('Invalid task number. Please try again.😒')


def delete_task():
    if not tasks_list:
        print('No tasks found. Please add a task first.😒')
    else:
        view_tasks()
        try:
            task_number = int(input('Enter the task number to delete: '))
        except ValueError:
            print('Please enter a number, not a letter.😒')
            return
        if 1 <= task_number <= len(tasks_list):
            deleted_task = tasks_list.pop(task_number - 1)
            save_tasks()
            print(f'Task "{deleted_task["task"]}" deleted successfully!✅')
        else:
            print('Invalid task number. Please try again.😒')


# Function to display menu
def menu():
    while True:
        print('=================Main Menu  =================')
        print('1. Add Task')
        print('2. View Tasks')
        print('3. Mark Task as Complete')
        print('4. Delete Task')
        print('5. Exit')

        try:
            choices = int(input('Enter your choice: '))
        except ValueError:
            print('Please enter a number, not a letter.😒')
            continue
        if choices == 1:
            add_task()
        elif choices == 2:
            view_tasks()
        elif choices == 3:
            mark_task_complete()
        elif choices == 4:
            delete_task()
        elif choices == 5:
            print('Exiting the program. Goodbye!😁')
            sys.exit()
        else:
            print('Invalid choice and try again😒')


if __name__ == '__main__':
    load_tasks()
    menu()
