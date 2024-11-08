
# Define file-based storage for sent job IDs
import os


def get_user_sent_ids(user_id):
    file_path = f"sent_ids_{user_id}.txt"
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return set(file.read().splitlines())
    else:
        return set()

def save_user_sent_ids(user_id, sent_ids):
    file_path = f"sent_ids_{user_id}.txt"
    with open(file_path, 'w') as file:
        for job_id in sent_ids:
            file.write(f"{job_id}\n")
