import boto3
import time
import os
from botocore.exceptions import ClientError

def take_snapshot_and_download(instance_id):
    """
    1. Creates an EBS snapshot from the given EC2 instance.
    2. Waits until snapshot is ready.
    3. Downloads the snapshot to local storage.
    """

    ec2 = boto3.client("ec2")

    try:
        # Get root volume ID of the instance
        volumes = ec2.describe_instances(InstanceIds=[instance_id])
        root_volume = volumes["Reservations"][0]["Instances"][0]["BlockDeviceMappings"][0]["Ebs"]["VolumeId"]

        # Step 1: Create snapshot
        snapshot = ec2.create_snapshot(
            VolumeId=root_volume,
            Description=f"Memory forensics snapshot for {instance_id}"
        )
        snapshot_id = snapshot["SnapshotId"]

        print(f"[+] Snapshot created: {snapshot_id}")

        # Step 2: Wait for snapshot to complete
        print("[+] Waiting for snapshot to finish...")
        waiter = ec2.get_waiter("snapshot_completed")
        waiter.wait(SnapshotIds=[snapshot_id])

        print("[+] Snapshot ready.")

        # Step 3: Download snapshot using EBS direct APIs
        return download_snapshot(snapshot_id)

    except ClientError as e:
        print("AWS ERROR:", str(e))
        return None


def download_snapshot(snapshot_id):
    """
    Downloads snapshot blocks using EBS direct APIs.
    Saves a raw file locally and returns its path.
    """
    ebs = boto3.client("ebs")

    try:
        snapshot = ebs.get_snapshot_block_list(SnapshotId=snapshot_id)
    except Exception as e:
        print("ERROR: Unable to list blocks:", e)
        return None

    output_path = os.path.join("memory_dumps", f"{snapshot_id}.raw")
    os.makedirs("memory_dumps", exist_ok=True)

    print(f"[+] Downloading snapshot blocks to {output_path}")

    with open(output_path, "wb") as f:
        for block in snapshot.get("Blocks", []):
            block_index = block["BlockIndex"]

            block_data = ebs.get_snapshot_block(
                SnapshotId=snapshot_id,
                BlockIndex=block_index,
                BlockToken=block["BlockToken"]
            )

            f.seek(block_index * 512 * 256)  # 512 KB blocks
            f.write(block_data["BlockData"])

    print("[+] Snapshot downloaded successfully.")
    return output_path
