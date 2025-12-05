import os
import shutil
from pathlib import Path

# Folders to organize
DOWNLOADS_FOLDER = Path.home() / "Downloads"
DESKTOP_FOLDER = Path.home() / "Desktop"

FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Audio": [".mp3", ".wav", ".aac", ".m4a"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".pptx", ".xlsx", ".csv"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".js", ".ts", ".html", ".css", ".cpp", ".c", ".java", ".ipynb"],
}


def create_category_folders(base_path: Path):
    """Create category folders (Images, Documents, etc.) inside the base path if missing."""
    for category in FILE_TYPES.keys():
        folder_path = base_path / category
        folder_path.mkdir(exist_ok=True)
    misc_path = base_path / "Misc"
    misc_path.mkdir(exist_ok=True)


def categorize_and_move_files(base_path: Path):
    """Move files in base_path into their respective category folders."""
    for item in base_path.iterdir():
        # Skip directories (our category folders etc.)
        if item.is_dir():
            continue

        extension = item.suffix.lower()
        moved = False

        for category, extensions in FILE_TYPES.items():
            if extension in extensions:
                target_folder = base_path / category
                target_path = target_folder / item.name

                # Handle name conflicts
                if target_path.exists():
                    target_path = handle_name_conflict(target_folder, item.name)

                shutil.move(str(item), str(target_path))
                moved = True
                break

        if not moved:
            misc_folder = base_path / "Misc"
            target_path = misc_folder / item.name

            if target_path.exists():
                target_path = handle_name_conflict(misc_folder, item.name)

            shutil.move(str(item), str(target_path))


def handle_name_conflict(folder: Path, filename: str) -> Path:
    """If a file with same name exists, append a number (1), (2), etc."""
    name, ext = os.path.splitext(filename)
    counter = 1
    new_name = f"{name} ({counter}){ext}"
    new_path = folder / new_name

    while new_path.exists():
        counter += 1
        new_name = f"{name} ({counter}){ext}"
        new_path = folder / new_name

    return new_path


def organize_folder(path: Path, label: str):
    print(f"\n📂 Organizing {label} at: {path}")
    if not path.exists():
        print(f"⚠️ {label} folder not found, skipping.")
        return

    create_category_folders(path)
    categorize_and_move_files(path)
    print(f"✅ {label} organized successfully!")


def main():
    print("✨ CleanDesk - Desktop & Downloads Organizer ✨")
    organize_folder(DOWNLOADS_FOLDER, "Downloads")
    organize_folder(DESKTOP_FOLDER, "Desktop")
    print("\nAll done. Enjoy your clean workspace! 😎")


if __name__ == "__main__":
    main()
