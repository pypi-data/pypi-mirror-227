'''
# `upcloud_managed_database_redis`

Refer to the Terraform Registory for docs: [`upcloud_managed_database_redis`](https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis).
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


class ManagedDatabaseRedis(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-upcloud.managedDatabaseRedis.ManagedDatabaseRedis",
):
    '''Represents a {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis upcloud_managed_database_redis}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        plan: builtins.str,
        zone: builtins.str,
        id: typing.Optional[builtins.str] = None,
        maintenance_window_dow: typing.Optional[builtins.str] = None,
        maintenance_window_time: typing.Optional[builtins.str] = None,
        powered: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        properties: typing.Optional[typing.Union["ManagedDatabaseRedisProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        title: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis upcloud_managed_database_redis} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Name of the service. The name is used as a prefix for the logical hostname. Must be unique within an account Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#name ManagedDatabaseRedis#name}
        :param plan: Service plan to use. This determines how much resources the instance will have. You can list available plans with ``upctl database plans <type>``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#plan ManagedDatabaseRedis#plan}
        :param zone: Zone where the instance resides, e.g. ``de-fra1``. You can list available zones with ``upctl zone list``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#zone ManagedDatabaseRedis#zone}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#id ManagedDatabaseRedis#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintenance_window_dow: Maintenance window day of week. Lower case weekday name (monday, tuesday, ...). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#maintenance_window_dow ManagedDatabaseRedis#maintenance_window_dow}
        :param maintenance_window_time: Maintenance window UTC time in hh:mm:ss format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#maintenance_window_time ManagedDatabaseRedis#maintenance_window_time}
        :param powered: The administrative power state of the service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#powered ManagedDatabaseRedis#powered}
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#properties ManagedDatabaseRedis#properties}
        :param title: Title of a managed database instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#title ManagedDatabaseRedis#title}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e10737b3441da242e45d6c2d2bc2f70394648ca22d7a0273fd99d90772bf1bc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ManagedDatabaseRedisConfig(
            name=name,
            plan=plan,
            zone=zone,
            id=id,
            maintenance_window_dow=maintenance_window_dow,
            maintenance_window_time=maintenance_window_time,
            powered=powered,
            properties=properties,
            title=title,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putProperties")
    def put_properties(
        self,
        *,
        automatic_utility_network_ip_filter: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        migration: typing.Optional[typing.Union["ManagedDatabaseRedisPropertiesMigration", typing.Dict[builtins.str, typing.Any]]] = None,
        public_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        redis_acl_channels_default: typing.Optional[builtins.str] = None,
        redis_io_threads: typing.Optional[jsii.Number] = None,
        redis_lfu_decay_time: typing.Optional[jsii.Number] = None,
        redis_lfu_log_factor: typing.Optional[jsii.Number] = None,
        redis_maxmemory_policy: typing.Optional[builtins.str] = None,
        redis_notify_keyspace_events: typing.Optional[builtins.str] = None,
        redis_number_of_databases: typing.Optional[jsii.Number] = None,
        redis_persistence: typing.Optional[builtins.str] = None,
        redis_pubsub_client_output_buffer_limit: typing.Optional[jsii.Number] = None,
        redis_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        redis_timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param automatic_utility_network_ip_filter: Automatic utility network IP Filter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#automatic_utility_network_ip_filter ManagedDatabaseRedis#automatic_utility_network_ip_filter}
        :param ip_filter: IP filter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#ip_filter ManagedDatabaseRedis#ip_filter}
        :param migration: migration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#migration ManagedDatabaseRedis#migration}
        :param public_access: Public access allows connections to your Managed Database services via the public internet. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#public_access ManagedDatabaseRedis#public_access}
        :param redis_acl_channels_default: Default ACL for pub/sub channels used when Redis user is created. Determines default pub/sub channels' ACL for new users if ACL is not supplied. When this option is not defined, all_channels is assumed to keep backward compatibility. This option doesn't affect Redis configuration acl-pubsub-default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_acl_channels_default ManagedDatabaseRedis#redis_acl_channels_default}
        :param redis_io_threads: Redis IO thread count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_io_threads ManagedDatabaseRedis#redis_io_threads}
        :param redis_lfu_decay_time: LFU maxmemory-policy counter decay time in minutes. Default is 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_lfu_decay_time ManagedDatabaseRedis#redis_lfu_decay_time}
        :param redis_lfu_log_factor: Counter logarithm factor for volatile-lfu and allkeys-lfu maxmemory-policies. Default is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_lfu_log_factor ManagedDatabaseRedis#redis_lfu_log_factor}
        :param redis_maxmemory_policy: Redis maxmemory-policy. Default is ``noeviction``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_maxmemory_policy ManagedDatabaseRedis#redis_maxmemory_policy}
        :param redis_notify_keyspace_events: Set notify-keyspace-events option. Default is "". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_notify_keyspace_events ManagedDatabaseRedis#redis_notify_keyspace_events}
        :param redis_number_of_databases: Number of redis databases. Set number of redis databases. Changing this will cause a restart of redis service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_number_of_databases ManagedDatabaseRedis#redis_number_of_databases}
        :param redis_persistence: Redis persistence. When persistence is 'rdb', Redis does RDB dumps each 10 minutes if any key is changed. Also RDB dumps are done according to backup schedule for backup purposes. When persistence is 'off', no RDB dumps and backups are done, so data can be lost at any moment if service is restarted for any reason, or if service is powered off. Also service can't be forked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_persistence ManagedDatabaseRedis#redis_persistence}
        :param redis_pubsub_client_output_buffer_limit: Pub/sub client output buffer hard limit in MB. Set output buffer limit for pub / sub clients in MB. The value is the hard limit, the soft limit is 1/4 of the hard limit. When setting the limit, be mindful of the available memory in the selected service plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_pubsub_client_output_buffer_limit ManagedDatabaseRedis#redis_pubsub_client_output_buffer_limit}
        :param redis_ssl: Require SSL to access Redis. Default is ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_ssl ManagedDatabaseRedis#redis_ssl}
        :param redis_timeout: Redis idle connection timeout in seconds. Default is 300. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_timeout ManagedDatabaseRedis#redis_timeout}
        '''
        value = ManagedDatabaseRedisProperties(
            automatic_utility_network_ip_filter=automatic_utility_network_ip_filter,
            ip_filter=ip_filter,
            migration=migration,
            public_access=public_access,
            redis_acl_channels_default=redis_acl_channels_default,
            redis_io_threads=redis_io_threads,
            redis_lfu_decay_time=redis_lfu_decay_time,
            redis_lfu_log_factor=redis_lfu_log_factor,
            redis_maxmemory_policy=redis_maxmemory_policy,
            redis_notify_keyspace_events=redis_notify_keyspace_events,
            redis_number_of_databases=redis_number_of_databases,
            redis_persistence=redis_persistence,
            redis_pubsub_client_output_buffer_limit=redis_pubsub_client_output_buffer_limit,
            redis_ssl=redis_ssl,
            redis_timeout=redis_timeout,
        )

        return typing.cast(None, jsii.invoke(self, "putProperties", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaintenanceWindowDow")
    def reset_maintenance_window_dow(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceWindowDow", []))

    @jsii.member(jsii_name="resetMaintenanceWindowTime")
    def reset_maintenance_window_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintenanceWindowTime", []))

    @jsii.member(jsii_name="resetPowered")
    def reset_powered(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPowered", []))

    @jsii.member(jsii_name="resetProperties")
    def reset_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProperties", []))

    @jsii.member(jsii_name="resetTitle")
    def reset_title(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTitle", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="components")
    def components(self) -> "ManagedDatabaseRedisComponentsList":
        return typing.cast("ManagedDatabaseRedisComponentsList", jsii.get(self, "components"))

    @builtins.property
    @jsii.member(jsii_name="nodeStates")
    def node_states(self) -> "ManagedDatabaseRedisNodeStatesList":
        return typing.cast("ManagedDatabaseRedisNodeStatesList", jsii.get(self, "nodeStates"))

    @builtins.property
    @jsii.member(jsii_name="primaryDatabase")
    def primary_database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "primaryDatabase"))

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(self) -> "ManagedDatabaseRedisPropertiesOutputReference":
        return typing.cast("ManagedDatabaseRedisPropertiesOutputReference", jsii.get(self, "properties"))

    @builtins.property
    @jsii.member(jsii_name="serviceHost")
    def service_host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceHost"))

    @builtins.property
    @jsii.member(jsii_name="servicePassword")
    def service_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servicePassword"))

    @builtins.property
    @jsii.member(jsii_name="servicePort")
    def service_port(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servicePort"))

    @builtins.property
    @jsii.member(jsii_name="serviceUri")
    def service_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceUri"))

    @builtins.property
    @jsii.member(jsii_name="serviceUsername")
    def service_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceUsername"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowDowInput")
    def maintenance_window_dow_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maintenanceWindowDowInput"))

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowTimeInput")
    def maintenance_window_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maintenanceWindowTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="planInput")
    def plan_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "planInput"))

    @builtins.property
    @jsii.member(jsii_name="poweredInput")
    def powered_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "poweredInput"))

    @builtins.property
    @jsii.member(jsii_name="propertiesInput")
    def properties_input(self) -> typing.Optional["ManagedDatabaseRedisProperties"]:
        return typing.cast(typing.Optional["ManagedDatabaseRedisProperties"], jsii.get(self, "propertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="titleInput")
    def title_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "titleInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneInput")
    def zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__034efef55e5a3bbebea436a291fa62e30ce0295c063f00efa32c2e4da24fa48e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowDow")
    def maintenance_window_dow(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintenanceWindowDow"))

    @maintenance_window_dow.setter
    def maintenance_window_dow(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73273528d0b8cb624417054adb344b6b88a235351d2cd957c16595add16c8387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenanceWindowDow", value)

    @builtins.property
    @jsii.member(jsii_name="maintenanceWindowTime")
    def maintenance_window_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintenanceWindowTime"))

    @maintenance_window_time.setter
    def maintenance_window_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3463082f9615ac3e2b28a306c8c416e034bb1455b562224418511e2b64e98aac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintenanceWindowTime", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c0777aa27ee2c0d2740288a9a2eda0f15e9a07783c54594720bbb763fcf3185)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="plan")
    def plan(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "plan"))

    @plan.setter
    def plan(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__149801ed2891da8e0ef20e0f41d11b22743e801cfdf02647165dfc8b2e3d43a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "plan", value)

    @builtins.property
    @jsii.member(jsii_name="powered")
    def powered(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "powered"))

    @powered.setter
    def powered(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ba0403ca1176e546e2415a5a55338ca5196302e1eba800025393e8cd2effefd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "powered", value)

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))

    @title.setter
    def title(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b9d5868df87b17b486ae6afcb3e738c388956d33f99b995a4c7ded4543a16f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "title", value)

    @builtins.property
    @jsii.member(jsii_name="zone")
    def zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zone"))

    @zone.setter
    def zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6200eb68a3f6b2c3f07f5e4d5f8ae376e15d54a8f63a9eaebb800986941df925)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zone", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-upcloud.managedDatabaseRedis.ManagedDatabaseRedisComponents",
    jsii_struct_bases=[],
    name_mapping={},
)
class ManagedDatabaseRedisComponents:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedDatabaseRedisComponents(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ManagedDatabaseRedisComponentsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-upcloud.managedDatabaseRedis.ManagedDatabaseRedisComponentsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75e57aca0ea172e4cff02b14eeaa7f164d2407fb7cc7e60a68b03fe484ccfabb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ManagedDatabaseRedisComponentsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3638c469678c1ee26b60ba0b78e20c1c01b3db110db4280e9884314cec942a20)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ManagedDatabaseRedisComponentsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__123d717dd88e816c65cab6091d48edb5f8df9a633dba87ec6eb60ffde8e6ffe9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7de82f36798ec3b4929e14320c93a81a40ef32c357088821d82e7f2dda5fc08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e969959ac62660fb87c4c430ebc9a800cf52dd0398d032cd90dab896168b1a57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class ManagedDatabaseRedisComponentsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-upcloud.managedDatabaseRedis.ManagedDatabaseRedisComponentsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a1cb80a7cb7d5bd3fe574b03feffdb31e2b4317eaf6581b414cf9db6788d82a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="component")
    def component(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "component"))

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="route")
    def route(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "route"))

    @builtins.property
    @jsii.member(jsii_name="usage")
    def usage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usage"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ManagedDatabaseRedisComponents]:
        return typing.cast(typing.Optional[ManagedDatabaseRedisComponents], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ManagedDatabaseRedisComponents],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cadf7da6ebfddac64d2c3486da03b72ef79772ed3bb7ff7fd01074c0d0aceeab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-upcloud.managedDatabaseRedis.ManagedDatabaseRedisConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "plan": "plan",
        "zone": "zone",
        "id": "id",
        "maintenance_window_dow": "maintenanceWindowDow",
        "maintenance_window_time": "maintenanceWindowTime",
        "powered": "powered",
        "properties": "properties",
        "title": "title",
    },
)
class ManagedDatabaseRedisConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        plan: builtins.str,
        zone: builtins.str,
        id: typing.Optional[builtins.str] = None,
        maintenance_window_dow: typing.Optional[builtins.str] = None,
        maintenance_window_time: typing.Optional[builtins.str] = None,
        powered: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        properties: typing.Optional[typing.Union["ManagedDatabaseRedisProperties", typing.Dict[builtins.str, typing.Any]]] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Name of the service. The name is used as a prefix for the logical hostname. Must be unique within an account Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#name ManagedDatabaseRedis#name}
        :param plan: Service plan to use. This determines how much resources the instance will have. You can list available plans with ``upctl database plans <type>``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#plan ManagedDatabaseRedis#plan}
        :param zone: Zone where the instance resides, e.g. ``de-fra1``. You can list available zones with ``upctl zone list``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#zone ManagedDatabaseRedis#zone}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#id ManagedDatabaseRedis#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintenance_window_dow: Maintenance window day of week. Lower case weekday name (monday, tuesday, ...). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#maintenance_window_dow ManagedDatabaseRedis#maintenance_window_dow}
        :param maintenance_window_time: Maintenance window UTC time in hh:mm:ss format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#maintenance_window_time ManagedDatabaseRedis#maintenance_window_time}
        :param powered: The administrative power state of the service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#powered ManagedDatabaseRedis#powered}
        :param properties: properties block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#properties ManagedDatabaseRedis#properties}
        :param title: Title of a managed database instance. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#title ManagedDatabaseRedis#title}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(properties, dict):
            properties = ManagedDatabaseRedisProperties(**properties)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__427affd4287d8a7a2c0271c2fa4103a967fb5adf7f546d78c1050110eae49ae4)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument plan", value=plan, expected_type=type_hints["plan"])
            check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument maintenance_window_dow", value=maintenance_window_dow, expected_type=type_hints["maintenance_window_dow"])
            check_type(argname="argument maintenance_window_time", value=maintenance_window_time, expected_type=type_hints["maintenance_window_time"])
            check_type(argname="argument powered", value=powered, expected_type=type_hints["powered"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "plan": plan,
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
        if id is not None:
            self._values["id"] = id
        if maintenance_window_dow is not None:
            self._values["maintenance_window_dow"] = maintenance_window_dow
        if maintenance_window_time is not None:
            self._values["maintenance_window_time"] = maintenance_window_time
        if powered is not None:
            self._values["powered"] = powered
        if properties is not None:
            self._values["properties"] = properties
        if title is not None:
            self._values["title"] = title

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
    def name(self) -> builtins.str:
        '''Name of the service.

        The name is used as a prefix for the logical hostname. Must be unique within an account

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#name ManagedDatabaseRedis#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def plan(self) -> builtins.str:
        '''Service plan to use.

        This determines how much resources the instance will have. You can list available plans with ``upctl database plans <type>``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#plan ManagedDatabaseRedis#plan}
        '''
        result = self._values.get("plan")
        assert result is not None, "Required property 'plan' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def zone(self) -> builtins.str:
        '''Zone where the instance resides, e.g. ``de-fra1``. You can list available zones with ``upctl zone list``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#zone ManagedDatabaseRedis#zone}
        '''
        result = self._values.get("zone")
        assert result is not None, "Required property 'zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#id ManagedDatabaseRedis#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_window_dow(self) -> typing.Optional[builtins.str]:
        '''Maintenance window day of week. Lower case weekday name (monday, tuesday, ...).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#maintenance_window_dow ManagedDatabaseRedis#maintenance_window_dow}
        '''
        result = self._values.get("maintenance_window_dow")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintenance_window_time(self) -> typing.Optional[builtins.str]:
        '''Maintenance window UTC time in hh:mm:ss format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#maintenance_window_time ManagedDatabaseRedis#maintenance_window_time}
        '''
        result = self._values.get("maintenance_window_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def powered(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The administrative power state of the service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#powered ManagedDatabaseRedis#powered}
        '''
        result = self._values.get("powered")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def properties(self) -> typing.Optional["ManagedDatabaseRedisProperties"]:
        '''properties block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#properties ManagedDatabaseRedis#properties}
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional["ManagedDatabaseRedisProperties"], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''Title of a managed database instance.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#title ManagedDatabaseRedis#title}
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedDatabaseRedisConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-upcloud.managedDatabaseRedis.ManagedDatabaseRedisNodeStates",
    jsii_struct_bases=[],
    name_mapping={},
)
class ManagedDatabaseRedisNodeStates:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedDatabaseRedisNodeStates(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ManagedDatabaseRedisNodeStatesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-upcloud.managedDatabaseRedis.ManagedDatabaseRedisNodeStatesList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__088293269764886cb30515f25b3eb2a8c94c0b1c14420735ad1ac267e442ac06)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ManagedDatabaseRedisNodeStatesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__507d2392485e33f8d31a7fc472023b6c8642b0b3a6c04f7ec4ae4927c3989231)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ManagedDatabaseRedisNodeStatesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c84e1e1dab92ee6bf7f6cc30017277c61c12537ca45cb66c57001f4af67f5c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b608d522cd5b29610674b7ee44258aaa92da7f4ddbd189074353cd83ebe044dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__370cb86e81dee1a23b1fd92a00f3cb678a81d7ff887340b5a7ab4beb087d7e36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class ManagedDatabaseRedisNodeStatesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-upcloud.managedDatabaseRedis.ManagedDatabaseRedisNodeStatesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29cd5f8b351037da5344c386af218418fda5af69f334b53378ff76f3cd21aa96)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ManagedDatabaseRedisNodeStates]:
        return typing.cast(typing.Optional[ManagedDatabaseRedisNodeStates], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ManagedDatabaseRedisNodeStates],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f2a3a9eee36fcd3a0e60fb75bc2afe78a8ee62b35117c45d02a76db30e62cc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-upcloud.managedDatabaseRedis.ManagedDatabaseRedisProperties",
    jsii_struct_bases=[],
    name_mapping={
        "automatic_utility_network_ip_filter": "automaticUtilityNetworkIpFilter",
        "ip_filter": "ipFilter",
        "migration": "migration",
        "public_access": "publicAccess",
        "redis_acl_channels_default": "redisAclChannelsDefault",
        "redis_io_threads": "redisIoThreads",
        "redis_lfu_decay_time": "redisLfuDecayTime",
        "redis_lfu_log_factor": "redisLfuLogFactor",
        "redis_maxmemory_policy": "redisMaxmemoryPolicy",
        "redis_notify_keyspace_events": "redisNotifyKeyspaceEvents",
        "redis_number_of_databases": "redisNumberOfDatabases",
        "redis_persistence": "redisPersistence",
        "redis_pubsub_client_output_buffer_limit": "redisPubsubClientOutputBufferLimit",
        "redis_ssl": "redisSsl",
        "redis_timeout": "redisTimeout",
    },
)
class ManagedDatabaseRedisProperties:
    def __init__(
        self,
        *,
        automatic_utility_network_ip_filter: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        migration: typing.Optional[typing.Union["ManagedDatabaseRedisPropertiesMigration", typing.Dict[builtins.str, typing.Any]]] = None,
        public_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        redis_acl_channels_default: typing.Optional[builtins.str] = None,
        redis_io_threads: typing.Optional[jsii.Number] = None,
        redis_lfu_decay_time: typing.Optional[jsii.Number] = None,
        redis_lfu_log_factor: typing.Optional[jsii.Number] = None,
        redis_maxmemory_policy: typing.Optional[builtins.str] = None,
        redis_notify_keyspace_events: typing.Optional[builtins.str] = None,
        redis_number_of_databases: typing.Optional[jsii.Number] = None,
        redis_persistence: typing.Optional[builtins.str] = None,
        redis_pubsub_client_output_buffer_limit: typing.Optional[jsii.Number] = None,
        redis_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        redis_timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param automatic_utility_network_ip_filter: Automatic utility network IP Filter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#automatic_utility_network_ip_filter ManagedDatabaseRedis#automatic_utility_network_ip_filter}
        :param ip_filter: IP filter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#ip_filter ManagedDatabaseRedis#ip_filter}
        :param migration: migration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#migration ManagedDatabaseRedis#migration}
        :param public_access: Public access allows connections to your Managed Database services via the public internet. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#public_access ManagedDatabaseRedis#public_access}
        :param redis_acl_channels_default: Default ACL for pub/sub channels used when Redis user is created. Determines default pub/sub channels' ACL for new users if ACL is not supplied. When this option is not defined, all_channels is assumed to keep backward compatibility. This option doesn't affect Redis configuration acl-pubsub-default. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_acl_channels_default ManagedDatabaseRedis#redis_acl_channels_default}
        :param redis_io_threads: Redis IO thread count. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_io_threads ManagedDatabaseRedis#redis_io_threads}
        :param redis_lfu_decay_time: LFU maxmemory-policy counter decay time in minutes. Default is 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_lfu_decay_time ManagedDatabaseRedis#redis_lfu_decay_time}
        :param redis_lfu_log_factor: Counter logarithm factor for volatile-lfu and allkeys-lfu maxmemory-policies. Default is 10. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_lfu_log_factor ManagedDatabaseRedis#redis_lfu_log_factor}
        :param redis_maxmemory_policy: Redis maxmemory-policy. Default is ``noeviction``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_maxmemory_policy ManagedDatabaseRedis#redis_maxmemory_policy}
        :param redis_notify_keyspace_events: Set notify-keyspace-events option. Default is "". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_notify_keyspace_events ManagedDatabaseRedis#redis_notify_keyspace_events}
        :param redis_number_of_databases: Number of redis databases. Set number of redis databases. Changing this will cause a restart of redis service. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_number_of_databases ManagedDatabaseRedis#redis_number_of_databases}
        :param redis_persistence: Redis persistence. When persistence is 'rdb', Redis does RDB dumps each 10 minutes if any key is changed. Also RDB dumps are done according to backup schedule for backup purposes. When persistence is 'off', no RDB dumps and backups are done, so data can be lost at any moment if service is restarted for any reason, or if service is powered off. Also service can't be forked. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_persistence ManagedDatabaseRedis#redis_persistence}
        :param redis_pubsub_client_output_buffer_limit: Pub/sub client output buffer hard limit in MB. Set output buffer limit for pub / sub clients in MB. The value is the hard limit, the soft limit is 1/4 of the hard limit. When setting the limit, be mindful of the available memory in the selected service plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_pubsub_client_output_buffer_limit ManagedDatabaseRedis#redis_pubsub_client_output_buffer_limit}
        :param redis_ssl: Require SSL to access Redis. Default is ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_ssl ManagedDatabaseRedis#redis_ssl}
        :param redis_timeout: Redis idle connection timeout in seconds. Default is 300. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_timeout ManagedDatabaseRedis#redis_timeout}
        '''
        if isinstance(migration, dict):
            migration = ManagedDatabaseRedisPropertiesMigration(**migration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45d231637cf0ee1419176ac95e538148c430674ed976ab685c332c60e8210f15)
            check_type(argname="argument automatic_utility_network_ip_filter", value=automatic_utility_network_ip_filter, expected_type=type_hints["automatic_utility_network_ip_filter"])
            check_type(argname="argument ip_filter", value=ip_filter, expected_type=type_hints["ip_filter"])
            check_type(argname="argument migration", value=migration, expected_type=type_hints["migration"])
            check_type(argname="argument public_access", value=public_access, expected_type=type_hints["public_access"])
            check_type(argname="argument redis_acl_channels_default", value=redis_acl_channels_default, expected_type=type_hints["redis_acl_channels_default"])
            check_type(argname="argument redis_io_threads", value=redis_io_threads, expected_type=type_hints["redis_io_threads"])
            check_type(argname="argument redis_lfu_decay_time", value=redis_lfu_decay_time, expected_type=type_hints["redis_lfu_decay_time"])
            check_type(argname="argument redis_lfu_log_factor", value=redis_lfu_log_factor, expected_type=type_hints["redis_lfu_log_factor"])
            check_type(argname="argument redis_maxmemory_policy", value=redis_maxmemory_policy, expected_type=type_hints["redis_maxmemory_policy"])
            check_type(argname="argument redis_notify_keyspace_events", value=redis_notify_keyspace_events, expected_type=type_hints["redis_notify_keyspace_events"])
            check_type(argname="argument redis_number_of_databases", value=redis_number_of_databases, expected_type=type_hints["redis_number_of_databases"])
            check_type(argname="argument redis_persistence", value=redis_persistence, expected_type=type_hints["redis_persistence"])
            check_type(argname="argument redis_pubsub_client_output_buffer_limit", value=redis_pubsub_client_output_buffer_limit, expected_type=type_hints["redis_pubsub_client_output_buffer_limit"])
            check_type(argname="argument redis_ssl", value=redis_ssl, expected_type=type_hints["redis_ssl"])
            check_type(argname="argument redis_timeout", value=redis_timeout, expected_type=type_hints["redis_timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if automatic_utility_network_ip_filter is not None:
            self._values["automatic_utility_network_ip_filter"] = automatic_utility_network_ip_filter
        if ip_filter is not None:
            self._values["ip_filter"] = ip_filter
        if migration is not None:
            self._values["migration"] = migration
        if public_access is not None:
            self._values["public_access"] = public_access
        if redis_acl_channels_default is not None:
            self._values["redis_acl_channels_default"] = redis_acl_channels_default
        if redis_io_threads is not None:
            self._values["redis_io_threads"] = redis_io_threads
        if redis_lfu_decay_time is not None:
            self._values["redis_lfu_decay_time"] = redis_lfu_decay_time
        if redis_lfu_log_factor is not None:
            self._values["redis_lfu_log_factor"] = redis_lfu_log_factor
        if redis_maxmemory_policy is not None:
            self._values["redis_maxmemory_policy"] = redis_maxmemory_policy
        if redis_notify_keyspace_events is not None:
            self._values["redis_notify_keyspace_events"] = redis_notify_keyspace_events
        if redis_number_of_databases is not None:
            self._values["redis_number_of_databases"] = redis_number_of_databases
        if redis_persistence is not None:
            self._values["redis_persistence"] = redis_persistence
        if redis_pubsub_client_output_buffer_limit is not None:
            self._values["redis_pubsub_client_output_buffer_limit"] = redis_pubsub_client_output_buffer_limit
        if redis_ssl is not None:
            self._values["redis_ssl"] = redis_ssl
        if redis_timeout is not None:
            self._values["redis_timeout"] = redis_timeout

    @builtins.property
    def automatic_utility_network_ip_filter(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Automatic utility network IP Filter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#automatic_utility_network_ip_filter ManagedDatabaseRedis#automatic_utility_network_ip_filter}
        '''
        result = self._values.get("automatic_utility_network_ip_filter")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ip_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''IP filter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#ip_filter ManagedDatabaseRedis#ip_filter}
        '''
        result = self._values.get("ip_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def migration(self) -> typing.Optional["ManagedDatabaseRedisPropertiesMigration"]:
        '''migration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#migration ManagedDatabaseRedis#migration}
        '''
        result = self._values.get("migration")
        return typing.cast(typing.Optional["ManagedDatabaseRedisPropertiesMigration"], result)

    @builtins.property
    def public_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Public access allows connections to your Managed Database services via the public internet.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#public_access ManagedDatabaseRedis#public_access}
        '''
        result = self._values.get("public_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def redis_acl_channels_default(self) -> typing.Optional[builtins.str]:
        '''Default ACL for pub/sub channels used when Redis user is created.

        Determines default pub/sub channels' ACL for new users if ACL is not supplied. When this option is not defined, all_channels is assumed to keep backward compatibility. This option doesn't affect Redis configuration acl-pubsub-default.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_acl_channels_default ManagedDatabaseRedis#redis_acl_channels_default}
        '''
        result = self._values.get("redis_acl_channels_default")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redis_io_threads(self) -> typing.Optional[jsii.Number]:
        '''Redis IO thread count.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_io_threads ManagedDatabaseRedis#redis_io_threads}
        '''
        result = self._values.get("redis_io_threads")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def redis_lfu_decay_time(self) -> typing.Optional[jsii.Number]:
        '''LFU maxmemory-policy counter decay time in minutes. Default is 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_lfu_decay_time ManagedDatabaseRedis#redis_lfu_decay_time}
        '''
        result = self._values.get("redis_lfu_decay_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def redis_lfu_log_factor(self) -> typing.Optional[jsii.Number]:
        '''Counter logarithm factor for volatile-lfu and allkeys-lfu maxmemory-policies. Default is 10.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_lfu_log_factor ManagedDatabaseRedis#redis_lfu_log_factor}
        '''
        result = self._values.get("redis_lfu_log_factor")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def redis_maxmemory_policy(self) -> typing.Optional[builtins.str]:
        '''Redis maxmemory-policy. Default is ``noeviction``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_maxmemory_policy ManagedDatabaseRedis#redis_maxmemory_policy}
        '''
        result = self._values.get("redis_maxmemory_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redis_notify_keyspace_events(self) -> typing.Optional[builtins.str]:
        '''Set notify-keyspace-events option. Default is "".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_notify_keyspace_events ManagedDatabaseRedis#redis_notify_keyspace_events}
        '''
        result = self._values.get("redis_notify_keyspace_events")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redis_number_of_databases(self) -> typing.Optional[jsii.Number]:
        '''Number of redis databases. Set number of redis databases. Changing this will cause a restart of redis service.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_number_of_databases ManagedDatabaseRedis#redis_number_of_databases}
        '''
        result = self._values.get("redis_number_of_databases")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def redis_persistence(self) -> typing.Optional[builtins.str]:
        '''Redis persistence.

        When persistence is 'rdb', Redis does RDB dumps each 10 minutes if any key is changed. Also RDB dumps are done according to backup schedule for backup purposes. When persistence is 'off', no RDB dumps and backups are done, so data can be lost at any moment if service is restarted for any reason, or if service is powered off. Also service can't be forked.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_persistence ManagedDatabaseRedis#redis_persistence}
        '''
        result = self._values.get("redis_persistence")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def redis_pubsub_client_output_buffer_limit(self) -> typing.Optional[jsii.Number]:
        '''Pub/sub client output buffer hard limit in MB.

        Set output buffer limit for pub / sub clients in MB. The value is the hard limit, the soft limit is 1/4 of the hard limit. When setting the limit, be mindful of the available memory in the selected service plan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_pubsub_client_output_buffer_limit ManagedDatabaseRedis#redis_pubsub_client_output_buffer_limit}
        '''
        result = self._values.get("redis_pubsub_client_output_buffer_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def redis_ssl(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Require SSL to access Redis. Default is ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_ssl ManagedDatabaseRedis#redis_ssl}
        '''
        result = self._values.get("redis_ssl")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def redis_timeout(self) -> typing.Optional[jsii.Number]:
        '''Redis idle connection timeout in seconds. Default is 300.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#redis_timeout ManagedDatabaseRedis#redis_timeout}
        '''
        result = self._values.get("redis_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedDatabaseRedisProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-upcloud.managedDatabaseRedis.ManagedDatabaseRedisPropertiesMigration",
    jsii_struct_bases=[],
    name_mapping={
        "dbname": "dbname",
        "host": "host",
        "ignore_dbs": "ignoreDbs",
        "password": "password",
        "port": "port",
        "ssl": "ssl",
        "username": "username",
    },
)
class ManagedDatabaseRedisPropertiesMigration:
    def __init__(
        self,
        *,
        dbname: typing.Optional[builtins.str] = None,
        host: typing.Optional[builtins.str] = None,
        ignore_dbs: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dbname: Database name for bootstrapping the initial connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#dbname ManagedDatabaseRedis#dbname}
        :param host: Hostname or IP address of the server where to migrate data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#host ManagedDatabaseRedis#host}
        :param ignore_dbs: Comma-separated list of databases, which should be ignored during migration (supported by MySQL only at the moment). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#ignore_dbs ManagedDatabaseRedis#ignore_dbs}
        :param password: Password for authentication with the server where to migrate data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#password ManagedDatabaseRedis#password}
        :param port: Port number of the server where to migrate data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#port ManagedDatabaseRedis#port}
        :param ssl: The server where to migrate data from is secured with SSL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#ssl ManagedDatabaseRedis#ssl}
        :param username: User name for authentication with the server where to migrate data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#username ManagedDatabaseRedis#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5868695ab3eeee48f1195fac696f82883094948c50a1392b710ba328c403e191)
            check_type(argname="argument dbname", value=dbname, expected_type=type_hints["dbname"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument ignore_dbs", value=ignore_dbs, expected_type=type_hints["ignore_dbs"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument ssl", value=ssl, expected_type=type_hints["ssl"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dbname is not None:
            self._values["dbname"] = dbname
        if host is not None:
            self._values["host"] = host
        if ignore_dbs is not None:
            self._values["ignore_dbs"] = ignore_dbs
        if password is not None:
            self._values["password"] = password
        if port is not None:
            self._values["port"] = port
        if ssl is not None:
            self._values["ssl"] = ssl
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def dbname(self) -> typing.Optional[builtins.str]:
        '''Database name for bootstrapping the initial connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#dbname ManagedDatabaseRedis#dbname}
        '''
        result = self._values.get("dbname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''Hostname or IP address of the server where to migrate data from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#host ManagedDatabaseRedis#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_dbs(self) -> typing.Optional[builtins.str]:
        '''Comma-separated list of databases, which should be ignored during migration (supported by MySQL only at the moment).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#ignore_dbs ManagedDatabaseRedis#ignore_dbs}
        '''
        result = self._values.get("ignore_dbs")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for authentication with the server where to migrate data from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#password ManagedDatabaseRedis#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''Port number of the server where to migrate data from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#port ManagedDatabaseRedis#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ssl(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''The server where to migrate data from is secured with SSL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#ssl ManagedDatabaseRedis#ssl}
        '''
        result = self._values.get("ssl")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''User name for authentication with the server where to migrate data from.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#username ManagedDatabaseRedis#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedDatabaseRedisPropertiesMigration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ManagedDatabaseRedisPropertiesMigrationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-upcloud.managedDatabaseRedis.ManagedDatabaseRedisPropertiesMigrationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3eba87ce19486725e846ce1f43831cae3000a132162660004d878fbe60a98551)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDbname")
    def reset_dbname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDbname", []))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @jsii.member(jsii_name="resetIgnoreDbs")
    def reset_ignore_dbs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreDbs", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetSsl")
    def reset_ssl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSsl", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @builtins.property
    @jsii.member(jsii_name="dbnameInput")
    def dbname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dbnameInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreDbsInput")
    def ignore_dbs_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ignoreDbsInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="sslInput")
    def ssl_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sslInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="dbname")
    def dbname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dbname"))

    @dbname.setter
    def dbname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a35b4d987c288c3f424ab316ab2be82e8e897a321703a552b6a60f8cb45f530)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dbname", value)

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76d9433fefa974e8fd1fe9e2a1ef5cf358003310f8e14fa3d6ef0e23e46f867c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value)

    @builtins.property
    @jsii.member(jsii_name="ignoreDbs")
    def ignore_dbs(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ignoreDbs"))

    @ignore_dbs.setter
    def ignore_dbs(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__007eee9dff2abcab87190d2496857d146bb6903679cde62609372d7f42cf7e5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreDbs", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0edcd87f37d9bf96c1e0d943d76f8b8ed634421134b290c428502f3a99935d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75a2ca20e595901240d6d567bd3fc1dc4ce140b0c673961e770d60b25562abdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="ssl")
    def ssl(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ssl"))

    @ssl.setter
    def ssl(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b64ae4a372bb2c41382589f8a0c1d8d986b1694c4dce4e4e55c546e23aa2073)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssl", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82fb203b3c22ecd9831bec0b187bf29feade0ccad7832897b49ef1c6def2fe27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[ManagedDatabaseRedisPropertiesMigration]:
        return typing.cast(typing.Optional[ManagedDatabaseRedisPropertiesMigration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ManagedDatabaseRedisPropertiesMigration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bc643aad8ee6415b2b24a7c3d1afef738a314f6945735e48ec970009f0e7b33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ManagedDatabaseRedisPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-upcloud.managedDatabaseRedis.ManagedDatabaseRedisPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95bbb7a31e1bcfa0d5dd974d3a82ed54477e19d28618e27d10a3de84a979f2be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putMigration")
    def put_migration(
        self,
        *,
        dbname: typing.Optional[builtins.str] = None,
        host: typing.Optional[builtins.str] = None,
        ignore_dbs: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dbname: Database name for bootstrapping the initial connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#dbname ManagedDatabaseRedis#dbname}
        :param host: Hostname or IP address of the server where to migrate data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#host ManagedDatabaseRedis#host}
        :param ignore_dbs: Comma-separated list of databases, which should be ignored during migration (supported by MySQL only at the moment). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#ignore_dbs ManagedDatabaseRedis#ignore_dbs}
        :param password: Password for authentication with the server where to migrate data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#password ManagedDatabaseRedis#password}
        :param port: Port number of the server where to migrate data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#port ManagedDatabaseRedis#port}
        :param ssl: The server where to migrate data from is secured with SSL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#ssl ManagedDatabaseRedis#ssl}
        :param username: User name for authentication with the server where to migrate data from. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/upcloudltd/upcloud/2.12.0/docs/resources/managed_database_redis#username ManagedDatabaseRedis#username}
        '''
        value = ManagedDatabaseRedisPropertiesMigration(
            dbname=dbname,
            host=host,
            ignore_dbs=ignore_dbs,
            password=password,
            port=port,
            ssl=ssl,
            username=username,
        )

        return typing.cast(None, jsii.invoke(self, "putMigration", [value]))

    @jsii.member(jsii_name="resetAutomaticUtilityNetworkIpFilter")
    def reset_automatic_utility_network_ip_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomaticUtilityNetworkIpFilter", []))

    @jsii.member(jsii_name="resetIpFilter")
    def reset_ip_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpFilter", []))

    @jsii.member(jsii_name="resetMigration")
    def reset_migration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMigration", []))

    @jsii.member(jsii_name="resetPublicAccess")
    def reset_public_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicAccess", []))

    @jsii.member(jsii_name="resetRedisAclChannelsDefault")
    def reset_redis_acl_channels_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedisAclChannelsDefault", []))

    @jsii.member(jsii_name="resetRedisIoThreads")
    def reset_redis_io_threads(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedisIoThreads", []))

    @jsii.member(jsii_name="resetRedisLfuDecayTime")
    def reset_redis_lfu_decay_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedisLfuDecayTime", []))

    @jsii.member(jsii_name="resetRedisLfuLogFactor")
    def reset_redis_lfu_log_factor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedisLfuLogFactor", []))

    @jsii.member(jsii_name="resetRedisMaxmemoryPolicy")
    def reset_redis_maxmemory_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedisMaxmemoryPolicy", []))

    @jsii.member(jsii_name="resetRedisNotifyKeyspaceEvents")
    def reset_redis_notify_keyspace_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedisNotifyKeyspaceEvents", []))

    @jsii.member(jsii_name="resetRedisNumberOfDatabases")
    def reset_redis_number_of_databases(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedisNumberOfDatabases", []))

    @jsii.member(jsii_name="resetRedisPersistence")
    def reset_redis_persistence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedisPersistence", []))

    @jsii.member(jsii_name="resetRedisPubsubClientOutputBufferLimit")
    def reset_redis_pubsub_client_output_buffer_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedisPubsubClientOutputBufferLimit", []))

    @jsii.member(jsii_name="resetRedisSsl")
    def reset_redis_ssl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedisSsl", []))

    @jsii.member(jsii_name="resetRedisTimeout")
    def reset_redis_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedisTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="migration")
    def migration(self) -> ManagedDatabaseRedisPropertiesMigrationOutputReference:
        return typing.cast(ManagedDatabaseRedisPropertiesMigrationOutputReference, jsii.get(self, "migration"))

    @builtins.property
    @jsii.member(jsii_name="automaticUtilityNetworkIpFilterInput")
    def automatic_utility_network_ip_filter_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "automaticUtilityNetworkIpFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="ipFilterInput")
    def ip_filter_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="migrationInput")
    def migration_input(
        self,
    ) -> typing.Optional[ManagedDatabaseRedisPropertiesMigration]:
        return typing.cast(typing.Optional[ManagedDatabaseRedisPropertiesMigration], jsii.get(self, "migrationInput"))

    @builtins.property
    @jsii.member(jsii_name="publicAccessInput")
    def public_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publicAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="redisAclChannelsDefaultInput")
    def redis_acl_channels_default_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redisAclChannelsDefaultInput"))

    @builtins.property
    @jsii.member(jsii_name="redisIoThreadsInput")
    def redis_io_threads_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "redisIoThreadsInput"))

    @builtins.property
    @jsii.member(jsii_name="redisLfuDecayTimeInput")
    def redis_lfu_decay_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "redisLfuDecayTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="redisLfuLogFactorInput")
    def redis_lfu_log_factor_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "redisLfuLogFactorInput"))

    @builtins.property
    @jsii.member(jsii_name="redisMaxmemoryPolicyInput")
    def redis_maxmemory_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redisMaxmemoryPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="redisNotifyKeyspaceEventsInput")
    def redis_notify_keyspace_events_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redisNotifyKeyspaceEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="redisNumberOfDatabasesInput")
    def redis_number_of_databases_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "redisNumberOfDatabasesInput"))

    @builtins.property
    @jsii.member(jsii_name="redisPersistenceInput")
    def redis_persistence_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "redisPersistenceInput"))

    @builtins.property
    @jsii.member(jsii_name="redisPubsubClientOutputBufferLimitInput")
    def redis_pubsub_client_output_buffer_limit_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "redisPubsubClientOutputBufferLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="redisSslInput")
    def redis_ssl_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "redisSslInput"))

    @builtins.property
    @jsii.member(jsii_name="redisTimeoutInput")
    def redis_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "redisTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="automaticUtilityNetworkIpFilter")
    def automatic_utility_network_ip_filter(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "automaticUtilityNetworkIpFilter"))

    @automatic_utility_network_ip_filter.setter
    def automatic_utility_network_ip_filter(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7a5bf9f686a94105029e10a6995c1eab34c833b8b4d0f6b257a85be803f9cf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "automaticUtilityNetworkIpFilter", value)

    @builtins.property
    @jsii.member(jsii_name="ipFilter")
    def ip_filter(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipFilter"))

    @ip_filter.setter
    def ip_filter(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb934638aa3c6e837012ab6df42e93f3bf87ae5645dab83d2b4e1d837c69565a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipFilter", value)

    @builtins.property
    @jsii.member(jsii_name="publicAccess")
    def public_access(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "publicAccess"))

    @public_access.setter
    def public_access(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83c60b1f4cdd9f89109ea2a9767620a069155ebf2e36d46af8ae1b70b75ea18c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicAccess", value)

    @builtins.property
    @jsii.member(jsii_name="redisAclChannelsDefault")
    def redis_acl_channels_default(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redisAclChannelsDefault"))

    @redis_acl_channels_default.setter
    def redis_acl_channels_default(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf6000768e540c92b24e550c2c1c1fc34bac8f6b73d11b42391121cda644b8f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redisAclChannelsDefault", value)

    @builtins.property
    @jsii.member(jsii_name="redisIoThreads")
    def redis_io_threads(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "redisIoThreads"))

    @redis_io_threads.setter
    def redis_io_threads(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edfcca068ee4e63dd84de12097907ae14b7832dbc1fa524cf28a1e54f2f12360)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redisIoThreads", value)

    @builtins.property
    @jsii.member(jsii_name="redisLfuDecayTime")
    def redis_lfu_decay_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "redisLfuDecayTime"))

    @redis_lfu_decay_time.setter
    def redis_lfu_decay_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__affc80a7f20c87e9dd7662c5536d1ea3d06117ad5af8f791b2bc59583c311376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redisLfuDecayTime", value)

    @builtins.property
    @jsii.member(jsii_name="redisLfuLogFactor")
    def redis_lfu_log_factor(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "redisLfuLogFactor"))

    @redis_lfu_log_factor.setter
    def redis_lfu_log_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__513b8def75b8902ce4d29b3e1d5601d368ad543aa26f39fba6037ff32606b759)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redisLfuLogFactor", value)

    @builtins.property
    @jsii.member(jsii_name="redisMaxmemoryPolicy")
    def redis_maxmemory_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redisMaxmemoryPolicy"))

    @redis_maxmemory_policy.setter
    def redis_maxmemory_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__381d9fdf60e200df9bad7bb3100dae73ecf96062310bc11dfb9599eeb8946ecf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redisMaxmemoryPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="redisNotifyKeyspaceEvents")
    def redis_notify_keyspace_events(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redisNotifyKeyspaceEvents"))

    @redis_notify_keyspace_events.setter
    def redis_notify_keyspace_events(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99bb21c3afdff00845e39526c1f7d7473bf3ede39fda58ffe8eefe74bd2b9103)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redisNotifyKeyspaceEvents", value)

    @builtins.property
    @jsii.member(jsii_name="redisNumberOfDatabases")
    def redis_number_of_databases(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "redisNumberOfDatabases"))

    @redis_number_of_databases.setter
    def redis_number_of_databases(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06f1275069b09b947fef98925e34b6772f6b5090664367d03f0649d350868037)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redisNumberOfDatabases", value)

    @builtins.property
    @jsii.member(jsii_name="redisPersistence")
    def redis_persistence(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "redisPersistence"))

    @redis_persistence.setter
    def redis_persistence(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf8fe4ddcf2e1308fb32f3bb85b66c2343dfb3c7013a2663f59502d9825d4644)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redisPersistence", value)

    @builtins.property
    @jsii.member(jsii_name="redisPubsubClientOutputBufferLimit")
    def redis_pubsub_client_output_buffer_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "redisPubsubClientOutputBufferLimit"))

    @redis_pubsub_client_output_buffer_limit.setter
    def redis_pubsub_client_output_buffer_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8355b24857cc5aadfa8a5534369d87543b80e86ca20ae91c75ed226dbbd47ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redisPubsubClientOutputBufferLimit", value)

    @builtins.property
    @jsii.member(jsii_name="redisSsl")
    def redis_ssl(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "redisSsl"))

    @redis_ssl.setter
    def redis_ssl(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__057f7f5182354ccae16e3c7bfa3860540df3fd2aa67a405cd0340973ee26ca65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redisSsl", value)

    @builtins.property
    @jsii.member(jsii_name="redisTimeout")
    def redis_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "redisTimeout"))

    @redis_timeout.setter
    def redis_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba162f9db4656382a3d7339ee77ad2e2c8a45687342c8e02df83ca9f165a9f5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "redisTimeout", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ManagedDatabaseRedisProperties]:
        return typing.cast(typing.Optional[ManagedDatabaseRedisProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ManagedDatabaseRedisProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ef79d6b479bc1b03c26a40398c74333abd844270bd19a04ed4333ba621709cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "ManagedDatabaseRedis",
    "ManagedDatabaseRedisComponents",
    "ManagedDatabaseRedisComponentsList",
    "ManagedDatabaseRedisComponentsOutputReference",
    "ManagedDatabaseRedisConfig",
    "ManagedDatabaseRedisNodeStates",
    "ManagedDatabaseRedisNodeStatesList",
    "ManagedDatabaseRedisNodeStatesOutputReference",
    "ManagedDatabaseRedisProperties",
    "ManagedDatabaseRedisPropertiesMigration",
    "ManagedDatabaseRedisPropertiesMigrationOutputReference",
    "ManagedDatabaseRedisPropertiesOutputReference",
]

publication.publish()

def _typecheckingstub__1e10737b3441da242e45d6c2d2bc2f70394648ca22d7a0273fd99d90772bf1bc(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    plan: builtins.str,
    zone: builtins.str,
    id: typing.Optional[builtins.str] = None,
    maintenance_window_dow: typing.Optional[builtins.str] = None,
    maintenance_window_time: typing.Optional[builtins.str] = None,
    powered: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    properties: typing.Optional[typing.Union[ManagedDatabaseRedisProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    title: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__034efef55e5a3bbebea436a291fa62e30ce0295c063f00efa32c2e4da24fa48e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73273528d0b8cb624417054adb344b6b88a235351d2cd957c16595add16c8387(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3463082f9615ac3e2b28a306c8c416e034bb1455b562224418511e2b64e98aac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c0777aa27ee2c0d2740288a9a2eda0f15e9a07783c54594720bbb763fcf3185(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__149801ed2891da8e0ef20e0f41d11b22743e801cfdf02647165dfc8b2e3d43a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba0403ca1176e546e2415a5a55338ca5196302e1eba800025393e8cd2effefd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b9d5868df87b17b486ae6afcb3e738c388956d33f99b995a4c7ded4543a16f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6200eb68a3f6b2c3f07f5e4d5f8ae376e15d54a8f63a9eaebb800986941df925(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75e57aca0ea172e4cff02b14eeaa7f164d2407fb7cc7e60a68b03fe484ccfabb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3638c469678c1ee26b60ba0b78e20c1c01b3db110db4280e9884314cec942a20(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__123d717dd88e816c65cab6091d48edb5f8df9a633dba87ec6eb60ffde8e6ffe9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7de82f36798ec3b4929e14320c93a81a40ef32c357088821d82e7f2dda5fc08(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e969959ac62660fb87c4c430ebc9a800cf52dd0398d032cd90dab896168b1a57(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a1cb80a7cb7d5bd3fe574b03feffdb31e2b4317eaf6581b414cf9db6788d82a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cadf7da6ebfddac64d2c3486da03b72ef79772ed3bb7ff7fd01074c0d0aceeab(
    value: typing.Optional[ManagedDatabaseRedisComponents],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__427affd4287d8a7a2c0271c2fa4103a967fb5adf7f546d78c1050110eae49ae4(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    plan: builtins.str,
    zone: builtins.str,
    id: typing.Optional[builtins.str] = None,
    maintenance_window_dow: typing.Optional[builtins.str] = None,
    maintenance_window_time: typing.Optional[builtins.str] = None,
    powered: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    properties: typing.Optional[typing.Union[ManagedDatabaseRedisProperties, typing.Dict[builtins.str, typing.Any]]] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__088293269764886cb30515f25b3eb2a8c94c0b1c14420735ad1ac267e442ac06(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__507d2392485e33f8d31a7fc472023b6c8642b0b3a6c04f7ec4ae4927c3989231(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c84e1e1dab92ee6bf7f6cc30017277c61c12537ca45cb66c57001f4af67f5c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b608d522cd5b29610674b7ee44258aaa92da7f4ddbd189074353cd83ebe044dc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__370cb86e81dee1a23b1fd92a00f3cb678a81d7ff887340b5a7ab4beb087d7e36(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29cd5f8b351037da5344c386af218418fda5af69f334b53378ff76f3cd21aa96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f2a3a9eee36fcd3a0e60fb75bc2afe78a8ee62b35117c45d02a76db30e62cc8(
    value: typing.Optional[ManagedDatabaseRedisNodeStates],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45d231637cf0ee1419176ac95e538148c430674ed976ab685c332c60e8210f15(
    *,
    automatic_utility_network_ip_filter: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ip_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    migration: typing.Optional[typing.Union[ManagedDatabaseRedisPropertiesMigration, typing.Dict[builtins.str, typing.Any]]] = None,
    public_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    redis_acl_channels_default: typing.Optional[builtins.str] = None,
    redis_io_threads: typing.Optional[jsii.Number] = None,
    redis_lfu_decay_time: typing.Optional[jsii.Number] = None,
    redis_lfu_log_factor: typing.Optional[jsii.Number] = None,
    redis_maxmemory_policy: typing.Optional[builtins.str] = None,
    redis_notify_keyspace_events: typing.Optional[builtins.str] = None,
    redis_number_of_databases: typing.Optional[jsii.Number] = None,
    redis_persistence: typing.Optional[builtins.str] = None,
    redis_pubsub_client_output_buffer_limit: typing.Optional[jsii.Number] = None,
    redis_ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    redis_timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5868695ab3eeee48f1195fac696f82883094948c50a1392b710ba328c403e191(
    *,
    dbname: typing.Optional[builtins.str] = None,
    host: typing.Optional[builtins.str] = None,
    ignore_dbs: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    ssl: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eba87ce19486725e846ce1f43831cae3000a132162660004d878fbe60a98551(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a35b4d987c288c3f424ab316ab2be82e8e897a321703a552b6a60f8cb45f530(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d9433fefa974e8fd1fe9e2a1ef5cf358003310f8e14fa3d6ef0e23e46f867c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__007eee9dff2abcab87190d2496857d146bb6903679cde62609372d7f42cf7e5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0edcd87f37d9bf96c1e0d943d76f8b8ed634421134b290c428502f3a99935d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a2ca20e595901240d6d567bd3fc1dc4ce140b0c673961e770d60b25562abdc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b64ae4a372bb2c41382589f8a0c1d8d986b1694c4dce4e4e55c546e23aa2073(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82fb203b3c22ecd9831bec0b187bf29feade0ccad7832897b49ef1c6def2fe27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bc643aad8ee6415b2b24a7c3d1afef738a314f6945735e48ec970009f0e7b33(
    value: typing.Optional[ManagedDatabaseRedisPropertiesMigration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95bbb7a31e1bcfa0d5dd974d3a82ed54477e19d28618e27d10a3de84a979f2be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7a5bf9f686a94105029e10a6995c1eab34c833b8b4d0f6b257a85be803f9cf8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb934638aa3c6e837012ab6df42e93f3bf87ae5645dab83d2b4e1d837c69565a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83c60b1f4cdd9f89109ea2a9767620a069155ebf2e36d46af8ae1b70b75ea18c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf6000768e540c92b24e550c2c1c1fc34bac8f6b73d11b42391121cda644b8f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edfcca068ee4e63dd84de12097907ae14b7832dbc1fa524cf28a1e54f2f12360(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__affc80a7f20c87e9dd7662c5536d1ea3d06117ad5af8f791b2bc59583c311376(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__513b8def75b8902ce4d29b3e1d5601d368ad543aa26f39fba6037ff32606b759(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__381d9fdf60e200df9bad7bb3100dae73ecf96062310bc11dfb9599eeb8946ecf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99bb21c3afdff00845e39526c1f7d7473bf3ede39fda58ffe8eefe74bd2b9103(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06f1275069b09b947fef98925e34b6772f6b5090664367d03f0649d350868037(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf8fe4ddcf2e1308fb32f3bb85b66c2343dfb3c7013a2663f59502d9825d4644(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8355b24857cc5aadfa8a5534369d87543b80e86ca20ae91c75ed226dbbd47ce(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__057f7f5182354ccae16e3c7bfa3860540df3fd2aa67a405cd0340973ee26ca65(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba162f9db4656382a3d7339ee77ad2e2c8a45687342c8e02df83ca9f165a9f5d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ef79d6b479bc1b03c26a40398c74333abd844270bd19a04ed4333ba621709cb(
    value: typing.Optional[ManagedDatabaseRedisProperties],
) -> None:
    """Type checking stubs"""
    pass
