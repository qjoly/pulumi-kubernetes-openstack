<p align="center">
    <img src="https://avatars.githubusercontent.com/u/82603435?v=4" width="140px" alt="Helm LOGO"/>
</p>

<div align="center">

  [![Blog](https://img.shields.io/badge/Blog-blue?style=for-the-badge&logo=buymeacoffee&logoColor=white)](https://une-tasse-de.cafe/)
  [![Pulumi](https://img.shields.io/badge/Pulumi-8A3391?style=for-the-badge&logo=pulumi&logoColor=white)](https://www.pulumi.com/)
  [![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)](https://kubernetes.io/)
  [![Openstack](https://img.shields.io/badge/Openstack-%23f01742.svg?style=for-the-badge&logo=openstack&logoColor=white)](https://www.openstack.org/)

</div>

## Pulumi Kubernetes Openstack Example

This example demonstrates how to deploy nodes for a Kubernetes cluster on Openstack using Pulumi.

Note: By default, the values in the `Pulumi.yaml` use Infomaniak Openstack. You can change the values in the `Pulumi.yaml` file to match your Openstack configuration.

### Prerequisites

1. [Install Pulumi](https://www.pulumi.com/docs/get-started/install/)
2. [Install Python3](https://www.python.org/downloads/)
3. Create a virtual environment:
```bash
python3 -m venv venv
```
4. Install the required Python packages:
```bash
python3 -m pip install -r requirements.txt
```

### Running the Example

Login to your openstack account (horizon) and source the openstack rc file:
```bash
source openstack.rc
```

Create a new project using this template:
```bash
pulumi new https://github.com/qjoly/pulumi-kubernetes-openstack/tree/main
```

Run the pulumi program:
```bash
pulumi up
```

### Install Kubernetes cluster

Export the private key that can be used to connect to the nodes:

```bash
pulumi stack output nodes_keypair --show-secrets > nodes_keypair.pem
```

Send it to the admin node:

```bash
scp nodes_keypair.pem debian@$(pulumi stack output admin_external_ip):.ssh/id_rsa
ssh debian@$(pulumi stack output admin_external_ip) chmod 600 .ssh/id_rsa
```

*:warning: Note that you have to set the pulumi config passphrase to access content of the private key.*

Generate the inventory file:

```bash
pulumi stack output ip_addresses --json | python3 generate_inventory.py > inventory.ini
scp inventory.ini debian@$(pulumi stack output admin_external_ip):./inventory.ini
```

On the admin node, Create a virtual environment and install the required packages:

```bash
ssh debian@$(pulumi stack output admin_external_ip)
git clone https://github.com/kubernetes-sigs/kubespray && cd kubespray
cp -r inventory/sample/ ./inventory/pulumi-cluster
cp ~/inventory.ini ./inventory/pulumi-cluster/inventory.ini
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

```bash
ansible-playbook -i ./inventory/pulumi-cluster/inventory.ini -u debian --become --become-user=root cluster.yml
```

<details>
  <summary>All in one script</summary>

:warning: Only run this script if you are sure of what you are doing. :warning:

```bash
pulumi stack output nodes_keypair --show-secrets > nodes_keypair.pem
scp nodes_keypair.pem debian@$(pulumi stack output admin_external_ip):.ssh/id_rsa
ssh debian@$(pulumi stack output admin_external_ip) chmod 600 .ssh/id_rsa
pulumi stack output ip_addresses --json | python3 generate_inventory.py > inventory.ini
scp inventory.ini debian@$(pulumi stack output admin_external_ip):./inventory.ini
ssh debian@$(pulumi stack output admin_external_ip) \ '
  git clone https://github.com/kubernetes-sigs/kubespray && cd kubespray && \
  cp -r inventory/sample/ ./inventory/pulumi-cluster && \
  cp ~/inventory.ini ./inventory/pulumi-cluster/inventory.ini && \
  python3 -m venv venv && \
  source venv/bin/activate && \
  pip install -r requirements.txt && \
  ansible-playbook -i ./inventory/pulumi-cluster/inventory.ini -u debian --become --become-user=root cluster.yml'

CP_IP=$(pulumi stack output 'ip_addresses' | jq -r '."kube-controlplane"[0]')
ssh debian@$(pulumi stack output admin_external_ip) "mkdir -p .kube && ssh $CP_IP sudo cat /root/.kube/config > .kube/config && sed -i 's/127.0.0.1/$CP_IP/g' ~/.kube/config && echo 'Done'"
```

</details>

### Output of the Pulumi program

<a href="https://asciinema.org/a/P9JDxnpB8zNKDE7XHO9OOMBvD" target="_blank"><img src="https://asciinema.org/a/P9JDxnpB8zNKDE7XHO9OOMBvD.svg" /></a>


:warning: Note that the output of the pulumi program will be different as the resources are created dynamically.

### Destroy the resources

To destroy the resources created by the Pulumi program, run the following command:

```bash
pulumi destroy
```
