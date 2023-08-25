'''
# `databricks_grants`

Refer to the Terraform Registory for docs: [`databricks_grants`](https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants).
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


class Grants(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.grants.Grants",
):
    '''Represents a {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants databricks_grants}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        grant: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GrantsGrant", typing.Dict[builtins.str, typing.Any]]]],
        catalog: typing.Optional[builtins.str] = None,
        external_location: typing.Optional[builtins.str] = None,
        function: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        materialized_view: typing.Optional[builtins.str] = None,
        metastore: typing.Optional[builtins.str] = None,
        schema: typing.Optional[builtins.str] = None,
        share: typing.Optional[builtins.str] = None,
        storage_credential: typing.Optional[builtins.str] = None,
        table: typing.Optional[builtins.str] = None,
        view: typing.Optional[builtins.str] = None,
        volume: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants databricks_grants} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param grant: grant block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#grant Grants#grant}
        :param catalog: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#catalog Grants#catalog}.
        :param external_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#external_location Grants#external_location}.
        :param function: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#function Grants#function}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#id Grants#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param materialized_view: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#materialized_view Grants#materialized_view}.
        :param metastore: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#metastore Grants#metastore}.
        :param schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#schema Grants#schema}.
        :param share: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#share Grants#share}.
        :param storage_credential: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#storage_credential Grants#storage_credential}.
        :param table: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#table Grants#table}.
        :param view: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#view Grants#view}.
        :param volume: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#volume Grants#volume}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f40060a32ecac08d2fb3a19b9b4f717e3a6b3d3611f7ba2461113e0a033d250c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GrantsConfig(
            grant=grant,
            catalog=catalog,
            external_location=external_location,
            function=function,
            id=id,
            materialized_view=materialized_view,
            metastore=metastore,
            schema=schema,
            share=share,
            storage_credential=storage_credential,
            table=table,
            view=view,
            volume=volume,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putGrant")
    def put_grant(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GrantsGrant", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c21d067b8be670bdbf9fb8df5f65f6c03f3f677fdadf369cba0a33ac116cff5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putGrant", [value]))

    @jsii.member(jsii_name="resetCatalog")
    def reset_catalog(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCatalog", []))

    @jsii.member(jsii_name="resetExternalLocation")
    def reset_external_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalLocation", []))

    @jsii.member(jsii_name="resetFunction")
    def reset_function(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFunction", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaterializedView")
    def reset_materialized_view(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaterializedView", []))

    @jsii.member(jsii_name="resetMetastore")
    def reset_metastore(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetastore", []))

    @jsii.member(jsii_name="resetSchema")
    def reset_schema(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchema", []))

    @jsii.member(jsii_name="resetShare")
    def reset_share(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShare", []))

    @jsii.member(jsii_name="resetStorageCredential")
    def reset_storage_credential(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageCredential", []))

    @jsii.member(jsii_name="resetTable")
    def reset_table(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTable", []))

    @jsii.member(jsii_name="resetView")
    def reset_view(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetView", []))

    @jsii.member(jsii_name="resetVolume")
    def reset_volume(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVolume", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="grant")
    def grant(self) -> "GrantsGrantList":
        return typing.cast("GrantsGrantList", jsii.get(self, "grant"))

    @builtins.property
    @jsii.member(jsii_name="catalogInput")
    def catalog_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "catalogInput"))

    @builtins.property
    @jsii.member(jsii_name="externalLocationInput")
    def external_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "externalLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="functionInput")
    def function_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionInput"))

    @builtins.property
    @jsii.member(jsii_name="grantInput")
    def grant_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GrantsGrant"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GrantsGrant"]]], jsii.get(self, "grantInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="materializedViewInput")
    def materialized_view_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "materializedViewInput"))

    @builtins.property
    @jsii.member(jsii_name="metastoreInput")
    def metastore_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metastoreInput"))

    @builtins.property
    @jsii.member(jsii_name="schemaInput")
    def schema_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schemaInput"))

    @builtins.property
    @jsii.member(jsii_name="shareInput")
    def share_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "shareInput"))

    @builtins.property
    @jsii.member(jsii_name="storageCredentialInput")
    def storage_credential_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageCredentialInput"))

    @builtins.property
    @jsii.member(jsii_name="tableInput")
    def table_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tableInput"))

    @builtins.property
    @jsii.member(jsii_name="viewInput")
    def view_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "viewInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeInput")
    def volume_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeInput"))

    @builtins.property
    @jsii.member(jsii_name="catalog")
    def catalog(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "catalog"))

    @catalog.setter
    def catalog(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85776b11cf9ffc26cc81c6408ca06b4beb626441660aac6d31a66744ddb3b079)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "catalog", value)

    @builtins.property
    @jsii.member(jsii_name="externalLocation")
    def external_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "externalLocation"))

    @external_location.setter
    def external_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0fac964bdfdd115c49b295ab23bf5c589fd182ff23b88dd09d27bf347b513c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalLocation", value)

    @builtins.property
    @jsii.member(jsii_name="function")
    def function(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "function"))

    @function.setter
    def function(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f8bbb072407aa66162c5e316648ae5d3859b2a0841cc1d4dd4987bf72e67487)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "function", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22e669a6def8a525c719d0ae770827788cf641fbc6b2eafdb16f206676bef24c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="materializedView")
    def materialized_view(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "materializedView"))

    @materialized_view.setter
    def materialized_view(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e704fd80a0e16d7a16cd241fb2376213f3755a7f6e02e42a3bbf69b75034ebff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "materializedView", value)

    @builtins.property
    @jsii.member(jsii_name="metastore")
    def metastore(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metastore"))

    @metastore.setter
    def metastore(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebb27f4e88e1c218c33209f5b65ddd7be236f48b6c0b8ea9fc36f4fea008b831)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metastore", value)

    @builtins.property
    @jsii.member(jsii_name="schema")
    def schema(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "schema"))

    @schema.setter
    def schema(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6834b5507f957fb54ec0d10af73b2df8fbc2a9098fce489de17ea45f70ecfd39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schema", value)

    @builtins.property
    @jsii.member(jsii_name="share")
    def share(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "share"))

    @share.setter
    def share(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0933200934c57c585a20c117bd85cc3c05d59bc57ab8cc143d3aad4d8ab20edb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "share", value)

    @builtins.property
    @jsii.member(jsii_name="storageCredential")
    def storage_credential(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageCredential"))

    @storage_credential.setter
    def storage_credential(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43f8a0224fbf9e8e11193aa865791aa4ea712495aeacf9fc0698a4118793120f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageCredential", value)

    @builtins.property
    @jsii.member(jsii_name="table")
    def table(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "table"))

    @table.setter
    def table(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325aa32ab5d546c5b87e39854e7a0d6c2bd84b62ffbcb79dcaf3a92fa113ccea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "table", value)

    @builtins.property
    @jsii.member(jsii_name="view")
    def view(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "view"))

    @view.setter
    def view(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdef415a4c06e570f9237973051f4a91c4f7ab84cee991c8c8859da50a1342b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "view", value)

    @builtins.property
    @jsii.member(jsii_name="volume")
    def volume(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volume"))

    @volume.setter
    def volume(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fb04ed6bd50ef08d301063a8f4fa4af33d233529bc0eacd22f30ab1614b80f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volume", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.grants.GrantsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "grant": "grant",
        "catalog": "catalog",
        "external_location": "externalLocation",
        "function": "function",
        "id": "id",
        "materialized_view": "materializedView",
        "metastore": "metastore",
        "schema": "schema",
        "share": "share",
        "storage_credential": "storageCredential",
        "table": "table",
        "view": "view",
        "volume": "volume",
    },
)
class GrantsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        grant: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["GrantsGrant", typing.Dict[builtins.str, typing.Any]]]],
        catalog: typing.Optional[builtins.str] = None,
        external_location: typing.Optional[builtins.str] = None,
        function: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        materialized_view: typing.Optional[builtins.str] = None,
        metastore: typing.Optional[builtins.str] = None,
        schema: typing.Optional[builtins.str] = None,
        share: typing.Optional[builtins.str] = None,
        storage_credential: typing.Optional[builtins.str] = None,
        table: typing.Optional[builtins.str] = None,
        view: typing.Optional[builtins.str] = None,
        volume: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param grant: grant block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#grant Grants#grant}
        :param catalog: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#catalog Grants#catalog}.
        :param external_location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#external_location Grants#external_location}.
        :param function: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#function Grants#function}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#id Grants#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param materialized_view: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#materialized_view Grants#materialized_view}.
        :param metastore: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#metastore Grants#metastore}.
        :param schema: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#schema Grants#schema}.
        :param share: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#share Grants#share}.
        :param storage_credential: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#storage_credential Grants#storage_credential}.
        :param table: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#table Grants#table}.
        :param view: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#view Grants#view}.
        :param volume: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#volume Grants#volume}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2c8588ec1d93d0da3ed88d6581d53cfff74bc0c442c2ab3f99f5a6538362e1e)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument grant", value=grant, expected_type=type_hints["grant"])
            check_type(argname="argument catalog", value=catalog, expected_type=type_hints["catalog"])
            check_type(argname="argument external_location", value=external_location, expected_type=type_hints["external_location"])
            check_type(argname="argument function", value=function, expected_type=type_hints["function"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument materialized_view", value=materialized_view, expected_type=type_hints["materialized_view"])
            check_type(argname="argument metastore", value=metastore, expected_type=type_hints["metastore"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument share", value=share, expected_type=type_hints["share"])
            check_type(argname="argument storage_credential", value=storage_credential, expected_type=type_hints["storage_credential"])
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
            check_type(argname="argument view", value=view, expected_type=type_hints["view"])
            check_type(argname="argument volume", value=volume, expected_type=type_hints["volume"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "grant": grant,
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
        if catalog is not None:
            self._values["catalog"] = catalog
        if external_location is not None:
            self._values["external_location"] = external_location
        if function is not None:
            self._values["function"] = function
        if id is not None:
            self._values["id"] = id
        if materialized_view is not None:
            self._values["materialized_view"] = materialized_view
        if metastore is not None:
            self._values["metastore"] = metastore
        if schema is not None:
            self._values["schema"] = schema
        if share is not None:
            self._values["share"] = share
        if storage_credential is not None:
            self._values["storage_credential"] = storage_credential
        if table is not None:
            self._values["table"] = table
        if view is not None:
            self._values["view"] = view
        if volume is not None:
            self._values["volume"] = volume

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
    def grant(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GrantsGrant"]]:
        '''grant block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#grant Grants#grant}
        '''
        result = self._values.get("grant")
        assert result is not None, "Required property 'grant' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["GrantsGrant"]], result)

    @builtins.property
    def catalog(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#catalog Grants#catalog}.'''
        result = self._values.get("catalog")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_location(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#external_location Grants#external_location}.'''
        result = self._values.get("external_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def function(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#function Grants#function}.'''
        result = self._values.get("function")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#id Grants#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def materialized_view(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#materialized_view Grants#materialized_view}.'''
        result = self._values.get("materialized_view")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metastore(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#metastore Grants#metastore}.'''
        result = self._values.get("metastore")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#schema Grants#schema}.'''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def share(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#share Grants#share}.'''
        result = self._values.get("share")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_credential(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#storage_credential Grants#storage_credential}.'''
        result = self._values.get("storage_credential")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#table Grants#table}.'''
        result = self._values.get("table")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def view(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#view Grants#view}.'''
        result = self._values.get("view")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volume(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#volume Grants#volume}.'''
        result = self._values.get("volume")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrantsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-databricks.grants.GrantsGrant",
    jsii_struct_bases=[],
    name_mapping={"principal": "principal", "privileges": "privileges"},
)
class GrantsGrant:
    def __init__(
        self,
        *,
        principal: builtins.str,
        privileges: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param principal: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#principal Grants#principal}.
        :param privileges: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#privileges Grants#privileges}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ebf75a36d33a4bd78b4b5f727217509bdd52b113159023764c181ff456183ab)
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
            check_type(argname="argument privileges", value=privileges, expected_type=type_hints["privileges"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "principal": principal,
            "privileges": privileges,
        }

    @builtins.property
    def principal(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#principal Grants#principal}.'''
        result = self._values.get("principal")
        assert result is not None, "Required property 'principal' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def privileges(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/databricks/databricks/1.23.0/docs/resources/grants#privileges Grants#privileges}.'''
        result = self._values.get("privileges")
        assert result is not None, "Required property 'privileges' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrantsGrant(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GrantsGrantList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.grants.GrantsGrantList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a9fa2076f1a604d430499690c568c822aa7629a09733f2e41b23edf0e33c0d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "GrantsGrantOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e25ee53fc3efd17bcb31a724b0e613b8b8ae432fb897888bc088f1293b49ca26)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("GrantsGrantOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4ce4881c4cbe83400fb087eb225b493f1e5a0cd27ddbfbe6ee6c5e0231b143c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cf793b5e60ca1dc14fc53b1d26c7659eb00002f661761bc72bf88d2c2b0dbd2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bfc87554034c9097a1152baf2c109e1a2c2743a99eed3c45bc39498bcfce3e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GrantsGrant]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GrantsGrant]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GrantsGrant]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d31394ea4db5a6bf996ccf561c4b5b255e11484ce61785512ad418fe70d42fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class GrantsGrantOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-databricks.grants.GrantsGrantOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8b434ce799ba425e01a1f68b54637bb9c7d865a7f32cee35890e282d2d287f1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="principalInput")
    def principal_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalInput"))

    @builtins.property
    @jsii.member(jsii_name="privilegesInput")
    def privileges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "privilegesInput"))

    @builtins.property
    @jsii.member(jsii_name="principal")
    def principal(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principal"))

    @principal.setter
    def principal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92fe3fbe64b78b64add8c7713e70bbf9998a04d0b0d7ae390e7fb90fd67824eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "principal", value)

    @builtins.property
    @jsii.member(jsii_name="privileges")
    def privileges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "privileges"))

    @privileges.setter
    def privileges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d67c6b995c26d93f002c4995dd860d1b593a6c015e1d9e6b9976b1c26b03cbf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privileges", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GrantsGrant]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GrantsGrant]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GrantsGrant]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9401cac3986b0daa125f110ef7180370f9c017a9da0a4ca2257690c63746dce7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "Grants",
    "GrantsConfig",
    "GrantsGrant",
    "GrantsGrantList",
    "GrantsGrantOutputReference",
]

publication.publish()

def _typecheckingstub__f40060a32ecac08d2fb3a19b9b4f717e3a6b3d3611f7ba2461113e0a033d250c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    grant: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GrantsGrant, typing.Dict[builtins.str, typing.Any]]]],
    catalog: typing.Optional[builtins.str] = None,
    external_location: typing.Optional[builtins.str] = None,
    function: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    materialized_view: typing.Optional[builtins.str] = None,
    metastore: typing.Optional[builtins.str] = None,
    schema: typing.Optional[builtins.str] = None,
    share: typing.Optional[builtins.str] = None,
    storage_credential: typing.Optional[builtins.str] = None,
    table: typing.Optional[builtins.str] = None,
    view: typing.Optional[builtins.str] = None,
    volume: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__0c21d067b8be670bdbf9fb8df5f65f6c03f3f677fdadf369cba0a33ac116cff5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GrantsGrant, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85776b11cf9ffc26cc81c6408ca06b4beb626441660aac6d31a66744ddb3b079(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0fac964bdfdd115c49b295ab23bf5c589fd182ff23b88dd09d27bf347b513c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f8bbb072407aa66162c5e316648ae5d3859b2a0841cc1d4dd4987bf72e67487(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22e669a6def8a525c719d0ae770827788cf641fbc6b2eafdb16f206676bef24c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e704fd80a0e16d7a16cd241fb2376213f3755a7f6e02e42a3bbf69b75034ebff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebb27f4e88e1c218c33209f5b65ddd7be236f48b6c0b8ea9fc36f4fea008b831(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6834b5507f957fb54ec0d10af73b2df8fbc2a9098fce489de17ea45f70ecfd39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0933200934c57c585a20c117bd85cc3c05d59bc57ab8cc143d3aad4d8ab20edb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43f8a0224fbf9e8e11193aa865791aa4ea712495aeacf9fc0698a4118793120f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325aa32ab5d546c5b87e39854e7a0d6c2bd84b62ffbcb79dcaf3a92fa113ccea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdef415a4c06e570f9237973051f4a91c4f7ab84cee991c8c8859da50a1342b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb04ed6bd50ef08d301063a8f4fa4af33d233529bc0eacd22f30ab1614b80f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2c8588ec1d93d0da3ed88d6581d53cfff74bc0c442c2ab3f99f5a6538362e1e(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    grant: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[GrantsGrant, typing.Dict[builtins.str, typing.Any]]]],
    catalog: typing.Optional[builtins.str] = None,
    external_location: typing.Optional[builtins.str] = None,
    function: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    materialized_view: typing.Optional[builtins.str] = None,
    metastore: typing.Optional[builtins.str] = None,
    schema: typing.Optional[builtins.str] = None,
    share: typing.Optional[builtins.str] = None,
    storage_credential: typing.Optional[builtins.str] = None,
    table: typing.Optional[builtins.str] = None,
    view: typing.Optional[builtins.str] = None,
    volume: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ebf75a36d33a4bd78b4b5f727217509bdd52b113159023764c181ff456183ab(
    *,
    principal: builtins.str,
    privileges: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a9fa2076f1a604d430499690c568c822aa7629a09733f2e41b23edf0e33c0d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25ee53fc3efd17bcb31a724b0e613b8b8ae432fb897888bc088f1293b49ca26(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4ce4881c4cbe83400fb087eb225b493f1e5a0cd27ddbfbe6ee6c5e0231b143c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cf793b5e60ca1dc14fc53b1d26c7659eb00002f661761bc72bf88d2c2b0dbd2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bfc87554034c9097a1152baf2c109e1a2c2743a99eed3c45bc39498bcfce3e5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d31394ea4db5a6bf996ccf561c4b5b255e11484ce61785512ad418fe70d42fd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[GrantsGrant]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8b434ce799ba425e01a1f68b54637bb9c7d865a7f32cee35890e282d2d287f1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92fe3fbe64b78b64add8c7713e70bbf9998a04d0b0d7ae390e7fb90fd67824eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d67c6b995c26d93f002c4995dd860d1b593a6c015e1d9e6b9976b1c26b03cbf6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9401cac3986b0daa125f110ef7180370f9c017a9da0a4ca2257690c63746dce7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, GrantsGrant]],
) -> None:
    """Type checking stubs"""
    pass
