import os
import shutil

def extract_memory_dump(disk_image_path):
    """
    Extracts the memory dump from the downloaded EBS snapshot.
    For simplicity, this version assumes:
      - The memory dump file exists inside the disk image folder
      - Or the raw file *is itself* the dump (most cloud forensic workflows)

    Real-world extraction may involve mounting the raw disk,
    but this is the minimal expected version for your project structure.
    """

    # In many cloud workflows, the snapshot already contains the memory dump
    # Example: memory.raw, vmemory.dmp, or winpmem.raw
    possible_names = ["memory.raw", "memory.dmp", "vmem.raw", "dump.raw"]

    # Directory where dumped memory files are stored
    output_dir = "memory_dumps"
    os.makedirs(output_dir, exist_ok=True)

    # Case 1: If the downloaded file *is already* a memory dump
    filename = os.path.basename(disk_image_path)
    lower = filename.lower()
    if lower.endswith(".raw") or lower.endswith(".dmp"):
        # Save a copy as the final dump
        final_dump_path = os.path.join(output_dir, filename)
        shutil.copy(disk_image_path, final_dump_path)
        return final_dump_path

    # Case 2: (Optional future) If raw disk image contains dump internally
    # Placeholder return for now
    return None
