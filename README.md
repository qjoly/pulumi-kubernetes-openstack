<p align="center">
    <img src="https://avatars.githubusercontent.com/u/82603435?v=4" width="140px" alt="Helm LOGO"/>
</p>

<div align="center">

  [![Blog](https://img.shields.io/badge/Blog-blue?style=for-the-badge&logo=buymeacoffee&logoColor=white)](https://une-tasse-de.cafe/)
  [![Pulumi](https://img.shields.io/badge/Pulumi-8A3391?style=for-the-badge&logo=pulumi&logoColor=white)](https://www.pulumi.com//)
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
