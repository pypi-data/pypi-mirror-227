'''
# `mongodbatlas_cloud_provider_access_setup`

Refer to the Terraform Registory for docs: [`mongodbatlas_cloud_provider_access_setup`](https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/cloud_provider_access_setup).
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


class CloudProviderAccessSetup(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.cloudProviderAccessSetup.CloudProviderAccessSetup",
):
    '''Represents a {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/cloud_provider_access_setup mongodbatlas_cloud_provider_access_setup}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        project_id: builtins.str,
        provider_name: builtins.str,
        azure_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudProviderAccessSetupAzureConfig", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/cloud_provider_access_setup mongodbatlas_cloud_provider_access_setup} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/cloud_provider_access_setup#project_id CloudProviderAccessSetup#project_id}.
        :param provider_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/cloud_provider_access_setup#provider_name CloudProviderAccessSetup#provider_name}.
        :param azure_config: azure_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/cloud_provider_access_setup#azure_config CloudProviderAccessSetup#azure_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/cloud_provider_access_setup#id CloudProviderAccessSetup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01a196fe0896ed4cd98601f2fac3a209b6c84dad478b0b6bcd30b0e4bb69865d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CloudProviderAccessSetupConfig(
            project_id=project_id,
            provider_name=provider_name,
            azure_config=azure_config,
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

    @jsii.member(jsii_name="putAzureConfig")
    def put_azure_config(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CloudProviderAccessSetupAzureConfig", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d752b256d79d92c4ae8993b044c8c6ff72da595ac013d4cfdaea353a68d8840)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAzureConfig", [value]))

    @jsii.member(jsii_name="resetAzureConfig")
    def reset_azure_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureConfig", []))

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
    @jsii.member(jsii_name="aws")
    def aws(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "aws"))

    @builtins.property
    @jsii.member(jsii_name="awsConfig")
    def aws_config(self) -> "CloudProviderAccessSetupAwsConfigList":
        return typing.cast("CloudProviderAccessSetupAwsConfigList", jsii.get(self, "awsConfig"))

    @builtins.property
    @jsii.member(jsii_name="azureConfig")
    def azure_config(self) -> "CloudProviderAccessSetupAzureConfigList":
        return typing.cast("CloudProviderAccessSetupAzureConfigList", jsii.get(self, "azureConfig"))

    @builtins.property
    @jsii.member(jsii_name="createdDate")
    def created_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdDate"))

    @builtins.property
    @jsii.member(jsii_name="lastUpdatedDate")
    def last_updated_date(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastUpdatedDate"))

    @builtins.property
    @jsii.member(jsii_name="roleId")
    def role_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleId"))

    @builtins.property
    @jsii.member(jsii_name="azureConfigInput")
    def azure_config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudProviderAccessSetupAzureConfig"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CloudProviderAccessSetupAzureConfig"]]], jsii.get(self, "azureConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="providerNameInput")
    def provider_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d8677e17fc86f3d69448e3c6f09b1459b1778670fcd8c65a86366633bfacbb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b45881bf8ae0de00aab16572caa3baca4f48226c94c16234d9b11e70592b5d3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value)

    @builtins.property
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerName"))

    @provider_name.setter
    def provider_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a587301f2010ec9153e20154969d458e5ae71357be59ac183e239356bef87ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerName", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.cloudProviderAccessSetup.CloudProviderAccessSetupAwsConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class CloudProviderAccessSetupAwsConfig:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudProviderAccessSetupAwsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudProviderAccessSetupAwsConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.cloudProviderAccessSetup.CloudProviderAccessSetupAwsConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3881c48844aedc354924abee06517fb8bc549cc83e546cd0c13f4d5e5b28fc4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudProviderAccessSetupAwsConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__937f3fa02c0b857f3aca465a08f42dfcb401b4e310d73425bbba6b019e30870a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudProviderAccessSetupAwsConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eec123dd429c0a52fe8a68df15c1b3b028be4ecd2ffb2a3a860d3f62785242f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6ad445f631b440845f12161dbfd776ea2668dee02485843d5066b6a6db0d2e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0dd423f9124c83a71eda8a5dd3e2bb0f5ab9039eddc003384f62ee903c3b0f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class CloudProviderAccessSetupAwsConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.cloudProviderAccessSetup.CloudProviderAccessSetupAwsConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4637f1b206d8b1034b90cec79ca6f6d0f7737cb75c842b4af9a8ca6c106f1914)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="atlasAssumedRoleExternalId")
    def atlas_assumed_role_external_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "atlasAssumedRoleExternalId"))

    @builtins.property
    @jsii.member(jsii_name="atlasAwsAccountArn")
    def atlas_aws_account_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "atlasAwsAccountArn"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CloudProviderAccessSetupAwsConfig]:
        return typing.cast(typing.Optional[CloudProviderAccessSetupAwsConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CloudProviderAccessSetupAwsConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be260c56a694977d17de4bd1a90acdca39f4bcd2966df3e1e331789f569a41f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.cloudProviderAccessSetup.CloudProviderAccessSetupAzureConfig",
    jsii_struct_bases=[],
    name_mapping={
        "atlas_azure_app_id": "atlasAzureAppId",
        "service_principal_id": "servicePrincipalId",
        "tenant_id": "tenantId",
    },
)
class CloudProviderAccessSetupAzureConfig:
    def __init__(
        self,
        *,
        atlas_azure_app_id: builtins.str,
        service_principal_id: builtins.str,
        tenant_id: builtins.str,
    ) -> None:
        '''
        :param atlas_azure_app_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/cloud_provider_access_setup#atlas_azure_app_id CloudProviderAccessSetup#atlas_azure_app_id}.
        :param service_principal_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/cloud_provider_access_setup#service_principal_id CloudProviderAccessSetup#service_principal_id}.
        :param tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/cloud_provider_access_setup#tenant_id CloudProviderAccessSetup#tenant_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afd9fde55e576c2e6ae2b99cba025bfbb5aa3c6395cd7b3ccbb521d8cf840d7c)
            check_type(argname="argument atlas_azure_app_id", value=atlas_azure_app_id, expected_type=type_hints["atlas_azure_app_id"])
            check_type(argname="argument service_principal_id", value=service_principal_id, expected_type=type_hints["service_principal_id"])
            check_type(argname="argument tenant_id", value=tenant_id, expected_type=type_hints["tenant_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "atlas_azure_app_id": atlas_azure_app_id,
            "service_principal_id": service_principal_id,
            "tenant_id": tenant_id,
        }

    @builtins.property
    def atlas_azure_app_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/cloud_provider_access_setup#atlas_azure_app_id CloudProviderAccessSetup#atlas_azure_app_id}.'''
        result = self._values.get("atlas_azure_app_id")
        assert result is not None, "Required property 'atlas_azure_app_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_principal_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/cloud_provider_access_setup#service_principal_id CloudProviderAccessSetup#service_principal_id}.'''
        result = self._values.get("service_principal_id")
        assert result is not None, "Required property 'service_principal_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tenant_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/cloud_provider_access_setup#tenant_id CloudProviderAccessSetup#tenant_id}.'''
        result = self._values.get("tenant_id")
        assert result is not None, "Required property 'tenant_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudProviderAccessSetupAzureConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudProviderAccessSetupAzureConfigList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.cloudProviderAccessSetup.CloudProviderAccessSetupAzureConfigList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__544042ecf1ba2a3aef03b0201077a0c5e082d4e4eb0cf075951c8116c5e58553)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CloudProviderAccessSetupAzureConfigOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__585974f62f92d293aa8f19262aff7c4be2b91bfee771ff885a9462fa282c6fd9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CloudProviderAccessSetupAzureConfigOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaed73b0dd7ea9c30a5bf842a82be4ae18625fd8c29d711c400e6a4b369ec786)
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
            type_hints = typing.get_type_hints(_typecheckingstub__02c62ae3f24628f0cf2d5efac8cd7fcbfdc1b6e1d2ed541c1ea541c0f66b7412)
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
            type_hints = typing.get_type_hints(_typecheckingstub__653ff07b98881f559d2d34cc06db16a867f27f7d0a721b8d68e97d0fb1f9cbd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudProviderAccessSetupAzureConfig]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudProviderAccessSetupAzureConfig]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudProviderAccessSetupAzureConfig]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a40b929631459964d4d8de11b8dfc6c0b92a01c5d68bfc8ca3a4d8e78116505)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class CloudProviderAccessSetupAzureConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.cloudProviderAccessSetup.CloudProviderAccessSetupAzureConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f374e5d71206422f549ccb46e6c8ab2ba5dd1c8a27a705ca9afca4dad60fc561)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="atlasAzureAppIdInput")
    def atlas_azure_app_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "atlasAzureAppIdInput"))

    @builtins.property
    @jsii.member(jsii_name="servicePrincipalIdInput")
    def service_principal_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "servicePrincipalIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantIdInput")
    def tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="atlasAzureAppId")
    def atlas_azure_app_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "atlasAzureAppId"))

    @atlas_azure_app_id.setter
    def atlas_azure_app_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1ad6fee04b4c2d770c1274b00017e2aa04883ffaa23b7928b1180cca37b843f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "atlasAzureAppId", value)

    @builtins.property
    @jsii.member(jsii_name="servicePrincipalId")
    def service_principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servicePrincipalId"))

    @service_principal_id.setter
    def service_principal_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa7aef75616ec231224cd3bfb493eeb18b1257f0dbce8478f269f2ca14f97111)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servicePrincipalId", value)

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @tenant_id.setter
    def tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a56cc0d7f4ee37a98099d4b7dbb2308b138580dad662968442b9f4288da872f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudProviderAccessSetupAzureConfig]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudProviderAccessSetupAzureConfig]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudProviderAccessSetupAzureConfig]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9ca9bd0f6ff409893793ed7d23ae5c3d1c9c80e62b86d4b6e4f649546b77f5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.cloudProviderAccessSetup.CloudProviderAccessSetupConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "project_id": "projectId",
        "provider_name": "providerName",
        "azure_config": "azureConfig",
        "id": "id",
    },
)
class CloudProviderAccessSetupConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        project_id: builtins.str,
        provider_name: builtins.str,
        azure_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudProviderAccessSetupAzureConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/cloud_provider_access_setup#project_id CloudProviderAccessSetup#project_id}.
        :param provider_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/cloud_provider_access_setup#provider_name CloudProviderAccessSetup#provider_name}.
        :param azure_config: azure_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/cloud_provider_access_setup#azure_config CloudProviderAccessSetup#azure_config}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/cloud_provider_access_setup#id CloudProviderAccessSetup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8de35fd1bb336fe6a671fe5ab75d4f9964342396d5a28c09546de148da363a71)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument provider_name", value=provider_name, expected_type=type_hints["provider_name"])
            check_type(argname="argument azure_config", value=azure_config, expected_type=type_hints["azure_config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "project_id": project_id,
            "provider_name": provider_name,
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
        if azure_config is not None:
            self._values["azure_config"] = azure_config
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
    def project_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/cloud_provider_access_setup#project_id CloudProviderAccessSetup#project_id}.'''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/cloud_provider_access_setup#provider_name CloudProviderAccessSetup#provider_name}.'''
        result = self._values.get("provider_name")
        assert result is not None, "Required property 'provider_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def azure_config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudProviderAccessSetupAzureConfig]]]:
        '''azure_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/cloud_provider_access_setup#azure_config CloudProviderAccessSetup#azure_config}
        '''
        result = self._values.get("azure_config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudProviderAccessSetupAzureConfig]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/resources/cloud_provider_access_setup#id CloudProviderAccessSetup#id}.

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
        return "CloudProviderAccessSetupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CloudProviderAccessSetup",
    "CloudProviderAccessSetupAwsConfig",
    "CloudProviderAccessSetupAwsConfigList",
    "CloudProviderAccessSetupAwsConfigOutputReference",
    "CloudProviderAccessSetupAzureConfig",
    "CloudProviderAccessSetupAzureConfigList",
    "CloudProviderAccessSetupAzureConfigOutputReference",
    "CloudProviderAccessSetupConfig",
]

publication.publish()

def _typecheckingstub__01a196fe0896ed4cd98601f2fac3a209b6c84dad478b0b6bcd30b0e4bb69865d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    project_id: builtins.str,
    provider_name: builtins.str,
    azure_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudProviderAccessSetupAzureConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__8d752b256d79d92c4ae8993b044c8c6ff72da595ac013d4cfdaea353a68d8840(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudProviderAccessSetupAzureConfig, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d8677e17fc86f3d69448e3c6f09b1459b1778670fcd8c65a86366633bfacbb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b45881bf8ae0de00aab16572caa3baca4f48226c94c16234d9b11e70592b5d3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a587301f2010ec9153e20154969d458e5ae71357be59ac183e239356bef87ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3881c48844aedc354924abee06517fb8bc549cc83e546cd0c13f4d5e5b28fc4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__937f3fa02c0b857f3aca465a08f42dfcb401b4e310d73425bbba6b019e30870a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eec123dd429c0a52fe8a68df15c1b3b028be4ecd2ffb2a3a860d3f62785242f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6ad445f631b440845f12161dbfd776ea2668dee02485843d5066b6a6db0d2e4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0dd423f9124c83a71eda8a5dd3e2bb0f5ab9039eddc003384f62ee903c3b0f5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4637f1b206d8b1034b90cec79ca6f6d0f7737cb75c842b4af9a8ca6c106f1914(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be260c56a694977d17de4bd1a90acdca39f4bcd2966df3e1e331789f569a41f4(
    value: typing.Optional[CloudProviderAccessSetupAwsConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afd9fde55e576c2e6ae2b99cba025bfbb5aa3c6395cd7b3ccbb521d8cf840d7c(
    *,
    atlas_azure_app_id: builtins.str,
    service_principal_id: builtins.str,
    tenant_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__544042ecf1ba2a3aef03b0201077a0c5e082d4e4eb0cf075951c8116c5e58553(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__585974f62f92d293aa8f19262aff7c4be2b91bfee771ff885a9462fa282c6fd9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaed73b0dd7ea9c30a5bf842a82be4ae18625fd8c29d711c400e6a4b369ec786(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02c62ae3f24628f0cf2d5efac8cd7fcbfdc1b6e1d2ed541c1ea541c0f66b7412(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653ff07b98881f559d2d34cc06db16a867f27f7d0a721b8d68e97d0fb1f9cbd7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a40b929631459964d4d8de11b8dfc6c0b92a01c5d68bfc8ca3a4d8e78116505(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CloudProviderAccessSetupAzureConfig]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f374e5d71206422f549ccb46e6c8ab2ba5dd1c8a27a705ca9afca4dad60fc561(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1ad6fee04b4c2d770c1274b00017e2aa04883ffaa23b7928b1180cca37b843f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa7aef75616ec231224cd3bfb493eeb18b1257f0dbce8478f269f2ca14f97111(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a56cc0d7f4ee37a98099d4b7dbb2308b138580dad662968442b9f4288da872f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9ca9bd0f6ff409893793ed7d23ae5c3d1c9c80e62b86d4b6e4f649546b77f5a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CloudProviderAccessSetupAzureConfig]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8de35fd1bb336fe6a671fe5ab75d4f9964342396d5a28c09546de148da363a71(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    project_id: builtins.str,
    provider_name: builtins.str,
    azure_config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CloudProviderAccessSetupAzureConfig, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
