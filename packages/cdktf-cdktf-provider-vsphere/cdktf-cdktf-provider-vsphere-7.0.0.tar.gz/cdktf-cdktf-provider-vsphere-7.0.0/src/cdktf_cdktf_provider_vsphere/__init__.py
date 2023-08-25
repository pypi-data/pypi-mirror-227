'''
# Terraform CDK vsphere Provider ~> 2.2

This repo builds and publishes the Terraform vsphere Provider bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-vsphere](https://www.npmjs.com/package/@cdktf/provider-vsphere).

`npm install @cdktf/provider-vsphere`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-vsphere](https://pypi.org/project/cdktf-cdktf-provider-vsphere).

`pipenv install cdktf-cdktf-provider-vsphere`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Vsphere](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Vsphere).

`dotnet add package HashiCorp.Cdktf.Providers.Vsphere`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-vsphere](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-vsphere).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-vsphere</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-vsphere-go`](https://github.com/cdktf/cdktf-provider-vsphere-go) package.

`go get github.com/cdktf/cdktf-provider-vsphere-go/vsphere`

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-vsphere).

## Versioning

This project is explicitly not tracking the Terraform vsphere Provider version 1:1. In fact, it always tracks `latest` of `~> 2.2` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by generating the [provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [Terraform CDK](https://cdk.tf)
* [Terraform vsphere Provider](https://registry.terraform.io/providers/hashicorp/vsphere/2.2.0)

  * This links to the minimum version being tracked, you can find the latest released version [in our releases](https://github.com/cdktf/cdktf-provider-vsphere/releases)
* [Terraform Engine](https://terraform.io)

If there are breaking changes (backward incompatible) in any of the above, the major version of this project will be bumped.

## Features / Issues / Bugs

Please report bugs and issues to the [terraform cdk](https://cdk.tf) project:

* [Create bug report](https://cdk.tf/bug)
* [Create feature request](https://cdk.tf/feature)

## Contributing

### projen

This is mostly based on [projen](https://github.com/eladb/projen), which takes care of generating the entire repository.

### cdktf-provider-project based on projen

There's a custom [project builder](https://github.com/hashicorp/cdktf-provider-project) which encapsulate the common settings for all `cdktf` providers.

### Provider Version

The provider version can be adjusted in [./.projenrc.js](./.projenrc.js).

### Repository Management

The repository is managed by [Repository Manager](https://github.com/hashicorp/cdktf-repository-manager/)
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

__all__ = [
    "compute_cluster",
    "compute_cluster_host_group",
    "compute_cluster_vm_affinity_rule",
    "compute_cluster_vm_anti_affinity_rule",
    "compute_cluster_vm_dependency_rule",
    "compute_cluster_vm_group",
    "compute_cluster_vm_host_rule",
    "content_library",
    "content_library_item",
    "custom_attribute",
    "data_vsphere_compute_cluster",
    "data_vsphere_compute_cluster_host_group",
    "data_vsphere_content_library",
    "data_vsphere_content_library_item",
    "data_vsphere_custom_attribute",
    "data_vsphere_datacenter",
    "data_vsphere_datastore",
    "data_vsphere_datastore_cluster",
    "data_vsphere_distributed_virtual_switch",
    "data_vsphere_dynamic",
    "data_vsphere_folder",
    "data_vsphere_host",
    "data_vsphere_host_pci_device",
    "data_vsphere_host_thumbprint",
    "data_vsphere_license",
    "data_vsphere_network",
    "data_vsphere_ovf_vm_template",
    "data_vsphere_resource_pool",
    "data_vsphere_role",
    "data_vsphere_storage_policy",
    "data_vsphere_tag",
    "data_vsphere_tag_category",
    "data_vsphere_vapp_container",
    "data_vsphere_virtual_machine",
    "data_vsphere_vmfs_disks",
    "datacenter",
    "datastore_cluster",
    "datastore_cluster_vm_anti_affinity_rule",
    "distributed_port_group",
    "distributed_virtual_switch",
    "dpm_host_override",
    "drs_vm_override",
    "entity_permissions",
    "file",
    "folder",
    "ha_vm_override",
    "host",
    "host_port_group",
    "host_virtual_switch",
    "license_resource",
    "nas_datastore",
    "provider",
    "resource_pool",
    "role",
    "storage_drs_vm_override",
    "tag",
    "tag_category",
    "vapp_container",
    "vapp_entity",
    "virtual_disk",
    "virtual_machine",
    "virtual_machine_snapshot",
    "vm_storage_policy",
    "vmfs_datastore",
    "vnic",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import compute_cluster
from . import compute_cluster_host_group
from . import compute_cluster_vm_affinity_rule
from . import compute_cluster_vm_anti_affinity_rule
from . import compute_cluster_vm_dependency_rule
from . import compute_cluster_vm_group
from . import compute_cluster_vm_host_rule
from . import content_library
from . import content_library_item
from . import custom_attribute
from . import data_vsphere_compute_cluster
from . import data_vsphere_compute_cluster_host_group
from . import data_vsphere_content_library
from . import data_vsphere_content_library_item
from . import data_vsphere_custom_attribute
from . import data_vsphere_datacenter
from . import data_vsphere_datastore
from . import data_vsphere_datastore_cluster
from . import data_vsphere_distributed_virtual_switch
from . import data_vsphere_dynamic
from . import data_vsphere_folder
from . import data_vsphere_host
from . import data_vsphere_host_pci_device
from . import data_vsphere_host_thumbprint
from . import data_vsphere_license
from . import data_vsphere_network
from . import data_vsphere_ovf_vm_template
from . import data_vsphere_resource_pool
from . import data_vsphere_role
from . import data_vsphere_storage_policy
from . import data_vsphere_tag
from . import data_vsphere_tag_category
from . import data_vsphere_vapp_container
from . import data_vsphere_virtual_machine
from . import data_vsphere_vmfs_disks
from . import datacenter
from . import datastore_cluster
from . import datastore_cluster_vm_anti_affinity_rule
from . import distributed_port_group
from . import distributed_virtual_switch
from . import dpm_host_override
from . import drs_vm_override
from . import entity_permissions
from . import file
from . import folder
from . import ha_vm_override
from . import host
from . import host_port_group
from . import host_virtual_switch
from . import license_resource
from . import nas_datastore
from . import provider
from . import resource_pool
from . import role
from . import storage_drs_vm_override
from . import tag
from . import tag_category
from . import vapp_container
from . import vapp_entity
from . import virtual_disk
from . import virtual_machine
from . import virtual_machine_snapshot
from . import vm_storage_policy
from . import vmfs_datastore
from . import vnic
