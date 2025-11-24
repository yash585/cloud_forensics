import os
import shutil

def extract_memory_dump(disk_image_path):

    # Example: memory.raw, vmemory.dmp, or winpmem.raw
    possible_names = ["memory.raw", "memory.dmp", "vmem.raw", "dump.raw"]

    # Directory where dumped memory files are stored
    output_dir = "memory_dumps"
    os.makedirs(output_dir, exist_ok=True)

    # Case 1: If the downloaded file *is already* a memory dump
    filename = os.path.basename(disk_image_path)
    lower = filename.lower()
    
    if lower.endswith(".raw") or lower.endswith(".dmp"):
        # Final dump path to store the memory dump
        final_dump_path = os.path.join(output_dir, filename)
        
        # Check if the source and destination are the same file
        if os.path.abspath(disk_image_path) == os.path.abspath(final_dump_path):
            print(f"Source and destination are the same file: {disk_image_path}. Skipping copy.")
            return final_dump_path  # Return the path without copying

        # Copy the file if source and destination are different
        print(f"Copying {disk_image_path} to {final_dump_path}")
        shutil.copy(disk_image_path, final_dump_path)
        print("\n\n\nhhhheeeeeeeellllllooooooooooooo\n\n\n")
        return final_dump_path

    # Case 2: (Optional future) If raw disk image contains dump internally
    # Placeholder return for now
    return None
