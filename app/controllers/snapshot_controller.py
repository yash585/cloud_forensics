from app.services.aws_snapshot import take_snapshot_and_download
from app.services.extractor import extract_memory_dump

def handle_snapshot(instance_id):
    """
    Controller that:
    1. Takes AWS snapshot
    2. Downloads the snapshot to local storage
    3. Extracts memory dump file (RAW/VMEM)
    """

    # Step 1: Create snapshot + download volume locally
    local_snapshot_file = take_snapshot_and_download(instance_id)

    if not local_snapshot_file:
        return {"status": "error", "message": "Failed to download snapshot"}

    # Step 2: Extract memory dump (raw memory file)
    dump_path = extract_memory_dump(local_snapshot_file)

    if not dump_path:
        return {"status": "error", "message": "Failed to extract memory dump"}

    return {
        "status": "success",
        "dump_path": dump_path,
        "message": "Snapshot created and memory dump extracted successfully"
    }
