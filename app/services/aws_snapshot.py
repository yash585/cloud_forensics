import boto3
import time
import os
from botocore.exceptions import ClientError
import yaml


def take_snapshot_and_download(instance_id):

    CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../config/config.yaml")

    with open(CONFIG_PATH, "r") as f:
        cfg = yaml.safe_load(f)

    aws_key    = cfg["aws"]["access_key"]
    aws_secret = cfg["aws"]["secret_key"]
    aws_region = cfg["aws"]["region"]

    ec2 = boto3.client(
        "ec2",
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret,
        region_name=aws_region
    )

    ebs = boto3.client(
        "ebs",
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret,
        region_name=aws_region
    )

    try:
        # STEP 0: Get root volume
        instance = ec2.describe_instances(InstanceIds=[instance_id])
        inst = instance["Reservations"][0]["Instances"][0]

        root_device = inst["RootDeviceName"]

        root_volume = None
        for dev in inst["BlockDeviceMappings"]:
            if dev["DeviceName"] == root_device:
                root_volume = dev["Ebs"]["VolumeId"]
                break

        if not root_volume:
            raise Exception("Unable to locate root EBS volume")

        print(f"[+] Root volume: {root_volume}")

        # STEP 1: Create REAL EC2 snapshot
        print("[+] Creating snapshot using EC2 API...")
        snap_resp = ec2.create_snapshot(
            VolumeId=root_volume,
            Description=f"Memory forensics snapshot of {instance_id}"
        )

        snapshot_id = snap_resp["SnapshotId"]
        print(f"[+] Snapshot started: {snapshot_id}")

        # STEP 2: Wait until completed
        print("[+] Waiting for snapshot to complete...")
        waiter = ec2.get_waiter('snapshot_completed')
        waiter.wait(SnapshotIds=[snapshot_id])
        print("[+] Snapshot completed.")

        # STEP 3: Use EBS direct API to read blocks
        return download_snapshot(snapshot_id, aws_key, aws_secret, aws_region)

    except ClientError as e:
        print("AWS ERROR:", str(e))
        return None



def download_snapshot(snapshot_id, aws_key, aws_secret, aws_region):

    ebs = boto3.client(
        "ebs",
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret,
        region_name=aws_region
    )

    try:
        block_list = ebs.list_snapshot_blocks(SnapshotId=snapshot_id)
    except Exception as e:
        print("ERROR listing blocks:", e)
        return None

    output_path = os.path.join("memory_dumps", f"{snapshot_id}.raw")
    os.makedirs("memory_dumps", exist_ok=True)

    print(f"[+] Downloading snapshot blocks to {output_path}")

    BLOCK_SIZE = 512 * 1024  # 512KiB

    with open(output_path, "wb") as f:
        for block in block_list.get("Blocks", []):
            idx = block["BlockIndex"]

            data = ebs.get_snapshot_block(
                SnapshotId=snapshot_id,
                BlockIndex=idx,
                BlockToken=block["BlockToken"]
            )

            f.seek(idx * BLOCK_SIZE)
            f.write(data["BlockData"].read())

    print("[+] Snapshot downloaded successfully.")
    return output_path
