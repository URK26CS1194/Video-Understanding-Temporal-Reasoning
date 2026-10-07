import os
import zipfile

def make_zip(source_dir: str, output_zip: str):
    """Packages source_dir into a clean zip file, skipping caches and large raw files."""
    excluded_names = {
        "__pycache__", ".git", ".pytest_cache", ".DS_Store", "Thumbs.db",
        "video_temporal_reasoning.zip", "test_data.db"
    }
    excluded_extensions = {".pyc", ".pyo", ".pyd"}

    print(f"Creating zip archive: {output_zip}")
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zip_out:
        for root, dirs, files in os.walk(source_dir):
            # Modify dirs in-place to avoid recursing into excluded directories
            dirs[:] = [d for d in dirs if d not in excluded_names]

            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if file in excluded_names or ext in excluded_extensions:
                    continue
                
                full_path = os.path.join(root, file)
                # Compute relative path inside the zip file
                rel_path = os.path.relpath(full_path, os.path.dirname(source_dir))
                zip_out.write(full_path, rel_path)
                print(f"  Added: {rel_path}")

    print(f"Successfully created zip archive: {output_zip} ({os.path.getsize(output_zip):,} bytes)")

if __name__ == "__main__":
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(repo_dir)
    target_zip = os.path.join(parent_dir, "video_temporal_reasoning.zip")
    make_zip(repo_dir, target_zip)
