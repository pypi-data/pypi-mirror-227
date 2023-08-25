'''
# Terraform CDK tls Provider ~> 4.0

This repo builds and publishes the Terraform tls Provider bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-tls](https://www.npmjs.com/package/@cdktf/provider-tls).

`npm install @cdktf/provider-tls`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-tls](https://pypi.org/project/cdktf-cdktf-provider-tls).

`pipenv install cdktf-cdktf-provider-tls`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Tls](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Tls).

`dotnet add package HashiCorp.Cdktf.Providers.Tls`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-tls](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-tls).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-tls</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-tls-go`](https://github.com/cdktf/cdktf-provider-tls-go) package.

`go get github.com/cdktf/cdktf-provider-tls-go/tls`

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-tls).

## Versioning

This project is explicitly not tracking the Terraform tls Provider version 1:1. In fact, it always tracks `latest` of `~> 4.0` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by generating the [provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [Terraform CDK](https://cdk.tf)
* [Terraform tls Provider](https://registry.terraform.io/providers/hashicorp/tls/4.0.0)

  * This links to the minimum version being tracked, you can find the latest released version [in our releases](https://github.com/cdktf/cdktf-provider-tls/releases)
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
    "cert_request",
    "data_tls_certificate",
    "data_tls_public_key",
    "locally_signed_cert",
    "private_key",
    "provider",
    "self_signed_cert",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import cert_request
from . import data_tls_certificate
from . import data_tls_public_key
from . import locally_signed_cert
from . import private_key
from . import provider
from . import self_signed_cert
