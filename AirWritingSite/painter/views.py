from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import subprocess
import sys
import os

from django.http import Http404, FileResponse
from .models import SavedSession
from . import document_utils


# ====================================================
# ORIGINAL YOUR CODE (UNCHANGED)
# ====================================================

def home(request):
    return render(request, 'painter/index.html')


def run_script(request):
    try:
        python_executable = sys.executable
        subprocess.Popen([python_executable, '-m', 'painter.main'])
        return redirect(reverse('home'))
    except Exception as e:
        print(f"CRITICAL: Failed to launch main.py. Error: {e}")
        return redirect(reverse('home'))


# ====================================================
# NEW — DATABASE-BASED FILE SYSTEM
# ====================================================

def saved_files(request):
    """
    List all saved sessions from the database.
    """
    files = SavedSession.objects.order_by('-created_at')
    return render(request, "painter/saved_files.html", {"files": files})


def view_file(request, file_id):
    """
    Open and read a specific saved file from DB entry.
    """
    try:
        file = SavedSession.objects.get(id=file_id)
    except SavedSession.DoesNotExist:
        raise Http404("File not found")

    try:
        with open(file.file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except:
        content = "(Unable to read file)"

    lines = content.splitlines()
    return render(
        request,
        "painter/view_file.html",
        {"file": file, "lines": lines},
    )


def download_file(request, file_id):
    """
    Download the saved text file.
    """
    try:
        file = SavedSession.objects.get(id=file_id)
        return FileResponse(open(file.file_path, "rb"), as_attachment=True, filename=file.file_name)
    except:
        raise Http404("File not found")


def delete_file(request, file_id):
    """
    Delete file from folder and delete DB entry.
    """
    try:
        file = SavedSession.objects.get(id=file_id)
    except SavedSession.DoesNotExist:
        raise Http404("File not found")

    try:
        os.remove(file.file_path)
    except:
        pass  # file already deleted

    file.delete()
    return redirect("saved_files")


def rename_file(request, file_id):
    if request.method == "POST":
        file_obj = get_object_or_404(SavedSession, id=file_id)
        new_name = request.POST.get('new_name')
        
        if new_name:
            # Optional: Ensure it ends with .txt if your system relies on it
            if not new_name.endswith('.txt'):
                new_name += '.txt'
                
            file_obj.file_name = new_name
            file_obj.save()
            
            # TODO: If you want to rename the ACTUAL physical file on disk, 
            # you would add os.rename() logic here. 
            # For now, we just rename the database entry.

    return redirect('saved_files')
