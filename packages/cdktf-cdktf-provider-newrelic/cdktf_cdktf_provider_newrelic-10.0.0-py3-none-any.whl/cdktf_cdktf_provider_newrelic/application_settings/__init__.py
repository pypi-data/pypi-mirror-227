'''
# `newrelic_application_settings`

Refer to the Terraform Registory for docs: [`newrelic_application_settings`](https://registry.terraform.io/providers/newrelic/newrelic/3.26.1/docs/resources/application_settings).
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


class ApplicationSettings(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.applicationSettings.ApplicationSettings",
):
    '''Represents a {@link https://registry.terraform.io/providers/newrelic/newrelic/3.26.1/docs/resources/application_settings newrelic_application_settings}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        app_apdex_threshold: jsii.Number,
        enable_real_user_monitoring: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        end_user_apdex_threshold: jsii.Number,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/newrelic/newrelic/3.26.1/docs/resources/application_settings newrelic_application_settings} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param app_apdex_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.26.1/docs/resources/application_settings#app_apdex_threshold ApplicationSettings#app_apdex_threshold}.
        :param enable_real_user_monitoring: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.26.1/docs/resources/application_settings#enable_real_user_monitoring ApplicationSettings#enable_real_user_monitoring}.
        :param end_user_apdex_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.26.1/docs/resources/application_settings#end_user_apdex_threshold ApplicationSettings#end_user_apdex_threshold}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.26.1/docs/resources/application_settings#name ApplicationSettings#name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.26.1/docs/resources/application_settings#id ApplicationSettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7797f81b4beabb76c8b23553e1fadd5d46a512fc6a6e816d2ecaed7bc863410)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ApplicationSettingsConfig(
            app_apdex_threshold=app_apdex_threshold,
            enable_real_user_monitoring=enable_real_user_monitoring,
            end_user_apdex_threshold=end_user_apdex_threshold,
            name=name,
            id=id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="appApdexThresholdInput")
    def app_apdex_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "appApdexThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="enableRealUserMonitoringInput")
    def enable_real_user_monitoring_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableRealUserMonitoringInput"))

    @builtins.property
    @jsii.member(jsii_name="endUserApdexThresholdInput")
    def end_user_apdex_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "endUserApdexThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="appApdexThreshold")
    def app_apdex_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "appApdexThreshold"))

    @app_apdex_threshold.setter
    def app_apdex_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29a01cec5206478d58bf73a0298ad00682a10d5ff430ef82ff3b12c9c0125aab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appApdexThreshold", value)

    @builtins.property
    @jsii.member(jsii_name="enableRealUserMonitoring")
    def enable_real_user_monitoring(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableRealUserMonitoring"))

    @enable_real_user_monitoring.setter
    def enable_real_user_monitoring(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e05a9968192e3c7eee16de2b7f41b200a7b7423d93bf1fff4accc2c14f2efd95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableRealUserMonitoring", value)

    @builtins.property
    @jsii.member(jsii_name="endUserApdexThreshold")
    def end_user_apdex_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "endUserApdexThreshold"))

    @end_user_apdex_threshold.setter
    def end_user_apdex_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__767bbdb0142bd90210e9e7dd00058ddacc8024b691342cb08787ae24de1e0674)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endUserApdexThreshold", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e61858e4c2e8c6b39d9c33380aec217e374127b0a4702d788463dc1681afc10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06abc014284bd38b6b968fa216499a355cff6900b6f471ca7c2f2822e81d96bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.applicationSettings.ApplicationSettingsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "app_apdex_threshold": "appApdexThreshold",
        "enable_real_user_monitoring": "enableRealUserMonitoring",
        "end_user_apdex_threshold": "endUserApdexThreshold",
        "name": "name",
        "id": "id",
    },
)
class ApplicationSettingsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        app_apdex_threshold: jsii.Number,
        enable_real_user_monitoring: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        end_user_apdex_threshold: jsii.Number,
        name: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param app_apdex_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.26.1/docs/resources/application_settings#app_apdex_threshold ApplicationSettings#app_apdex_threshold}.
        :param enable_real_user_monitoring: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.26.1/docs/resources/application_settings#enable_real_user_monitoring ApplicationSettings#enable_real_user_monitoring}.
        :param end_user_apdex_threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.26.1/docs/resources/application_settings#end_user_apdex_threshold ApplicationSettings#end_user_apdex_threshold}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.26.1/docs/resources/application_settings#name ApplicationSettings#name}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.26.1/docs/resources/application_settings#id ApplicationSettings#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__543787d805174e2ea9e2c92790b4477ce9bb231c59312336a134c28ae3006107)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument app_apdex_threshold", value=app_apdex_threshold, expected_type=type_hints["app_apdex_threshold"])
            check_type(argname="argument enable_real_user_monitoring", value=enable_real_user_monitoring, expected_type=type_hints["enable_real_user_monitoring"])
            check_type(argname="argument end_user_apdex_threshold", value=end_user_apdex_threshold, expected_type=type_hints["end_user_apdex_threshold"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_apdex_threshold": app_apdex_threshold,
            "enable_real_user_monitoring": enable_real_user_monitoring,
            "end_user_apdex_threshold": end_user_apdex_threshold,
            "name": name,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if id is not None:
            self._values["id"] = id

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def app_apdex_threshold(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.26.1/docs/resources/application_settings#app_apdex_threshold ApplicationSettings#app_apdex_threshold}.'''
        result = self._values.get("app_apdex_threshold")
        assert result is not None, "Required property 'app_apdex_threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def enable_real_user_monitoring(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.26.1/docs/resources/application_settings#enable_real_user_monitoring ApplicationSettings#enable_real_user_monitoring}.'''
        result = self._values.get("enable_real_user_monitoring")
        assert result is not None, "Required property 'enable_real_user_monitoring' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def end_user_apdex_threshold(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.26.1/docs/resources/application_settings#end_user_apdex_threshold ApplicationSettings#end_user_apdex_threshold}.'''
        result = self._values.get("end_user_apdex_threshold")
        assert result is not None, "Required property 'end_user_apdex_threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.26.1/docs/resources/application_settings#name ApplicationSettings#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.26.1/docs/resources/application_settings#id ApplicationSettings#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationSettingsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ApplicationSettings",
    "ApplicationSettingsConfig",
]

publication.publish()

def _typecheckingstub__d7797f81b4beabb76c8b23553e1fadd5d46a512fc6a6e816d2ecaed7bc863410(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    app_apdex_threshold: jsii.Number,
    enable_real_user_monitoring: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    end_user_apdex_threshold: jsii.Number,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29a01cec5206478d58bf73a0298ad00682a10d5ff430ef82ff3b12c9c0125aab(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e05a9968192e3c7eee16de2b7f41b200a7b7423d93bf1fff4accc2c14f2efd95(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__767bbdb0142bd90210e9e7dd00058ddacc8024b691342cb08787ae24de1e0674(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e61858e4c2e8c6b39d9c33380aec217e374127b0a4702d788463dc1681afc10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06abc014284bd38b6b968fa216499a355cff6900b6f471ca7c2f2822e81d96bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__543787d805174e2ea9e2c92790b4477ce9bb231c59312336a134c28ae3006107(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    app_apdex_threshold: jsii.Number,
    enable_real_user_monitoring: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    end_user_apdex_threshold: jsii.Number,
    name: builtins.str,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
