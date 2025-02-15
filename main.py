from function import process_text

text = """
John has to buy the snacks for all of us. 
Also, John needs to submit the report by 5 pm.
David needs to buy mobile today  
"""

# Process text and get categorized tasks
categorized_tasks = process_text(text)

# Print structured tasks
for category, tasks in categorized_tasks.items():
    print(f"Category: {category}")
    for task in tasks:
        print(f"  Task: {task['task']}")
        print(f"  Person: {task['person'] if task['person'] else 'Unknown'}")
        print(f"  Deadline: {task['deadline'] if task['deadline'] else 'No deadline specified'}")
        print()