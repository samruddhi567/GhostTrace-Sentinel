import os
from pathlib import Path

def get_project_code_content(project_path, target_extensions=None):
    """
    Scans a folder for specific file types and returns their content as a dictionary.
    
    :param project_path: Path to the GhostTrace project folder
    :param target_extensions: List of extensions to scan (e.g., ['.py', '.html', '.css'])
    :return: Dictionary where { filename: file_content }
    """
    if target_extensions is None:
        target_extensions = ['.py', '.html', '.css']
        
    code_snapshot = {}
    path_obj = Path(project_path)

    print(f"📂 Scanning files in: {project_path}")

    # .rglob("*") searches all subfolders recursively
    for file_path in path_obj.rglob("*"):
        if file_path.suffix in target_extensions:
            try:
                # Read the actual code inside the file
                content = file_path.read_text(encoding='utf-8')
                # Store it with a relative path for the AI to identify it
                relative_name = file_path.relative_to(project_path)
                code_snapshot[str(relative_name)] = content
                print(f"  ✅ Read: {relative_name}")
            except Exception as e:
                print(f"  ⚠️ Could not read {file_path.name}: {e}")

    return code_snapshot

# --- FOR TESTING ---
if __name__ == "__main__":
    # Point this to your GhostTrace folder
    MY_DIR = r"C:\Users\samru\Desktop\GhostTrace"
    results = get_project_code_content(MY_DIR)
    
    print(f"\n🚀 Total files captured: {len(results)}")