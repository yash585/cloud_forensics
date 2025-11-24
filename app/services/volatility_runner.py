import subprocess
import os

def run_plugins(dump_path):

    if not os.path.exists(dump_path):
        print("[-] Memory dump not found:", dump_path)
        return None

    output_dir = "analysis_output"
    os.makedirs(output_dir, exist_ok=True)

    # Define plugins to run
    plugins = [
        "windows.pslist",
        "windows.pstree",
        "windows.netscan",
        "windows.cmdline",
        "windows.pslist.PsList"
        "windows.pstree.PsTree",
    ]

    results = {}

    for plugin in plugins:
        try:
            print(f"[+] Running plugin: {plugin}")

            #volatility
            cmd = [
                "python", "../../volatility3/vol.py",
                "-f", dump_path,
                plugin
            ]

            # Run the command and capture output
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            decoded = output.decode("utf-8", errors="ignore")

            # Save raw output to file
            plugin_name = plugin.replace(".", "_")  # windows.pslist → windows_pslist
            raw_file = os.path.join(output_dir, f"{plugin_name}.txt")

            with open(raw_file, "w") as f:
                f.write(decoded)

            results[plugin] = decoded

        except subprocess.CalledProcessError as e:
            print(f"[-] Error running {plugin}: {e.output.decode(errors='ignore')}")
            results[plugin] = None

    return results


run_plugins("../../memory_dumps/snap-0adee022bac8c1186.raw")