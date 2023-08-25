'''
# `data_mongodbatlas_federated_database_instance`

Refer to the Terraform Registory for docs: [`data_mongodbatlas_federated_database_instance`](https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/federated_database_instance).
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


class DataMongodbatlasFederatedDatabaseInstance(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstance",
):
    '''Represents a {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/federated_database_instance mongodbatlas_federated_database_instance}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        project_id: builtins.str,
        cloud_provider_config: typing.Optional[typing.Union["DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/federated_database_instance mongodbatlas_federated_database_instance} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/federated_database_instance#name DataMongodbatlasFederatedDatabaseInstance#name}.
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/federated_database_instance#project_id DataMongodbatlasFederatedDatabaseInstance#project_id}.
        :param cloud_provider_config: cloud_provider_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/federated_database_instance#cloud_provider_config DataMongodbatlasFederatedDatabaseInstance#cloud_provider_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/federated_database_instance#id DataMongodbatlasFederatedDatabaseInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f6c9fbfc3bce328651493537601fe8544ee93cf9001ec412c2b638a39bed9e7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataMongodbatlasFederatedDatabaseInstanceConfig(
            name=name,
            project_id=project_id,
            cloud_provider_config=cloud_provider_config,
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

    @jsii.member(jsii_name="putCloudProviderConfig")
    def put_cloud_provider_config(
        self,
        *,
        aws: typing.Optional[typing.Union["DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigAws", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aws: aws block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/federated_database_instance#aws DataMongodbatlasFederatedDatabaseInstance#aws}
        '''
        value = DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfig(aws=aws)

        return typing.cast(None, jsii.invoke(self, "putCloudProviderConfig", [value]))

    @jsii.member(jsii_name="resetCloudProviderConfig")
    def reset_cloud_provider_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudProviderConfig", []))

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
    @jsii.member(jsii_name="cloudProviderConfig")
    def cloud_provider_config(
        self,
    ) -> "DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigOutputReference":
        return typing.cast("DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigOutputReference", jsii.get(self, "cloudProviderConfig"))

    @builtins.property
    @jsii.member(jsii_name="dataProcessRegion")
    def data_process_region(
        self,
    ) -> "DataMongodbatlasFederatedDatabaseInstanceDataProcessRegionList":
        return typing.cast("DataMongodbatlasFederatedDatabaseInstanceDataProcessRegionList", jsii.get(self, "dataProcessRegion"))

    @builtins.property
    @jsii.member(jsii_name="hostnames")
    def hostnames(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "hostnames"))

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "state"))

    @builtins.property
    @jsii.member(jsii_name="storageDatabases")
    def storage_databases(
        self,
    ) -> "DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesList":
        return typing.cast("DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesList", jsii.get(self, "storageDatabases"))

    @builtins.property
    @jsii.member(jsii_name="storageStores")
    def storage_stores(
        self,
    ) -> "DataMongodbatlasFederatedDatabaseInstanceStorageStoresList":
        return typing.cast("DataMongodbatlasFederatedDatabaseInstanceStorageStoresList", jsii.get(self, "storageStores"))

    @builtins.property
    @jsii.member(jsii_name="cloudProviderConfigInput")
    def cloud_provider_config_input(
        self,
    ) -> typing.Optional["DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfig"]:
        return typing.cast(typing.Optional["DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfig"], jsii.get(self, "cloudProviderConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b803c314c51ae23d8b0218295ca4623c58fb7ed3faffdd765ae66df97eb234e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7310716058577682d44a0e475b6f4efcab25076883ea2fc3b61ab91ec9ae4b5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e59e521bba5e04a6a4f322b256d5722166da1c227a247f93bab739b8ebdbd24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfig",
    jsii_struct_bases=[],
    name_mapping={"aws": "aws"},
)
class DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfig:
    def __init__(
        self,
        *,
        aws: typing.Optional[typing.Union["DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigAws", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param aws: aws block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/federated_database_instance#aws DataMongodbatlasFederatedDatabaseInstance#aws}
        '''
        if isinstance(aws, dict):
            aws = DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigAws(**aws)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a90e91c3cd81cc463431432d531ca14c739ed0f2c51f9a78fbc0018464926309)
            check_type(argname="argument aws", value=aws, expected_type=type_hints["aws"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws is not None:
            self._values["aws"] = aws

    @builtins.property
    def aws(
        self,
    ) -> typing.Optional["DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigAws"]:
        '''aws block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/federated_database_instance#aws DataMongodbatlasFederatedDatabaseInstance#aws}
        '''
        result = self._values.get("aws")
        return typing.cast(typing.Optional["DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigAws"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigAws",
    jsii_struct_bases=[],
    name_mapping={"test_s3_bucket": "testS3Bucket"},
)
class DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigAws:
    def __init__(self, *, test_s3_bucket: typing.Optional[builtins.str] = None) -> None:
        '''
        :param test_s3_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/federated_database_instance#test_s3_bucket DataMongodbatlasFederatedDatabaseInstance#test_s3_bucket}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3e7489843c284e837146043d614bc004b8c601c765aadf93ce5701930f9d08c)
            check_type(argname="argument test_s3_bucket", value=test_s3_bucket, expected_type=type_hints["test_s3_bucket"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if test_s3_bucket is not None:
            self._values["test_s3_bucket"] = test_s3_bucket

    @builtins.property
    def test_s3_bucket(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/federated_database_instance#test_s3_bucket DataMongodbatlasFederatedDatabaseInstance#test_s3_bucket}.'''
        result = self._values.get("test_s3_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigAws(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigAwsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigAwsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__777e569862e67be8a2cc87af241f4dbcfabcd5e39e287a856c2ba4b94233f04e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTestS3Bucket")
    def reset_test_s3_bucket(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTestS3Bucket", []))

    @builtins.property
    @jsii.member(jsii_name="externalId")
    def external_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalId"))

    @builtins.property
    @jsii.member(jsii_name="iamAssumedRoleArn")
    def iam_assumed_role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "iamAssumedRoleArn"))

    @builtins.property
    @jsii.member(jsii_name="iamUserArn")
    def iam_user_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "iamUserArn"))

    @builtins.property
    @jsii.member(jsii_name="roleId")
    def role_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleId"))

    @builtins.property
    @jsii.member(jsii_name="testS3BucketInput")
    def test_s3_bucket_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "testS3BucketInput"))

    @builtins.property
    @jsii.member(jsii_name="testS3Bucket")
    def test_s3_bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "testS3Bucket"))

    @test_s3_bucket.setter
    def test_s3_bucket(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4bc239ef63abe3159e127dc7dd7cc9fc76dfc69d66f3ede1eb06777967277e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "testS3Bucket", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigAws]:
        return typing.cast(typing.Optional[DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigAws], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigAws],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dd585aa32ffd6a7fbe30c19798523d2283c3e66c50c3b70ee3c0923ec8e8e4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ed2945bccc687732179824075b8a6d3dadb7e80b42e8523119b2d15e353644d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAws")
    def put_aws(self, *, test_s3_bucket: typing.Optional[builtins.str] = None) -> None:
        '''
        :param test_s3_bucket: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/federated_database_instance#test_s3_bucket DataMongodbatlasFederatedDatabaseInstance#test_s3_bucket}.
        '''
        value = DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigAws(
            test_s3_bucket=test_s3_bucket
        )

        return typing.cast(None, jsii.invoke(self, "putAws", [value]))

    @jsii.member(jsii_name="resetAws")
    def reset_aws(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAws", []))

    @builtins.property
    @jsii.member(jsii_name="aws")
    def aws(
        self,
    ) -> DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigAwsOutputReference:
        return typing.cast(DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigAwsOutputReference, jsii.get(self, "aws"))

    @builtins.property
    @jsii.member(jsii_name="awsInput")
    def aws_input(
        self,
    ) -> typing.Optional[DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigAws]:
        return typing.cast(typing.Optional[DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigAws], jsii.get(self, "awsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfig]:
        return typing.cast(typing.Optional[DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__380b6a1b4f8a3402417bdb0d20256a2d13032bcf8c901be956494d905ae781fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceConfig",
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
        "project_id": "projectId",
        "cloud_provider_config": "cloudProviderConfig",
        "id": "id",
    },
)
class DataMongodbatlasFederatedDatabaseInstanceConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        project_id: builtins.str,
        cloud_provider_config: typing.Optional[typing.Union[DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/federated_database_instance#name DataMongodbatlasFederatedDatabaseInstance#name}.
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/federated_database_instance#project_id DataMongodbatlasFederatedDatabaseInstance#project_id}.
        :param cloud_provider_config: cloud_provider_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/federated_database_instance#cloud_provider_config DataMongodbatlasFederatedDatabaseInstance#cloud_provider_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/federated_database_instance#id DataMongodbatlasFederatedDatabaseInstance#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(cloud_provider_config, dict):
            cloud_provider_config = DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfig(**cloud_provider_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed7217143d8663461b24de1650c1fb971f5c2f8c1c10302f246db2e8fe179179)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument cloud_provider_config", value=cloud_provider_config, expected_type=type_hints["cloud_provider_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "project_id": project_id,
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
        if cloud_provider_config is not None:
            self._values["cloud_provider_config"] = cloud_provider_config
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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/federated_database_instance#name DataMongodbatlasFederatedDatabaseInstance#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/federated_database_instance#project_id DataMongodbatlasFederatedDatabaseInstance#project_id}.'''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloud_provider_config(
        self,
    ) -> typing.Optional[DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfig]:
        '''cloud_provider_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/federated_database_instance#cloud_provider_config DataMongodbatlasFederatedDatabaseInstance#cloud_provider_config}
        '''
        result = self._values.get("cloud_provider_config")
        return typing.cast(typing.Optional[DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfig], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/federated_database_instance#id DataMongodbatlasFederatedDatabaseInstance#id}.

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
        return "DataMongodbatlasFederatedDatabaseInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceDataProcessRegion",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataMongodbatlasFederatedDatabaseInstanceDataProcessRegion:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataMongodbatlasFederatedDatabaseInstanceDataProcessRegion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataMongodbatlasFederatedDatabaseInstanceDataProcessRegionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceDataProcessRegionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52462564004e25fc7a201dbad1bcac7b0c57ec81dd9a07d7f3f06b9379b64815)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataMongodbatlasFederatedDatabaseInstanceDataProcessRegionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4fa44d00d5bb120ed0834c0d8385162af6a874d15b431f1d9ea239620ce5f05)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataMongodbatlasFederatedDatabaseInstanceDataProcessRegionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__585fc6b12893fd55abb811c6f522d7fb65fe7cc0b44456cc72eb1049f685d263)
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
            type_hints = typing.get_type_hints(_typecheckingstub__833ada1a6e218dc31ef7bcb4dc4dca2a7e34b30775784d14c1294e612903b2f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__296aaea047846009299d7c5de1a519abcce08de0fcfb39790b49e745cef14a11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataMongodbatlasFederatedDatabaseInstanceDataProcessRegionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceDataProcessRegionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7f648d87f8c0701c553ab3ec94c3fe62f538967bed7baaf356ea4935a84fde9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="cloudProvider")
    def cloud_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudProvider"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataMongodbatlasFederatedDatabaseInstanceDataProcessRegion]:
        return typing.cast(typing.Optional[DataMongodbatlasFederatedDatabaseInstanceDataProcessRegion], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataMongodbatlasFederatedDatabaseInstanceDataProcessRegion],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2028475efc6f5ebf8464ac9655d6676398411c45a617463497b50eb3eef35385)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceStorageDatabases",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataMongodbatlasFederatedDatabaseInstanceStorageDatabases:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataMongodbatlasFederatedDatabaseInstanceStorageDatabases(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollections",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollections:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollections(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsDataSources",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsDataSources:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsDataSources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsDataSourcesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsDataSourcesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ef30a5a20ffab8598e217b243759c9d11ba6b5ebd2dd3516a5251d176f002a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsDataSourcesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47be5975aa9e37de9bd4659749689a9525d4858382719e169e048fadfeabeb02)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsDataSourcesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18e4163c88650913c04cd0051cf44b30df2278cf447ea2e365458ae35e35b467)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7174327c24b00e9cae3b297758639e167e083a39851581404640ea3c59ee2824)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ec94a49cdef6378f93c20dd5d7efd6b4db6d387c10f8e813e40d4071668206b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsDataSourcesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsDataSourcesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__962495b9c829602bd420ba05e110e3782308f8e3c41827590984420f8184e540)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="allowInsecure")
    def allow_insecure(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "allowInsecure"))

    @builtins.property
    @jsii.member(jsii_name="collection")
    def collection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collection"))

    @builtins.property
    @jsii.member(jsii_name="collectionRegex")
    def collection_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collectionRegex"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @builtins.property
    @jsii.member(jsii_name="databaseRegex")
    def database_regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "databaseRegex"))

    @builtins.property
    @jsii.member(jsii_name="defaultFormat")
    def default_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultFormat"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="provenanceFieldName")
    def provenance_field_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "provenanceFieldName"))

    @builtins.property
    @jsii.member(jsii_name="storeName")
    def store_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storeName"))

    @builtins.property
    @jsii.member(jsii_name="urls")
    def urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "urls"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsDataSources]:
        return typing.cast(typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsDataSources], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsDataSources],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55b302c8abf38c4bb025dee88eb8a01ec4cd7410a6a8a989202be1a65899a279)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4509edcf7ea9e5416b7a6fa7a86df0038e2dcab8519f3703bb20c434c23176d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34dc0e1ee2149b4f66e19523db5c68de9971c9ab45ae1c8c75064dd907d17ebb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__047c47c71927c6221fc45d34a16b33c924691c2c9b3a5f0db7b3118f085a7930)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20cc14ff0c1d9ffb17f6b179e6fccb683774c55087047c1756f79e22052fa821)
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
            type_hints = typing.get_type_hints(_typecheckingstub__598e0415e12c183bd080777865f94a016fd8fd8a4fd48307bcd6457268cd6d1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9b01d090ae5e707a8553dd72bc107e697a01489c60f3c55cf5854f551c0ece4d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dataSources")
    def data_sources(
        self,
    ) -> DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsDataSourcesList:
        return typing.cast(DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsDataSourcesList, jsii.get(self, "dataSources"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollections]:
        return typing.cast(typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollections], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollections],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c48116de97d53cee575588e91c6a5a07fef1158e0ca8d3c0a7c50badfb3d184b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a7ea52753485403bbac8b0a14446586909d8ea1586d539ebfd3335021b218e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed6333990dab02a0d8cd0c05c0a82ad24a2d45e30cd0e75e83135780b2aac878)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__777370f6170861a3d4080404d0154e2630db27491a0ef62aab6ef4e4ad61a2a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b7cbae5c3da803ad2fd001e3d9e1a360d2eca8476e4ea32e68218b91df54c59)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49166086997138201688a77eb3751e8ff8e0cd40fbbb1cf1e5e42c1a160cae08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ef293cf7fe1b1007bfad97d26fa749212618301fb3b684cc11882a7ed6c6149)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="collections")
    def collections(
        self,
    ) -> DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsList:
        return typing.cast(DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsList, jsii.get(self, "collections"))

    @builtins.property
    @jsii.member(jsii_name="maxWildcardCollections")
    def max_wildcard_collections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxWildcardCollections"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="views")
    def views(
        self,
    ) -> "DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesViewsList":
        return typing.cast("DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesViewsList", jsii.get(self, "views"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageDatabases]:
        return typing.cast(typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageDatabases], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageDatabases],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d06bfce7bc82be66057646aecd40ca19e63690947988464500c2277fdc7b984d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesViews",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesViews:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesViews(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesViewsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesViewsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__21fec42f1f97cbcb8f19d470855f40654c22f1ca0db450903ec6079688286a71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesViewsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c3278c9e68cef4bcc84325826501531ac6f98d2eea104fbbd7b7c6975877613)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesViewsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea0a01df99247b983f41732d0d8f9ad8905a8fa7f16b56799c55dfc54707ad13)
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
            type_hints = typing.get_type_hints(_typecheckingstub__98e04fc961ebfd0310b934cc48be503e3e3572ee204708cf3ceba23c5c69021a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91d8d80cd1d02dcca068b83fccff86d74d1aacdcbcc08c10e288faa593195ae7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesViewsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesViewsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c4ee9e786c82919165df31a44112ef5aa7839a035bb60b79498b01b26aa024c)
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
    @jsii.member(jsii_name="pipeline")
    def pipeline(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pipeline"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesViews]:
        return typing.cast(typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesViews], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesViews],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd878662ed5eb4dcaa4808c154e9c74314dd47e81ada696bdaf6f225851ffa45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceStorageStores",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataMongodbatlasFederatedDatabaseInstanceStorageStores:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataMongodbatlasFederatedDatabaseInstanceStorageStores(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataMongodbatlasFederatedDatabaseInstanceStorageStoresList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceStorageStoresList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65ef1711fae1b02ea1670bf4aba3432f9c52dd2c724efbf49e34690de080a947)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataMongodbatlasFederatedDatabaseInstanceStorageStoresOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e374fff101896495d14bef91a23cdc4452edfc1d509f4c03b4727441a22a544)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataMongodbatlasFederatedDatabaseInstanceStorageStoresOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e4b5535169999dd2b3754c0f255b3bdb40a1bc94c81ee64779bff619d3deb21)
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
            type_hints = typing.get_type_hints(_typecheckingstub__914021bebaa783d372e1fcf4319896569b7cc55292844977fcc2e8a99333a724)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4da2050f436b86e660f14534b7d44233fc8db911b8e046078a91867fab11f888)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataMongodbatlasFederatedDatabaseInstanceStorageStoresOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceStorageStoresOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38509689b8844d503d722794f1f0f606aeafd4b9f3941b909cbf1d940a98845c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="additionalStorageClasses")
    def additional_storage_classes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "additionalStorageClasses"))

    @builtins.property
    @jsii.member(jsii_name="allowInsecure")
    def allow_insecure(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "allowInsecure"))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucket"))

    @builtins.property
    @jsii.member(jsii_name="clusterId")
    def cluster_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterId"))

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

    @builtins.property
    @jsii.member(jsii_name="defaultFormat")
    def default_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultFormat"))

    @builtins.property
    @jsii.member(jsii_name="delimiter")
    def delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delimiter"))

    @builtins.property
    @jsii.member(jsii_name="includeTags")
    def include_tags(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "includeTags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "provider"))

    @builtins.property
    @jsii.member(jsii_name="public")
    def public(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "public"))

    @builtins.property
    @jsii.member(jsii_name="readPreference")
    def read_preference(
        self,
    ) -> "DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceList":
        return typing.cast("DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceList", jsii.get(self, "readPreference"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="urls")
    def urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "urls"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageStores]:
        return typing.cast(typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageStores], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageStores],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cde6aaea9e58a4c654296700883ca722b8eabecda25060b8395080eef3ee3ead)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreference",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreference:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e344ea36cc4278c531dcc4781531969da159febfd7a0052dca3ad240d9cece51)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b99e33c4d42af9b6694cc766a736e1adacd8337879dbbf010558fb926c3caa35)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81a677fe8855ad51c767bf9e6d0e0b1df5cca8e54f444eb165aa3f638e84df90)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9b83db3b597c01c52e876530f679558a5950242abcebcc9baca8748a31f3e86)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ca447068c55e568a9e93e10b13d7929d089783e789330b2d1ff3520400de49b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7fffb68e685288f34b18f940ffa890f473a0a0a34011cb1026a431773158e647)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="maxStalenessSeconds")
    def max_staleness_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxStalenessSeconds"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(
        self,
    ) -> "DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceTagsList":
        return typing.cast("DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceTagsList", jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreference]:
        return typing.cast(typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreference], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreference],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2198c379c7e5d946fccb857d0c8a8bb6631f2d2a21d6e8bbac79c7051fc17e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceTags",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceTags:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceTagsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceTagsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__be60e8e85d4ce4a4eea0a4179dc3babbab6c2984a2119243af8496fba320fa26)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceTagsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1cd7849d8b9b295db582ad769afa7cd1e7c49a521d63fbd0004ee908b250d99)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceTagsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__818b653312ff0cc5b90ead1f264ae5f0b32613e5887e49f0aea66b663829e2b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__323854f2321b7632136db85b9246d2441fb8891aca9cc65dc64858390bda6e50)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5a7ce92d7d8e7dfedf3f7ff0045fd534771e2962416b8bb46c9bfde15e0db50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasFederatedDatabaseInstance.DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f74288f3b2bbc764db7e03d7786e41d27653c79e445eaaec38a72648bc54223)
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
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceTags]:
        return typing.cast(typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceTags], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceTags],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8b2d59bcd140d711861b9ba918bbf667edf24320ec950931bcd529c0984dfe5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataMongodbatlasFederatedDatabaseInstance",
    "DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfig",
    "DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigAws",
    "DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigAwsOutputReference",
    "DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigOutputReference",
    "DataMongodbatlasFederatedDatabaseInstanceConfig",
    "DataMongodbatlasFederatedDatabaseInstanceDataProcessRegion",
    "DataMongodbatlasFederatedDatabaseInstanceDataProcessRegionList",
    "DataMongodbatlasFederatedDatabaseInstanceDataProcessRegionOutputReference",
    "DataMongodbatlasFederatedDatabaseInstanceStorageDatabases",
    "DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollections",
    "DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsDataSources",
    "DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsDataSourcesList",
    "DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsDataSourcesOutputReference",
    "DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsList",
    "DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsOutputReference",
    "DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesList",
    "DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesOutputReference",
    "DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesViews",
    "DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesViewsList",
    "DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesViewsOutputReference",
    "DataMongodbatlasFederatedDatabaseInstanceStorageStores",
    "DataMongodbatlasFederatedDatabaseInstanceStorageStoresList",
    "DataMongodbatlasFederatedDatabaseInstanceStorageStoresOutputReference",
    "DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreference",
    "DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceList",
    "DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceOutputReference",
    "DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceTags",
    "DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceTagsList",
    "DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceTagsOutputReference",
]

