import re
import spacy
from collections import defaultdict


nlp = spacy.load("en_core_web_sm")

# Function to preprocess text
def preprocess_text(text):
    """Cleans text by removing special characters and tokenizing sentences."""
    text = re.sub(r'[^a-zA-Z0-9 .]', '', text) 
    return nlp(text)

def extract_tasks(doc):
    """Identifies task-related sentences based on heuristic rules."""
    tasks = []
    for sent in doc.sents:
        verbs = [token.lemma_ for token in sent if token.pos_ == "VERB"]
        if any(v in ["buy", "submit", "clean", "schedule", "review"] for v in verbs):
            tasks.append(sent.text)
    return tasks

def extract_task_details(tasks):
    """Extracts person and deadline if present in task-related sentences."""
    task_details = []
    for task in tasks:
        doc = nlp(task)
        person = None
        deadline = None
        
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                person = ent.text
            elif ent.label_ in ["TIME", "DATE"]:
                deadline = ent.text
        
        task_details.append({"task": task, "person": person, "deadline": deadline})
    return task_details


categories = {
    "Shopping": ["buy", "purchase"],
    "Work": ["submit", "review", "write"],
    "Cleaning": ["clean", "wash"]
}

def categorize_task(task_details):
    """Categorizes tasks based on keywords."""
    categorized_tasks = defaultdict(list)
    for task in task_details:
        category = "Other"
        for cat, keywords in categories.items():
            if any(kw in task["task"].lower() for kw in keywords):
                category = cat
                break
        categorized_tasks[category].append(task)
    return categorized_tasks

def process_text(text):
    """Processes text to extract and categorize tasks."""
    doc = preprocess_text(text)
    tasks = extract_tasks(doc)
    task_details = extract_task_details(tasks)
    categorized_tasks = categorize_task(task_details)
    return categorized_tasks
