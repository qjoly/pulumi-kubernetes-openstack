import sys
import json


def convert_to_ini(json_data):
    ini_content = "[all]\n"
    control_plane_count = 1
    worker_count = 1

    for node_type, ips in json_data.items():
        for ip in ips:
            if node_type == "kube-controlplane":
                ini_content += (
                    f"control-plane-{control_plane_count} ansible_host={ip}\n"
                )
                control_plane_count += 1
            elif node_type == "kube-node":
                ini_content += f"worker-{worker_count} ansible_host={ip}\n"
                worker_count += 1

    ini_content += "\n"
    ini_content += "[kube_control_plane]\n"
    for i in range(1, control_plane_count):
        ini_content += f"control-plane-{i}\n"

    ini_content += "\n"
    ini_content += "[etcd]\n"
    for i in range(1, control_plane_count):
        ini_content += f"control-plane-{i}\n"

    ini_content += "\n"
    ini_content += "[kube_node]\n"
    for i in range(1, control_plane_count):
        ini_content += f"control-plane-{i}\n"
    for i in range(1, worker_count):
        ini_content += f"worker-{i}\n"

    ini_content += "\n"
    ini_content += "[calico_rr]\n\n"

    ini_content += "\n"
    ini_content += "[k8s_cluster:children]\n"
    ini_content += "kube_control_plane\n"
    ini_content += "kube_node\n"
    ini_content += "calico_rr\n"

    return ini_content


def main():
    # Read JSON data from stdin
    json_data = json.load(sys.stdin)

    # Convert JSON to INI
    ini_content = convert_to_ini(json_data)

    # Write the INI content to stdout
    sys.stdout.write(ini_content)


if __name__ == "__main__":
    main()