publication.publish()

def _typecheckingstub__4f6c9fbfc3bce328651493537601fe8544ee93cf9001ec412c2b638a39bed9e7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    project_id: builtins.str,
    cloud_provider_config: typing.Optional[typing.Union[DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfig, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__8b803c314c51ae23d8b0218295ca4623c58fb7ed3faffdd765ae66df97eb234e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7310716058577682d44a0e475b6f4efcab25076883ea2fc3b61ab91ec9ae4b5e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e59e521bba5e04a6a4f322b256d5722166da1c227a247f93bab739b8ebdbd24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a90e91c3cd81cc463431432d531ca14c739ed0f2c51f9a78fbc0018464926309(
    *,
    aws: typing.Optional[typing.Union[DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigAws, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3e7489843c284e837146043d614bc004b8c601c765aadf93ce5701930f9d08c(
    *,
    test_s3_bucket: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__777e569862e67be8a2cc87af241f4dbcfabcd5e39e287a856c2ba4b94233f04e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4bc239ef63abe3159e127dc7dd7cc9fc76dfc69d66f3ede1eb06777967277e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd585aa32ffd6a7fbe30c19798523d2283c3e66c50c3b70ee3c0923ec8e8e4b(
    value: typing.Optional[DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfigAws],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ed2945bccc687732179824075b8a6d3dadb7e80b42e8523119b2d15e353644d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__380b6a1b4f8a3402417bdb0d20256a2d13032bcf8c901be956494d905ae781fe(
    value: typing.Optional[DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed7217143d8663461b24de1650c1fb971f5c2f8c1c10302f246db2e8fe179179(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    project_id: builtins.str,
    cloud_provider_config: typing.Optional[typing.Union[DataMongodbatlasFederatedDatabaseInstanceCloudProviderConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52462564004e25fc7a201dbad1bcac7b0c57ec81dd9a07d7f3f06b9379b64815(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4fa44d00d5bb120ed0834c0d8385162af6a874d15b431f1d9ea239620ce5f05(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__585fc6b12893fd55abb811c6f522d7fb65fe7cc0b44456cc72eb1049f685d263(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__833ada1a6e218dc31ef7bcb4dc4dca2a7e34b30775784d14c1294e612903b2f9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__296aaea047846009299d7c5de1a519abcce08de0fcfb39790b49e745cef14a11(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7f648d87f8c0701c553ab3ec94c3fe62f538967bed7baaf356ea4935a84fde9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2028475efc6f5ebf8464ac9655d6676398411c45a617463497b50eb3eef35385(
    value: typing.Optional[DataMongodbatlasFederatedDatabaseInstanceDataProcessRegion],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef30a5a20ffab8598e217b243759c9d11ba6b5ebd2dd3516a5251d176f002a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47be5975aa9e37de9bd4659749689a9525d4858382719e169e048fadfeabeb02(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18e4163c88650913c04cd0051cf44b30df2278cf447ea2e365458ae35e35b467(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7174327c24b00e9cae3b297758639e167e083a39851581404640ea3c59ee2824(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec94a49cdef6378f93c20dd5d7efd6b4db6d387c10f8e813e40d4071668206b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__962495b9c829602bd420ba05e110e3782308f8e3c41827590984420f8184e540(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55b302c8abf38c4bb025dee88eb8a01ec4cd7410a6a8a989202be1a65899a279(
    value: typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollectionsDataSources],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4509edcf7ea9e5416b7a6fa7a86df0038e2dcab8519f3703bb20c434c23176d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34dc0e1ee2149b4f66e19523db5c68de9971c9ab45ae1c8c75064dd907d17ebb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__047c47c71927c6221fc45d34a16b33c924691c2c9b3a5f0db7b3118f085a7930(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20cc14ff0c1d9ffb17f6b179e6fccb683774c55087047c1756f79e22052fa821(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__598e0415e12c183bd080777865f94a016fd8fd8a4fd48307bcd6457268cd6d1f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b01d090ae5e707a8553dd72bc107e697a01489c60f3c55cf5854f551c0ece4d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c48116de97d53cee575588e91c6a5a07fef1158e0ca8d3c0a7c50badfb3d184b(
    value: typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesCollections],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a7ea52753485403bbac8b0a14446586909d8ea1586d539ebfd3335021b218e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed6333990dab02a0d8cd0c05c0a82ad24a2d45e30cd0e75e83135780b2aac878(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__777370f6170861a3d4080404d0154e2630db27491a0ef62aab6ef4e4ad61a2a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b7cbae5c3da803ad2fd001e3d9e1a360d2eca8476e4ea32e68218b91df54c59(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49166086997138201688a77eb3751e8ff8e0cd40fbbb1cf1e5e42c1a160cae08(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ef293cf7fe1b1007bfad97d26fa749212618301fb3b684cc11882a7ed6c6149(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d06bfce7bc82be66057646aecd40ca19e63690947988464500c2277fdc7b984d(
    value: typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageDatabases],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21fec42f1f97cbcb8f19d470855f40654c22f1ca0db450903ec6079688286a71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c3278c9e68cef4bcc84325826501531ac6f98d2eea104fbbd7b7c6975877613(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea0a01df99247b983f41732d0d8f9ad8905a8fa7f16b56799c55dfc54707ad13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98e04fc961ebfd0310b934cc48be503e3e3572ee204708cf3ceba23c5c69021a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91d8d80cd1d02dcca068b83fccff86d74d1aacdcbcc08c10e288faa593195ae7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c4ee9e786c82919165df31a44112ef5aa7839a035bb60b79498b01b26aa024c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd878662ed5eb4dcaa4808c154e9c74314dd47e81ada696bdaf6f225851ffa45(
    value: typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageDatabasesViews],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65ef1711fae1b02ea1670bf4aba3432f9c52dd2c724efbf49e34690de080a947(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e374fff101896495d14bef91a23cdc4452edfc1d509f4c03b4727441a22a544(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e4b5535169999dd2b3754c0f255b3bdb40a1bc94c81ee64779bff619d3deb21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__914021bebaa783d372e1fcf4319896569b7cc55292844977fcc2e8a99333a724(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4da2050f436b86e660f14534b7d44233fc8db911b8e046078a91867fab11f888(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38509689b8844d503d722794f1f0f606aeafd4b9f3941b909cbf1d940a98845c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cde6aaea9e58a4c654296700883ca722b8eabecda25060b8395080eef3ee3ead(
    value: typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageStores],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e344ea36cc4278c531dcc4781531969da159febfd7a0052dca3ad240d9cece51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b99e33c4d42af9b6694cc766a736e1adacd8337879dbbf010558fb926c3caa35(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81a677fe8855ad51c767bf9e6d0e0b1df5cca8e54f444eb165aa3f638e84df90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9b83db3b597c01c52e876530f679558a5950242abcebcc9baca8748a31f3e86(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ca447068c55e568a9e93e10b13d7929d089783e789330b2d1ff3520400de49b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fffb68e685288f34b18f940ffa890f473a0a0a34011cb1026a431773158e647(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2198c379c7e5d946fccb857d0c8a8bb6631f2d2a21d6e8bbac79c7051fc17e7(
    value: typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreference],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be60e8e85d4ce4a4eea0a4179dc3babbab6c2984a2119243af8496fba320fa26(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1cd7849d8b9b295db582ad769afa7cd1e7c49a521d63fbd0004ee908b250d99(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__818b653312ff0cc5b90ead1f264ae5f0b32613e5887e49f0aea66b663829e2b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__323854f2321b7632136db85b9246d2441fb8891aca9cc65dc64858390bda6e50(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5a7ce92d7d8e7dfedf3f7ff0045fd534771e2962416b8bb46c9bfde15e0db50(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f74288f3b2bbc764db7e03d7786e41d27653c79e445eaaec38a72648bc54223(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8b2d59bcd140d711861b9ba918bbf667edf24320ec950931bcd529c0984dfe5(
    value: typing.Optional[DataMongodbatlasFederatedDatabaseInstanceStorageStoresReadPreferenceTags],
) -> None:
    """Type checking stubs"""
    pass
