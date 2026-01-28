from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # Start the air-writing script
    path('run-local/', views.run_script, name='run_local'),

    # ---------------------------------------------------
    # NEW: Saved files system (DATABASE BASED)
    # ---------------------------------------------------
    path('saved-files/', views.saved_files, name='saved_files'),

    # View file (using file_id, NOT filename)
    path("file/<int:file_id>/view/", views.view_file, name="view_file"),

    # Download file
    path("file/<int:file_id>/download/", views.download_file, name="download_file"),

    # Delete file
    path("file/<int:file_id>/delete/", views.delete_file, name="delete_file"),

    # Rename file
    path("file/<int:file_id>/rename/", views.rename_file, name="rename_file"),
]
