import os
import shutil
from pathlib import Path

# Mapping of file extensions to target folder names
EXTENSIONS_MAP = {
    'Images': ['.jpeg', '.jpg', '.png', '.gif', '.svg', '.webp'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.csv'],
    'Archives': ['.zip', '.tar', '.gz', '.rar'],
    'Installers': ['.dmg', '.pkg', '.exe', '.msi'],
    'Code': ['.py', '.js', '.html', '.css', '.json']
}

def clean_directory(target_dir: str):
    """Organizes files in the target directory into designated folders by extension."""
    target_path = Path(target_dir)
    if not target_path.exists():
        print(f"Error: Directory '{target_dir}' does not exist.")
        return

    moved_count = 0
    for item in target_path.iterdir():
        if item.is_file() and not item.name.startswith('.'):
            file_ext = item.suffix.lower()
            
            # Find matching category
            category = "Other"
            for folder_name, extensions in EXTENSIONS_MAP.items():
                if file_ext in extensions:
                    category = folder_name
                    break
            
            # Create folder if it doesn't exist
            category_path = target_path / category
            category_path.mkdir(exist_ok=True)
            
            # Move file
            try:
                shutil.move(str(item), str(category_path / item.name))
                moved_count += 1
                print(f"Moved: {item.name} -> {category}/")
            except Exception as e:
                print(f"Failed to move {item.name}: {e}")
                
    print(f"\n✅ Cleanup complete! Organized {moved_count} files.")

if __name__ == "__main__":
    desktop_path = os.path.expanduser("~/Desktop")
    print(f"Cleaning exactly: {desktop_path}...")
    clean_directory(desktop_path)
