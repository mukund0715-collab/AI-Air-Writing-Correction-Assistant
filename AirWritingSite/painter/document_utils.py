# document_utils.py

from pathlib import Path
from datetime import datetime
from .models import SavedSession


# Base folder of the Django project
BASE_DIR = Path(__file__).resolve().parent.parent

# Folder to store all session files
DOCS_FOLDER = BASE_DIR / "saved_docs"


def save_session_sentences(sentences):
    folder = Path(__file__).resolve().parent.parent / "saved_docs"
    folder.mkdir(exist_ok=True)

    filename = f"session_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    file_path = folder / filename

    # Join the list into a single string
    full_text_content = " ".join(sentences) 

    # 1. Write to File (Physical backup)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(full_text_content)

    # 2. Save to DB (Include the content now)
    SavedSession.objects.create(
        file_name=filename,
        file_path=str(file_path),
        content=full_text_content  # <--- PASS THE DATA HERE
    )

    print(f"SESSION SAVED → {file_path}")

def list_saved_sessions():
    """
    Return a sorted list of .txt files saved as session_*.txt
    """
    DOCS_FOLDER.mkdir(exist_ok=True)
    return sorted([f.name for f in DOCS_FOLDER.glob("session_*.txt")])


def read_session_file(filename):
    """
    Read the content of a given session file.
    Returns the content (str) or None if not found.
    """
    path = DOCS_FOLDER / filename
    if not path.exists():
        return None

    return path.read_text(encoding="utf-8")
