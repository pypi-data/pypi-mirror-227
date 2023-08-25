'''
# `data_mongodbatlas_search_index`

Refer to the Terraform Registory for docs: [`data_mongodbatlas_search_index`](https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index).
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


class DataMongodbatlasSearchIndex(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasSearchIndex.DataMongodbatlasSearchIndex",
):
    '''Represents a {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index mongodbatlas_search_index}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cluster_name: builtins.str,
        index_id: builtins.str,
        project_id: builtins.str,
        analyzer: typing.Optional[builtins.str] = None,
        analyzers: typing.Optional[builtins.str] = None,
        collection_name: typing.Optional[builtins.str] = None,
        database: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        mappings_dynamic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mappings_fields: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        search_analyzer: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index mongodbatlas_search_index} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cluster_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#cluster_name DataMongodbatlasSearchIndex#cluster_name}.
        :param index_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#index_id DataMongodbatlasSearchIndex#index_id}.
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#project_id DataMongodbatlasSearchIndex#project_id}.
        :param analyzer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#analyzer DataMongodbatlasSearchIndex#analyzer}.
        :param analyzers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#analyzers DataMongodbatlasSearchIndex#analyzers}.
        :param collection_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#collection_name DataMongodbatlasSearchIndex#collection_name}.
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#database DataMongodbatlasSearchIndex#database}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#id DataMongodbatlasSearchIndex#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mappings_dynamic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#mappings_dynamic DataMongodbatlasSearchIndex#mappings_dynamic}.
        :param mappings_fields: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#mappings_fields DataMongodbatlasSearchIndex#mappings_fields}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#name DataMongodbatlasSearchIndex#name}.
        :param search_analyzer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#search_analyzer DataMongodbatlasSearchIndex#search_analyzer}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#status DataMongodbatlasSearchIndex#status}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c65d7a5c6ef4490925ee1dd6170b9c56d313ec32f83f145ef00d63c9dd85f3a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataMongodbatlasSearchIndexConfig(
            cluster_name=cluster_name,
            index_id=index_id,
            project_id=project_id,
            analyzer=analyzer,
            analyzers=analyzers,
            collection_name=collection_name,
            database=database,
            id=id,
            mappings_dynamic=mappings_dynamic,
            mappings_fields=mappings_fields,
            name=name,
            search_analyzer=search_analyzer,
            status=status,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetAnalyzer")
    def reset_analyzer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnalyzer", []))

    @jsii.member(jsii_name="resetAnalyzers")
    def reset_analyzers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnalyzers", []))

    @jsii.member(jsii_name="resetCollectionName")
    def reset_collection_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCollectionName", []))

    @jsii.member(jsii_name="resetDatabase")
    def reset_database(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabase", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMappingsDynamic")
    def reset_mappings_dynamic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMappingsDynamic", []))

    @jsii.member(jsii_name="resetMappingsFields")
    def reset_mappings_fields(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMappingsFields", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetSearchAnalyzer")
    def reset_search_analyzer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSearchAnalyzer", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="synonyms")
    def synonyms(self) -> "DataMongodbatlasSearchIndexSynonymsList":
        return typing.cast("DataMongodbatlasSearchIndexSynonymsList", jsii.get(self, "synonyms"))

    @builtins.property
    @jsii.member(jsii_name="analyzerInput")
    def analyzer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "analyzerInput"))

    @builtins.property
    @jsii.member(jsii_name="analyzersInput")
    def analyzers_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "analyzersInput"))

    @builtins.property
    @jsii.member(jsii_name="clusterNameInput")
    def cluster_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clusterNameInput"))

    @builtins.property
    @jsii.member(jsii_name="collectionNameInput")
    def collection_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "collectionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="databaseInput")
    def database_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "databaseInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="indexIdInput")
    def index_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "indexIdInput"))

    @builtins.property
    @jsii.member(jsii_name="mappingsDynamicInput")
    def mappings_dynamic_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mappingsDynamicInput"))

    @builtins.property
    @jsii.member(jsii_name="mappingsFieldsInput")
    def mappings_fields_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mappingsFieldsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="searchAnalyzerInput")
    def search_analyzer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "searchAnalyzerInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="analyzer")
    def analyzer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "analyzer"))

    @analyzer.setter
    def analyzer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9e0a67b6335563b611466fbcace56fb530b72c837e70a5b1fdfa00fdc87744b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "analyzer", value)

    @builtins.property
    @jsii.member(jsii_name="analyzers")
    def analyzers(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "analyzers"))

    @analyzers.setter
    def analyzers(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1a60d8cc37b7d7af4ddb334f2af6474e027c44da2183f4c12761944a31c3545)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "analyzers", value)

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterName"))

    @cluster_name.setter
    def cluster_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e00aeaf0bc4218f94c898d9977d351d45a240ac80b837a9292021192ed23857)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clusterName", value)

    @builtins.property
    @jsii.member(jsii_name="collectionName")
    def collection_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "collectionName"))

    @collection_name.setter
    def collection_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5593e22dd9031824ff10dc9933036bc343e87fd94c31f58dda36808648c467be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collectionName", value)

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "database"))

    @database.setter
    def database(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a3329cc2453740f9bf12ca4508f91e781f44a000d239ecbf2245505ef0e1d7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "database", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4b1d13a65533aeef975bb0e54ae1d97da561d00b9d9f48337e75ade9798322d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="indexId")
    def index_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "indexId"))

    @index_id.setter
    def index_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6bb43b4ae8e76d09b2eb6186eaef9ee816dd5bc885e7d54fcaa5411b431fb63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "indexId", value)

    @builtins.property
    @jsii.member(jsii_name="mappingsDynamic")
    def mappings_dynamic(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mappingsDynamic"))

    @mappings_dynamic.setter
    def mappings_dynamic(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__564e7925d2abd9a72fc219181e84833bcc16341bc26ec6d7b9bc6ee7bb8b274c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mappingsDynamic", value)

    @builtins.property
    @jsii.member(jsii_name="mappingsFields")
    def mappings_fields(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mappingsFields"))

    @mappings_fields.setter
    def mappings_fields(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__350ebc11b6aeecf357ee3f56e4e1e65c3cf198cf94be8e3a17d90b071b27dd4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mappingsFields", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b534341df1bc3b4122958e109560c0db041b57831923e4449b430c89089c0340)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acd3cc15b1be0fdc13a877a029a4f0653cdbf8b62cd6a24e783e255424c2db2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value)

    @builtins.property
    @jsii.member(jsii_name="searchAnalyzer")
    def search_analyzer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "searchAnalyzer"))

    @search_analyzer.setter
    def search_analyzer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28b8b813f29c157f6f72171c45047f7d14970595ddd5ee0738e933552a36e7d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "searchAnalyzer", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c5ca05e4d8d93ff2a12a25a4c6ca0f348532a0dd5c4ccb2f4bba4816d9e39b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasSearchIndex.DataMongodbatlasSearchIndexConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cluster_name": "clusterName",
        "index_id": "indexId",
        "project_id": "projectId",
        "analyzer": "analyzer",
        "analyzers": "analyzers",
        "collection_name": "collectionName",
        "database": "database",
        "id": "id",
        "mappings_dynamic": "mappingsDynamic",
        "mappings_fields": "mappingsFields",
        "name": "name",
        "search_analyzer": "searchAnalyzer",
        "status": "status",
    },
)
class DataMongodbatlasSearchIndexConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cluster_name: builtins.str,
        index_id: builtins.str,
        project_id: builtins.str,
        analyzer: typing.Optional[builtins.str] = None,
        analyzers: typing.Optional[builtins.str] = None,
        collection_name: typing.Optional[builtins.str] = None,
        database: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        mappings_dynamic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mappings_fields: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        search_analyzer: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cluster_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#cluster_name DataMongodbatlasSearchIndex#cluster_name}.
        :param index_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#index_id DataMongodbatlasSearchIndex#index_id}.
        :param project_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#project_id DataMongodbatlasSearchIndex#project_id}.
        :param analyzer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#analyzer DataMongodbatlasSearchIndex#analyzer}.
        :param analyzers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#analyzers DataMongodbatlasSearchIndex#analyzers}.
        :param collection_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#collection_name DataMongodbatlasSearchIndex#collection_name}.
        :param database: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#database DataMongodbatlasSearchIndex#database}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#id DataMongodbatlasSearchIndex#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mappings_dynamic: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#mappings_dynamic DataMongodbatlasSearchIndex#mappings_dynamic}.
        :param mappings_fields: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#mappings_fields DataMongodbatlasSearchIndex#mappings_fields}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#name DataMongodbatlasSearchIndex#name}.
        :param search_analyzer: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#search_analyzer DataMongodbatlasSearchIndex#search_analyzer}.
        :param status: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#status DataMongodbatlasSearchIndex#status}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f81d5fb433912d3736cb28b52993263899574f82b61311d6d5dfdc9b858aa78)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument index_id", value=index_id, expected_type=type_hints["index_id"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument analyzer", value=analyzer, expected_type=type_hints["analyzer"])
            check_type(argname="argument analyzers", value=analyzers, expected_type=type_hints["analyzers"])
            check_type(argname="argument collection_name", value=collection_name, expected_type=type_hints["collection_name"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument mappings_dynamic", value=mappings_dynamic, expected_type=type_hints["mappings_dynamic"])
            check_type(argname="argument mappings_fields", value=mappings_fields, expected_type=type_hints["mappings_fields"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument search_analyzer", value=search_analyzer, expected_type=type_hints["search_analyzer"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster_name": cluster_name,
            "index_id": index_id,
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
        if analyzer is not None:
            self._values["analyzer"] = analyzer
        if analyzers is not None:
            self._values["analyzers"] = analyzers
        if collection_name is not None:
            self._values["collection_name"] = collection_name
        if database is not None:
            self._values["database"] = database
        if id is not None:
            self._values["id"] = id
        if mappings_dynamic is not None:
            self._values["mappings_dynamic"] = mappings_dynamic
        if mappings_fields is not None:
            self._values["mappings_fields"] = mappings_fields
        if name is not None:
            self._values["name"] = name
        if search_analyzer is not None:
            self._values["search_analyzer"] = search_analyzer
        if status is not None:
            self._values["status"] = status

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
    def cluster_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#cluster_name DataMongodbatlasSearchIndex#cluster_name}.'''
        result = self._values.get("cluster_name")
        assert result is not None, "Required property 'cluster_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def index_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#index_id DataMongodbatlasSearchIndex#index_id}.'''
        result = self._values.get("index_id")
        assert result is not None, "Required property 'index_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#project_id DataMongodbatlasSearchIndex#project_id}.'''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def analyzer(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#analyzer DataMongodbatlasSearchIndex#analyzer}.'''
        result = self._values.get("analyzer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def analyzers(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#analyzers DataMongodbatlasSearchIndex#analyzers}.'''
        result = self._values.get("analyzers")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def collection_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#collection_name DataMongodbatlasSearchIndex#collection_name}.'''
        result = self._values.get("collection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def database(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#database DataMongodbatlasSearchIndex#database}.'''
        result = self._values.get("database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#id DataMongodbatlasSearchIndex#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mappings_dynamic(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#mappings_dynamic DataMongodbatlasSearchIndex#mappings_dynamic}.'''
        result = self._values.get("mappings_dynamic")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def mappings_fields(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#mappings_fields DataMongodbatlasSearchIndex#mappings_fields}.'''
        result = self._values.get("mappings_fields")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#name DataMongodbatlasSearchIndex#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def search_analyzer(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#search_analyzer DataMongodbatlasSearchIndex#search_analyzer}.'''
        result = self._values.get("search_analyzer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/mongodb/mongodbatlas/1.11.0/docs/data-sources/search_index#status DataMongodbatlasSearchIndex#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataMongodbatlasSearchIndexConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasSearchIndex.DataMongodbatlasSearchIndexSynonyms",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataMongodbatlasSearchIndexSynonyms:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataMongodbatlasSearchIndexSynonyms(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataMongodbatlasSearchIndexSynonymsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasSearchIndex.DataMongodbatlasSearchIndexSynonymsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a75a5e1fcbc7ea1c04cdf5f33e6e26a277765e255186323e90c15d901568a75)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataMongodbatlasSearchIndexSynonymsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94135d2742c37ac13e54d534da9dc3013f03e85b3b8c57688e800a79f6e00d01)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataMongodbatlasSearchIndexSynonymsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e14465ebdd2531d9ae644cf1e421c6dcabb01240284b3abf12a4d47eb3d98a1f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a5238ada888c33618da1ea69a3619b5fb058d89d1732875ec77d43ae27b5230)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef35d04da93338a08a362e311c4ec4baed2358772c8ba95d5bd9fb0d21274cb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class DataMongodbatlasSearchIndexSynonymsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-mongodbatlas.dataMongodbatlasSearchIndex.DataMongodbatlasSearchIndexSynonymsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28edaea7dd4b16207c1d8515dd75b9841d037c9c6b299247f94241e9bd82ae9f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="analyzer")
    def analyzer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "analyzer"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="sourceCollection")
    def source_collection(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceCollection"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataMongodbatlasSearchIndexSynonyms]:
        return typing.cast(typing.Optional[DataMongodbatlasSearchIndexSynonyms], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataMongodbatlasSearchIndexSynonyms],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__957ba692a46d9e273898bf18c22295ea92d2f76c226cb06f92676a5a8547613f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataMongodbatlasSearchIndex",
    "DataMongodbatlasSearchIndexConfig",
    "DataMongodbatlasSearchIndexSynonyms",
    "DataMongodbatlasSearchIndexSynonymsList",
    "DataMongodbatlasSearchIndexSynonymsOutputReference",
]

publication.publish()

def _typecheckingstub__9c65d7a5c6ef4490925ee1dd6170b9c56d313ec32f83f145ef00d63c9dd85f3a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cluster_name: builtins.str,
    index_id: builtins.str,
    project_id: builtins.str,
    analyzer: typing.Optional[builtins.str] = None,
    analyzers: typing.Optional[builtins.str] = None,
    collection_name: typing.Optional[builtins.str] = None,
    database: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    mappings_dynamic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    mappings_fields: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    search_analyzer: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__e9e0a67b6335563b611466fbcace56fb530b72c837e70a5b1fdfa00fdc87744b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1a60d8cc37b7d7af4ddb334f2af6474e027c44da2183f4c12761944a31c3545(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e00aeaf0bc4218f94c898d9977d351d45a240ac80b837a9292021192ed23857(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5593e22dd9031824ff10dc9933036bc343e87fd94c31f58dda36808648c467be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a3329cc2453740f9bf12ca4508f91e781f44a000d239ecbf2245505ef0e1d7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4b1d13a65533aeef975bb0e54ae1d97da561d00b9d9f48337e75ade9798322d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6bb43b4ae8e76d09b2eb6186eaef9ee816dd5bc885e7d54fcaa5411b431fb63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__564e7925d2abd9a72fc219181e84833bcc16341bc26ec6d7b9bc6ee7bb8b274c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__350ebc11b6aeecf357ee3f56e4e1e65c3cf198cf94be8e3a17d90b071b27dd4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b534341df1bc3b4122958e109560c0db041b57831923e4449b430c89089c0340(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acd3cc15b1be0fdc13a877a029a4f0653cdbf8b62cd6a24e783e255424c2db2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b8b813f29c157f6f72171c45047f7d14970595ddd5ee0738e933552a36e7d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c5ca05e4d8d93ff2a12a25a4c6ca0f348532a0dd5c4ccb2f4bba4816d9e39b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f81d5fb433912d3736cb28b52993263899574f82b61311d6d5dfdc9b858aa78(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cluster_name: builtins.str,
    index_id: builtins.str,
    project_id: builtins.str,
    analyzer: typing.Optional[builtins.str] = None,
    analyzers: typing.Optional[builtins.str] = None,
    collection_name: typing.Optional[builtins.str] = None,
    database: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    mappings_dynamic: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    mappings_fields: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    search_analyzer: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a75a5e1fcbc7ea1c04cdf5f33e6e26a277765e255186323e90c15d901568a75(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94135d2742c37ac13e54d534da9dc3013f03e85b3b8c57688e800a79f6e00d01(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e14465ebdd2531d9ae644cf1e421c6dcabb01240284b3abf12a4d47eb3d98a1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a5238ada888c33618da1ea69a3619b5fb058d89d1732875ec77d43ae27b5230(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef35d04da93338a08a362e311c4ec4baed2358772c8ba95d5bd9fb0d21274cb5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28edaea7dd4b16207c1d8515dd75b9841d037c9c6b299247f94241e9bd82ae9f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__957ba692a46d9e273898bf18c22295ea92d2f76c226cb06f92676a5a8547613f(
    value: typing.Optional[DataMongodbatlasSearchIndexSynonyms],
) -> None:
    """Type checking stubs"""
    pass
