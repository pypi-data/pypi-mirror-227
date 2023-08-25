'''
# `provider`

Refer to the Terraform Registory for docs: [`http`](https://registry.terraform.io/providers/hashicorp/http/3.4.0/docs).
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


class HttpProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-http.provider.HttpProvider",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/http/3.4.0/docs http}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        alias: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/http/3.4.0/docs http} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.4.0/docs#alias HttpProvider#alias}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed4656733258f821890abe9b576315755fbb2c26c5225d063440932e3244ec0a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = HttpProviderConfig(alias=alias)

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

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
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a464a53f72b8c9140bf7b12dbfeaa18c8e2e52599bb50526635945997a50e756)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-http.provider.HttpProviderConfig",
    jsii_struct_bases=[],
    name_mapping={"alias": "alias"},
)
class HttpProviderConfig:
    def __init__(self, *, alias: typing.Optional[builtins.str] = None) -> None:
        '''
        :param alias: Alias name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.4.0/docs#alias HttpProvider#alias}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5e292f1b2ced23926cb25076c6e327c7591be5943163c3c72b898964467f963)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alias is not None:
            self._values["alias"] = alias

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/http/3.4.0/docs#alias HttpProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "HttpProvider",
    "HttpProviderConfig",
]

publication.publish()

def _typecheckingstub__ed4656733258f821890abe9b576315755fbb2c26c5225d063440932e3244ec0a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    alias: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a464a53f72b8c9140bf7b12dbfeaa18c8e2e52599bb50526635945997a50e756(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5e292f1b2ced23926cb25076c6e327c7591be5943163c3c72b898964467f963(
    *,
    alias: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
