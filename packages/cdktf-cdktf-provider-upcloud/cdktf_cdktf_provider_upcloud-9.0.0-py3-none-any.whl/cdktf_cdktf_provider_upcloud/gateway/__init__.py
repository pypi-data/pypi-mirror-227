'''
# `upcloud_gateway`

Refer to the Terraform Registory for docs: [`upcloud_gateway`](https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway).
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


class Gateway(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-upcloud.gateway.Gateway",
):
    '''Represents a {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway upcloud_gateway}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        features: typing.Sequence[builtins.str],
        name: builtins.str,
        router: typing.Union["GatewayRouter", typing.Dict[builtins.str, typing.Any]],
        zone: builtins.str,
        configured_status: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway upcloud_gateway} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param features: Features enabled for the gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway#features Gateway#features}
        :param name: Gateway name. Needs to be unique within the account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway#name Gateway#name}
        :param router: router block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway#router Gateway#router}
        :param zone: Zone in which the gateway will be hosted, e.g. ``de-fra1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway#zone Gateway#zone}
        :param configured_status: The service configured status indicates the service's current intended status. Managed by the customer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway#configured_status Gateway#configured_status}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway#id Gateway#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Key-value pairs to classify the network gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway#labels Gateway#labels}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5004a2546e9442c11e1ddc6c725e44f286815709779966f78ab5b098792aa65)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GatewayConfig(
            features=features,
            name=name,
            router=router,
            zone=zone,
            configured_status=configured_status,
            id=id,
            labels=labels,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putRouter")
    def put_router(self, *, id: builtins.str) -> None:
        '''
        :param id: ID of the router attached to the gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway#id Gateway#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        value = GatewayRouter(id=id)

        return typing.cast(None, jsii.invoke(self, "putRouter", [value]))

    @jsii.member(jsii_name="resetConfiguredStatus")
    def reset_configured_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfiguredStatus", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="operationalState")
    def operational_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operationalState"))

    @builtins.property
    @jsii.member(jsii_name="router")
    def router(self) -> "GatewayRouterOutputReference":
        return typing.cast("GatewayRouterOutputReference", jsii.get(self, "router"))

    @builtins.property
    @jsii.member(jsii_name="configuredStatusInput")
    def configured_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configuredStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="featuresInput")
    def features_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "featuresInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="routerInput")
    def router_input(self) -> typing.Optional["GatewayRouter"]:
        return typing.cast(typing.Optional["GatewayRouter"], jsii.get(self, "routerInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="configuredStatus")
    def configured_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configuredStatus"))

    @configured_status.setter
    def configured_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d3ceb8da63fedf803a33c0cf4042706436095bd185585fd4f2d4066c2d42301)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configuredStatus", value)

    @builtins.property
    @jsii.member(jsii_name="features")
    def features(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "features"))

    @features.setter
    def features(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94599dd299b053c9fa4e3585542fed3e0f4de6c6b2f699988f736c808ca5676f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "features", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fabe7cabf8280b56c20218b44521e645d89fea5bdd72f3d3dfba3489da1a0f04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "labels"))

    @labels.setter
    def labels(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28caa4359433feaa3e11ba0a3a5ad925b8f03afe2a5a2997cb8b61c0f9bd4275)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2c5d28159ca3dac2ea92e9af2bb081a4326b986cc12ca65061f2a279603b82d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb73e8f0fe354e887808b5bf127fd5ac0c6707e04487d3c8585afb386405ed4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-upcloud.gateway.GatewayConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "features": "features",
        "name": "name",
        "router": "router",
        "zone": "zone",
        "configured_status": "configuredStatus",
        "id": "id",
        "labels": "labels",
    },
)
class GatewayConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        features: typing.Sequence[builtins.str],
        name: builtins.str,
        router: typing.Union["GatewayRouter", typing.Dict[builtins.str, typing.Any]],
        zone: builtins.str,
        configured_status: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param features: Features enabled for the gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway#features Gateway#features}
        :param name: Gateway name. Needs to be unique within the account. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway#name Gateway#name}
        :param router: router block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway#router Gateway#router}
        :param zone: Zone in which the gateway will be hosted, e.g. ``de-fra1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway#zone Gateway#zone}
        :param configured_status: The service configured status indicates the service's current intended status. Managed by the customer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway#configured_status Gateway#configured_status}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway#id Gateway#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: Key-value pairs to classify the network gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway#labels Gateway#labels}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(router, dict):
            router = GatewayRouter(**router)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5913e78f6a79aa5b74134144999cbeb9af7af46d3a269c9af3928cc7b7b6bf8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument features", value=features, expected_type=type_hints["features"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument router", value=router, expected_type=type_hints["router"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
            check_type(argname="argument configured_status", value=configured_status, expected_type=type_hints["configured_status"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "features": features,
            "name": name,
            "router": router,
            "zone": zone,
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
        if configured_status is not None:
            self._values["configured_status"] = configured_status
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels

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
    def features(self) -> typing.List[builtins.str]:
        '''Features enabled for the gateway.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway#features Gateway#features}
        '''
        result = self._values.get("features")
        assert result is not None, "Required property 'features' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Gateway name. Needs to be unique within the account.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway#name Gateway#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def router(self) -> "GatewayRouter":
        '''router block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway#router Gateway#router}
        '''
        result = self._values.get("router")
        assert result is not None, "Required property 'router' is missing"
        return typing.cast("GatewayRouter", result)

    @builtins.property
    def zone(self) -> builtins.str:
        '''Zone in which the gateway will be hosted, e.g. ``de-fra1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway#zone Gateway#zone}
        '''
        result = self._values.get("zone")
        assert result is not None, "Required property 'zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configured_status(self) -> typing.Optional[builtins.str]:
        '''The service configured status indicates the service's current intended status. Managed by the customer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway#configured_status Gateway#configured_status}
        '''
        result = self._values.get("configured_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway#id Gateway#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Key-value pairs to classify the network gateway.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway#labels Gateway#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GatewayConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-upcloud.gateway.GatewayRouter",
    jsii_struct_bases=[],
    name_mapping={"id": "id"},
)
class GatewayRouter:
    def __init__(self, *, id: builtins.str) -> None:
        '''
        :param id: ID of the router attached to the gateway. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway#id Gateway#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec6d5ccf3e805f30e341a3cd9f4f396b1b94f09fded4ca2733934ac1d447f38b)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''ID of the router attached to the gateway.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/gateway#id Gateway#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GatewayRouter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GatewayRouterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-upcloud.gateway.GatewayRouterOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39cde6c30f5264645bf5e4ec2389eef0e33f665a768766f6f399789cd2aeebf6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab5ca3b00171a73e17cc382cbf956dd56828d5e5c1e4b79a39bb69f998be7b21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[GatewayRouter]:
        return typing.cast(typing.Optional[GatewayRouter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[GatewayRouter]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5af2000bc2111ed75c0613b13003d2b17d86ab5ae8b1253df886868176e2553f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "Gateway",
    "GatewayConfig",
    "GatewayRouter",
    "GatewayRouterOutputReference",
]

publication.publish()

def _typecheckingstub__b5004a2546e9442c11e1ddc6c725e44f286815709779966f78ab5b098792aa65(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    features: typing.Sequence[builtins.str],
    name: builtins.str,
    router: typing.Union[GatewayRouter, typing.Dict[builtins.str, typing.Any]],
    zone: builtins.str,
    configured_status: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__3d3ceb8da63fedf803a33c0cf4042706436095bd185585fd4f2d4066c2d42301(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94599dd299b053c9fa4e3585542fed3e0f4de6c6b2f699988f736c808ca5676f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fabe7cabf8280b56c20218b44521e645d89fea5bdd72f3d3dfba3489da1a0f04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28caa4359433feaa3e11ba0a3a5ad925b8f03afe2a5a2997cb8b61c0f9bd4275(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2c5d28159ca3dac2ea92e9af2bb081a4326b986cc12ca65061f2a279603b82d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb73e8f0fe354e887808b5bf127fd5ac0c6707e04487d3c8585afb386405ed4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5913e78f6a79aa5b74134144999cbeb9af7af46d3a269c9af3928cc7b7b6bf8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    features: typing.Sequence[builtins.str],
    name: builtins.str,
    router: typing.Union[GatewayRouter, typing.Dict[builtins.str, typing.Any]],
    zone: builtins.str,
    configured_status: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec6d5ccf3e805f30e341a3cd9f4f396b1b94f09fded4ca2733934ac1d447f38b(
    *,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39cde6c30f5264645bf5e4ec2389eef0e33f665a768766f6f399789cd2aeebf6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab5ca3b00171a73e17cc382cbf956dd56828d5e5c1e4b79a39bb69f998be7b21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af2000bc2111ed75c0613b13003d2b17d86ab5ae8b1253df886868176e2553f(
    value: typing.Optional[GatewayRouter],
) -> None:
    """Type checking stubs"""
    pass
