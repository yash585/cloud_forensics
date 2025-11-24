from app.services.aws_snapshot import take_snapshot_and_download
from app.services.extractor import extract_memory_dump

def handle_snapshot(instance_id):
    local_snapshot_file = take_snapshot_and_download(instance_id)

    if not local_snapshot_file:
        return {"status": "error", "message": "Failed to download snapshot"}

    dump_path = extract_memory_dump(local_snapshot_file)
    print(dump_path)

    if not dump_path:
        return {"status": "error", "message": "Failed to extract memory dump"}

    return {
        "status": "success",
        "dump_path": dump_path,
        "message": "Snapshot created and memory dump extracted successfully"
    }
