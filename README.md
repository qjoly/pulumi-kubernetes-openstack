## Pulumi Kubernetes Openstack Example

This example demonstrates how to deploy nodes for a Kubernetes cluster on Openstack using Pulumi.

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
