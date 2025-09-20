import os
import sys
from kivy.utils import platform
from pathlib import Path

def get_db_path():
    """Get the appropriate database path for the current platform."""
    try:
        if platform == 'android':
            from android.storage import primary_external_storage_path
            from android.permissions import request_permissions, Permission

            # Request storage permissions (for public Documents access)
            request_permissions([
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE
            ])

            # Store DB in a public, easy to access path: Documents/KickerApp
            docs_dir = os.path.join(primary_external_storage_path(), 'Documents')
            data_dir = os.path.join(docs_dir, 'KickerApp')
        else:
            # For desktop platforms
            data_dir = os.path.join(os.path.expanduser('~'), '.kicker_app')
        
        # Create the directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Return the full path to the database file
        db_path = os.path.join(data_dir, 'kicker.db')
        print(f"Database path: {db_path}", file=sys.stderr)
        return db_path
        
    except Exception as e:
        print(f"Error getting database path: {str(e)}", file=sys.stderr)
        # Fallback to a safe path if there's an error
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kicker.db')
# Database configuration
DB_DATEI = get_db_path()
TABELLE = "spiele"


class text_parameter:
    titel = "Kicker Ergebnis eintragen"
