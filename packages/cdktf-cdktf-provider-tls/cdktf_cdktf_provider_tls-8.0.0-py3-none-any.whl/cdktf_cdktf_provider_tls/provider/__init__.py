'''
# `provider`

Refer to the Terraform Registory for docs: [`tls`](https://registry.terraform.io/providers/hashicorp/tls/4.0.4/docs).
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

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class TlsProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-tls.provider.TlsProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/tls/4.0.4/docs tls}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        alias: typing.Optional[builtins.str] = None,
        proxy: typing.Optional[typing.Union["TlsProviderProxy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/tls/4.0.4/docs tls} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.0.4/docs#alias TlsProvider#alias}
        :param proxy: proxy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.0.4/docs#proxy TlsProvider#proxy}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf8a72a2002ea12c9852076c3248eeb6ceaf28ea8e879a2296ddbf44c430bf58)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = TlsProviderConfig(alias=alias, proxy=proxy)

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetProxy")
    def reset_proxy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxy", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyInput")
    def proxy_input(self) -> typing.Optional["TlsProviderProxy"]:
        return typing.cast(typing.Optional["TlsProviderProxy"], jsii.get(self, "proxyInput"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eae8f1b5149aa2f09f7c1fe4512ad7ee4ee50de0749b8a1fd67f9985434ee9a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value)

    @builtins.property
    @jsii.member(jsii_name="proxy")
    def proxy(self) -> typing.Optional["TlsProviderProxy"]:
        return typing.cast(typing.Optional["TlsProviderProxy"], jsii.get(self, "proxy"))

    @proxy.setter
    def proxy(self, value: typing.Optional["TlsProviderProxy"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55307b57edc3a31452806f5213cdf453dae0931974131ffbe3c0ddfabe0005cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxy", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-tls.provider.TlsProviderConfig",
    jsii_struct_bases=[],
    name_mapping={"alias": "alias", "proxy": "proxy"},
)
class TlsProviderConfig:
    def __init__(
        self,
        *,
        alias: typing.Optional[builtins.str] = None,
        proxy: typing.Optional[typing.Union["TlsProviderProxy", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.0.4/docs#alias TlsProvider#alias}
        :param proxy: proxy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.0.4/docs#proxy TlsProvider#proxy}
        '''
        if isinstance(proxy, dict):
            proxy = TlsProviderProxy(**proxy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7efaf0d00d51c1fa807496879c1cb56b50bbca1433c4ad9a92dbaa80f57a323)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument proxy", value=proxy, expected_type=type_hints["proxy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alias is not None:
            self._values["alias"] = alias
        if proxy is not None:
            self._values["proxy"] = proxy

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.0.4/docs#alias TlsProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy(self) -> typing.Optional["TlsProviderProxy"]:
        '''proxy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.0.4/docs#proxy TlsProvider#proxy}
        '''
        result = self._values.get("proxy")
        return typing.cast(typing.Optional["TlsProviderProxy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TlsProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-tls.provider.TlsProviderProxy",
    jsii_struct_bases=[],
    name_mapping={
        "from_env": "fromEnv",
        "password": "password",
        "url": "url",
        "username": "username",
    },
)
class TlsProviderProxy:
    def __init__(
        self,
        *,
        from_env: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password: typing.Optional[builtins.str] = None,
        url: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param from_env: When ``true`` the provider will discover the proxy configuration from environment variables. This is based upon ```http.ProxyFromEnvironment`` <https://pkg.go.dev/net/http#ProxyFromEnvironment>`_ and it supports the same environment variables (default: ``true``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.0.4/docs#from_env TlsProvider#from_env}
        :param password: Password used for Basic authentication against the Proxy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.0.4/docs#password TlsProvider#password}
        :param url: URL used to connect to the Proxy. Accepted schemes are: ``http``, ``https``, ``socks5``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.0.4/docs#url TlsProvider#url}
        :param username: Username (or Token) used for Basic authentication against the Proxy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.0.4/docs#username TlsProvider#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ea50a8088ea8dd808b035d9c72caf92ce75f4311275c65fa60feb517b4ea829)
            check_type(argname="argument from_env", value=from_env, expected_type=type_hints["from_env"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if from_env is not None:
            self._values["from_env"] = from_env
        if password is not None:
            self._values["password"] = password
        if url is not None:
            self._values["url"] = url
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def from_env(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''When ``true`` the provider will discover the proxy configuration from environment variables.

        This is based upon ```http.ProxyFromEnvironment`` <https://pkg.go.dev/net/http#ProxyFromEnvironment>`_ and it supports the same environment variables (default: ``true``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.0.4/docs#from_env TlsProvider#from_env}
        '''
        result = self._values.get("from_env")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password used for Basic authentication against the Proxy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.0.4/docs#password TlsProvider#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''URL used to connect to the Proxy. Accepted schemes are: ``http``, ``https``, ``socks5``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.0.4/docs#url TlsProvider#url}
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''Username (or Token) used for Basic authentication against the Proxy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/tls/4.0.4/docs#username TlsProvider#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TlsProviderProxy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "TlsProvider",
    "TlsProviderConfig",
    "TlsProviderProxy",
]

publication.publish()

def _typecheckingstub__bf8a72a2002ea12c9852076c3248eeb6ceaf28ea8e879a2296ddbf44c430bf58(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    alias: typing.Optional[builtins.str] = None,
    proxy: typing.Optional[typing.Union[TlsProviderProxy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eae8f1b5149aa2f09f7c1fe4512ad7ee4ee50de0749b8a1fd67f9985434ee9a6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55307b57edc3a31452806f5213cdf453dae0931974131ffbe3c0ddfabe0005cc(
    value: typing.Optional[TlsProviderProxy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7efaf0d00d51c1fa807496879c1cb56b50bbca1433c4ad9a92dbaa80f57a323(
    *,
    alias: typing.Optional[builtins.str] = None,
    proxy: typing.Optional[typing.Union[TlsProviderProxy, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ea50a8088ea8dd808b035d9c72caf92ce75f4311275c65fa60feb517b4ea829(
    *,
    from_env: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
