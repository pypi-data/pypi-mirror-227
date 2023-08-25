'''
# `mongodbatlas_advanced_cluster`

Refer to the Terraform Registory for docs: [`mongodbatlas_advanced_cluster`](https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster).
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


class AdvancedCluster(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedCluster",
):
    '''Represents a {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster mongodbatlas_advanced_cluster}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster_type: builtins.str,
        name: builtins.str,
        project_id: builtins.str,
        replication_specs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AdvancedClusterReplicationSpecs", typing.Dict[builtins.str, typing.Any]]]],
        advanced_configuration: typing.Optional[typing.Union["AdvancedClusterAdvancedConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bi_connector: typing.Optional[typing.Union["AdvancedClusterBiConnector", typing.Dict[builtins.str, typing.Any]]] = None,
        bi_connector_config: typing.Optional[typing.Union["AdvancedClusterBiConnectorConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        encryption_at_rest_provider: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AdvancedClusterLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mongo_db_major_version: typing.Optional[builtins.str] = None,
        paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pit_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retain_backups_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        root_cert_type: typing.Optional[builtins.str] = None,
        termination_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["AdvancedClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version_release_system: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster mongodbatlas_advanced_cluster} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#cluster_type AdvancedCluster#cluster_type}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#name AdvancedCluster#name}.
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#project_id AdvancedCluster#project_id}.
        :param replication_specs: replication_specs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#replication_specs AdvancedCluster#replication_specs}
        :param advanced_configuration: advanced_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#advanced_configuration AdvancedCluster#advanced_configuration}
        :param backup_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#backup_enabled AdvancedCluster#backup_enabled}.
        :param bi_connector: bi_connector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#bi_connector AdvancedCluster#bi_connector}
        :param bi_connector_config: bi_connector_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#bi_connector_config AdvancedCluster#bi_connector_config}
        :param disk_size_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#disk_size_gb AdvancedCluster#disk_size_gb}.
        :param encryption_at_rest_provider: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#encryption_at_rest_provider AdvancedCluster#encryption_at_rest_provider}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#id AdvancedCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#labels AdvancedCluster#labels}
        :param mongo_db_major_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#mongo_db_major_version AdvancedCluster#mongo_db_major_version}.
        :param paused: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#paused AdvancedCluster#paused}.
        :param pit_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#pit_enabled AdvancedCluster#pit_enabled}.
        :param retain_backups_enabled: Flag that indicates whether to retain backup snapshots for the deleted dedicated cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#retain_backups_enabled AdvancedCluster#retain_backups_enabled}
        :param root_cert_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#root_cert_type AdvancedCluster#root_cert_type}.
        :param termination_protection_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#termination_protection_enabled AdvancedCluster#termination_protection_enabled}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#timeouts AdvancedCluster#timeouts}
        :param version_release_system: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#version_release_system AdvancedCluster#version_release_system}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ca391e210dd2501c08a1078aaa9b0b13dafb996142bf6967d14ad720147cc40)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AdvancedClusterConfig(
            cluster_type=cluster_type,
            name=name,
            project_id=project_id,
            replication_specs=replication_specs,
            advanced_configuration=advanced_configuration,
            backup_enabled=backup_enabled,
            bi_connector=bi_connector,
            bi_connector_config=bi_connector_config,
            disk_size_gb=disk_size_gb,
            encryption_at_rest_provider=encryption_at_rest_provider,
            id=id,
            labels=labels,
            mongo_db_major_version=mongo_db_major_version,
            paused=paused,
            pit_enabled=pit_enabled,
            retain_backups_enabled=retain_backups_enabled,
            root_cert_type=root_cert_type,
            termination_protection_enabled=termination_protection_enabled,
            timeouts=timeouts,
            version_release_system=version_release_system,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putAdvancedConfiguration")
    def put_advanced_configuration(
        self,
        *,
        default_read_concern: typing.Optional[builtins.str] = None,
        default_write_concern: typing.Optional[builtins.str] = None,
        fail_index_key_too_long: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        javascript_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        minimum_enabled_tls_protocol: typing.Optional[builtins.str] = None,
        no_table_scan: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        oplog_min_retention_hours: typing.Optional[jsii.Number] = None,
        oplog_size_mb: typing.Optional[jsii.Number] = None,
        sample_refresh_interval_bi_connector: typing.Optional[jsii.Number] = None,
        sample_size_bi_connector: typing.Optional[jsii.Number] = None,
        transaction_lifetime_limit_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param default_read_concern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#default_read_concern AdvancedCluster#default_read_concern}.
        :param default_write_concern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#default_write_concern AdvancedCluster#default_write_concern}.
        :param fail_index_key_too_long: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#fail_index_key_too_long AdvancedCluster#fail_index_key_too_long}.
        :param javascript_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#javascript_enabled AdvancedCluster#javascript_enabled}.
        :param minimum_enabled_tls_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#minimum_enabled_tls_protocol AdvancedCluster#minimum_enabled_tls_protocol}.
        :param no_table_scan: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#no_table_scan AdvancedCluster#no_table_scan}.
        :param oplog_min_retention_hours: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#oplog_min_retention_hours AdvancedCluster#oplog_min_retention_hours}.
        :param oplog_size_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#oplog_size_mb AdvancedCluster#oplog_size_mb}.
        :param sample_refresh_interval_bi_connector: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#sample_refresh_interval_bi_connector AdvancedCluster#sample_refresh_interval_bi_connector}.
        :param sample_size_bi_connector: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#sample_size_bi_connector AdvancedCluster#sample_size_bi_connector}.
        :param transaction_lifetime_limit_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#transaction_lifetime_limit_seconds AdvancedCluster#transaction_lifetime_limit_seconds}.
        '''
        value = AdvancedClusterAdvancedConfiguration(
            default_read_concern=default_read_concern,
            default_write_concern=default_write_concern,
            fail_index_key_too_long=fail_index_key_too_long,
            javascript_enabled=javascript_enabled,
            minimum_enabled_tls_protocol=minimum_enabled_tls_protocol,
            no_table_scan=no_table_scan,
            oplog_min_retention_hours=oplog_min_retention_hours,
            oplog_size_mb=oplog_size_mb,
            sample_refresh_interval_bi_connector=sample_refresh_interval_bi_connector,
            sample_size_bi_connector=sample_size_bi_connector,
            transaction_lifetime_limit_seconds=transaction_lifetime_limit_seconds,
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedConfiguration", [value]))

    @jsii.member(jsii_name="putBiConnector")
    def put_bi_connector(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        read_preference: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#enabled AdvancedCluster#enabled}.
        :param read_preference: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#read_preference AdvancedCluster#read_preference}.
        '''
        value = AdvancedClusterBiConnector(
            enabled=enabled, read_preference=read_preference
        )

        return typing.cast(None, jsii.invoke(self, "putBiConnector", [value]))

    @jsii.member(jsii_name="putBiConnectorConfig")
    def put_bi_connector_config(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        read_preference: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#enabled AdvancedCluster#enabled}.
        :param read_preference: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#read_preference AdvancedCluster#read_preference}.
        '''
        value = AdvancedClusterBiConnectorConfig(
            enabled=enabled, read_preference=read_preference
        )

        return typing.cast(None, jsii.invoke(self, "putBiConnectorConfig", [value]))

    @jsii.member(jsii_name="putLabels")
    def put_labels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AdvancedClusterLabels", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0f54960afae626e790c1acd0c2f3d6ea13873f5c4a95cd47c86efd327ecf0e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLabels", [value]))

    @jsii.member(jsii_name="putReplicationSpecs")
    def put_replication_specs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AdvancedClusterReplicationSpecs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45a92f697d36829c0ed5d33dfa4e117ceb29aa47f23bc874fda9adc1c7265ff2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putReplicationSpecs", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#create AdvancedCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#delete AdvancedCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#update AdvancedCluster#update}.
        '''
        value = AdvancedClusterTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdvancedConfiguration")
    def reset_advanced_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedConfiguration", []))

    @jsii.member(jsii_name="resetBackupEnabled")
    def reset_backup_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackupEnabled", []))

    @jsii.member(jsii_name="resetBiConnector")
    def reset_bi_connector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBiConnector", []))

    @jsii.member(jsii_name="resetBiConnectorConfig")
    def reset_bi_connector_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBiConnectorConfig", []))

    @jsii.member(jsii_name="resetDiskSizeGb")
    def reset_disk_size_gb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskSizeGb", []))

    @jsii.member(jsii_name="resetEncryptionAtRestProvider")
    def reset_encryption_at_rest_provider(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionAtRestProvider", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLabels")
    def reset_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabels", []))

    @jsii.member(jsii_name="resetMongoDbMajorVersion")
    def reset_mongo_db_major_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMongoDbMajorVersion", []))

    @jsii.member(jsii_name="resetPaused")
    def reset_paused(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPaused", []))

    @jsii.member(jsii_name="resetPitEnabled")
    def reset_pit_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPitEnabled", []))

    @jsii.member(jsii_name="resetRetainBackupsEnabled")
    def reset_retain_backups_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetainBackupsEnabled", []))

    @jsii.member(jsii_name="resetRootCertType")
    def reset_root_cert_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootCertType", []))

    @jsii.member(jsii_name="resetTerminationProtectionEnabled")
    def reset_termination_protection_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTerminationProtectionEnabled", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVersionReleaseSystem")
    def reset_version_release_system(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVersionReleaseSystem", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="advancedConfiguration")
    def advanced_configuration(
        self,
    ) -> "AdvancedClusterAdvancedConfigurationOutputReference":
        return typing.cast("AdvancedClusterAdvancedConfigurationOutputReference", jsii.get(self, "advancedConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="biConnector")
    def bi_connector(self) -> "AdvancedClusterBiConnectorOutputReference":
        return typing.cast("AdvancedClusterBiConnectorOutputReference", jsii.get(self, "biConnector"))

    @builtins.property
    @jsii.member(jsii_name="biConnectorConfig")
    def bi_connector_config(self) -> "AdvancedClusterBiConnectorConfigOutputReference":
        return typing.cast("AdvancedClusterBiConnectorConfigOutputReference", jsii.get(self, "biConnectorConfig"))

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @builtins.property
    @jsii.member(jsii_name="connectionStrings")
    def connection_strings(self) -> "AdvancedClusterConnectionStringsList":
        return typing.cast("AdvancedClusterConnectionStringsList", jsii.get(self, "connectionStrings"))

    @builtins.property
    @jsii.member(jsii_name="createDate")
    def create_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createDate"))

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> "AdvancedClusterLabelsList":
        return typing.cast("AdvancedClusterLabelsList", jsii.get(self, "labels"))

    @builtins.property
    @jsii.member(jsii_name="mongoDbVersion")
    def mongo_db_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mongoDbVersion"))

    @builtins.property
    @jsii.member(jsii_name="replicationSpecs")
    def replication_specs(self) -> "AdvancedClusterReplicationSpecsList":
        return typing.cast("AdvancedClusterReplicationSpecsList", jsii.get(self, "replicationSpecs"))

    @builtins.property
    @jsii.member(jsii_name="stateName")
    def state_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stateName"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "AdvancedClusterTimeoutsOutputReference":
        return typing.cast("AdvancedClusterTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="advancedConfigurationInput")
    def advanced_configuration_input(
        self,
    ) -> typing.Optional["AdvancedClusterAdvancedConfiguration"]:
        return typing.cast(typing.Optional["AdvancedClusterAdvancedConfiguration"], jsii.get(self, "advancedConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="backupEnabledInput")
    def backup_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "backupEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="biConnectorConfigInput")
    def bi_connector_config_input(
        self,
    ) -> typing.Optional["AdvancedClusterBiConnectorConfig"]:
        return typing.cast(typing.Optional["AdvancedClusterBiConnectorConfig"], jsii.get(self, "biConnectorConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="biConnectorInput")
    def bi_connector_input(self) -> typing.Optional["AdvancedClusterBiConnector"]:
        return typing.cast(typing.Optional["AdvancedClusterBiConnector"], jsii.get(self, "biConnectorInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterTypeInput")
    def cluster_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="diskSizeGbInput")
    def disk_size_gb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskSizeGbInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionAtRestProviderInput")
    def encryption_at_rest_provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "encryptionAtRestProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="labelsInput")
    def labels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AdvancedClusterLabels"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AdvancedClusterLabels"]]], jsii.get(self, "labelsInput"))

    @builtins.property
    @jsii.member(jsii_name="mongoDbMajorVersionInput")
    def mongo_db_major_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mongoDbMajorVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pausedInput")
    def paused_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pausedInput"))

    @builtins.property
    @jsii.member(jsii_name="pitEnabledInput")
    def pit_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pitEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="replicationSpecsInput")
    def replication_specs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AdvancedClusterReplicationSpecs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AdvancedClusterReplicationSpecs"]]], jsii.get(self, "replicationSpecsInput"))

    @builtins.property
    @jsii.member(jsii_name="retainBackupsEnabledInput")
    def retain_backups_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "retainBackupsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="rootCertTypeInput")
    def root_cert_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rootCertTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="terminationProtectionEnabledInput")
    def termination_protection_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "terminationProtectionEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AdvancedClusterTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "AdvancedClusterTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="versionReleaseSystemInput")
    def version_release_system_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionReleaseSystemInput"))

    @builtins.property
    @jsii.member(jsii_name="backupEnabled")
    def backup_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "backupEnabled"))

    @backup_enabled.setter
    def backup_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f36d43ee09f62eda38ca52a630ce978a4d2a6b0e80d07a0f6ee73d0ddc45898)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backupEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="clusterType")
    def cluster_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterType"))

    @cluster_type.setter
    def cluster_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88b381b94247030bd2ec13b3f5a8ebb5e68c37110cc3e8d6e72484668592363f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterType", value)

    @builtins.property
    @jsii.member(jsii_name="diskSizeGb")
    def disk_size_gb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskSizeGb"))

    @disk_size_gb.setter
    def disk_size_gb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2207623f87bfee8e123a93206e9e1faa8872ae0d187432c7945861c01c3542b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskSizeGb", value)

    @builtins.property
    @jsii.member(jsii_name="encryptionAtRestProvider")
    def encryption_at_rest_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "encryptionAtRestProvider"))

    @encryption_at_rest_provider.setter
    def encryption_at_rest_provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef0dba68b05b7e0a97c174a2e5e44232bdc4e6f6516649ecf9d9dd971393b7df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryptionAtRestProvider", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca23373bec3ef7123444356794b16d1b1be1ec03ac8ecaabb3bf93ca1c28f9c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="mongoDbMajorVersion")
    def mongo_db_major_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mongoDbMajorVersion"))

    @mongo_db_major_version.setter
    def mongo_db_major_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01ea4321617f74da287d8dc515d628c7d2501cc13d8655a9c57d1d0777d94196)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mongoDbMajorVersion", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__936076a5bc0c4e679d136fea19895c5f7a381b5eca5ee69886a0d1fdaf110550)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="paused")
    def paused(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "paused"))

    @paused.setter
    def paused(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4e4972712a5af56caf23cc7d07d9c086e697327db7061268358e792380c229b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "paused", value)

    @builtins.property
    @jsii.member(jsii_name="pitEnabled")
    def pit_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pitEnabled"))

    @pit_enabled.setter
    def pit_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c2f2162190ceb431ce37f41993d349adff76de2914942509299a8c28d057ce8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pitEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62c600021a78716ee8cd967e6b21480b96bb9119e5726fc6f649a6ab848e4dd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value)

    @builtins.property
    @jsii.member(jsii_name="retainBackupsEnabled")
    def retain_backups_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "retainBackupsEnabled"))

    @retain_backups_enabled.setter
    def retain_backups_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef0c5231e480aa88441b6f8415419e59309e0ae70264afc4620986897c5f0321)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retainBackupsEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="rootCertType")
    def root_cert_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rootCertType"))

    @root_cert_type.setter
    def root_cert_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__834f398d42a6bb39f756bc583136ff7d6787605621cebb8e15e3a39601d8ae12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootCertType", value)

    @builtins.property
    @jsii.member(jsii_name="terminationProtectionEnabled")
    def termination_protection_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "terminationProtectionEnabled"))

    @termination_protection_enabled.setter
    def termination_protection_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afc159d24c4c98c2ca7aa715ea2245f04b4480895168c28cad658cc425c307dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terminationProtectionEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="versionReleaseSystem")
    def version_release_system(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "versionReleaseSystem"))

    @version_release_system.setter
    def version_release_system(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c77ed15f187542791ad1047ad7cbd8966e5f65e81b6a133a58f872cd5e87d56f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionReleaseSystem", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterAdvancedConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "default_read_concern": "defaultReadConcern",
        "default_write_concern": "defaultWriteConcern",
        "fail_index_key_too_long": "failIndexKeyTooLong",
        "javascript_enabled": "javascriptEnabled",
        "minimum_enabled_tls_protocol": "minimumEnabledTlsProtocol",
        "no_table_scan": "noTableScan",
        "oplog_min_retention_hours": "oplogMinRetentionHours",
        "oplog_size_mb": "oplogSizeMb",
        "sample_refresh_interval_bi_connector": "sampleRefreshIntervalBiConnector",
        "sample_size_bi_connector": "sampleSizeBiConnector",
        "transaction_lifetime_limit_seconds": "transactionLifetimeLimitSeconds",
    },
)
class AdvancedClusterAdvancedConfiguration:
    def __init__(
        self,
        *,
        default_read_concern: typing.Optional[builtins.str] = None,
        default_write_concern: typing.Optional[builtins.str] = None,
        fail_index_key_too_long: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        javascript_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        minimum_enabled_tls_protocol: typing.Optional[builtins.str] = None,
        no_table_scan: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        oplog_min_retention_hours: typing.Optional[jsii.Number] = None,
        oplog_size_mb: typing.Optional[jsii.Number] = None,
        sample_refresh_interval_bi_connector: typing.Optional[jsii.Number] = None,
        sample_size_bi_connector: typing.Optional[jsii.Number] = None,
        transaction_lifetime_limit_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param default_read_concern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#default_read_concern AdvancedCluster#default_read_concern}.
        :param default_write_concern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#default_write_concern AdvancedCluster#default_write_concern}.
        :param fail_index_key_too_long: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#fail_index_key_too_long AdvancedCluster#fail_index_key_too_long}.
        :param javascript_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#javascript_enabled AdvancedCluster#javascript_enabled}.
        :param minimum_enabled_tls_protocol: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#minimum_enabled_tls_protocol AdvancedCluster#minimum_enabled_tls_protocol}.
        :param no_table_scan: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#no_table_scan AdvancedCluster#no_table_scan}.
        :param oplog_min_retention_hours: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#oplog_min_retention_hours AdvancedCluster#oplog_min_retention_hours}.
        :param oplog_size_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#oplog_size_mb AdvancedCluster#oplog_size_mb}.
        :param sample_refresh_interval_bi_connector: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#sample_refresh_interval_bi_connector AdvancedCluster#sample_refresh_interval_bi_connector}.
        :param sample_size_bi_connector: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#sample_size_bi_connector AdvancedCluster#sample_size_bi_connector}.
        :param transaction_lifetime_limit_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#transaction_lifetime_limit_seconds AdvancedCluster#transaction_lifetime_limit_seconds}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f07f574c8fa825280fa076178783cd1825a9a5aa840a722e7c12419caa7537be)
            check_type(argname="argument default_read_concern", value=default_read_concern, expected_type=type_hints["default_read_concern"])
            check_type(argname="argument default_write_concern", value=default_write_concern, expected_type=type_hints["default_write_concern"])
            check_type(argname="argument fail_index_key_too_long", value=fail_index_key_too_long, expected_type=type_hints["fail_index_key_too_long"])
            check_type(argname="argument javascript_enabled", value=javascript_enabled, expected_type=type_hints["javascript_enabled"])
            check_type(argname="argument minimum_enabled_tls_protocol", value=minimum_enabled_tls_protocol, expected_type=type_hints["minimum_enabled_tls_protocol"])
            check_type(argname="argument no_table_scan", value=no_table_scan, expected_type=type_hints["no_table_scan"])
            check_type(argname="argument oplog_min_retention_hours", value=oplog_min_retention_hours, expected_type=type_hints["oplog_min_retention_hours"])
            check_type(argname="argument oplog_size_mb", value=oplog_size_mb, expected_type=type_hints["oplog_size_mb"])
            check_type(argname="argument sample_refresh_interval_bi_connector", value=sample_refresh_interval_bi_connector, expected_type=type_hints["sample_refresh_interval_bi_connector"])
            check_type(argname="argument sample_size_bi_connector", value=sample_size_bi_connector, expected_type=type_hints["sample_size_bi_connector"])
            check_type(argname="argument transaction_lifetime_limit_seconds", value=transaction_lifetime_limit_seconds, expected_type=type_hints["transaction_lifetime_limit_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if default_read_concern is not None:
            self._values["default_read_concern"] = default_read_concern
        if default_write_concern is not None:
            self._values["default_write_concern"] = default_write_concern
        if fail_index_key_too_long is not None:
            self._values["fail_index_key_too_long"] = fail_index_key_too_long
        if javascript_enabled is not None:
            self._values["javascript_enabled"] = javascript_enabled
        if minimum_enabled_tls_protocol is not None:
            self._values["minimum_enabled_tls_protocol"] = minimum_enabled_tls_protocol
        if no_table_scan is not None:
            self._values["no_table_scan"] = no_table_scan
        if oplog_min_retention_hours is not None:
            self._values["oplog_min_retention_hours"] = oplog_min_retention_hours
        if oplog_size_mb is not None:
            self._values["oplog_size_mb"] = oplog_size_mb
        if sample_refresh_interval_bi_connector is not None:
            self._values["sample_refresh_interval_bi_connector"] = sample_refresh_interval_bi_connector
        if sample_size_bi_connector is not None:
            self._values["sample_size_bi_connector"] = sample_size_bi_connector
        if transaction_lifetime_limit_seconds is not None:
            self._values["transaction_lifetime_limit_seconds"] = transaction_lifetime_limit_seconds

    @builtins.property
    def default_read_concern(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#default_read_concern AdvancedCluster#default_read_concern}.'''
        result = self._values.get("default_read_concern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_write_concern(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#default_write_concern AdvancedCluster#default_write_concern}.'''
        result = self._values.get("default_write_concern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fail_index_key_too_long(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#fail_index_key_too_long AdvancedCluster#fail_index_key_too_long}.'''
        result = self._values.get("fail_index_key_too_long")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def javascript_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#javascript_enabled AdvancedCluster#javascript_enabled}.'''
        result = self._values.get("javascript_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def minimum_enabled_tls_protocol(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#minimum_enabled_tls_protocol AdvancedCluster#minimum_enabled_tls_protocol}.'''
        result = self._values.get("minimum_enabled_tls_protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_table_scan(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#no_table_scan AdvancedCluster#no_table_scan}.'''
        result = self._values.get("no_table_scan")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def oplog_min_retention_hours(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#oplog_min_retention_hours AdvancedCluster#oplog_min_retention_hours}.'''
        result = self._values.get("oplog_min_retention_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def oplog_size_mb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#oplog_size_mb AdvancedCluster#oplog_size_mb}.'''
        result = self._values.get("oplog_size_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sample_refresh_interval_bi_connector(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#sample_refresh_interval_bi_connector AdvancedCluster#sample_refresh_interval_bi_connector}.'''
        result = self._values.get("sample_refresh_interval_bi_connector")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def sample_size_bi_connector(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#sample_size_bi_connector AdvancedCluster#sample_size_bi_connector}.'''
        result = self._values.get("sample_size_bi_connector")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def transaction_lifetime_limit_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#transaction_lifetime_limit_seconds AdvancedCluster#transaction_lifetime_limit_seconds}.'''
        result = self._values.get("transaction_lifetime_limit_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdvancedClusterAdvancedConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AdvancedClusterAdvancedConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterAdvancedConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c975f663462f36982521e95f7c1fe6b57ef1d81da2e6ab4e5ed39f7730aa571)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDefaultReadConcern")
    def reset_default_read_concern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultReadConcern", []))

    @jsii.member(jsii_name="resetDefaultWriteConcern")
    def reset_default_write_concern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultWriteConcern", []))

    @jsii.member(jsii_name="resetFailIndexKeyTooLong")
    def reset_fail_index_key_too_long(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFailIndexKeyTooLong", []))

    @jsii.member(jsii_name="resetJavascriptEnabled")
    def reset_javascript_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJavascriptEnabled", []))

    @jsii.member(jsii_name="resetMinimumEnabledTlsProtocol")
    def reset_minimum_enabled_tls_protocol(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumEnabledTlsProtocol", []))

    @jsii.member(jsii_name="resetNoTableScan")
    def reset_no_table_scan(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoTableScan", []))

    @jsii.member(jsii_name="resetOplogMinRetentionHours")
    def reset_oplog_min_retention_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOplogMinRetentionHours", []))

    @jsii.member(jsii_name="resetOplogSizeMb")
    def reset_oplog_size_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOplogSizeMb", []))

    @jsii.member(jsii_name="resetSampleRefreshIntervalBiConnector")
    def reset_sample_refresh_interval_bi_connector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSampleRefreshIntervalBiConnector", []))

    @jsii.member(jsii_name="resetSampleSizeBiConnector")
    def reset_sample_size_bi_connector(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSampleSizeBiConnector", []))

    @jsii.member(jsii_name="resetTransactionLifetimeLimitSeconds")
    def reset_transaction_lifetime_limit_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransactionLifetimeLimitSeconds", []))

    @builtins.property
    @jsii.member(jsii_name="defaultReadConcernInput")
    def default_read_concern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultReadConcernInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultWriteConcernInput")
    def default_write_concern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultWriteConcernInput"))

    @builtins.property
    @jsii.member(jsii_name="failIndexKeyTooLongInput")
    def fail_index_key_too_long_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "failIndexKeyTooLongInput"))

    @builtins.property
    @jsii.member(jsii_name="javascriptEnabledInput")
    def javascript_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "javascriptEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumEnabledTlsProtocolInput")
    def minimum_enabled_tls_protocol_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minimumEnabledTlsProtocolInput"))

    @builtins.property
    @jsii.member(jsii_name="noTableScanInput")
    def no_table_scan_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noTableScanInput"))

    @builtins.property
    @jsii.member(jsii_name="oplogMinRetentionHoursInput")
    def oplog_min_retention_hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "oplogMinRetentionHoursInput"))

    @builtins.property
    @jsii.member(jsii_name="oplogSizeMbInput")
    def oplog_size_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "oplogSizeMbInput"))

    @builtins.property
    @jsii.member(jsii_name="sampleRefreshIntervalBiConnectorInput")
    def sample_refresh_interval_bi_connector_input(
        self,
    ) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sampleRefreshIntervalBiConnectorInput"))

    @builtins.property
    @jsii.member(jsii_name="sampleSizeBiConnectorInput")
    def sample_size_bi_connector_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sampleSizeBiConnectorInput"))

    @builtins.property
    @jsii.member(jsii_name="transactionLifetimeLimitSecondsInput")
    def transaction_lifetime_limit_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "transactionLifetimeLimitSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultReadConcern")
    def default_read_concern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultReadConcern"))

    @default_read_concern.setter
    def default_read_concern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ae4d5ec4e494cb89987768cc5ee557be889fd253f54376da23912b4f601866f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultReadConcern", value)

    @builtins.property
    @jsii.member(jsii_name="defaultWriteConcern")
    def default_write_concern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultWriteConcern"))

    @default_write_concern.setter
    def default_write_concern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d225ef8f1fed237dc5286680280c4d6c905b6cff2d1517d8e487f6905600514)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultWriteConcern", value)

    @builtins.property
    @jsii.member(jsii_name="failIndexKeyTooLong")
    def fail_index_key_too_long(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "failIndexKeyTooLong"))

    @fail_index_key_too_long.setter
    def fail_index_key_too_long(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd4cb7ee12b8c30c5083a4badced9c5d6b20279ebfb62a1ea57a3aed15d64b93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failIndexKeyTooLong", value)

    @builtins.property
    @jsii.member(jsii_name="javascriptEnabled")
    def javascript_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "javascriptEnabled"))

    @javascript_enabled.setter
    def javascript_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caae5634c05f81728ddb96703412f068d28d97dcbaa6cb01c8cb45c535be49ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "javascriptEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="minimumEnabledTlsProtocol")
    def minimum_enabled_tls_protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimumEnabledTlsProtocol"))

    @minimum_enabled_tls_protocol.setter
    def minimum_enabled_tls_protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__821004f34ef005b4543d12a9cada93d5b8f791c04eb5f40ae9a37629c3a1350e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumEnabledTlsProtocol", value)

    @builtins.property
    @jsii.member(jsii_name="noTableScan")
    def no_table_scan(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noTableScan"))

    @no_table_scan.setter
    def no_table_scan(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fc2273dfea54f6b8d680c0129d12f046f0dae72194d339376fb83a11f4eb0db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noTableScan", value)

    @builtins.property
    @jsii.member(jsii_name="oplogMinRetentionHours")
    def oplog_min_retention_hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "oplogMinRetentionHours"))

    @oplog_min_retention_hours.setter
    def oplog_min_retention_hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b810895493074079670d2ead5c313d607880aececb73e81cac91ecc55fde0cef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oplogMinRetentionHours", value)

    @builtins.property
    @jsii.member(jsii_name="oplogSizeMb")
    def oplog_size_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "oplogSizeMb"))

    @oplog_size_mb.setter
    def oplog_size_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89107f11f98a245655bdea9a3802fa476eed1aa8db157eceb9872bc62a8577d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oplogSizeMb", value)

    @builtins.property
    @jsii.member(jsii_name="sampleRefreshIntervalBiConnector")
    def sample_refresh_interval_bi_connector(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sampleRefreshIntervalBiConnector"))

    @sample_refresh_interval_bi_connector.setter
    def sample_refresh_interval_bi_connector(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ece2be870ca344009bad309d78c6b9464752378c276cb42686fe0e6d7436dc41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleRefreshIntervalBiConnector", value)

    @builtins.property
    @jsii.member(jsii_name="sampleSizeBiConnector")
    def sample_size_bi_connector(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sampleSizeBiConnector"))

    @sample_size_bi_connector.setter
    def sample_size_bi_connector(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8372262400117b8b85773571d23accdd28b0c99e7ac9633dee47628bd513a56b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleSizeBiConnector", value)

    @builtins.property
    @jsii.member(jsii_name="transactionLifetimeLimitSeconds")
    def transaction_lifetime_limit_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "transactionLifetimeLimitSeconds"))

    @transaction_lifetime_limit_seconds.setter
    def transaction_lifetime_limit_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca1d68d84db63873b044ba72b3c748dba19826398340fa4b0b111748f23d164e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transactionLifetimeLimitSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AdvancedClusterAdvancedConfiguration]:
        return typing.cast(typing.Optional[AdvancedClusterAdvancedConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AdvancedClusterAdvancedConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10111819735c9050a9477bbe0003476fab1dde30d153e59a390f60cb76158217)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterBiConnector",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "read_preference": "readPreference"},
)
class AdvancedClusterBiConnector:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        read_preference: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#enabled AdvancedCluster#enabled}.
        :param read_preference: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#read_preference AdvancedCluster#read_preference}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66ba636ed83dc56cbf615e406699b342a917dc02e8ef2ca9d4f7c7bfaee4feae)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument read_preference", value=read_preference, expected_type=type_hints["read_preference"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if read_preference is not None:
            self._values["read_preference"] = read_preference

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#enabled AdvancedCluster#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def read_preference(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#read_preference AdvancedCluster#read_preference}.'''
        result = self._values.get("read_preference")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdvancedClusterBiConnector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterBiConnectorConfig",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "read_preference": "readPreference"},
)
class AdvancedClusterBiConnectorConfig:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        read_preference: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#enabled AdvancedCluster#enabled}.
        :param read_preference: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#read_preference AdvancedCluster#read_preference}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fd542d3c606f4b134cc8957c519b14013250ce2bd271a16969b5137c79c03bb)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument read_preference", value=read_preference, expected_type=type_hints["read_preference"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if read_preference is not None:
            self._values["read_preference"] = read_preference

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#enabled AdvancedCluster#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def read_preference(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#read_preference AdvancedCluster#read_preference}.'''
        result = self._values.get("read_preference")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdvancedClusterBiConnectorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AdvancedClusterBiConnectorConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterBiConnectorConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__10db520513acf5894f7f007cb234f434ae1e796dc914f719b5d118bd3d0c9b6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetReadPreference")
    def reset_read_preference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadPreference", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="readPreferenceInput")
    def read_preference_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readPreferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__906560276e1f1414721bd1e51e3991002381689c98389d6012ec92970018e6f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="readPreference")
    def read_preference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "readPreference"))

    @read_preference.setter
    def read_preference(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fd2f5b912abd381ce9da0d4938c8e5b92fc2b10f41d51acad1146bdcd6aa450)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readPreference", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AdvancedClusterBiConnectorConfig]:
        return typing.cast(typing.Optional[AdvancedClusterBiConnectorConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AdvancedClusterBiConnectorConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e0e3639fcc451a43294a5307a83345db8f359be114788e18c3cb54e8d8dc75b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AdvancedClusterBiConnectorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterBiConnectorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e33796d80afb9d8f7fd7dbc20721b1f9c4a2983cdd38304780c3c4664a00900)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetReadPreference")
    def reset_read_preference(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadPreference", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="readPreferenceInput")
    def read_preference_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readPreferenceInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7e49b6a9b630d29962c56424fc5cfede1d59b994db2641926cf75c66bb46e30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="readPreference")
    def read_preference(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "readPreference"))

    @read_preference.setter
    def read_preference(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__026b6a96329ccfd575fff77352d2918c1f16cf22194711a5893e91784163adf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readPreference", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AdvancedClusterBiConnector]:
        return typing.cast(typing.Optional[AdvancedClusterBiConnector], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AdvancedClusterBiConnector],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__157416fe5fa2bbd3b3f40a760bc241470adefa9887cdc83fa12ab9aa3787ca82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cluster_type": "clusterType",
        "name": "name",
        "project_id": "projectId",
        "replication_specs": "replicationSpecs",
        "advanced_configuration": "advancedConfiguration",
        "backup_enabled": "backupEnabled",
        "bi_connector": "biConnector",
        "bi_connector_config": "biConnectorConfig",
        "disk_size_gb": "diskSizeGb",
        "encryption_at_rest_provider": "encryptionAtRestProvider",
        "id": "id",
        "labels": "labels",
        "mongo_db_major_version": "mongoDbMajorVersion",
        "paused": "paused",
        "pit_enabled": "pitEnabled",
        "retain_backups_enabled": "retainBackupsEnabled",
        "root_cert_type": "rootCertType",
        "termination_protection_enabled": "terminationProtectionEnabled",
        "timeouts": "timeouts",
        "version_release_system": "versionReleaseSystem",
    },
)
class AdvancedClusterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cluster_type: builtins.str,
        name: builtins.str,
        project_id: builtins.str,
        replication_specs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AdvancedClusterReplicationSpecs", typing.Dict[builtins.str, typing.Any]]]],
        advanced_configuration: typing.Optional[typing.Union[AdvancedClusterAdvancedConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bi_connector: typing.Optional[typing.Union[AdvancedClusterBiConnector, typing.Dict[builtins.str, typing.Any]]] = None,
        bi_connector_config: typing.Optional[typing.Union[AdvancedClusterBiConnectorConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        disk_size_gb: typing.Optional[jsii.Number] = None,
        encryption_at_rest_provider: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AdvancedClusterLabels", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mongo_db_major_version: typing.Optional[builtins.str] = None,
        paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pit_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retain_backups_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        root_cert_type: typing.Optional[builtins.str] = None,
        termination_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["AdvancedClusterTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        version_release_system: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#cluster_type AdvancedCluster#cluster_type}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#name AdvancedCluster#name}.
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#project_id AdvancedCluster#project_id}.
        :param replication_specs: replication_specs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#replication_specs AdvancedCluster#replication_specs}
        :param advanced_configuration: advanced_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#advanced_configuration AdvancedCluster#advanced_configuration}
        :param backup_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#backup_enabled AdvancedCluster#backup_enabled}.
        :param bi_connector: bi_connector block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#bi_connector AdvancedCluster#bi_connector}
        :param bi_connector_config: bi_connector_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#bi_connector_config AdvancedCluster#bi_connector_config}
        :param disk_size_gb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#disk_size_gb AdvancedCluster#disk_size_gb}.
        :param encryption_at_rest_provider: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#encryption_at_rest_provider AdvancedCluster#encryption_at_rest_provider}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#id AdvancedCluster#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param labels: labels block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#labels AdvancedCluster#labels}
        :param mongo_db_major_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#mongo_db_major_version AdvancedCluster#mongo_db_major_version}.
        :param paused: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#paused AdvancedCluster#paused}.
        :param pit_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#pit_enabled AdvancedCluster#pit_enabled}.
        :param retain_backups_enabled: Flag that indicates whether to retain backup snapshots for the deleted dedicated cluster. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#retain_backups_enabled AdvancedCluster#retain_backups_enabled}
        :param root_cert_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#root_cert_type AdvancedCluster#root_cert_type}.
        :param termination_protection_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#termination_protection_enabled AdvancedCluster#termination_protection_enabled}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#timeouts AdvancedCluster#timeouts}
        :param version_release_system: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#version_release_system AdvancedCluster#version_release_system}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(advanced_configuration, dict):
            advanced_configuration = AdvancedClusterAdvancedConfiguration(**advanced_configuration)
        if isinstance(bi_connector, dict):
            bi_connector = AdvancedClusterBiConnector(**bi_connector)
        if isinstance(bi_connector_config, dict):
            bi_connector_config = AdvancedClusterBiConnectorConfig(**bi_connector_config)
        if isinstance(timeouts, dict):
            timeouts = AdvancedClusterTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a30363ced36434a5e9034e0121c751d81ecf1ea1bcb86ae6e5a509ce56875323)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cluster_type", value=cluster_type, expected_type=type_hints["cluster_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument replication_specs", value=replication_specs, expected_type=type_hints["replication_specs"])
            check_type(argname="argument advanced_configuration", value=advanced_configuration, expected_type=type_hints["advanced_configuration"])
            check_type(argname="argument backup_enabled", value=backup_enabled, expected_type=type_hints["backup_enabled"])
            check_type(argname="argument bi_connector", value=bi_connector, expected_type=type_hints["bi_connector"])
            check_type(argname="argument bi_connector_config", value=bi_connector_config, expected_type=type_hints["bi_connector_config"])
            check_type(argname="argument disk_size_gb", value=disk_size_gb, expected_type=type_hints["disk_size_gb"])
            check_type(argname="argument encryption_at_rest_provider", value=encryption_at_rest_provider, expected_type=type_hints["encryption_at_rest_provider"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument mongo_db_major_version", value=mongo_db_major_version, expected_type=type_hints["mongo_db_major_version"])
            check_type(argname="argument paused", value=paused, expected_type=type_hints["paused"])
            check_type(argname="argument pit_enabled", value=pit_enabled, expected_type=type_hints["pit_enabled"])
            check_type(argname="argument retain_backups_enabled", value=retain_backups_enabled, expected_type=type_hints["retain_backups_enabled"])
            check_type(argname="argument root_cert_type", value=root_cert_type, expected_type=type_hints["root_cert_type"])
            check_type(argname="argument termination_protection_enabled", value=termination_protection_enabled, expected_type=type_hints["termination_protection_enabled"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument version_release_system", value=version_release_system, expected_type=type_hints["version_release_system"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_type": cluster_type,
            "name": name,
            "project_id": project_id,
            "replication_specs": replication_specs,
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
        if advanced_configuration is not None:
            self._values["advanced_configuration"] = advanced_configuration
        if backup_enabled is not None:
            self._values["backup_enabled"] = backup_enabled
        if bi_connector is not None:
            self._values["bi_connector"] = bi_connector
        if bi_connector_config is not None:
            self._values["bi_connector_config"] = bi_connector_config
        if disk_size_gb is not None:
            self._values["disk_size_gb"] = disk_size_gb
        if encryption_at_rest_provider is not None:
            self._values["encryption_at_rest_provider"] = encryption_at_rest_provider
        if id is not None:
            self._values["id"] = id
        if labels is not None:
            self._values["labels"] = labels
        if mongo_db_major_version is not None:
            self._values["mongo_db_major_version"] = mongo_db_major_version
        if paused is not None:
            self._values["paused"] = paused
        if pit_enabled is not None:
            self._values["pit_enabled"] = pit_enabled
        if retain_backups_enabled is not None:
            self._values["retain_backups_enabled"] = retain_backups_enabled
        if root_cert_type is not None:
            self._values["root_cert_type"] = root_cert_type
        if termination_protection_enabled is not None:
            self._values["termination_protection_enabled"] = termination_protection_enabled
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if version_release_system is not None:
            self._values["version_release_system"] = version_release_system

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
    def cluster_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#cluster_type AdvancedCluster#cluster_type}.'''
        result = self._values.get("cluster_type")
        assert result is not None, "Required property 'cluster_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#name AdvancedCluster#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#project_id AdvancedCluster#project_id}.'''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def replication_specs(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AdvancedClusterReplicationSpecs"]]:
        '''replication_specs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#replication_specs AdvancedCluster#replication_specs}
        '''
        result = self._values.get("replication_specs")
        assert result is not None, "Required property 'replication_specs' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AdvancedClusterReplicationSpecs"]], result)

    @builtins.property
    def advanced_configuration(
        self,
    ) -> typing.Optional[AdvancedClusterAdvancedConfiguration]:
        '''advanced_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#advanced_configuration AdvancedCluster#advanced_configuration}
        '''
        result = self._values.get("advanced_configuration")
        return typing.cast(typing.Optional[AdvancedClusterAdvancedConfiguration], result)

    @builtins.property
    def backup_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#backup_enabled AdvancedCluster#backup_enabled}.'''
        result = self._values.get("backup_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def bi_connector(self) -> typing.Optional[AdvancedClusterBiConnector]:
        '''bi_connector block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#bi_connector AdvancedCluster#bi_connector}
        '''
        result = self._values.get("bi_connector")
        return typing.cast(typing.Optional[AdvancedClusterBiConnector], result)

    @builtins.property
    def bi_connector_config(self) -> typing.Optional[AdvancedClusterBiConnectorConfig]:
        '''bi_connector_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#bi_connector_config AdvancedCluster#bi_connector_config}
        '''
        result = self._values.get("bi_connector_config")
        return typing.cast(typing.Optional[AdvancedClusterBiConnectorConfig], result)

    @builtins.property
    def disk_size_gb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#disk_size_gb AdvancedCluster#disk_size_gb}.'''
        result = self._values.get("disk_size_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def encryption_at_rest_provider(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#encryption_at_rest_provider AdvancedCluster#encryption_at_rest_provider}.'''
        result = self._values.get("encryption_at_rest_provider")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#id AdvancedCluster#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def labels(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AdvancedClusterLabels"]]]:
        '''labels block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#labels AdvancedCluster#labels}
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AdvancedClusterLabels"]]], result)

    @builtins.property
    def mongo_db_major_version(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#mongo_db_major_version AdvancedCluster#mongo_db_major_version}.'''
        result = self._values.get("mongo_db_major_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def paused(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#paused AdvancedCluster#paused}.'''
        result = self._values.get("paused")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def pit_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#pit_enabled AdvancedCluster#pit_enabled}.'''
        result = self._values.get("pit_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def retain_backups_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Flag that indicates whether to retain backup snapshots for the deleted dedicated cluster.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#retain_backups_enabled AdvancedCluster#retain_backups_enabled}
        '''
        result = self._values.get("retain_backups_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def root_cert_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#root_cert_type AdvancedCluster#root_cert_type}.'''
        result = self._values.get("root_cert_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def termination_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#termination_protection_enabled AdvancedCluster#termination_protection_enabled}.'''
        result = self._values.get("termination_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["AdvancedClusterTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#timeouts AdvancedCluster#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["AdvancedClusterTimeouts"], result)

    @builtins.property
    def version_release_system(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#version_release_system AdvancedCluster#version_release_system}.'''
        result = self._values.get("version_release_system")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdvancedClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterConnectionStrings",
    jsii_struct_bases=[],
    name_mapping={},
)
class AdvancedClusterConnectionStrings:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdvancedClusterConnectionStrings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AdvancedClusterConnectionStringsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterConnectionStringsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__441e6926327622b405eea34ff99aac9e39a54e90d4648b11cae462c092eb83d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AdvancedClusterConnectionStringsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c9ccc1e5691636f8f558c88ada542962192f5bea9a0089e5ef93707837eaf3d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AdvancedClusterConnectionStringsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5e6cd82f6bb97796d8b1ca5b23df4994d99382b8b0b093ef374316ace543295)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1d77284f4b144ba7629d9143c5ac3dd8dc8dee07cd55fbe0d4c8832ac207559)
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
            type_hints = typing.get_type_hints(_typecheckingstub__decdd79a87080e6c962f848f0c401bc1d6bd33c24f0fbf74b034f37f02b2b6c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class AdvancedClusterConnectionStringsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterConnectionStringsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__54f1fad330fc00229d19cc71fad1a83eeb70096ca62900e83cbc535b20a4304d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="awsPrivateLink")
    def aws_private_link(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "awsPrivateLink"))

    @builtins.property
    @jsii.member(jsii_name="awsPrivateLinkSrv")
    def aws_private_link_srv(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "awsPrivateLinkSrv"))

    @builtins.property
    @jsii.member(jsii_name="private")
    def private(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "private"))

    @builtins.property
    @jsii.member(jsii_name="privateEndpoint")
    def private_endpoint(self) -> "AdvancedClusterConnectionStringsPrivateEndpointList":
        return typing.cast("AdvancedClusterConnectionStringsPrivateEndpointList", jsii.get(self, "privateEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="privateSrv")
    def private_srv(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateSrv"))

    @builtins.property
    @jsii.member(jsii_name="standard")
    def standard(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "standard"))

    @builtins.property
    @jsii.member(jsii_name="standardSrv")
    def standard_srv(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "standardSrv"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AdvancedClusterConnectionStrings]:
        return typing.cast(typing.Optional[AdvancedClusterConnectionStrings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AdvancedClusterConnectionStrings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c44de2fe56fb3710900cb775195498eb1b83315955399d5c8c36f435b8e1d7b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterConnectionStringsPrivateEndpoint",
    jsii_struct_bases=[],
    name_mapping={},
)
class AdvancedClusterConnectionStringsPrivateEndpoint:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdvancedClusterConnectionStringsPrivateEndpoint(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterConnectionStringsPrivateEndpointEndpoints",
    jsii_struct_bases=[],
    name_mapping={},
)
class AdvancedClusterConnectionStringsPrivateEndpointEndpoints:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdvancedClusterConnectionStringsPrivateEndpointEndpoints(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AdvancedClusterConnectionStringsPrivateEndpointEndpointsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterConnectionStringsPrivateEndpointEndpointsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b7d8d8e125f511bd3b5200aab60804105dbd07580c502d53c8ca0cfef58f068)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AdvancedClusterConnectionStringsPrivateEndpointEndpointsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01ab42e3af384730962cf6009e614759ed863504b621bbb89623a9bab6e3707b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AdvancedClusterConnectionStringsPrivateEndpointEndpointsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c165827c1d030c7c306ddfff3b103f928633acaa73e2c481cab4b94e123551d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5451b4f1d704bc71cae244109009c3271983f07a605d52dec7119bb1794978d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__034fe5d10e4a8012ca85456ac94ead1cb67676e27f25bee15c271c86edc7ca3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class AdvancedClusterConnectionStringsPrivateEndpointEndpointsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterConnectionStringsPrivateEndpointEndpointsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a4154a4664a41b9a262d7e2e17449755aa4d1ba17d56a769fea5738aa492fc1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="endpointId")
    def endpoint_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointId"))

    @builtins.property
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerName"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AdvancedClusterConnectionStringsPrivateEndpointEndpoints]:
        return typing.cast(typing.Optional[AdvancedClusterConnectionStringsPrivateEndpointEndpoints], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AdvancedClusterConnectionStringsPrivateEndpointEndpoints],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14612d1af0dcfeab45ffd2113f5cadbc8d87ec37e4cb9d732dcc54b7f8df7382)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AdvancedClusterConnectionStringsPrivateEndpointList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterConnectionStringsPrivateEndpointList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcf8f3aed5a2ed0dec16991e015d361e6c9fe7793ff9b7303d070dc11406b5fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AdvancedClusterConnectionStringsPrivateEndpointOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1124f3f9d4691b977265847607da40ad1c9566689b2cd138c0b682600cc63450)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AdvancedClusterConnectionStringsPrivateEndpointOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d381cfcb7043c9221df5fe5e8007884ff95aa181d6e94ab965ea2bc405ef3ae0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79f756d8b8f7a5f37ed5d0c5a208d00d923643bb97238512b45568ab2959b250)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2835b675ce1e87fb6b38864ca75591a1cebe8c613149eedcc91f5e2bb172e0ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class AdvancedClusterConnectionStringsPrivateEndpointOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterConnectionStringsPrivateEndpointOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b07d524d51554b47b32aad1ac325df2e1ebe63304e260992ee7b2afab56c09d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="connectionString")
    def connection_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionString"))

    @builtins.property
    @jsii.member(jsii_name="endpoints")
    def endpoints(self) -> AdvancedClusterConnectionStringsPrivateEndpointEndpointsList:
        return typing.cast(AdvancedClusterConnectionStringsPrivateEndpointEndpointsList, jsii.get(self, "endpoints"))

    @builtins.property
    @jsii.member(jsii_name="srvConnectionString")
    def srv_connection_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "srvConnectionString"))

    @builtins.property
    @jsii.member(jsii_name="srvShardOptimizedConnectionString")
    def srv_shard_optimized_connection_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "srvShardOptimizedConnectionString"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AdvancedClusterConnectionStringsPrivateEndpoint]:
        return typing.cast(typing.Optional[AdvancedClusterConnectionStringsPrivateEndpoint], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AdvancedClusterConnectionStringsPrivateEndpoint],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73734012490414811d8d51b1f354aeb854351f022cbc0d2762e595873ed2a2c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterLabels",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class AdvancedClusterLabels:
    def __init__(
        self,
        *,
        key: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#key AdvancedCluster#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#value AdvancedCluster#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3ccbe321c0568cc90cfe481a65f7f9964ccd6f0184448ca35a6e484c52cce20)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if key is not None:
            self._values["key"] = key
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#key AdvancedCluster#key}.'''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#value AdvancedCluster#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdvancedClusterLabels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AdvancedClusterLabelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterLabelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3bf8dc858e84dd2fc203c5d9368565f1f7c34b356f67f0ce3ff6e4f92542cfe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AdvancedClusterLabelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14c98b4688cb2f9586569693244f9ca52ba8fdc49fe8da2405db5eed1d30c184)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AdvancedClusterLabelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd13169ed65041b63ae02df1a6a97baef196b92bf03d0ed21c86bd69797b998a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df49d7ad99124522d89ba62074f8ff00380d23486651f4d59e83f8a60aa4a4de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__98502041bcb95aa0aaef01c96deb9e34eaa0a9ed0a6c6a9302b308b71c143d2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AdvancedClusterLabels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AdvancedClusterLabels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AdvancedClusterLabels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2143ce7db45869716ed6df3fe5317fc95783cd5b43e4a94efd06ab3270d9e7f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AdvancedClusterLabelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterLabelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c16b041f2b6715d394c3c637547924c202b89cd77eaae315c679d41c7bd708a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetKey")
    def reset_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKey", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aab59bc233589b61d55464d9ed8b2f6bfdb7467266802249e9e8b26a8ae5c7f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36150de8473982913142a1f22852a39b03dac55e80506626587938315ad49362)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AdvancedClusterLabels]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AdvancedClusterLabels]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AdvancedClusterLabels]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__997eb9d23afa104cbe41e004db15fe41afc7bd746dd484abefe0200ef2da968f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterReplicationSpecs",
    jsii_struct_bases=[],
    name_mapping={
        "region_configs": "regionConfigs",
        "num_shards": "numShards",
        "zone_name": "zoneName",
    },
)
class AdvancedClusterReplicationSpecs:
    def __init__(
        self,
        *,
        region_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AdvancedClusterReplicationSpecsRegionConfigs", typing.Dict[builtins.str, typing.Any]]]],
        num_shards: typing.Optional[jsii.Number] = None,
        zone_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param region_configs: region_configs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#region_configs AdvancedCluster#region_configs}
        :param num_shards: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#num_shards AdvancedCluster#num_shards}.
        :param zone_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#zone_name AdvancedCluster#zone_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2d180acb0d93a5929b7a49a95b70b19ad6d2475380444c34817bb223d300400)
            check_type(argname="argument region_configs", value=region_configs, expected_type=type_hints["region_configs"])
            check_type(argname="argument num_shards", value=num_shards, expected_type=type_hints["num_shards"])
            check_type(argname="argument zone_name", value=zone_name, expected_type=type_hints["zone_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "region_configs": region_configs,
        }
        if num_shards is not None:
            self._values["num_shards"] = num_shards
        if zone_name is not None:
            self._values["zone_name"] = zone_name

    @builtins.property
    def region_configs(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AdvancedClusterReplicationSpecsRegionConfigs"]]:
        '''region_configs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#region_configs AdvancedCluster#region_configs}
        '''
        result = self._values.get("region_configs")
        assert result is not None, "Required property 'region_configs' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AdvancedClusterReplicationSpecsRegionConfigs"]], result)

    @builtins.property
    def num_shards(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#num_shards AdvancedCluster#num_shards}.'''
        result = self._values.get("num_shards")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def zone_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#zone_name AdvancedCluster#zone_name}.'''
        result = self._values.get("zone_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdvancedClusterReplicationSpecs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AdvancedClusterReplicationSpecsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterReplicationSpecsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73ffce17b0b155003028c31dafe0afa96211e3e0fec4237aeab27fed28dbb6d9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AdvancedClusterReplicationSpecsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51a0172233442ed7ae307fde176c482424259ac42d1c7b6fa51058d4e3c55011)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AdvancedClusterReplicationSpecsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b02eb90791bc66d46831b8a07a40c3cc765f87ed59b7fc03231a2d5c8c6abf7e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fc60e26f503809fe442d057bbb89bb553a5ec8f3c25df1be2b6d6548d7e7c0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c108a9ce6889fbecccab6b11c59c5cf4dc049bd142bcae66cbfd4d07342ff3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AdvancedClusterReplicationSpecs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AdvancedClusterReplicationSpecs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AdvancedClusterReplicationSpecs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00934695c03893e843e577c5abffdfabca7a96b1e9db8826c337eb764f16a7fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AdvancedClusterReplicationSpecsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterReplicationSpecsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__386584b0e17f3e007c092a4d067612039313c608c274c06028a6456c7a03e630)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRegionConfigs")
    def put_region_configs(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AdvancedClusterReplicationSpecsRegionConfigs", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b7a8acba93d2dae8d26620ee50ddb62894c3e914dc259b949daaf661528b6ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRegionConfigs", [value]))

    @jsii.member(jsii_name="resetNumShards")
    def reset_num_shards(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNumShards", []))

    @jsii.member(jsii_name="resetZoneName")
    def reset_zone_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZoneName", []))

    @builtins.property
    @jsii.member(jsii_name="containerId")
    def container_id(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "containerId"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="regionConfigs")
    def region_configs(self) -> "AdvancedClusterReplicationSpecsRegionConfigsList":
        return typing.cast("AdvancedClusterReplicationSpecsRegionConfigsList", jsii.get(self, "regionConfigs"))

    @builtins.property
    @jsii.member(jsii_name="numShardsInput")
    def num_shards_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numShardsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionConfigsInput")
    def region_configs_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AdvancedClusterReplicationSpecsRegionConfigs"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AdvancedClusterReplicationSpecsRegionConfigs"]]], jsii.get(self, "regionConfigsInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneNameInput")
    def zone_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zoneNameInput"))

    @builtins.property
    @jsii.member(jsii_name="numShards")
    def num_shards(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "numShards"))

    @num_shards.setter
    def num_shards(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a43b0be6cae2badd91b3d29b069ea02f3e59ae9e264fc9589e70b8f0f6d11db9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "numShards", value)

    @builtins.property
    @jsii.member(jsii_name="zoneName")
    def zone_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zoneName"))

    @zone_name.setter
    def zone_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb66a21263dafadfbdaf4b3ee1d445ef83cae0475ab47abb03bb78e9ff3dd221)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AdvancedClusterReplicationSpecs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AdvancedClusterReplicationSpecs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AdvancedClusterReplicationSpecs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d2a9cb3bc5fac581d0aac396900b60306828af063861dcfccc31e34c72d39f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterReplicationSpecsRegionConfigs",
    jsii_struct_bases=[],
    name_mapping={
        "priority": "priority",
        "provider_name": "providerName",
        "region_name": "regionName",
        "analytics_auto_scaling": "analyticsAutoScaling",
        "analytics_specs": "analyticsSpecs",
        "auto_scaling": "autoScaling",
        "backing_provider_name": "backingProviderName",
        "electable_specs": "electableSpecs",
        "read_only_specs": "readOnlySpecs",
    },
)
class AdvancedClusterReplicationSpecsRegionConfigs:
    def __init__(
        self,
        *,
        priority: jsii.Number,
        provider_name: builtins.str,
        region_name: builtins.str,
        analytics_auto_scaling: typing.Optional[typing.Union["AdvancedClusterReplicationSpecsRegionConfigsAnalyticsAutoScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        analytics_specs: typing.Optional[typing.Union["AdvancedClusterReplicationSpecsRegionConfigsAnalyticsSpecs", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_scaling: typing.Optional[typing.Union["AdvancedClusterReplicationSpecsRegionConfigsAutoScaling", typing.Dict[builtins.str, typing.Any]]] = None,
        backing_provider_name: typing.Optional[builtins.str] = None,
        electable_specs: typing.Optional[typing.Union["AdvancedClusterReplicationSpecsRegionConfigsElectableSpecs", typing.Dict[builtins.str, typing.Any]]] = None,
        read_only_specs: typing.Optional[typing.Union["AdvancedClusterReplicationSpecsRegionConfigsReadOnlySpecs", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#priority AdvancedCluster#priority}.
        :param provider_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#provider_name AdvancedCluster#provider_name}.
        :param region_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#region_name AdvancedCluster#region_name}.
        :param analytics_auto_scaling: analytics_auto_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#analytics_auto_scaling AdvancedCluster#analytics_auto_scaling}
        :param analytics_specs: analytics_specs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#analytics_specs AdvancedCluster#analytics_specs}
        :param auto_scaling: auto_scaling block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#auto_scaling AdvancedCluster#auto_scaling}
        :param backing_provider_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#backing_provider_name AdvancedCluster#backing_provider_name}.
        :param electable_specs: electable_specs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#electable_specs AdvancedCluster#electable_specs}
        :param read_only_specs: read_only_specs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#read_only_specs AdvancedCluster#read_only_specs}
        '''
        if isinstance(analytics_auto_scaling, dict):
            analytics_auto_scaling = AdvancedClusterReplicationSpecsRegionConfigsAnalyticsAutoScaling(**analytics_auto_scaling)
        if isinstance(analytics_specs, dict):
            analytics_specs = AdvancedClusterReplicationSpecsRegionConfigsAnalyticsSpecs(**analytics_specs)
        if isinstance(auto_scaling, dict):
            auto_scaling = AdvancedClusterReplicationSpecsRegionConfigsAutoScaling(**auto_scaling)
        if isinstance(electable_specs, dict):
            electable_specs = AdvancedClusterReplicationSpecsRegionConfigsElectableSpecs(**electable_specs)
        if isinstance(read_only_specs, dict):
            read_only_specs = AdvancedClusterReplicationSpecsRegionConfigsReadOnlySpecs(**read_only_specs)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f89b39e6209455119c0ff4d709ed7625af830dd9f115cc59c05422b5707f613)
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument provider_name", value=provider_name, expected_type=type_hints["provider_name"])
            check_type(argname="argument region_name", value=region_name, expected_type=type_hints["region_name"])
            check_type(argname="argument analytics_auto_scaling", value=analytics_auto_scaling, expected_type=type_hints["analytics_auto_scaling"])
            check_type(argname="argument analytics_specs", value=analytics_specs, expected_type=type_hints["analytics_specs"])
            check_type(argname="argument auto_scaling", value=auto_scaling, expected_type=type_hints["auto_scaling"])
            check_type(argname="argument backing_provider_name", value=backing_provider_name, expected_type=type_hints["backing_provider_name"])
            check_type(argname="argument electable_specs", value=electable_specs, expected_type=type_hints["electable_specs"])
            check_type(argname="argument read_only_specs", value=read_only_specs, expected_type=type_hints["read_only_specs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "priority": priority,
            "provider_name": provider_name,
            "region_name": region_name,
        }
        if analytics_auto_scaling is not None:
            self._values["analytics_auto_scaling"] = analytics_auto_scaling
        if analytics_specs is not None:
            self._values["analytics_specs"] = analytics_specs
        if auto_scaling is not None:
            self._values["auto_scaling"] = auto_scaling
        if backing_provider_name is not None:
            self._values["backing_provider_name"] = backing_provider_name
        if electable_specs is not None:
            self._values["electable_specs"] = electable_specs
        if read_only_specs is not None:
            self._values["read_only_specs"] = read_only_specs

    @builtins.property
    def priority(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#priority AdvancedCluster#priority}.'''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def provider_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#provider_name AdvancedCluster#provider_name}.'''
        result = self._values.get("provider_name")
        assert result is not None, "Required property 'provider_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#region_name AdvancedCluster#region_name}.'''
        result = self._values.get("region_name")
        assert result is not None, "Required property 'region_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def analytics_auto_scaling(
        self,
    ) -> typing.Optional["AdvancedClusterReplicationSpecsRegionConfigsAnalyticsAutoScaling"]:
        '''analytics_auto_scaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#analytics_auto_scaling AdvancedCluster#analytics_auto_scaling}
        '''
        result = self._values.get("analytics_auto_scaling")
        return typing.cast(typing.Optional["AdvancedClusterReplicationSpecsRegionConfigsAnalyticsAutoScaling"], result)

    @builtins.property
    def analytics_specs(
        self,
    ) -> typing.Optional["AdvancedClusterReplicationSpecsRegionConfigsAnalyticsSpecs"]:
        '''analytics_specs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#analytics_specs AdvancedCluster#analytics_specs}
        '''
        result = self._values.get("analytics_specs")
        return typing.cast(typing.Optional["AdvancedClusterReplicationSpecsRegionConfigsAnalyticsSpecs"], result)

    @builtins.property
    def auto_scaling(
        self,
    ) -> typing.Optional["AdvancedClusterReplicationSpecsRegionConfigsAutoScaling"]:
        '''auto_scaling block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#auto_scaling AdvancedCluster#auto_scaling}
        '''
        result = self._values.get("auto_scaling")
        return typing.cast(typing.Optional["AdvancedClusterReplicationSpecsRegionConfigsAutoScaling"], result)

    @builtins.property
    def backing_provider_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#backing_provider_name AdvancedCluster#backing_provider_name}.'''
        result = self._values.get("backing_provider_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def electable_specs(
        self,
    ) -> typing.Optional["AdvancedClusterReplicationSpecsRegionConfigsElectableSpecs"]:
        '''electable_specs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#electable_specs AdvancedCluster#electable_specs}
        '''
        result = self._values.get("electable_specs")
        return typing.cast(typing.Optional["AdvancedClusterReplicationSpecsRegionConfigsElectableSpecs"], result)

    @builtins.property
    def read_only_specs(
        self,
    ) -> typing.Optional["AdvancedClusterReplicationSpecsRegionConfigsReadOnlySpecs"]:
        '''read_only_specs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#read_only_specs AdvancedCluster#read_only_specs}
        '''
        result = self._values.get("read_only_specs")
        return typing.cast(typing.Optional["AdvancedClusterReplicationSpecsRegionConfigsReadOnlySpecs"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdvancedClusterReplicationSpecsRegionConfigs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterReplicationSpecsRegionConfigsAnalyticsAutoScaling",
    jsii_struct_bases=[],
    name_mapping={
        "compute_enabled": "computeEnabled",
        "compute_max_instance_size": "computeMaxInstanceSize",
        "compute_min_instance_size": "computeMinInstanceSize",
        "compute_scale_down_enabled": "computeScaleDownEnabled",
        "disk_gb_enabled": "diskGbEnabled",
    },
)
class AdvancedClusterReplicationSpecsRegionConfigsAnalyticsAutoScaling:
    def __init__(
        self,
        *,
        compute_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        compute_max_instance_size: typing.Optional[builtins.str] = None,
        compute_min_instance_size: typing.Optional[builtins.str] = None,
        compute_scale_down_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disk_gb_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param compute_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#compute_enabled AdvancedCluster#compute_enabled}.
        :param compute_max_instance_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#compute_max_instance_size AdvancedCluster#compute_max_instance_size}.
        :param compute_min_instance_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#compute_min_instance_size AdvancedCluster#compute_min_instance_size}.
        :param compute_scale_down_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#compute_scale_down_enabled AdvancedCluster#compute_scale_down_enabled}.
        :param disk_gb_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#disk_gb_enabled AdvancedCluster#disk_gb_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8fa91b983bdaa15543467e3f7b99a9ec2f155950d0b2739930a080ee4543bd8)
            check_type(argname="argument compute_enabled", value=compute_enabled, expected_type=type_hints["compute_enabled"])
            check_type(argname="argument compute_max_instance_size", value=compute_max_instance_size, expected_type=type_hints["compute_max_instance_size"])
            check_type(argname="argument compute_min_instance_size", value=compute_min_instance_size, expected_type=type_hints["compute_min_instance_size"])
            check_type(argname="argument compute_scale_down_enabled", value=compute_scale_down_enabled, expected_type=type_hints["compute_scale_down_enabled"])
            check_type(argname="argument disk_gb_enabled", value=disk_gb_enabled, expected_type=type_hints["disk_gb_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compute_enabled is not None:
            self._values["compute_enabled"] = compute_enabled
        if compute_max_instance_size is not None:
            self._values["compute_max_instance_size"] = compute_max_instance_size
        if compute_min_instance_size is not None:
            self._values["compute_min_instance_size"] = compute_min_instance_size
        if compute_scale_down_enabled is not None:
            self._values["compute_scale_down_enabled"] = compute_scale_down_enabled
        if disk_gb_enabled is not None:
            self._values["disk_gb_enabled"] = disk_gb_enabled

    @builtins.property
    def compute_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#compute_enabled AdvancedCluster#compute_enabled}.'''
        result = self._values.get("compute_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def compute_max_instance_size(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#compute_max_instance_size AdvancedCluster#compute_max_instance_size}.'''
        result = self._values.get("compute_max_instance_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compute_min_instance_size(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#compute_min_instance_size AdvancedCluster#compute_min_instance_size}.'''
        result = self._values.get("compute_min_instance_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compute_scale_down_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#compute_scale_down_enabled AdvancedCluster#compute_scale_down_enabled}.'''
        result = self._values.get("compute_scale_down_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disk_gb_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#disk_gb_enabled AdvancedCluster#disk_gb_enabled}.'''
        result = self._values.get("disk_gb_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdvancedClusterReplicationSpecsRegionConfigsAnalyticsAutoScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AdvancedClusterReplicationSpecsRegionConfigsAnalyticsAutoScalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterReplicationSpecsRegionConfigsAnalyticsAutoScalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39b1aa2c8e90fbb6a63ee7a53ae67783515e62d11de809dd8b41a94608a63966)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetComputeEnabled")
    def reset_compute_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputeEnabled", []))

    @jsii.member(jsii_name="resetComputeMaxInstanceSize")
    def reset_compute_max_instance_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputeMaxInstanceSize", []))

    @jsii.member(jsii_name="resetComputeMinInstanceSize")
    def reset_compute_min_instance_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputeMinInstanceSize", []))

    @jsii.member(jsii_name="resetComputeScaleDownEnabled")
    def reset_compute_scale_down_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputeScaleDownEnabled", []))

    @jsii.member(jsii_name="resetDiskGbEnabled")
    def reset_disk_gb_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskGbEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="computeEnabledInput")
    def compute_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "computeEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="computeMaxInstanceSizeInput")
    def compute_max_instance_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computeMaxInstanceSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="computeMinInstanceSizeInput")
    def compute_min_instance_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computeMinInstanceSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="computeScaleDownEnabledInput")
    def compute_scale_down_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "computeScaleDownEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="diskGbEnabledInput")
    def disk_gb_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "diskGbEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="computeEnabled")
    def compute_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "computeEnabled"))

    @compute_enabled.setter
    def compute_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a778bca85a83662fbc97ecf4cfbba880e2d5ab642fc44b93670bf7fc8e4ba5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="computeMaxInstanceSize")
    def compute_max_instance_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "computeMaxInstanceSize"))

    @compute_max_instance_size.setter
    def compute_max_instance_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaaa772d439d24961669f64c4fb0a818d73cf6a5ae3587ad3e1bf3f6e6e83546)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeMaxInstanceSize", value)

    @builtins.property
    @jsii.member(jsii_name="computeMinInstanceSize")
    def compute_min_instance_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "computeMinInstanceSize"))

    @compute_min_instance_size.setter
    def compute_min_instance_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1563320de123ff2637a23dc8755bae1273f34bfbd415f10274b325481780e878)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeMinInstanceSize", value)

    @builtins.property
    @jsii.member(jsii_name="computeScaleDownEnabled")
    def compute_scale_down_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "computeScaleDownEnabled"))

    @compute_scale_down_enabled.setter
    def compute_scale_down_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e2661fa351dbe12333c774555a1b260fcd805c8e2ce1f2bd331951a5569a5de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeScaleDownEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="diskGbEnabled")
    def disk_gb_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "diskGbEnabled"))

    @disk_gb_enabled.setter
    def disk_gb_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27bad33602d73cbe77aad4affc529996f948f8866e5697b823c4b5b4f4b1f04c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskGbEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsAnalyticsAutoScaling]:
        return typing.cast(typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsAnalyticsAutoScaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsAnalyticsAutoScaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85e6aacb2bb1ce976dcf2820709074312287889c1c5e45a85cf8527cce89d1bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterReplicationSpecsRegionConfigsAnalyticsSpecs",
    jsii_struct_bases=[],
    name_mapping={
        "instance_size": "instanceSize",
        "disk_iops": "diskIops",
        "ebs_volume_type": "ebsVolumeType",
        "node_count": "nodeCount",
    },
)
class AdvancedClusterReplicationSpecsRegionConfigsAnalyticsSpecs:
    def __init__(
        self,
        *,
        instance_size: builtins.str,
        disk_iops: typing.Optional[jsii.Number] = None,
        ebs_volume_type: typing.Optional[builtins.str] = None,
        node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param instance_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#instance_size AdvancedCluster#instance_size}.
        :param disk_iops: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#disk_iops AdvancedCluster#disk_iops}.
        :param ebs_volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#ebs_volume_type AdvancedCluster#ebs_volume_type}.
        :param node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#node_count AdvancedCluster#node_count}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f10cc668c743624c66680fb1e290c2db3fb4cf78c7e4815f4c3335590bf3941)
            check_type(argname="argument instance_size", value=instance_size, expected_type=type_hints["instance_size"])
            check_type(argname="argument disk_iops", value=disk_iops, expected_type=type_hints["disk_iops"])
            check_type(argname="argument ebs_volume_type", value=ebs_volume_type, expected_type=type_hints["ebs_volume_type"])
            check_type(argname="argument node_count", value=node_count, expected_type=type_hints["node_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_size": instance_size,
        }
        if disk_iops is not None:
            self._values["disk_iops"] = disk_iops
        if ebs_volume_type is not None:
            self._values["ebs_volume_type"] = ebs_volume_type
        if node_count is not None:
            self._values["node_count"] = node_count

    @builtins.property
    def instance_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#instance_size AdvancedCluster#instance_size}.'''
        result = self._values.get("instance_size")
        assert result is not None, "Required property 'instance_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disk_iops(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#disk_iops AdvancedCluster#disk_iops}.'''
        result = self._values.get("disk_iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ebs_volume_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#ebs_volume_type AdvancedCluster#ebs_volume_type}.'''
        result = self._values.get("ebs_volume_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#node_count AdvancedCluster#node_count}.'''
        result = self._values.get("node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdvancedClusterReplicationSpecsRegionConfigsAnalyticsSpecs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AdvancedClusterReplicationSpecsRegionConfigsAnalyticsSpecsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterReplicationSpecsRegionConfigsAnalyticsSpecsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d53ee5fa3f483080b6904e6aaf09b61ca458979a4e0deac980190fdbed708fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDiskIops")
    def reset_disk_iops(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskIops", []))

    @jsii.member(jsii_name="resetEbsVolumeType")
    def reset_ebs_volume_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEbsVolumeType", []))

    @jsii.member(jsii_name="resetNodeCount")
    def reset_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeCount", []))

    @builtins.property
    @jsii.member(jsii_name="diskIopsInput")
    def disk_iops_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskIopsInput"))

    @builtins.property
    @jsii.member(jsii_name="ebsVolumeTypeInput")
    def ebs_volume_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ebsVolumeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceSizeInput")
    def instance_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeCountInput")
    def node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="diskIops")
    def disk_iops(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskIops"))

    @disk_iops.setter
    def disk_iops(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe7428ed944875ade07fb0ca99102a395e4afd2a8263bd4925430e2e2a6c02f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskIops", value)

    @builtins.property
    @jsii.member(jsii_name="ebsVolumeType")
    def ebs_volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ebsVolumeType"))

    @ebs_volume_type.setter
    def ebs_volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d5a68c71041ba21574c61e3eb019cdd973f713565d92cf784bdef7885de1a4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ebsVolumeType", value)

    @builtins.property
    @jsii.member(jsii_name="instanceSize")
    def instance_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceSize"))

    @instance_size.setter
    def instance_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0666d188175162ef8cdd79ce9e1367c2ce7fc17973d69a38c15a9d0fd8dd31c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceSize", value)

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @node_count.setter
    def node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9dd3152f1ff1c493be34e7b5b6f559787b0fae8319a46b39c5965c9fdf373f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCount", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsAnalyticsSpecs]:
        return typing.cast(typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsAnalyticsSpecs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsAnalyticsSpecs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35970a2c568f7ec62497d2ac596fee0e1e23344eb3ad475b6b536741028934c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterReplicationSpecsRegionConfigsAutoScaling",
    jsii_struct_bases=[],
    name_mapping={
        "compute_enabled": "computeEnabled",
        "compute_max_instance_size": "computeMaxInstanceSize",
        "compute_min_instance_size": "computeMinInstanceSize",
        "compute_scale_down_enabled": "computeScaleDownEnabled",
        "disk_gb_enabled": "diskGbEnabled",
    },
)
class AdvancedClusterReplicationSpecsRegionConfigsAutoScaling:
    def __init__(
        self,
        *,
        compute_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        compute_max_instance_size: typing.Optional[builtins.str] = None,
        compute_min_instance_size: typing.Optional[builtins.str] = None,
        compute_scale_down_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disk_gb_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param compute_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#compute_enabled AdvancedCluster#compute_enabled}.
        :param compute_max_instance_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#compute_max_instance_size AdvancedCluster#compute_max_instance_size}.
        :param compute_min_instance_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#compute_min_instance_size AdvancedCluster#compute_min_instance_size}.
        :param compute_scale_down_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#compute_scale_down_enabled AdvancedCluster#compute_scale_down_enabled}.
        :param disk_gb_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#disk_gb_enabled AdvancedCluster#disk_gb_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3db5dc6d3fe2339a164af5963ca30e956dd91e03838a3a074f70b75922e6a310)
            check_type(argname="argument compute_enabled", value=compute_enabled, expected_type=type_hints["compute_enabled"])
            check_type(argname="argument compute_max_instance_size", value=compute_max_instance_size, expected_type=type_hints["compute_max_instance_size"])
            check_type(argname="argument compute_min_instance_size", value=compute_min_instance_size, expected_type=type_hints["compute_min_instance_size"])
            check_type(argname="argument compute_scale_down_enabled", value=compute_scale_down_enabled, expected_type=type_hints["compute_scale_down_enabled"])
            check_type(argname="argument disk_gb_enabled", value=disk_gb_enabled, expected_type=type_hints["disk_gb_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compute_enabled is not None:
            self._values["compute_enabled"] = compute_enabled
        if compute_max_instance_size is not None:
            self._values["compute_max_instance_size"] = compute_max_instance_size
        if compute_min_instance_size is not None:
            self._values["compute_min_instance_size"] = compute_min_instance_size
        if compute_scale_down_enabled is not None:
            self._values["compute_scale_down_enabled"] = compute_scale_down_enabled
        if disk_gb_enabled is not None:
            self._values["disk_gb_enabled"] = disk_gb_enabled

    @builtins.property
    def compute_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#compute_enabled AdvancedCluster#compute_enabled}.'''
        result = self._values.get("compute_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def compute_max_instance_size(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#compute_max_instance_size AdvancedCluster#compute_max_instance_size}.'''
        result = self._values.get("compute_max_instance_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compute_min_instance_size(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#compute_min_instance_size AdvancedCluster#compute_min_instance_size}.'''
        result = self._values.get("compute_min_instance_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compute_scale_down_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#compute_scale_down_enabled AdvancedCluster#compute_scale_down_enabled}.'''
        result = self._values.get("compute_scale_down_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def disk_gb_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#disk_gb_enabled AdvancedCluster#disk_gb_enabled}.'''
        result = self._values.get("disk_gb_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdvancedClusterReplicationSpecsRegionConfigsAutoScaling(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AdvancedClusterReplicationSpecsRegionConfigsAutoScalingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterReplicationSpecsRegionConfigsAutoScalingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bc61e4bfa347ac6253e832a0355d46077e11f66f9c5acb8b021396529c40461)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetComputeEnabled")
    def reset_compute_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputeEnabled", []))

    @jsii.member(jsii_name="resetComputeMaxInstanceSize")
    def reset_compute_max_instance_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputeMaxInstanceSize", []))

    @jsii.member(jsii_name="resetComputeMinInstanceSize")
    def reset_compute_min_instance_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputeMinInstanceSize", []))

    @jsii.member(jsii_name="resetComputeScaleDownEnabled")
    def reset_compute_scale_down_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComputeScaleDownEnabled", []))

    @jsii.member(jsii_name="resetDiskGbEnabled")
    def reset_disk_gb_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskGbEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="computeEnabledInput")
    def compute_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "computeEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="computeMaxInstanceSizeInput")
    def compute_max_instance_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computeMaxInstanceSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="computeMinInstanceSizeInput")
    def compute_min_instance_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computeMinInstanceSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="computeScaleDownEnabledInput")
    def compute_scale_down_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "computeScaleDownEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="diskGbEnabledInput")
    def disk_gb_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "diskGbEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="computeEnabled")
    def compute_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "computeEnabled"))

    @compute_enabled.setter
    def compute_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fa6c7de3b5d5a8071330c10d372b33987fa8617c05e7d8e28efd54949437102)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="computeMaxInstanceSize")
    def compute_max_instance_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "computeMaxInstanceSize"))

    @compute_max_instance_size.setter
    def compute_max_instance_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50a7d34700bd1e35948ff5b5167f1d3da3f26e90fc9a680066c5a5dc616c00e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeMaxInstanceSize", value)

    @builtins.property
    @jsii.member(jsii_name="computeMinInstanceSize")
    def compute_min_instance_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "computeMinInstanceSize"))

    @compute_min_instance_size.setter
    def compute_min_instance_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c016847e380fc6851ec2589c5fa5bd61a85b3e6b67e6f58e8931be5ce1fc26dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeMinInstanceSize", value)

    @builtins.property
    @jsii.member(jsii_name="computeScaleDownEnabled")
    def compute_scale_down_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "computeScaleDownEnabled"))

    @compute_scale_down_enabled.setter
    def compute_scale_down_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc1f664817df3280b1b18bb7a1e224ddca8280220b1777de3c807a736168dd3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeScaleDownEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="diskGbEnabled")
    def disk_gb_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "diskGbEnabled"))

    @disk_gb_enabled.setter
    def disk_gb_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6406c116c2001b944a3c85877e5e3be234a69f1c995ad503590e66848b4d6075)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskGbEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsAutoScaling]:
        return typing.cast(typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsAutoScaling], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsAutoScaling],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0318b8be9c0c9586daaedb0d9eb2c6cb5e0f58643698097f25292bc5ff818926)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterReplicationSpecsRegionConfigsElectableSpecs",
    jsii_struct_bases=[],
    name_mapping={
        "instance_size": "instanceSize",
        "disk_iops": "diskIops",
        "ebs_volume_type": "ebsVolumeType",
        "node_count": "nodeCount",
    },
)
class AdvancedClusterReplicationSpecsRegionConfigsElectableSpecs:
    def __init__(
        self,
        *,
        instance_size: builtins.str,
        disk_iops: typing.Optional[jsii.Number] = None,
        ebs_volume_type: typing.Optional[builtins.str] = None,
        node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param instance_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#instance_size AdvancedCluster#instance_size}.
        :param disk_iops: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#disk_iops AdvancedCluster#disk_iops}.
        :param ebs_volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#ebs_volume_type AdvancedCluster#ebs_volume_type}.
        :param node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#node_count AdvancedCluster#node_count}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__164f3e989882cd637971788cdd0d10ac6e593a9a015251fdf303438afff1a9d7)
            check_type(argname="argument instance_size", value=instance_size, expected_type=type_hints["instance_size"])
            check_type(argname="argument disk_iops", value=disk_iops, expected_type=type_hints["disk_iops"])
            check_type(argname="argument ebs_volume_type", value=ebs_volume_type, expected_type=type_hints["ebs_volume_type"])
            check_type(argname="argument node_count", value=node_count, expected_type=type_hints["node_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_size": instance_size,
        }
        if disk_iops is not None:
            self._values["disk_iops"] = disk_iops
        if ebs_volume_type is not None:
            self._values["ebs_volume_type"] = ebs_volume_type
        if node_count is not None:
            self._values["node_count"] = node_count

    @builtins.property
    def instance_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#instance_size AdvancedCluster#instance_size}.'''
        result = self._values.get("instance_size")
        assert result is not None, "Required property 'instance_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disk_iops(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#disk_iops AdvancedCluster#disk_iops}.'''
        result = self._values.get("disk_iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ebs_volume_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#ebs_volume_type AdvancedCluster#ebs_volume_type}.'''
        result = self._values.get("ebs_volume_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#node_count AdvancedCluster#node_count}.'''
        result = self._values.get("node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdvancedClusterReplicationSpecsRegionConfigsElectableSpecs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AdvancedClusterReplicationSpecsRegionConfigsElectableSpecsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterReplicationSpecsRegionConfigsElectableSpecsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1cad0e35a9b740cc41c340daf8a1bcb1f241fb99069b55cb871d75546111a85)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDiskIops")
    def reset_disk_iops(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskIops", []))

    @jsii.member(jsii_name="resetEbsVolumeType")
    def reset_ebs_volume_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEbsVolumeType", []))

    @jsii.member(jsii_name="resetNodeCount")
    def reset_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeCount", []))

    @builtins.property
    @jsii.member(jsii_name="diskIopsInput")
    def disk_iops_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskIopsInput"))

    @builtins.property
    @jsii.member(jsii_name="ebsVolumeTypeInput")
    def ebs_volume_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ebsVolumeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceSizeInput")
    def instance_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeCountInput")
    def node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="diskIops")
    def disk_iops(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskIops"))

    @disk_iops.setter
    def disk_iops(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dec61c8ff531826b9f8709812359d4bf9a81434ed0e6e992cd7133c233a2398b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskIops", value)

    @builtins.property
    @jsii.member(jsii_name="ebsVolumeType")
    def ebs_volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ebsVolumeType"))

    @ebs_volume_type.setter
    def ebs_volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa7423c783ad5054155fd19b4a86a4a071511ab2dbfe1a1b42eae53531bc1d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ebsVolumeType", value)

    @builtins.property
    @jsii.member(jsii_name="instanceSize")
    def instance_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceSize"))

    @instance_size.setter
    def instance_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7824cb99472b10a4518048605c53d0cbe28a2e2afc02156f48fdf07766411ad0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceSize", value)

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @node_count.setter
    def node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a7bd989b191841033d952a70d27ddbdf8d408738ceb58982767f315ff26c7ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCount", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsElectableSpecs]:
        return typing.cast(typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsElectableSpecs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsElectableSpecs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9007f7f86c25968ebbfdc88643ae50fa9b8e6d65826605da9adbcee745f4cbea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AdvancedClusterReplicationSpecsRegionConfigsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterReplicationSpecsRegionConfigsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1266a49ffa52e52965f301e2bc1aad2e4b64ae10d1587fefcc6eade0141eaa66)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AdvancedClusterReplicationSpecsRegionConfigsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e06bec31faef36629f18cf9c218de91ce2b58d77772fa90fce3e0c7592f59588)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AdvancedClusterReplicationSpecsRegionConfigsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af7674908b34616d24c1b11b6175d07a16282fff4452b22351814d348723ec27)
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
            type_hints = typing.get_type_hints(_typecheckingstub__493cfc0fb66de0eaaab80849f36098230291f1ede73d4927f7ccd539d001218f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cf4d1df87051ee469b14dd38c48709ad38f3210c4fa9a727466488c381ea68a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AdvancedClusterReplicationSpecsRegionConfigs]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AdvancedClusterReplicationSpecsRegionConfigs]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AdvancedClusterReplicationSpecsRegionConfigs]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a4172cdcfb7d961eff6c2d2f359d9ad008053d1e1e308e07ed4161abeecfb3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class AdvancedClusterReplicationSpecsRegionConfigsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterReplicationSpecsRegionConfigsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa72d912f6eee8599136cd1113d202d2fefe2230b1936c9d92d4fe1868fb4da3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAnalyticsAutoScaling")
    def put_analytics_auto_scaling(
        self,
        *,
        compute_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        compute_max_instance_size: typing.Optional[builtins.str] = None,
        compute_min_instance_size: typing.Optional[builtins.str] = None,
        compute_scale_down_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disk_gb_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param compute_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#compute_enabled AdvancedCluster#compute_enabled}.
        :param compute_max_instance_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#compute_max_instance_size AdvancedCluster#compute_max_instance_size}.
        :param compute_min_instance_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#compute_min_instance_size AdvancedCluster#compute_min_instance_size}.
        :param compute_scale_down_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#compute_scale_down_enabled AdvancedCluster#compute_scale_down_enabled}.
        :param disk_gb_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#disk_gb_enabled AdvancedCluster#disk_gb_enabled}.
        '''
        value = AdvancedClusterReplicationSpecsRegionConfigsAnalyticsAutoScaling(
            compute_enabled=compute_enabled,
            compute_max_instance_size=compute_max_instance_size,
            compute_min_instance_size=compute_min_instance_size,
            compute_scale_down_enabled=compute_scale_down_enabled,
            disk_gb_enabled=disk_gb_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putAnalyticsAutoScaling", [value]))

    @jsii.member(jsii_name="putAnalyticsSpecs")
    def put_analytics_specs(
        self,
        *,
        instance_size: builtins.str,
        disk_iops: typing.Optional[jsii.Number] = None,
        ebs_volume_type: typing.Optional[builtins.str] = None,
        node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param instance_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#instance_size AdvancedCluster#instance_size}.
        :param disk_iops: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#disk_iops AdvancedCluster#disk_iops}.
        :param ebs_volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#ebs_volume_type AdvancedCluster#ebs_volume_type}.
        :param node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#node_count AdvancedCluster#node_count}.
        '''
        value = AdvancedClusterReplicationSpecsRegionConfigsAnalyticsSpecs(
            instance_size=instance_size,
            disk_iops=disk_iops,
            ebs_volume_type=ebs_volume_type,
            node_count=node_count,
        )

        return typing.cast(None, jsii.invoke(self, "putAnalyticsSpecs", [value]))

    @jsii.member(jsii_name="putAutoScaling")
    def put_auto_scaling(
        self,
        *,
        compute_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        compute_max_instance_size: typing.Optional[builtins.str] = None,
        compute_min_instance_size: typing.Optional[builtins.str] = None,
        compute_scale_down_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        disk_gb_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param compute_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#compute_enabled AdvancedCluster#compute_enabled}.
        :param compute_max_instance_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#compute_max_instance_size AdvancedCluster#compute_max_instance_size}.
        :param compute_min_instance_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#compute_min_instance_size AdvancedCluster#compute_min_instance_size}.
        :param compute_scale_down_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#compute_scale_down_enabled AdvancedCluster#compute_scale_down_enabled}.
        :param disk_gb_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#disk_gb_enabled AdvancedCluster#disk_gb_enabled}.
        '''
        value = AdvancedClusterReplicationSpecsRegionConfigsAutoScaling(
            compute_enabled=compute_enabled,
            compute_max_instance_size=compute_max_instance_size,
            compute_min_instance_size=compute_min_instance_size,
            compute_scale_down_enabled=compute_scale_down_enabled,
            disk_gb_enabled=disk_gb_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putAutoScaling", [value]))

    @jsii.member(jsii_name="putElectableSpecs")
    def put_electable_specs(
        self,
        *,
        instance_size: builtins.str,
        disk_iops: typing.Optional[jsii.Number] = None,
        ebs_volume_type: typing.Optional[builtins.str] = None,
        node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param instance_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#instance_size AdvancedCluster#instance_size}.
        :param disk_iops: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#disk_iops AdvancedCluster#disk_iops}.
        :param ebs_volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#ebs_volume_type AdvancedCluster#ebs_volume_type}.
        :param node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#node_count AdvancedCluster#node_count}.
        '''
        value = AdvancedClusterReplicationSpecsRegionConfigsElectableSpecs(
            instance_size=instance_size,
            disk_iops=disk_iops,
            ebs_volume_type=ebs_volume_type,
            node_count=node_count,
        )

        return typing.cast(None, jsii.invoke(self, "putElectableSpecs", [value]))

    @jsii.member(jsii_name="putReadOnlySpecs")
    def put_read_only_specs(
        self,
        *,
        instance_size: builtins.str,
        disk_iops: typing.Optional[jsii.Number] = None,
        ebs_volume_type: typing.Optional[builtins.str] = None,
        node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param instance_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#instance_size AdvancedCluster#instance_size}.
        :param disk_iops: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#disk_iops AdvancedCluster#disk_iops}.
        :param ebs_volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#ebs_volume_type AdvancedCluster#ebs_volume_type}.
        :param node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#node_count AdvancedCluster#node_count}.
        '''
        value = AdvancedClusterReplicationSpecsRegionConfigsReadOnlySpecs(
            instance_size=instance_size,
            disk_iops=disk_iops,
            ebs_volume_type=ebs_volume_type,
            node_count=node_count,
        )

        return typing.cast(None, jsii.invoke(self, "putReadOnlySpecs", [value]))

    @jsii.member(jsii_name="resetAnalyticsAutoScaling")
    def reset_analytics_auto_scaling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnalyticsAutoScaling", []))

    @jsii.member(jsii_name="resetAnalyticsSpecs")
    def reset_analytics_specs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnalyticsSpecs", []))

    @jsii.member(jsii_name="resetAutoScaling")
    def reset_auto_scaling(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoScaling", []))

    @jsii.member(jsii_name="resetBackingProviderName")
    def reset_backing_provider_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackingProviderName", []))

    @jsii.member(jsii_name="resetElectableSpecs")
    def reset_electable_specs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElectableSpecs", []))

    @jsii.member(jsii_name="resetReadOnlySpecs")
    def reset_read_only_specs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadOnlySpecs", []))

    @builtins.property
    @jsii.member(jsii_name="analyticsAutoScaling")
    def analytics_auto_scaling(
        self,
    ) -> AdvancedClusterReplicationSpecsRegionConfigsAnalyticsAutoScalingOutputReference:
        return typing.cast(AdvancedClusterReplicationSpecsRegionConfigsAnalyticsAutoScalingOutputReference, jsii.get(self, "analyticsAutoScaling"))

    @builtins.property
    @jsii.member(jsii_name="analyticsSpecs")
    def analytics_specs(
        self,
    ) -> AdvancedClusterReplicationSpecsRegionConfigsAnalyticsSpecsOutputReference:
        return typing.cast(AdvancedClusterReplicationSpecsRegionConfigsAnalyticsSpecsOutputReference, jsii.get(self, "analyticsSpecs"))

    @builtins.property
    @jsii.member(jsii_name="autoScaling")
    def auto_scaling(
        self,
    ) -> AdvancedClusterReplicationSpecsRegionConfigsAutoScalingOutputReference:
        return typing.cast(AdvancedClusterReplicationSpecsRegionConfigsAutoScalingOutputReference, jsii.get(self, "autoScaling"))

    @builtins.property
    @jsii.member(jsii_name="electableSpecs")
    def electable_specs(
        self,
    ) -> AdvancedClusterReplicationSpecsRegionConfigsElectableSpecsOutputReference:
        return typing.cast(AdvancedClusterReplicationSpecsRegionConfigsElectableSpecsOutputReference, jsii.get(self, "electableSpecs"))

    @builtins.property
    @jsii.member(jsii_name="readOnlySpecs")
    def read_only_specs(
        self,
    ) -> "AdvancedClusterReplicationSpecsRegionConfigsReadOnlySpecsOutputReference":
        return typing.cast("AdvancedClusterReplicationSpecsRegionConfigsReadOnlySpecsOutputReference", jsii.get(self, "readOnlySpecs"))

    @builtins.property
    @jsii.member(jsii_name="analyticsAutoScalingInput")
    def analytics_auto_scaling_input(
        self,
    ) -> typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsAnalyticsAutoScaling]:
        return typing.cast(typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsAnalyticsAutoScaling], jsii.get(self, "analyticsAutoScalingInput"))

    @builtins.property
    @jsii.member(jsii_name="analyticsSpecsInput")
    def analytics_specs_input(
        self,
    ) -> typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsAnalyticsSpecs]:
        return typing.cast(typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsAnalyticsSpecs], jsii.get(self, "analyticsSpecsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoScalingInput")
    def auto_scaling_input(
        self,
    ) -> typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsAutoScaling]:
        return typing.cast(typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsAutoScaling], jsii.get(self, "autoScalingInput"))

    @builtins.property
    @jsii.member(jsii_name="backingProviderNameInput")
    def backing_provider_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "backingProviderNameInput"))

    @builtins.property
    @jsii.member(jsii_name="electableSpecsInput")
    def electable_specs_input(
        self,
    ) -> typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsElectableSpecs]:
        return typing.cast(typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsElectableSpecs], jsii.get(self, "electableSpecsInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="providerNameInput")
    def provider_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="readOnlySpecsInput")
    def read_only_specs_input(
        self,
    ) -> typing.Optional["AdvancedClusterReplicationSpecsRegionConfigsReadOnlySpecs"]:
        return typing.cast(typing.Optional["AdvancedClusterReplicationSpecsRegionConfigsReadOnlySpecs"], jsii.get(self, "readOnlySpecsInput"))

    @builtins.property
    @jsii.member(jsii_name="regionNameInput")
    def region_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="backingProviderName")
    def backing_provider_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "backingProviderName"))

    @backing_provider_name.setter
    def backing_provider_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f40f5fe5079fddbe9cdf9e02a5d9a5648ae5d9d513991b8df5e9e60b6762c1bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "backingProviderName", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ed4549696819e0815367b8386d33360740ff65d27397c813e11846873812a06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerName"))

    @provider_name.setter
    def provider_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__314c99ccc4777909fa8d67228de873b1a8c25f976b0158bc7d736d8a320759b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerName", value)

    @builtins.property
    @jsii.member(jsii_name="regionName")
    def region_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regionName"))

    @region_name.setter
    def region_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1a503d86bf488dce68d36351fc57d2eddb6931c2cc26c94203758c44844fbfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regionName", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AdvancedClusterReplicationSpecsRegionConfigs]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AdvancedClusterReplicationSpecsRegionConfigs]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AdvancedClusterReplicationSpecsRegionConfigs]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b832485f52d253cd2ddc9086d00dd0212471780f339b0517ceb94a113a761dca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterReplicationSpecsRegionConfigsReadOnlySpecs",
    jsii_struct_bases=[],
    name_mapping={
        "instance_size": "instanceSize",
        "disk_iops": "diskIops",
        "ebs_volume_type": "ebsVolumeType",
        "node_count": "nodeCount",
    },
)
class AdvancedClusterReplicationSpecsRegionConfigsReadOnlySpecs:
    def __init__(
        self,
        *,
        instance_size: builtins.str,
        disk_iops: typing.Optional[jsii.Number] = None,
        ebs_volume_type: typing.Optional[builtins.str] = None,
        node_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param instance_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#instance_size AdvancedCluster#instance_size}.
        :param disk_iops: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#disk_iops AdvancedCluster#disk_iops}.
        :param ebs_volume_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#ebs_volume_type AdvancedCluster#ebs_volume_type}.
        :param node_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#node_count AdvancedCluster#node_count}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a7e404e394e65612df18057f235390c8ceda8983bade9f5fa147d84458002df)
            check_type(argname="argument instance_size", value=instance_size, expected_type=type_hints["instance_size"])
            check_type(argname="argument disk_iops", value=disk_iops, expected_type=type_hints["disk_iops"])
            check_type(argname="argument ebs_volume_type", value=ebs_volume_type, expected_type=type_hints["ebs_volume_type"])
            check_type(argname="argument node_count", value=node_count, expected_type=type_hints["node_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_size": instance_size,
        }
        if disk_iops is not None:
            self._values["disk_iops"] = disk_iops
        if ebs_volume_type is not None:
            self._values["ebs_volume_type"] = ebs_volume_type
        if node_count is not None:
            self._values["node_count"] = node_count

    @builtins.property
    def instance_size(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#instance_size AdvancedCluster#instance_size}.'''
        result = self._values.get("instance_size")
        assert result is not None, "Required property 'instance_size' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def disk_iops(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#disk_iops AdvancedCluster#disk_iops}.'''
        result = self._values.get("disk_iops")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ebs_volume_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#ebs_volume_type AdvancedCluster#ebs_volume_type}.'''
        result = self._values.get("ebs_volume_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#node_count AdvancedCluster#node_count}.'''
        result = self._values.get("node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdvancedClusterReplicationSpecsRegionConfigsReadOnlySpecs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AdvancedClusterReplicationSpecsRegionConfigsReadOnlySpecsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterReplicationSpecsRegionConfigsReadOnlySpecsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e05f2845dce062c5ca8160c443726398fbd34145167aedf31d710b4c6a4282e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDiskIops")
    def reset_disk_iops(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskIops", []))

    @jsii.member(jsii_name="resetEbsVolumeType")
    def reset_ebs_volume_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEbsVolumeType", []))

    @jsii.member(jsii_name="resetNodeCount")
    def reset_node_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeCount", []))

    @builtins.property
    @jsii.member(jsii_name="diskIopsInput")
    def disk_iops_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskIopsInput"))

    @builtins.property
    @jsii.member(jsii_name="ebsVolumeTypeInput")
    def ebs_volume_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ebsVolumeTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceSizeInput")
    def instance_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeCountInput")
    def node_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "nodeCountInput"))

    @builtins.property
    @jsii.member(jsii_name="diskIops")
    def disk_iops(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskIops"))

    @disk_iops.setter
    def disk_iops(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__282192367c1e5faa067b6e49ba626476652e4a00f776beda555e88aa74ca859a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskIops", value)

    @builtins.property
    @jsii.member(jsii_name="ebsVolumeType")
    def ebs_volume_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ebsVolumeType"))

    @ebs_volume_type.setter
    def ebs_volume_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__003ac845552592f7e503ee2904ee8f5dc9eab43ea3aa4a477a20c9eb7e209f37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ebsVolumeType", value)

    @builtins.property
    @jsii.member(jsii_name="instanceSize")
    def instance_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "instanceSize"))

    @instance_size.setter
    def instance_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4f2554be211065e295b33d48dfab6711af8ab2ed6e6bdcdebd26d163847c5da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceSize", value)

    @builtins.property
    @jsii.member(jsii_name="nodeCount")
    def node_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "nodeCount"))

    @node_count.setter
    def node_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7fdea532d80a4f963199a48e71d026d30e3478f42b22b1dae19595d3162419e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeCount", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsReadOnlySpecs]:
        return typing.cast(typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsReadOnlySpecs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsReadOnlySpecs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2767f32671242c6abdc39c9f3574f58b776a08078e0b9730c8505d84db978804)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class AdvancedClusterTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#create AdvancedCluster#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#delete AdvancedCluster#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#update AdvancedCluster#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2f49bd273108840fd515b3138d013cbe626a564cf104e8f7e3583104276b3e3)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#create AdvancedCluster#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#delete AdvancedCluster#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/advanced_cluster#update AdvancedCluster#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdvancedClusterTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AdvancedClusterTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.advancedCluster.AdvancedClusterTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50d2058a092626c12df4259396ef475a23ce063b143e579faf07450e287d9302)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__261361f4a79540f5dee6d42940ed125a0874e98feb7e14ab1cc57b44e9dc8726)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed3bbc6ce48eb4d172917adc252179f759c95ab8c880163b1f3bf78cb6f1c512)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6a9772dfcd759fc396b362125cdc9204875203c4d0f2f5385ab3c317af089ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AdvancedClusterTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AdvancedClusterTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AdvancedClusterTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__914fa1653293fcb2bf0cd9b27a290cf286dd5931e2a31e4870811109386bc6cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "AdvancedCluster",
    "AdvancedClusterAdvancedConfiguration",
    "AdvancedClusterAdvancedConfigurationOutputReference",
    "AdvancedClusterBiConnector",
    "AdvancedClusterBiConnectorConfig",
    "AdvancedClusterBiConnectorConfigOutputReference",
    "AdvancedClusterBiConnectorOutputReference",
    "AdvancedClusterConfig",
    "AdvancedClusterConnectionStrings",
    "AdvancedClusterConnectionStringsList",
    "AdvancedClusterConnectionStringsOutputReference",
    "AdvancedClusterConnectionStringsPrivateEndpoint",
    "AdvancedClusterConnectionStringsPrivateEndpointEndpoints",
    "AdvancedClusterConnectionStringsPrivateEndpointEndpointsList",
    "AdvancedClusterConnectionStringsPrivateEndpointEndpointsOutputReference",
    "AdvancedClusterConnectionStringsPrivateEndpointList",
    "AdvancedClusterConnectionStringsPrivateEndpointOutputReference",
    "AdvancedClusterLabels",
    "AdvancedClusterLabelsList",
    "AdvancedClusterLabelsOutputReference",
    "AdvancedClusterReplicationSpecs",
    "AdvancedClusterReplicationSpecsList",
    "AdvancedClusterReplicationSpecsOutputReference",
    "AdvancedClusterReplicationSpecsRegionConfigs",
    "AdvancedClusterReplicationSpecsRegionConfigsAnalyticsAutoScaling",
    "AdvancedClusterReplicationSpecsRegionConfigsAnalyticsAutoScalingOutputReference",
    "AdvancedClusterReplicationSpecsRegionConfigsAnalyticsSpecs",
    "AdvancedClusterReplicationSpecsRegionConfigsAnalyticsSpecsOutputReference",
    "AdvancedClusterReplicationSpecsRegionConfigsAutoScaling",
    "AdvancedClusterReplicationSpecsRegionConfigsAutoScalingOutputReference",
    "AdvancedClusterReplicationSpecsRegionConfigsElectableSpecs",
    "AdvancedClusterReplicationSpecsRegionConfigsElectableSpecsOutputReference",
    "AdvancedClusterReplicationSpecsRegionConfigsList",
    "AdvancedClusterReplicationSpecsRegionConfigsOutputReference",
    "AdvancedClusterReplicationSpecsRegionConfigsReadOnlySpecs",
    "AdvancedClusterReplicationSpecsRegionConfigsReadOnlySpecsOutputReference",
    "AdvancedClusterTimeouts",
    "AdvancedClusterTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__6ca391e210dd2501c08a1078aaa9b0b13dafb996142bf6967d14ad720147cc40(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster_type: builtins.str,
    name: builtins.str,
    project_id: builtins.str,
    replication_specs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AdvancedClusterReplicationSpecs, typing.Dict[builtins.str, typing.Any]]]],
    advanced_configuration: typing.Optional[typing.Union[AdvancedClusterAdvancedConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bi_connector: typing.Optional[typing.Union[AdvancedClusterBiConnector, typing.Dict[builtins.str, typing.Any]]] = None,
    bi_connector_config: typing.Optional[typing.Union[AdvancedClusterBiConnectorConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    disk_size_gb: typing.Optional[jsii.Number] = None,
    encryption_at_rest_provider: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AdvancedClusterLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mongo_db_major_version: typing.Optional[builtins.str] = None,
    paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    pit_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retain_backups_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    root_cert_type: typing.Optional[builtins.str] = None,
    termination_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[AdvancedClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version_release_system: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__a0f54960afae626e790c1acd0c2f3d6ea13873f5c4a95cd47c86efd327ecf0e9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AdvancedClusterLabels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a92f697d36829c0ed5d33dfa4e117ceb29aa47f23bc874fda9adc1c7265ff2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AdvancedClusterReplicationSpecs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f36d43ee09f62eda38ca52a630ce978a4d2a6b0e80d07a0f6ee73d0ddc45898(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88b381b94247030bd2ec13b3f5a8ebb5e68c37110cc3e8d6e72484668592363f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2207623f87bfee8e123a93206e9e1faa8872ae0d187432c7945861c01c3542b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef0dba68b05b7e0a97c174a2e5e44232bdc4e6f6516649ecf9d9dd971393b7df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca23373bec3ef7123444356794b16d1b1be1ec03ac8ecaabb3bf93ca1c28f9c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01ea4321617f74da287d8dc515d628c7d2501cc13d8655a9c57d1d0777d94196(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__936076a5bc0c4e679d136fea19895c5f7a381b5eca5ee69886a0d1fdaf110550(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4e4972712a5af56caf23cc7d07d9c086e697327db7061268358e792380c229b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c2f2162190ceb431ce37f41993d349adff76de2914942509299a8c28d057ce8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62c600021a78716ee8cd967e6b21480b96bb9119e5726fc6f649a6ab848e4dd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef0c5231e480aa88441b6f8415419e59309e0ae70264afc4620986897c5f0321(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__834f398d42a6bb39f756bc583136ff7d6787605621cebb8e15e3a39601d8ae12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afc159d24c4c98c2ca7aa715ea2245f04b4480895168c28cad658cc425c307dd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c77ed15f187542791ad1047ad7cbd8966e5f65e81b6a133a58f872cd5e87d56f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f07f574c8fa825280fa076178783cd1825a9a5aa840a722e7c12419caa7537be(
    *,
    default_read_concern: typing.Optional[builtins.str] = None,
    default_write_concern: typing.Optional[builtins.str] = None,
    fail_index_key_too_long: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    javascript_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    minimum_enabled_tls_protocol: typing.Optional[builtins.str] = None,
    no_table_scan: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    oplog_min_retention_hours: typing.Optional[jsii.Number] = None,
    oplog_size_mb: typing.Optional[jsii.Number] = None,
    sample_refresh_interval_bi_connector: typing.Optional[jsii.Number] = None,
    sample_size_bi_connector: typing.Optional[jsii.Number] = None,
    transaction_lifetime_limit_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c975f663462f36982521e95f7c1fe6b57ef1d81da2e6ab4e5ed39f7730aa571(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae4d5ec4e494cb89987768cc5ee557be889fd253f54376da23912b4f601866f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d225ef8f1fed237dc5286680280c4d6c905b6cff2d1517d8e487f6905600514(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd4cb7ee12b8c30c5083a4badced9c5d6b20279ebfb62a1ea57a3aed15d64b93(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caae5634c05f81728ddb96703412f068d28d97dcbaa6cb01c8cb45c535be49ca(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__821004f34ef005b4543d12a9cada93d5b8f791c04eb5f40ae9a37629c3a1350e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc2273dfea54f6b8d680c0129d12f046f0dae72194d339376fb83a11f4eb0db(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b810895493074079670d2ead5c313d607880aececb73e81cac91ecc55fde0cef(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89107f11f98a245655bdea9a3802fa476eed1aa8db157eceb9872bc62a8577d6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ece2be870ca344009bad309d78c6b9464752378c276cb42686fe0e6d7436dc41(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8372262400117b8b85773571d23accdd28b0c99e7ac9633dee47628bd513a56b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca1d68d84db63873b044ba72b3c748dba19826398340fa4b0b111748f23d164e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10111819735c9050a9477bbe0003476fab1dde30d153e59a390f60cb76158217(
    value: typing.Optional[AdvancedClusterAdvancedConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66ba636ed83dc56cbf615e406699b342a917dc02e8ef2ca9d4f7c7bfaee4feae(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    read_preference: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fd542d3c606f4b134cc8957c519b14013250ce2bd271a16969b5137c79c03bb(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    read_preference: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10db520513acf5894f7f007cb234f434ae1e796dc914f719b5d118bd3d0c9b6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__906560276e1f1414721bd1e51e3991002381689c98389d6012ec92970018e6f2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fd2f5b912abd381ce9da0d4938c8e5b92fc2b10f41d51acad1146bdcd6aa450(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e0e3639fcc451a43294a5307a83345db8f359be114788e18c3cb54e8d8dc75b(
    value: typing.Optional[AdvancedClusterBiConnectorConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e33796d80afb9d8f7fd7dbc20721b1f9c4a2983cdd38304780c3c4664a00900(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7e49b6a9b630d29962c56424fc5cfede1d59b994db2641926cf75c66bb46e30(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__026b6a96329ccfd575fff77352d2918c1f16cf22194711a5893e91784163adf8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__157416fe5fa2bbd3b3f40a760bc241470adefa9887cdc83fa12ab9aa3787ca82(
    value: typing.Optional[AdvancedClusterBiConnector],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a30363ced36434a5e9034e0121c751d81ecf1ea1bcb86ae6e5a509ce56875323(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_type: builtins.str,
    name: builtins.str,
    project_id: builtins.str,
    replication_specs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AdvancedClusterReplicationSpecs, typing.Dict[builtins.str, typing.Any]]]],
    advanced_configuration: typing.Optional[typing.Union[AdvancedClusterAdvancedConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    backup_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bi_connector: typing.Optional[typing.Union[AdvancedClusterBiConnector, typing.Dict[builtins.str, typing.Any]]] = None,
    bi_connector_config: typing.Optional[typing.Union[AdvancedClusterBiConnectorConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    disk_size_gb: typing.Optional[jsii.Number] = None,
    encryption_at_rest_provider: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    labels: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AdvancedClusterLabels, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mongo_db_major_version: typing.Optional[builtins.str] = None,
    paused: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    pit_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retain_backups_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    root_cert_type: typing.Optional[builtins.str] = None,
    termination_protection_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[AdvancedClusterTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    version_release_system: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__441e6926327622b405eea34ff99aac9e39a54e90d4648b11cae462c092eb83d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c9ccc1e5691636f8f558c88ada542962192f5bea9a0089e5ef93707837eaf3d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5e6cd82f6bb97796d8b1ca5b23df4994d99382b8b0b093ef374316ace543295(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d77284f4b144ba7629d9143c5ac3dd8dc8dee07cd55fbe0d4c8832ac207559(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__decdd79a87080e6c962f848f0c401bc1d6bd33c24f0fbf74b034f37f02b2b6c1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f1fad330fc00229d19cc71fad1a83eeb70096ca62900e83cbc535b20a4304d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c44de2fe56fb3710900cb775195498eb1b83315955399d5c8c36f435b8e1d7b3(
    value: typing.Optional[AdvancedClusterConnectionStrings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7d8d8e125f511bd3b5200aab60804105dbd07580c502d53c8ca0cfef58f068(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01ab42e3af384730962cf6009e614759ed863504b621bbb89623a9bab6e3707b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c165827c1d030c7c306ddfff3b103f928633acaa73e2c481cab4b94e123551d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5451b4f1d704bc71cae244109009c3271983f07a605d52dec7119bb1794978d8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__034fe5d10e4a8012ca85456ac94ead1cb67676e27f25bee15c271c86edc7ca3e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a4154a4664a41b9a262d7e2e17449755aa4d1ba17d56a769fea5738aa492fc1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14612d1af0dcfeab45ffd2113f5cadbc8d87ec37e4cb9d732dcc54b7f8df7382(
    value: typing.Optional[AdvancedClusterConnectionStringsPrivateEndpointEndpoints],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcf8f3aed5a2ed0dec16991e015d361e6c9fe7793ff9b7303d070dc11406b5fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1124f3f9d4691b977265847607da40ad1c9566689b2cd138c0b682600cc63450(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d381cfcb7043c9221df5fe5e8007884ff95aa181d6e94ab965ea2bc405ef3ae0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79f756d8b8f7a5f37ed5d0c5a208d00d923643bb97238512b45568ab2959b250(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2835b675ce1e87fb6b38864ca75591a1cebe8c613149eedcc91f5e2bb172e0ec(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b07d524d51554b47b32aad1ac325df2e1ebe63304e260992ee7b2afab56c09d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73734012490414811d8d51b1f354aeb854351f022cbc0d2762e595873ed2a2c1(
    value: typing.Optional[AdvancedClusterConnectionStringsPrivateEndpoint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3ccbe321c0568cc90cfe481a65f7f9964ccd6f0184448ca35a6e484c52cce20(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3bf8dc858e84dd2fc203c5d9368565f1f7c34b356f67f0ce3ff6e4f92542cfe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14c98b4688cb2f9586569693244f9ca52ba8fdc49fe8da2405db5eed1d30c184(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd13169ed65041b63ae02df1a6a97baef196b92bf03d0ed21c86bd69797b998a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df49d7ad99124522d89ba62074f8ff00380d23486651f4d59e83f8a60aa4a4de(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98502041bcb95aa0aaef01c96deb9e34eaa0a9ed0a6c6a9302b308b71c143d2f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2143ce7db45869716ed6df3fe5317fc95783cd5b43e4a94efd06ab3270d9e7f8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AdvancedClusterLabels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c16b041f2b6715d394c3c637547924c202b89cd77eaae315c679d41c7bd708a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aab59bc233589b61d55464d9ed8b2f6bfdb7467266802249e9e8b26a8ae5c7f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36150de8473982913142a1f22852a39b03dac55e80506626587938315ad49362(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__997eb9d23afa104cbe41e004db15fe41afc7bd746dd484abefe0200ef2da968f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AdvancedClusterLabels]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2d180acb0d93a5929b7a49a95b70b19ad6d2475380444c34817bb223d300400(
    *,
    region_configs: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AdvancedClusterReplicationSpecsRegionConfigs, typing.Dict[builtins.str, typing.Any]]]],
    num_shards: typing.Optional[jsii.Number] = None,
    zone_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73ffce17b0b155003028c31dafe0afa96211e3e0fec4237aeab27fed28dbb6d9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51a0172233442ed7ae307fde176c482424259ac42d1c7b6fa51058d4e3c55011(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b02eb90791bc66d46831b8a07a40c3cc765f87ed59b7fc03231a2d5c8c6abf7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fc60e26f503809fe442d057bbb89bb553a5ec8f3c25df1be2b6d6548d7e7c0b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c108a9ce6889fbecccab6b11c59c5cf4dc049bd142bcae66cbfd4d07342ff3b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00934695c03893e843e577c5abffdfabca7a96b1e9db8826c337eb764f16a7fb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AdvancedClusterReplicationSpecs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__386584b0e17f3e007c092a4d067612039313c608c274c06028a6456c7a03e630(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b7a8acba93d2dae8d26620ee50ddb62894c3e914dc259b949daaf661528b6ec(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AdvancedClusterReplicationSpecsRegionConfigs, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a43b0be6cae2badd91b3d29b069ea02f3e59ae9e264fc9589e70b8f0f6d11db9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb66a21263dafadfbdaf4b3ee1d445ef83cae0475ab47abb03bb78e9ff3dd221(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d2a9cb3bc5fac581d0aac396900b60306828af063861dcfccc31e34c72d39f4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AdvancedClusterReplicationSpecs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f89b39e6209455119c0ff4d709ed7625af830dd9f115cc59c05422b5707f613(
    *,
    priority: jsii.Number,
    provider_name: builtins.str,
    region_name: builtins.str,
    analytics_auto_scaling: typing.Optional[typing.Union[AdvancedClusterReplicationSpecsRegionConfigsAnalyticsAutoScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    analytics_specs: typing.Optional[typing.Union[AdvancedClusterReplicationSpecsRegionConfigsAnalyticsSpecs, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_scaling: typing.Optional[typing.Union[AdvancedClusterReplicationSpecsRegionConfigsAutoScaling, typing.Dict[builtins.str, typing.Any]]] = None,
    backing_provider_name: typing.Optional[builtins.str] = None,
    electable_specs: typing.Optional[typing.Union[AdvancedClusterReplicationSpecsRegionConfigsElectableSpecs, typing.Dict[builtins.str, typing.Any]]] = None,
    read_only_specs: typing.Optional[typing.Union[AdvancedClusterReplicationSpecsRegionConfigsReadOnlySpecs, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8fa91b983bdaa15543467e3f7b99a9ec2f155950d0b2739930a080ee4543bd8(
    *,
    compute_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    compute_max_instance_size: typing.Optional[builtins.str] = None,
    compute_min_instance_size: typing.Optional[builtins.str] = None,
    compute_scale_down_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disk_gb_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39b1aa2c8e90fbb6a63ee7a53ae67783515e62d11de809dd8b41a94608a63966(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a778bca85a83662fbc97ecf4cfbba880e2d5ab642fc44b93670bf7fc8e4ba5e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaaa772d439d24961669f64c4fb0a818d73cf6a5ae3587ad3e1bf3f6e6e83546(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1563320de123ff2637a23dc8755bae1273f34bfbd415f10274b325481780e878(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e2661fa351dbe12333c774555a1b260fcd805c8e2ce1f2bd331951a5569a5de(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27bad33602d73cbe77aad4affc529996f948f8866e5697b823c4b5b4f4b1f04c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e6aacb2bb1ce976dcf2820709074312287889c1c5e45a85cf8527cce89d1bf(
    value: typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsAnalyticsAutoScaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f10cc668c743624c66680fb1e290c2db3fb4cf78c7e4815f4c3335590bf3941(
    *,
    instance_size: builtins.str,
    disk_iops: typing.Optional[jsii.Number] = None,
    ebs_volume_type: typing.Optional[builtins.str] = None,
    node_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d53ee5fa3f483080b6904e6aaf09b61ca458979a4e0deac980190fdbed708fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe7428ed944875ade07fb0ca99102a395e4afd2a8263bd4925430e2e2a6c02f2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d5a68c71041ba21574c61e3eb019cdd973f713565d92cf784bdef7885de1a4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0666d188175162ef8cdd79ce9e1367c2ce7fc17973d69a38c15a9d0fd8dd31c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9dd3152f1ff1c493be34e7b5b6f559787b0fae8319a46b39c5965c9fdf373f8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35970a2c568f7ec62497d2ac596fee0e1e23344eb3ad475b6b536741028934c3(
    value: typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsAnalyticsSpecs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db5dc6d3fe2339a164af5963ca30e956dd91e03838a3a074f70b75922e6a310(
    *,
    compute_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    compute_max_instance_size: typing.Optional[builtins.str] = None,
    compute_min_instance_size: typing.Optional[builtins.str] = None,
    compute_scale_down_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    disk_gb_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bc61e4bfa347ac6253e832a0355d46077e11f66f9c5acb8b021396529c40461(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fa6c7de3b5d5a8071330c10d372b33987fa8617c05e7d8e28efd54949437102(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a7d34700bd1e35948ff5b5167f1d3da3f26e90fc9a680066c5a5dc616c00e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c016847e380fc6851ec2589c5fa5bd61a85b3e6b67e6f58e8931be5ce1fc26dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1f664817df3280b1b18bb7a1e224ddca8280220b1777de3c807a736168dd3b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6406c116c2001b944a3c85877e5e3be234a69f1c995ad503590e66848b4d6075(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0318b8be9c0c9586daaedb0d9eb2c6cb5e0f58643698097f25292bc5ff818926(
    value: typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsAutoScaling],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__164f3e989882cd637971788cdd0d10ac6e593a9a015251fdf303438afff1a9d7(
    *,
    instance_size: builtins.str,
    disk_iops: typing.Optional[jsii.Number] = None,
    ebs_volume_type: typing.Optional[builtins.str] = None,
    node_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1cad0e35a9b740cc41c340daf8a1bcb1f241fb99069b55cb871d75546111a85(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec61c8ff531826b9f8709812359d4bf9a81434ed0e6e992cd7133c233a2398b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa7423c783ad5054155fd19b4a86a4a071511ab2dbfe1a1b42eae53531bc1d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7824cb99472b10a4518048605c53d0cbe28a2e2afc02156f48fdf07766411ad0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7bd989b191841033d952a70d27ddbdf8d408738ceb58982767f315ff26c7ca(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9007f7f86c25968ebbfdc88643ae50fa9b8e6d65826605da9adbcee745f4cbea(
    value: typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsElectableSpecs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1266a49ffa52e52965f301e2bc1aad2e4b64ae10d1587fefcc6eade0141eaa66(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e06bec31faef36629f18cf9c218de91ce2b58d77772fa90fce3e0c7592f59588(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af7674908b34616d24c1b11b6175d07a16282fff4452b22351814d348723ec27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__493cfc0fb66de0eaaab80849f36098230291f1ede73d4927f7ccd539d001218f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cf4d1df87051ee469b14dd38c48709ad38f3210c4fa9a727466488c381ea68a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a4172cdcfb7d961eff6c2d2f359d9ad008053d1e1e308e07ed4161abeecfb3d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AdvancedClusterReplicationSpecsRegionConfigs]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa72d912f6eee8599136cd1113d202d2fefe2230b1936c9d92d4fe1868fb4da3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f40f5fe5079fddbe9cdf9e02a5d9a5648ae5d9d513991b8df5e9e60b6762c1bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ed4549696819e0815367b8386d33360740ff65d27397c813e11846873812a06(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__314c99ccc4777909fa8d67228de873b1a8c25f976b0158bc7d736d8a320759b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1a503d86bf488dce68d36351fc57d2eddb6931c2cc26c94203758c44844fbfa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b832485f52d253cd2ddc9086d00dd0212471780f339b0517ceb94a113a761dca(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AdvancedClusterReplicationSpecsRegionConfigs]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a7e404e394e65612df18057f235390c8ceda8983bade9f5fa147d84458002df(
    *,
    instance_size: builtins.str,
    disk_iops: typing.Optional[jsii.Number] = None,
    ebs_volume_type: typing.Optional[builtins.str] = None,
    node_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e05f2845dce062c5ca8160c443726398fbd34145167aedf31d710b4c6a4282e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__282192367c1e5faa067b6e49ba626476652e4a00f776beda555e88aa74ca859a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__003ac845552592f7e503ee2904ee8f5dc9eab43ea3aa4a477a20c9eb7e209f37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4f2554be211065e295b33d48dfab6711af8ab2ed6e6bdcdebd26d163847c5da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7fdea532d80a4f963199a48e71d026d30e3478f42b22b1dae19595d3162419e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2767f32671242c6abdc39c9f3574f58b776a08078e0b9730c8505d84db978804(
    value: typing.Optional[AdvancedClusterReplicationSpecsRegionConfigsReadOnlySpecs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f49bd273108840fd515b3138d013cbe626a564cf104e8f7e3583104276b3e3(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50d2058a092626c12df4259396ef475a23ce063b143e579faf07450e287d9302(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__261361f4a79540f5dee6d42940ed125a0874e98feb7e14ab1cc57b44e9dc8726(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed3bbc6ce48eb4d172917adc252179f759c95ab8c880163b1f3bf78cb6f1c512(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6a9772dfcd759fc396b362125cdc9204875203c4d0f2f5385ab3c317af089ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__914fa1653293fcb2bf0cd9b27a290cf286dd5931e2a31e4870811109386bc6cb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AdvancedClusterTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
