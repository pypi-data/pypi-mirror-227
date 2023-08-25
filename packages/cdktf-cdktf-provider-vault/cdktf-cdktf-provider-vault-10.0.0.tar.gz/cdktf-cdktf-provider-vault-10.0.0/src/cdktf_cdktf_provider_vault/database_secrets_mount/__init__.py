'''
# `vault_database_secrets_mount`

Refer to the Terraform Registory for docs: [`vault_database_secrets_mount`](https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount).
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


class DatabaseSecretsMount(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMount",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount vault_database_secrets_mount}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        path: builtins.str,
        allowed_managed_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        audit_non_hmac_request_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        audit_non_hmac_response_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        cassandra: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountCassandra", typing.Dict[builtins.str, typing.Any]]]]] = None,
        couchbase: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountCouchbase", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_lease_ttl_seconds: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        elasticsearch: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountElasticsearch", typing.Dict[builtins.str, typing.Any]]]]] = None,
        external_entropy_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hana: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountHana", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        influxdb: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountInfluxdb", typing.Dict[builtins.str, typing.Any]]]]] = None,
        local: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_lease_ttl_seconds: typing.Optional[jsii.Number] = None,
        mongodb: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountMongodb", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mongodbatlas: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountMongodbatlas", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mssql: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountMssql", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mysql: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountMysql", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mysql_aurora: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountMysqlAurora", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mysql_legacy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountMysqlLegacy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mysql_rds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountMysqlRds", typing.Dict[builtins.str, typing.Any]]]]] = None,
        namespace: typing.Optional[builtins.str] = None,
        options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        oracle: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountOracle", typing.Dict[builtins.str, typing.Any]]]]] = None,
        postgresql: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountPostgresql", typing.Dict[builtins.str, typing.Any]]]]] = None,
        redis: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountRedis", typing.Dict[builtins.str, typing.Any]]]]] = None,
        redis_elasticache: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountRedisElasticache", typing.Dict[builtins.str, typing.Any]]]]] = None,
        redshift: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountRedshift", typing.Dict[builtins.str, typing.Any]]]]] = None,
        seal_wrap: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        snowflake: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountSnowflake", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount vault_database_secrets_mount} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param path: Where the secret backend will be mounted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#path DatabaseSecretsMount#path}
        :param allowed_managed_keys: List of managed key registry entry names that the mount in question is allowed to access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_managed_keys DatabaseSecretsMount#allowed_managed_keys}
        :param audit_non_hmac_request_keys: Specifies the list of keys that will not be HMAC'd by audit devices in the request data object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#audit_non_hmac_request_keys DatabaseSecretsMount#audit_non_hmac_request_keys}
        :param audit_non_hmac_response_keys: Specifies the list of keys that will not be HMAC'd by audit devices in the response data object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#audit_non_hmac_response_keys DatabaseSecretsMount#audit_non_hmac_response_keys}
        :param cassandra: cassandra block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#cassandra DatabaseSecretsMount#cassandra}
        :param couchbase: couchbase block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#couchbase DatabaseSecretsMount#couchbase}
        :param default_lease_ttl_seconds: Default lease duration for tokens and secrets in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#default_lease_ttl_seconds DatabaseSecretsMount#default_lease_ttl_seconds}
        :param description: Human-friendly description of the mount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#description DatabaseSecretsMount#description}
        :param elasticsearch: elasticsearch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#elasticsearch DatabaseSecretsMount#elasticsearch}
        :param external_entropy_access: Enable the secrets engine to access Vault's external entropy source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#external_entropy_access DatabaseSecretsMount#external_entropy_access}
        :param hana: hana block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#hana DatabaseSecretsMount#hana}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#id DatabaseSecretsMount#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param influxdb: influxdb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#influxdb DatabaseSecretsMount#influxdb}
        :param local: Local mount flag that can be explicitly set to true to enforce local mount in HA environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#local DatabaseSecretsMount#local}
        :param max_lease_ttl_seconds: Maximum possible lease duration for tokens and secrets in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_lease_ttl_seconds DatabaseSecretsMount#max_lease_ttl_seconds}
        :param mongodb: mongodb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#mongodb DatabaseSecretsMount#mongodb}
        :param mongodbatlas: mongodbatlas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#mongodbatlas DatabaseSecretsMount#mongodbatlas}
        :param mssql: mssql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#mssql DatabaseSecretsMount#mssql}
        :param mysql: mysql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#mysql DatabaseSecretsMount#mysql}
        :param mysql_aurora: mysql_aurora block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#mysql_aurora DatabaseSecretsMount#mysql_aurora}
        :param mysql_legacy: mysql_legacy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#mysql_legacy DatabaseSecretsMount#mysql_legacy}
        :param mysql_rds: mysql_rds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#mysql_rds DatabaseSecretsMount#mysql_rds}
        :param namespace: Target namespace. (requires Enterprise). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#namespace DatabaseSecretsMount#namespace}
        :param options: Specifies mount type specific options that are passed to the backend. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#options DatabaseSecretsMount#options}
        :param oracle: oracle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#oracle DatabaseSecretsMount#oracle}
        :param postgresql: postgresql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#postgresql DatabaseSecretsMount#postgresql}
        :param redis: redis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#redis DatabaseSecretsMount#redis}
        :param redis_elasticache: redis_elasticache block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#redis_elasticache DatabaseSecretsMount#redis_elasticache}
        :param redshift: redshift block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#redshift DatabaseSecretsMount#redshift}
        :param seal_wrap: Enable seal wrapping for the mount, causing values stored by the mount to be wrapped by the seal's encryption capability. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#seal_wrap DatabaseSecretsMount#seal_wrap}
        :param snowflake: snowflake block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#snowflake DatabaseSecretsMount#snowflake}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac8f62cbd006ac2878530cb2f917cded0ae67aa667f7ca0cc17e2d8ab8d8ef03)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DatabaseSecretsMountConfig(
            path=path,
            allowed_managed_keys=allowed_managed_keys,
            audit_non_hmac_request_keys=audit_non_hmac_request_keys,
            audit_non_hmac_response_keys=audit_non_hmac_response_keys,
            cassandra=cassandra,
            couchbase=couchbase,
            default_lease_ttl_seconds=default_lease_ttl_seconds,
            description=description,
            elasticsearch=elasticsearch,
            external_entropy_access=external_entropy_access,
            hana=hana,
            id=id,
            influxdb=influxdb,
            local=local,
            max_lease_ttl_seconds=max_lease_ttl_seconds,
            mongodb=mongodb,
            mongodbatlas=mongodbatlas,
            mssql=mssql,
            mysql=mysql,
            mysql_aurora=mysql_aurora,
            mysql_legacy=mysql_legacy,
            mysql_rds=mysql_rds,
            namespace=namespace,
            options=options,
            oracle=oracle,
            postgresql=postgresql,
            redis=redis,
            redis_elasticache=redis_elasticache,
            redshift=redshift,
            seal_wrap=seal_wrap,
            snowflake=snowflake,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putCassandra")
    def put_cassandra(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountCassandra", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35437877e9f9e1bfe0a8c81c67337c8265a1ab0a6e6462067a6b376087f463b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCassandra", [value]))

    @jsii.member(jsii_name="putCouchbase")
    def put_couchbase(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountCouchbase", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e04cad43ad1e2016b0b8e72fb21259fa3cc4ac867dfffcd0e8da76924d550b39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCouchbase", [value]))

    @jsii.member(jsii_name="putElasticsearch")
    def put_elasticsearch(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountElasticsearch", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae2ffcbe755867ca7aba40c068e2a96c2c0fe9f02a5e266fbea50b8c3f91d767)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putElasticsearch", [value]))

    @jsii.member(jsii_name="putHana")
    def put_hana(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountHana", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd960c87cff028125fc432d38ec1c6c70524323a1f4d9818acc430158ffff876)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHana", [value]))

    @jsii.member(jsii_name="putInfluxdb")
    def put_influxdb(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountInfluxdb", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d960c9fcf95941970bb01cefb0115ea6da4b9e9a1ae565aee5bdde0b7a72db30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInfluxdb", [value]))

    @jsii.member(jsii_name="putMongodb")
    def put_mongodb(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountMongodb", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd82b7062e0cfef43cb591382826d6d0e946004467c6644e14fc5d2b30815767)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMongodb", [value]))

    @jsii.member(jsii_name="putMongodbatlas")
    def put_mongodbatlas(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountMongodbatlas", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bc789f2500e3bde017fa0fa961ec73e8a9f346686c1e55133f28692215dc7fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMongodbatlas", [value]))

    @jsii.member(jsii_name="putMssql")
    def put_mssql(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountMssql", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a77e037b4b32699d4f8f89f91c8f1cb794f0381cdb90c3075dda6186ad078546)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMssql", [value]))

    @jsii.member(jsii_name="putMysql")
    def put_mysql(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountMysql", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e6d2fb2d8857883722f1368c78e7c7b3e323c1d1c0c9f8421ab30e1a1de5d63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMysql", [value]))

    @jsii.member(jsii_name="putMysqlAurora")
    def put_mysql_aurora(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountMysqlAurora", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__806d0361fb5f220bb806976857a5e12d6c255d124755f8038b7e0e56be68a184)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMysqlAurora", [value]))

    @jsii.member(jsii_name="putMysqlLegacy")
    def put_mysql_legacy(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountMysqlLegacy", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5df8a73042d21375ba940d4cc69deed09bec7c8546ab93271b61719d7704675)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMysqlLegacy", [value]))

    @jsii.member(jsii_name="putMysqlRds")
    def put_mysql_rds(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountMysqlRds", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29f0489ae0700063ee1dfd357c0f571b779ccb6a8c3c4e6d9fa53d54ee36a37b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMysqlRds", [value]))

    @jsii.member(jsii_name="putOracle")
    def put_oracle(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountOracle", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fedef04bc561e841934a42b3b8a664a3379f343ba6fa213bab59b7bac26893b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putOracle", [value]))

    @jsii.member(jsii_name="putPostgresql")
    def put_postgresql(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountPostgresql", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c07124bc8298bc07cc53ce0d7a167eb5be31b26ee530e055a7b3b0f93856ce7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPostgresql", [value]))

    @jsii.member(jsii_name="putRedis")
    def put_redis(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountRedis", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dd109a922cdcb189aff490613d3516f5355a370e1aea01e231dc786750d41d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRedis", [value]))

    @jsii.member(jsii_name="putRedisElasticache")
    def put_redis_elasticache(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountRedisElasticache", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8298f39af04e163ece85c640509417705ea1510c8e5577d5c1ff2f2642453f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRedisElasticache", [value]))

    @jsii.member(jsii_name="putRedshift")
    def put_redshift(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountRedshift", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60a159973f513373d3335d5f4300f29562f50d3185c75a2c9e989175ce72a01b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRedshift", [value]))

    @jsii.member(jsii_name="putSnowflake")
    def put_snowflake(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountSnowflake", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cda27a3c69ecbdf0e425e853e9bfc3b3bc7bbb772788d1946c83976adcae84e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSnowflake", [value]))

    @jsii.member(jsii_name="resetAllowedManagedKeys")
    def reset_allowed_managed_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedManagedKeys", []))

    @jsii.member(jsii_name="resetAuditNonHmacRequestKeys")
    def reset_audit_non_hmac_request_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuditNonHmacRequestKeys", []))

    @jsii.member(jsii_name="resetAuditNonHmacResponseKeys")
    def reset_audit_non_hmac_response_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuditNonHmacResponseKeys", []))

    @jsii.member(jsii_name="resetCassandra")
    def reset_cassandra(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCassandra", []))

    @jsii.member(jsii_name="resetCouchbase")
    def reset_couchbase(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCouchbase", []))

    @jsii.member(jsii_name="resetDefaultLeaseTtlSeconds")
    def reset_default_lease_ttl_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultLeaseTtlSeconds", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetElasticsearch")
    def reset_elasticsearch(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticsearch", []))

    @jsii.member(jsii_name="resetExternalEntropyAccess")
    def reset_external_entropy_access(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExternalEntropyAccess", []))

    @jsii.member(jsii_name="resetHana")
    def reset_hana(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHana", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInfluxdb")
    def reset_influxdb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInfluxdb", []))

    @jsii.member(jsii_name="resetLocal")
    def reset_local(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocal", []))

    @jsii.member(jsii_name="resetMaxLeaseTtlSeconds")
    def reset_max_lease_ttl_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxLeaseTtlSeconds", []))

    @jsii.member(jsii_name="resetMongodb")
    def reset_mongodb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMongodb", []))

    @jsii.member(jsii_name="resetMongodbatlas")
    def reset_mongodbatlas(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMongodbatlas", []))

    @jsii.member(jsii_name="resetMssql")
    def reset_mssql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMssql", []))

    @jsii.member(jsii_name="resetMysql")
    def reset_mysql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMysql", []))

    @jsii.member(jsii_name="resetMysqlAurora")
    def reset_mysql_aurora(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMysqlAurora", []))

    @jsii.member(jsii_name="resetMysqlLegacy")
    def reset_mysql_legacy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMysqlLegacy", []))

    @jsii.member(jsii_name="resetMysqlRds")
    def reset_mysql_rds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMysqlRds", []))

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @jsii.member(jsii_name="resetOptions")
    def reset_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOptions", []))

    @jsii.member(jsii_name="resetOracle")
    def reset_oracle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOracle", []))

    @jsii.member(jsii_name="resetPostgresql")
    def reset_postgresql(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPostgresql", []))

    @jsii.member(jsii_name="resetRedis")
    def reset_redis(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedis", []))

    @jsii.member(jsii_name="resetRedisElasticache")
    def reset_redis_elasticache(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedisElasticache", []))

    @jsii.member(jsii_name="resetRedshift")
    def reset_redshift(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRedshift", []))

    @jsii.member(jsii_name="resetSealWrap")
    def reset_seal_wrap(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSealWrap", []))

    @jsii.member(jsii_name="resetSnowflake")
    def reset_snowflake(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSnowflake", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="accessor")
    def accessor(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessor"))

    @builtins.property
    @jsii.member(jsii_name="cassandra")
    def cassandra(self) -> "DatabaseSecretsMountCassandraList":
        return typing.cast("DatabaseSecretsMountCassandraList", jsii.get(self, "cassandra"))

    @builtins.property
    @jsii.member(jsii_name="couchbase")
    def couchbase(self) -> "DatabaseSecretsMountCouchbaseList":
        return typing.cast("DatabaseSecretsMountCouchbaseList", jsii.get(self, "couchbase"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearch")
    def elasticsearch(self) -> "DatabaseSecretsMountElasticsearchList":
        return typing.cast("DatabaseSecretsMountElasticsearchList", jsii.get(self, "elasticsearch"))

    @builtins.property
    @jsii.member(jsii_name="engineCount")
    def engine_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "engineCount"))

    @builtins.property
    @jsii.member(jsii_name="hana")
    def hana(self) -> "DatabaseSecretsMountHanaList":
        return typing.cast("DatabaseSecretsMountHanaList", jsii.get(self, "hana"))

    @builtins.property
    @jsii.member(jsii_name="influxdb")
    def influxdb(self) -> "DatabaseSecretsMountInfluxdbList":
        return typing.cast("DatabaseSecretsMountInfluxdbList", jsii.get(self, "influxdb"))

    @builtins.property
    @jsii.member(jsii_name="mongodb")
    def mongodb(self) -> "DatabaseSecretsMountMongodbList":
        return typing.cast("DatabaseSecretsMountMongodbList", jsii.get(self, "mongodb"))

    @builtins.property
    @jsii.member(jsii_name="mongodbatlas")
    def mongodbatlas(self) -> "DatabaseSecretsMountMongodbatlasList":
        return typing.cast("DatabaseSecretsMountMongodbatlasList", jsii.get(self, "mongodbatlas"))

    @builtins.property
    @jsii.member(jsii_name="mssql")
    def mssql(self) -> "DatabaseSecretsMountMssqlList":
        return typing.cast("DatabaseSecretsMountMssqlList", jsii.get(self, "mssql"))

    @builtins.property
    @jsii.member(jsii_name="mysql")
    def mysql(self) -> "DatabaseSecretsMountMysqlList":
        return typing.cast("DatabaseSecretsMountMysqlList", jsii.get(self, "mysql"))

    @builtins.property
    @jsii.member(jsii_name="mysqlAurora")
    def mysql_aurora(self) -> "DatabaseSecretsMountMysqlAuroraList":
        return typing.cast("DatabaseSecretsMountMysqlAuroraList", jsii.get(self, "mysqlAurora"))

    @builtins.property
    @jsii.member(jsii_name="mysqlLegacy")
    def mysql_legacy(self) -> "DatabaseSecretsMountMysqlLegacyList":
        return typing.cast("DatabaseSecretsMountMysqlLegacyList", jsii.get(self, "mysqlLegacy"))

    @builtins.property
    @jsii.member(jsii_name="mysqlRds")
    def mysql_rds(self) -> "DatabaseSecretsMountMysqlRdsList":
        return typing.cast("DatabaseSecretsMountMysqlRdsList", jsii.get(self, "mysqlRds"))

    @builtins.property
    @jsii.member(jsii_name="oracle")
    def oracle(self) -> "DatabaseSecretsMountOracleList":
        return typing.cast("DatabaseSecretsMountOracleList", jsii.get(self, "oracle"))

    @builtins.property
    @jsii.member(jsii_name="postgresql")
    def postgresql(self) -> "DatabaseSecretsMountPostgresqlList":
        return typing.cast("DatabaseSecretsMountPostgresqlList", jsii.get(self, "postgresql"))

    @builtins.property
    @jsii.member(jsii_name="redis")
    def redis(self) -> "DatabaseSecretsMountRedisList":
        return typing.cast("DatabaseSecretsMountRedisList", jsii.get(self, "redis"))

    @builtins.property
    @jsii.member(jsii_name="redisElasticache")
    def redis_elasticache(self) -> "DatabaseSecretsMountRedisElasticacheList":
        return typing.cast("DatabaseSecretsMountRedisElasticacheList", jsii.get(self, "redisElasticache"))

    @builtins.property
    @jsii.member(jsii_name="redshift")
    def redshift(self) -> "DatabaseSecretsMountRedshiftList":
        return typing.cast("DatabaseSecretsMountRedshiftList", jsii.get(self, "redshift"))

    @builtins.property
    @jsii.member(jsii_name="snowflake")
    def snowflake(self) -> "DatabaseSecretsMountSnowflakeList":
        return typing.cast("DatabaseSecretsMountSnowflakeList", jsii.get(self, "snowflake"))

    @builtins.property
    @jsii.member(jsii_name="allowedManagedKeysInput")
    def allowed_managed_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedManagedKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="auditNonHmacRequestKeysInput")
    def audit_non_hmac_request_keys_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "auditNonHmacRequestKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="auditNonHmacResponseKeysInput")
    def audit_non_hmac_response_keys_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "auditNonHmacResponseKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="cassandraInput")
    def cassandra_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountCassandra"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountCassandra"]]], jsii.get(self, "cassandraInput"))

    @builtins.property
    @jsii.member(jsii_name="couchbaseInput")
    def couchbase_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountCouchbase"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountCouchbase"]]], jsii.get(self, "couchbaseInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultLeaseTtlSecondsInput")
    def default_lease_ttl_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultLeaseTtlSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticsearchInput")
    def elasticsearch_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountElasticsearch"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountElasticsearch"]]], jsii.get(self, "elasticsearchInput"))

    @builtins.property
    @jsii.member(jsii_name="externalEntropyAccessInput")
    def external_entropy_access_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "externalEntropyAccessInput"))

    @builtins.property
    @jsii.member(jsii_name="hanaInput")
    def hana_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountHana"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountHana"]]], jsii.get(self, "hanaInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="influxdbInput")
    def influxdb_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountInfluxdb"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountInfluxdb"]]], jsii.get(self, "influxdbInput"))

    @builtins.property
    @jsii.member(jsii_name="localInput")
    def local_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "localInput"))

    @builtins.property
    @jsii.member(jsii_name="maxLeaseTtlSecondsInput")
    def max_lease_ttl_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxLeaseTtlSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="mongodbatlasInput")
    def mongodbatlas_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMongodbatlas"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMongodbatlas"]]], jsii.get(self, "mongodbatlasInput"))

    @builtins.property
    @jsii.member(jsii_name="mongodbInput")
    def mongodb_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMongodb"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMongodb"]]], jsii.get(self, "mongodbInput"))

    @builtins.property
    @jsii.member(jsii_name="mssqlInput")
    def mssql_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMssql"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMssql"]]], jsii.get(self, "mssqlInput"))

    @builtins.property
    @jsii.member(jsii_name="mysqlAuroraInput")
    def mysql_aurora_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMysqlAurora"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMysqlAurora"]]], jsii.get(self, "mysqlAuroraInput"))

    @builtins.property
    @jsii.member(jsii_name="mysqlInput")
    def mysql_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMysql"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMysql"]]], jsii.get(self, "mysqlInput"))

    @builtins.property
    @jsii.member(jsii_name="mysqlLegacyInput")
    def mysql_legacy_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMysqlLegacy"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMysqlLegacy"]]], jsii.get(self, "mysqlLegacyInput"))

    @builtins.property
    @jsii.member(jsii_name="mysqlRdsInput")
    def mysql_rds_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMysqlRds"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMysqlRds"]]], jsii.get(self, "mysqlRdsInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="optionsInput")
    def options_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "optionsInput"))

    @builtins.property
    @jsii.member(jsii_name="oracleInput")
    def oracle_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountOracle"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountOracle"]]], jsii.get(self, "oracleInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="postgresqlInput")
    def postgresql_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountPostgresql"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountPostgresql"]]], jsii.get(self, "postgresqlInput"))

    @builtins.property
    @jsii.member(jsii_name="redisElasticacheInput")
    def redis_elasticache_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountRedisElasticache"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountRedisElasticache"]]], jsii.get(self, "redisElasticacheInput"))

    @builtins.property
    @jsii.member(jsii_name="redisInput")
    def redis_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountRedis"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountRedis"]]], jsii.get(self, "redisInput"))

    @builtins.property
    @jsii.member(jsii_name="redshiftInput")
    def redshift_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountRedshift"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountRedshift"]]], jsii.get(self, "redshiftInput"))

    @builtins.property
    @jsii.member(jsii_name="sealWrapInput")
    def seal_wrap_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sealWrapInput"))

    @builtins.property
    @jsii.member(jsii_name="snowflakeInput")
    def snowflake_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountSnowflake"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountSnowflake"]]], jsii.get(self, "snowflakeInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedManagedKeys")
    def allowed_managed_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedManagedKeys"))

    @allowed_managed_keys.setter
    def allowed_managed_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e261229ad4936afeca04a28a468b6b0b1ff54c6bf57fa1062a6c3b91cfe87ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedManagedKeys", value)

    @builtins.property
    @jsii.member(jsii_name="auditNonHmacRequestKeys")
    def audit_non_hmac_request_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "auditNonHmacRequestKeys"))

    @audit_non_hmac_request_keys.setter
    def audit_non_hmac_request_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bb289b9d4777709effeeb03308fb7c1b2cb68dbcd6e16abe74524e84708c352)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "auditNonHmacRequestKeys", value)

    @builtins.property
    @jsii.member(jsii_name="auditNonHmacResponseKeys")
    def audit_non_hmac_response_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "auditNonHmacResponseKeys"))

    @audit_non_hmac_response_keys.setter
    def audit_non_hmac_response_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ead257c41f35a41688108eed3b5fb0d17b9724a026266f8c552063117838ce3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "auditNonHmacResponseKeys", value)

    @builtins.property
    @jsii.member(jsii_name="defaultLeaseTtlSeconds")
    def default_lease_ttl_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultLeaseTtlSeconds"))

    @default_lease_ttl_seconds.setter
    def default_lease_ttl_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2853819a74919c31d315f1e83f6c2d087a75b5ca020431c6d2495dd6e614a4a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultLeaseTtlSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4991794f327924d1c5ca8e42c5c9d1740e01ba2e9e837d5992e001e97c9fc42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="externalEntropyAccess")
    def external_entropy_access(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "externalEntropyAccess"))

    @external_entropy_access.setter
    def external_entropy_access(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7b7bb250b16bbd9af2fdcbf2ed60d4806d90ce4a1738fdbf5176b5d2905af13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "externalEntropyAccess", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86995ff3f3a92992024991bb0544ee1912cfec14a8727e552f5f3204299c48e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="local")
    def local(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "local"))

    @local.setter
    def local(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30e5ce497808449c5065cf788d98e3b89257e927dc3ff83826f19f2e448e8a6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "local", value)

    @builtins.property
    @jsii.member(jsii_name="maxLeaseTtlSeconds")
    def max_lease_ttl_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxLeaseTtlSeconds"))

    @max_lease_ttl_seconds.setter
    def max_lease_ttl_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d57fad8b014ac341c538941158880c7567b6b533e40db86872a0c0e35e902ae1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxLeaseTtlSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acb029bd2219c6244522bffce6bcef6d695dc12a34bd09b60afd9502e65f8124)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value)

    @builtins.property
    @jsii.member(jsii_name="options")
    def options(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "options"))

    @options.setter
    def options(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37e6c6b4147de2bd4cd413db7eaebcc7e8789983be3a214198e5eacdee095868)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "options", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99fdcdd08aecfbb7eb70b558a3be81d9346d21cc6337bd80a0d0576bc80a98fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="sealWrap")
    def seal_wrap(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sealWrap"))

    @seal_wrap.setter
    def seal_wrap(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b745a6bb72ac25b3e608f62e44ed7241168056fa433aaed7c3a0abea67820b64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sealWrap", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountCassandra",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "allowed_roles": "allowedRoles",
        "connect_timeout": "connectTimeout",
        "data": "data",
        "hosts": "hosts",
        "insecure_tls": "insecureTls",
        "password": "password",
        "pem_bundle": "pemBundle",
        "pem_json": "pemJson",
        "plugin_name": "pluginName",
        "port": "port",
        "protocol_version": "protocolVersion",
        "root_rotation_statements": "rootRotationStatements",
        "tls": "tls",
        "username": "username",
        "verify_connection": "verifyConnection",
    },
)
class DatabaseSecretsMountCassandra:
    def __init__(
        self,
        *,
        name: builtins.str,
        allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        connect_timeout: typing.Optional[jsii.Number] = None,
        data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        hosts: typing.Optional[typing.Sequence[builtins.str]] = None,
        insecure_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password: typing.Optional[builtins.str] = None,
        pem_bundle: typing.Optional[builtins.str] = None,
        pem_json: typing.Optional[builtins.str] = None,
        plugin_name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol_version: typing.Optional[jsii.Number] = None,
        root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
        tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        username: typing.Optional[builtins.str] = None,
        verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Name of the database connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        :param allowed_roles: A list of roles that are allowed to use this connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        :param connect_timeout: The number of seconds to use as a connection timeout. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#connect_timeout DatabaseSecretsMount#connect_timeout}
        :param data: A map of sensitive data to pass to the endpoint. Useful for templated connection strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        :param hosts: Cassandra hosts to connect to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#hosts DatabaseSecretsMount#hosts}
        :param insecure_tls: Whether to skip verification of the server certificate when using TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#insecure_tls DatabaseSecretsMount#insecure_tls}
        :param password: The password to use when authenticating with Cassandra. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        :param pem_bundle: Concatenated PEM blocks containing a certificate and private key; a certificate, private key, and issuing CA certificate; or just a CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#pem_bundle DatabaseSecretsMount#pem_bundle}
        :param pem_json: Specifies JSON containing a certificate and private key; a certificate, private key, and issuing CA certificate; or just a CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#pem_json DatabaseSecretsMount#pem_json}
        :param plugin_name: Specifies the name of the plugin to use for this connection. Must be prefixed with the name of one of the supported database engine types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        :param port: The transport port to use to connect to Cassandra. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#port DatabaseSecretsMount#port}
        :param protocol_version: The CQL protocol version to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#protocol_version DatabaseSecretsMount#protocol_version}
        :param root_rotation_statements: A list of database statements to be executed to rotate the root user's credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        :param tls: Whether to use TLS when connecting to Cassandra. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#tls DatabaseSecretsMount#tls}
        :param username: The username to use when authenticating with Cassandra. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        :param verify_connection: Specifies if the connection is verified during initial configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bc0e2a228a7d8cabe8ffaeb8d3f171391408a88a2f11fd9d6bfc524f249f8b5)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allowed_roles", value=allowed_roles, expected_type=type_hints["allowed_roles"])
            check_type(argname="argument connect_timeout", value=connect_timeout, expected_type=type_hints["connect_timeout"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument hosts", value=hosts, expected_type=type_hints["hosts"])
            check_type(argname="argument insecure_tls", value=insecure_tls, expected_type=type_hints["insecure_tls"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument pem_bundle", value=pem_bundle, expected_type=type_hints["pem_bundle"])
            check_type(argname="argument pem_json", value=pem_json, expected_type=type_hints["pem_json"])
            check_type(argname="argument plugin_name", value=plugin_name, expected_type=type_hints["plugin_name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol_version", value=protocol_version, expected_type=type_hints["protocol_version"])
            check_type(argname="argument root_rotation_statements", value=root_rotation_statements, expected_type=type_hints["root_rotation_statements"])
            check_type(argname="argument tls", value=tls, expected_type=type_hints["tls"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument verify_connection", value=verify_connection, expected_type=type_hints["verify_connection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if allowed_roles is not None:
            self._values["allowed_roles"] = allowed_roles
        if connect_timeout is not None:
            self._values["connect_timeout"] = connect_timeout
        if data is not None:
            self._values["data"] = data
        if hosts is not None:
            self._values["hosts"] = hosts
        if insecure_tls is not None:
            self._values["insecure_tls"] = insecure_tls
        if password is not None:
            self._values["password"] = password
        if pem_bundle is not None:
            self._values["pem_bundle"] = pem_bundle
        if pem_json is not None:
            self._values["pem_json"] = pem_json
        if plugin_name is not None:
            self._values["plugin_name"] = plugin_name
        if port is not None:
            self._values["port"] = port
        if protocol_version is not None:
            self._values["protocol_version"] = protocol_version
        if root_rotation_statements is not None:
            self._values["root_rotation_statements"] = root_rotation_statements
        if tls is not None:
            self._values["tls"] = tls
        if username is not None:
            self._values["username"] = username
        if verify_connection is not None:
            self._values["verify_connection"] = verify_connection

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the database connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of roles that are allowed to use this connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        '''
        result = self._values.get("allowed_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def connect_timeout(self) -> typing.Optional[jsii.Number]:
        '''The number of seconds to use as a connection timeout.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#connect_timeout DatabaseSecretsMount#connect_timeout}
        '''
        result = self._values.get("connect_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def data(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of sensitive data to pass to the endpoint. Useful for templated connection strings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def hosts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Cassandra hosts to connect to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#hosts DatabaseSecretsMount#hosts}
        '''
        result = self._values.get("hosts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def insecure_tls(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to skip verification of the server certificate when using TLS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#insecure_tls DatabaseSecretsMount#insecure_tls}
        '''
        result = self._values.get("insecure_tls")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The password to use when authenticating with Cassandra.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pem_bundle(self) -> typing.Optional[builtins.str]:
        '''Concatenated PEM blocks containing a certificate and private key;

        a certificate, private key, and issuing CA certificate; or just a CA certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#pem_bundle DatabaseSecretsMount#pem_bundle}
        '''
        result = self._values.get("pem_bundle")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pem_json(self) -> typing.Optional[builtins.str]:
        '''Specifies JSON containing a certificate and private key;

        a certificate, private key, and issuing CA certificate; or just a CA certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#pem_json DatabaseSecretsMount#pem_json}
        '''
        result = self._values.get("pem_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugin_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the plugin to use for this connection.

        Must be prefixed with the name of one of the supported database engine types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        '''
        result = self._values.get("plugin_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The transport port to use to connect to Cassandra.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#port DatabaseSecretsMount#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol_version(self) -> typing.Optional[jsii.Number]:
        '''The CQL protocol version to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#protocol_version DatabaseSecretsMount#protocol_version}
        '''
        result = self._values.get("protocol_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def root_rotation_statements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of database statements to be executed to rotate the root user's credentials.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        '''
        result = self._values.get("root_rotation_statements")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tls(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to use TLS when connecting to Cassandra.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#tls DatabaseSecretsMount#tls}
        '''
        result = self._values.get("tls")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The username to use when authenticating with Cassandra.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verify_connection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if the connection is verified during initial configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        result = self._values.get("verify_connection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseSecretsMountCassandra(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseSecretsMountCassandraList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountCassandraList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__610357533e7a5ff7d26271410ae37932900dc171385da75b5fe5bce46fbce020)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DatabaseSecretsMountCassandraOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ee00824f7c2395df86ccfc5f55436cab80014d10c8e97cc89da42d79c802e82)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatabaseSecretsMountCassandraOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6631d5423c7baf3edfffa83e0c2a9b127b9762e48d0b903e00a48192f0320f23)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a34a2343c762ea22858e4a720cd0395d2a566f446593c6917f77c2d403b96bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__221362b61450727741ea18c807a2b422081670fe2c2d45e28bd7429ead9f328e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountCassandra]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountCassandra]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountCassandra]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa8cc00add67c5b9c1a6843a24fbb4e53633d2c9c13ea0f791ba1e50a59af4f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatabaseSecretsMountCassandraOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountCassandraOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c43d508a3fd1ed41e0f23d5f1eb4fced939a573ca449d550bc04228e60ad7cf7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllowedRoles")
    def reset_allowed_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedRoles", []))

    @jsii.member(jsii_name="resetConnectTimeout")
    def reset_connect_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectTimeout", []))

    @jsii.member(jsii_name="resetData")
    def reset_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetData", []))

    @jsii.member(jsii_name="resetHosts")
    def reset_hosts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHosts", []))

    @jsii.member(jsii_name="resetInsecureTls")
    def reset_insecure_tls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsecureTls", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPemBundle")
    def reset_pem_bundle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPemBundle", []))

    @jsii.member(jsii_name="resetPemJson")
    def reset_pem_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPemJson", []))

    @jsii.member(jsii_name="resetPluginName")
    def reset_plugin_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginName", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetProtocolVersion")
    def reset_protocol_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProtocolVersion", []))

    @jsii.member(jsii_name="resetRootRotationStatements")
    def reset_root_rotation_statements(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootRotationStatements", []))

    @jsii.member(jsii_name="resetTls")
    def reset_tls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTls", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @jsii.member(jsii_name="resetVerifyConnection")
    def reset_verify_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerifyConnection", []))

    @builtins.property
    @jsii.member(jsii_name="allowedRolesInput")
    def allowed_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="connectTimeoutInput")
    def connect_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "connectTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="hostsInput")
    def hosts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "hostsInput"))

    @builtins.property
    @jsii.member(jsii_name="insecureTlsInput")
    def insecure_tls_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecureTlsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="pemBundleInput")
    def pem_bundle_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pemBundleInput"))

    @builtins.property
    @jsii.member(jsii_name="pemJsonInput")
    def pem_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pemJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginNameInput")
    def plugin_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginNameInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="protocolVersionInput")
    def protocol_version_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "protocolVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatementsInput")
    def root_rotation_statements_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rootRotationStatementsInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsInput")
    def tls_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tlsInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyConnectionInput")
    def verify_connection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verifyConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedRoles")
    def allowed_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedRoles"))

    @allowed_roles.setter
    def allowed_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9e9373ca52d9aa9fa11656f9badb19e89596f128f0e0f6d60fcf9b6a816ff1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedRoles", value)

    @builtins.property
    @jsii.member(jsii_name="connectTimeout")
    def connect_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "connectTimeout"))

    @connect_timeout.setter
    def connect_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f79ced0a79e2097daf4fce7eb84d2a9bb0d0b632f81ff39f25b5fc45a36a6d96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectTimeout", value)

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "data"))

    @data.setter
    def data(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c66c617f5d732db9480038d1fdbed647d3bcc10f669bb92d950d52d95b8b43e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value)

    @builtins.property
    @jsii.member(jsii_name="hosts")
    def hosts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "hosts"))

    @hosts.setter
    def hosts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb5fde135c1d2db43a4440770380618ba3b2adf253c39a01617140a68ffd58fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hosts", value)

    @builtins.property
    @jsii.member(jsii_name="insecureTls")
    def insecure_tls(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "insecureTls"))

    @insecure_tls.setter
    def insecure_tls(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8e340f58d30fe0d361239131695503687067f679cfd36e554f475e1351d06a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insecureTls", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ce9ef962c419bde13b5ad363482d00e638dc930f7eea671ac3e838710117a62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68502b209a4cc2e4b0157641d79acd25ed5a659d0c0694e3405cad356b1d9649)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="pemBundle")
    def pem_bundle(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pemBundle"))

    @pem_bundle.setter
    def pem_bundle(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__773a7eb8510d77a382c2ff53eef08a8d89cea1d1ab0228bb979734e8af5d6ffc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pemBundle", value)

    @builtins.property
    @jsii.member(jsii_name="pemJson")
    def pem_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pemJson"))

    @pem_json.setter
    def pem_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__062caac504306d28494c413d575a9045fadad2d18073bd3144745f83bff46854)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pemJson", value)

    @builtins.property
    @jsii.member(jsii_name="pluginName")
    def plugin_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginName"))

    @plugin_name.setter
    def plugin_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81fa21156d6df39a222a9670648f0b1cb2c3b33f867cbac0da77f99d8fed2b39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginName", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71f1d8debf2621b4f32c6f2378fe7b0d70fd299599090fa2ae5e2bd895e8f1c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="protocolVersion")
    def protocol_version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "protocolVersion"))

    @protocol_version.setter
    def protocol_version(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed438a3e5ae3d8b2eb51c13202a9be4fa4ff0765da051e3ca71f68935f1066ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocolVersion", value)

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatements")
    def root_rotation_statements(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rootRotationStatements"))

    @root_rotation_statements.setter
    def root_rotation_statements(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3ad1cea42b41579fec239f8d43b53304fdfb2da34cd4cbdc24f93df90212358)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootRotationStatements", value)

    @builtins.property
    @jsii.member(jsii_name="tls")
    def tls(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tls"))

    @tls.setter
    def tls(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce448508530c290e34d02444be2eb9b14fff71839731e1d4b9598117af5dd01c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tls", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d8a5a26792fea0845f76807393fcc332d09e8cc0c165c0c92ff2d0b66bc7e3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="verifyConnection")
    def verify_connection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verifyConnection"))

    @verify_connection.setter
    def verify_connection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b728eb45f0fb428c22078ed0eb01f605cc5d8fe7b2496eec761fb5d086c23a3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifyConnection", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountCassandra]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountCassandra]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountCassandra]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5b43eca688bab6857cf2cb3780de51f6ca375602874e0b547e69f37002452ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "path": "path",
        "allowed_managed_keys": "allowedManagedKeys",
        "audit_non_hmac_request_keys": "auditNonHmacRequestKeys",
        "audit_non_hmac_response_keys": "auditNonHmacResponseKeys",
        "cassandra": "cassandra",
        "couchbase": "couchbase",
        "default_lease_ttl_seconds": "defaultLeaseTtlSeconds",
        "description": "description",
        "elasticsearch": "elasticsearch",
        "external_entropy_access": "externalEntropyAccess",
        "hana": "hana",
        "id": "id",
        "influxdb": "influxdb",
        "local": "local",
        "max_lease_ttl_seconds": "maxLeaseTtlSeconds",
        "mongodb": "mongodb",
        "mongodbatlas": "mongodbatlas",
        "mssql": "mssql",
        "mysql": "mysql",
        "mysql_aurora": "mysqlAurora",
        "mysql_legacy": "mysqlLegacy",
        "mysql_rds": "mysqlRds",
        "namespace": "namespace",
        "options": "options",
        "oracle": "oracle",
        "postgresql": "postgresql",
        "redis": "redis",
        "redis_elasticache": "redisElasticache",
        "redshift": "redshift",
        "seal_wrap": "sealWrap",
        "snowflake": "snowflake",
    },
)
class DatabaseSecretsMountConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        path: builtins.str,
        allowed_managed_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        audit_non_hmac_request_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        audit_non_hmac_response_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        cassandra: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountCassandra, typing.Dict[builtins.str, typing.Any]]]]] = None,
        couchbase: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountCouchbase", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_lease_ttl_seconds: typing.Optional[jsii.Number] = None,
        description: typing.Optional[builtins.str] = None,
        elasticsearch: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountElasticsearch", typing.Dict[builtins.str, typing.Any]]]]] = None,
        external_entropy_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        hana: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountHana", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        influxdb: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountInfluxdb", typing.Dict[builtins.str, typing.Any]]]]] = None,
        local: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_lease_ttl_seconds: typing.Optional[jsii.Number] = None,
        mongodb: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountMongodb", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mongodbatlas: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountMongodbatlas", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mssql: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountMssql", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mysql: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountMysql", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mysql_aurora: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountMysqlAurora", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mysql_legacy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountMysqlLegacy", typing.Dict[builtins.str, typing.Any]]]]] = None,
        mysql_rds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountMysqlRds", typing.Dict[builtins.str, typing.Any]]]]] = None,
        namespace: typing.Optional[builtins.str] = None,
        options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        oracle: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountOracle", typing.Dict[builtins.str, typing.Any]]]]] = None,
        postgresql: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountPostgresql", typing.Dict[builtins.str, typing.Any]]]]] = None,
        redis: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountRedis", typing.Dict[builtins.str, typing.Any]]]]] = None,
        redis_elasticache: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountRedisElasticache", typing.Dict[builtins.str, typing.Any]]]]] = None,
        redshift: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountRedshift", typing.Dict[builtins.str, typing.Any]]]]] = None,
        seal_wrap: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        snowflake: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DatabaseSecretsMountSnowflake", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param path: Where the secret backend will be mounted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#path DatabaseSecretsMount#path}
        :param allowed_managed_keys: List of managed key registry entry names that the mount in question is allowed to access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_managed_keys DatabaseSecretsMount#allowed_managed_keys}
        :param audit_non_hmac_request_keys: Specifies the list of keys that will not be HMAC'd by audit devices in the request data object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#audit_non_hmac_request_keys DatabaseSecretsMount#audit_non_hmac_request_keys}
        :param audit_non_hmac_response_keys: Specifies the list of keys that will not be HMAC'd by audit devices in the response data object. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#audit_non_hmac_response_keys DatabaseSecretsMount#audit_non_hmac_response_keys}
        :param cassandra: cassandra block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#cassandra DatabaseSecretsMount#cassandra}
        :param couchbase: couchbase block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#couchbase DatabaseSecretsMount#couchbase}
        :param default_lease_ttl_seconds: Default lease duration for tokens and secrets in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#default_lease_ttl_seconds DatabaseSecretsMount#default_lease_ttl_seconds}
        :param description: Human-friendly description of the mount. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#description DatabaseSecretsMount#description}
        :param elasticsearch: elasticsearch block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#elasticsearch DatabaseSecretsMount#elasticsearch}
        :param external_entropy_access: Enable the secrets engine to access Vault's external entropy source. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#external_entropy_access DatabaseSecretsMount#external_entropy_access}
        :param hana: hana block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#hana DatabaseSecretsMount#hana}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#id DatabaseSecretsMount#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param influxdb: influxdb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#influxdb DatabaseSecretsMount#influxdb}
        :param local: Local mount flag that can be explicitly set to true to enforce local mount in HA environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#local DatabaseSecretsMount#local}
        :param max_lease_ttl_seconds: Maximum possible lease duration for tokens and secrets in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_lease_ttl_seconds DatabaseSecretsMount#max_lease_ttl_seconds}
        :param mongodb: mongodb block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#mongodb DatabaseSecretsMount#mongodb}
        :param mongodbatlas: mongodbatlas block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#mongodbatlas DatabaseSecretsMount#mongodbatlas}
        :param mssql: mssql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#mssql DatabaseSecretsMount#mssql}
        :param mysql: mysql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#mysql DatabaseSecretsMount#mysql}
        :param mysql_aurora: mysql_aurora block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#mysql_aurora DatabaseSecretsMount#mysql_aurora}
        :param mysql_legacy: mysql_legacy block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#mysql_legacy DatabaseSecretsMount#mysql_legacy}
        :param mysql_rds: mysql_rds block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#mysql_rds DatabaseSecretsMount#mysql_rds}
        :param namespace: Target namespace. (requires Enterprise). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#namespace DatabaseSecretsMount#namespace}
        :param options: Specifies mount type specific options that are passed to the backend. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#options DatabaseSecretsMount#options}
        :param oracle: oracle block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#oracle DatabaseSecretsMount#oracle}
        :param postgresql: postgresql block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#postgresql DatabaseSecretsMount#postgresql}
        :param redis: redis block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#redis DatabaseSecretsMount#redis}
        :param redis_elasticache: redis_elasticache block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#redis_elasticache DatabaseSecretsMount#redis_elasticache}
        :param redshift: redshift block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#redshift DatabaseSecretsMount#redshift}
        :param seal_wrap: Enable seal wrapping for the mount, causing values stored by the mount to be wrapped by the seal's encryption capability. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#seal_wrap DatabaseSecretsMount#seal_wrap}
        :param snowflake: snowflake block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#snowflake DatabaseSecretsMount#snowflake}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e0a282c97b99e84c8991454c3106a78d4d2f27824bc5990a8abf3546c7278fe)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument allowed_managed_keys", value=allowed_managed_keys, expected_type=type_hints["allowed_managed_keys"])
            check_type(argname="argument audit_non_hmac_request_keys", value=audit_non_hmac_request_keys, expected_type=type_hints["audit_non_hmac_request_keys"])
            check_type(argname="argument audit_non_hmac_response_keys", value=audit_non_hmac_response_keys, expected_type=type_hints["audit_non_hmac_response_keys"])
            check_type(argname="argument cassandra", value=cassandra, expected_type=type_hints["cassandra"])
            check_type(argname="argument couchbase", value=couchbase, expected_type=type_hints["couchbase"])
            check_type(argname="argument default_lease_ttl_seconds", value=default_lease_ttl_seconds, expected_type=type_hints["default_lease_ttl_seconds"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument elasticsearch", value=elasticsearch, expected_type=type_hints["elasticsearch"])
            check_type(argname="argument external_entropy_access", value=external_entropy_access, expected_type=type_hints["external_entropy_access"])
            check_type(argname="argument hana", value=hana, expected_type=type_hints["hana"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument influxdb", value=influxdb, expected_type=type_hints["influxdb"])
            check_type(argname="argument local", value=local, expected_type=type_hints["local"])
            check_type(argname="argument max_lease_ttl_seconds", value=max_lease_ttl_seconds, expected_type=type_hints["max_lease_ttl_seconds"])
            check_type(argname="argument mongodb", value=mongodb, expected_type=type_hints["mongodb"])
            check_type(argname="argument mongodbatlas", value=mongodbatlas, expected_type=type_hints["mongodbatlas"])
            check_type(argname="argument mssql", value=mssql, expected_type=type_hints["mssql"])
            check_type(argname="argument mysql", value=mysql, expected_type=type_hints["mysql"])
            check_type(argname="argument mysql_aurora", value=mysql_aurora, expected_type=type_hints["mysql_aurora"])
            check_type(argname="argument mysql_legacy", value=mysql_legacy, expected_type=type_hints["mysql_legacy"])
            check_type(argname="argument mysql_rds", value=mysql_rds, expected_type=type_hints["mysql_rds"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument oracle", value=oracle, expected_type=type_hints["oracle"])
            check_type(argname="argument postgresql", value=postgresql, expected_type=type_hints["postgresql"])
            check_type(argname="argument redis", value=redis, expected_type=type_hints["redis"])
            check_type(argname="argument redis_elasticache", value=redis_elasticache, expected_type=type_hints["redis_elasticache"])
            check_type(argname="argument redshift", value=redshift, expected_type=type_hints["redshift"])
            check_type(argname="argument seal_wrap", value=seal_wrap, expected_type=type_hints["seal_wrap"])
            check_type(argname="argument snowflake", value=snowflake, expected_type=type_hints["snowflake"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "path": path,
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
        if allowed_managed_keys is not None:
            self._values["allowed_managed_keys"] = allowed_managed_keys
        if audit_non_hmac_request_keys is not None:
            self._values["audit_non_hmac_request_keys"] = audit_non_hmac_request_keys
        if audit_non_hmac_response_keys is not None:
            self._values["audit_non_hmac_response_keys"] = audit_non_hmac_response_keys
        if cassandra is not None:
            self._values["cassandra"] = cassandra
        if couchbase is not None:
            self._values["couchbase"] = couchbase
        if default_lease_ttl_seconds is not None:
            self._values["default_lease_ttl_seconds"] = default_lease_ttl_seconds
        if description is not None:
            self._values["description"] = description
        if elasticsearch is not None:
            self._values["elasticsearch"] = elasticsearch
        if external_entropy_access is not None:
            self._values["external_entropy_access"] = external_entropy_access
        if hana is not None:
            self._values["hana"] = hana
        if id is not None:
            self._values["id"] = id
        if influxdb is not None:
            self._values["influxdb"] = influxdb
        if local is not None:
            self._values["local"] = local
        if max_lease_ttl_seconds is not None:
            self._values["max_lease_ttl_seconds"] = max_lease_ttl_seconds
        if mongodb is not None:
            self._values["mongodb"] = mongodb
        if mongodbatlas is not None:
            self._values["mongodbatlas"] = mongodbatlas
        if mssql is not None:
            self._values["mssql"] = mssql
        if mysql is not None:
            self._values["mysql"] = mysql
        if mysql_aurora is not None:
            self._values["mysql_aurora"] = mysql_aurora
        if mysql_legacy is not None:
            self._values["mysql_legacy"] = mysql_legacy
        if mysql_rds is not None:
            self._values["mysql_rds"] = mysql_rds
        if namespace is not None:
            self._values["namespace"] = namespace
        if options is not None:
            self._values["options"] = options
        if oracle is not None:
            self._values["oracle"] = oracle
        if postgresql is not None:
            self._values["postgresql"] = postgresql
        if redis is not None:
            self._values["redis"] = redis
        if redis_elasticache is not None:
            self._values["redis_elasticache"] = redis_elasticache
        if redshift is not None:
            self._values["redshift"] = redshift
        if seal_wrap is not None:
            self._values["seal_wrap"] = seal_wrap
        if snowflake is not None:
            self._values["snowflake"] = snowflake

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
    def path(self) -> builtins.str:
        '''Where the secret backend will be mounted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#path DatabaseSecretsMount#path}
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_managed_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of managed key registry entry names that the mount in question is allowed to access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_managed_keys DatabaseSecretsMount#allowed_managed_keys}
        '''
        result = self._values.get("allowed_managed_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def audit_non_hmac_request_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the list of keys that will not be HMAC'd by audit devices in the request data object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#audit_non_hmac_request_keys DatabaseSecretsMount#audit_non_hmac_request_keys}
        '''
        result = self._values.get("audit_non_hmac_request_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def audit_non_hmac_response_keys(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the list of keys that will not be HMAC'd by audit devices in the response data object.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#audit_non_hmac_response_keys DatabaseSecretsMount#audit_non_hmac_response_keys}
        '''
        result = self._values.get("audit_non_hmac_response_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cassandra(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountCassandra]]]:
        '''cassandra block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#cassandra DatabaseSecretsMount#cassandra}
        '''
        result = self._values.get("cassandra")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountCassandra]]], result)

    @builtins.property
    def couchbase(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountCouchbase"]]]:
        '''couchbase block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#couchbase DatabaseSecretsMount#couchbase}
        '''
        result = self._values.get("couchbase")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountCouchbase"]]], result)

    @builtins.property
    def default_lease_ttl_seconds(self) -> typing.Optional[jsii.Number]:
        '''Default lease duration for tokens and secrets in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#default_lease_ttl_seconds DatabaseSecretsMount#default_lease_ttl_seconds}
        '''
        result = self._values.get("default_lease_ttl_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Human-friendly description of the mount.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#description DatabaseSecretsMount#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def elasticsearch(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountElasticsearch"]]]:
        '''elasticsearch block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#elasticsearch DatabaseSecretsMount#elasticsearch}
        '''
        result = self._values.get("elasticsearch")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountElasticsearch"]]], result)

    @builtins.property
    def external_entropy_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable the secrets engine to access Vault's external entropy source.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#external_entropy_access DatabaseSecretsMount#external_entropy_access}
        '''
        result = self._values.get("external_entropy_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def hana(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountHana"]]]:
        '''hana block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#hana DatabaseSecretsMount#hana}
        '''
        result = self._values.get("hana")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountHana"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#id DatabaseSecretsMount#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def influxdb(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountInfluxdb"]]]:
        '''influxdb block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#influxdb DatabaseSecretsMount#influxdb}
        '''
        result = self._values.get("influxdb")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountInfluxdb"]]], result)

    @builtins.property
    def local(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Local mount flag that can be explicitly set to true to enforce local mount in HA environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#local DatabaseSecretsMount#local}
        '''
        result = self._values.get("local")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_lease_ttl_seconds(self) -> typing.Optional[jsii.Number]:
        '''Maximum possible lease duration for tokens and secrets in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_lease_ttl_seconds DatabaseSecretsMount#max_lease_ttl_seconds}
        '''
        result = self._values.get("max_lease_ttl_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def mongodb(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMongodb"]]]:
        '''mongodb block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#mongodb DatabaseSecretsMount#mongodb}
        '''
        result = self._values.get("mongodb")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMongodb"]]], result)

    @builtins.property
    def mongodbatlas(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMongodbatlas"]]]:
        '''mongodbatlas block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#mongodbatlas DatabaseSecretsMount#mongodbatlas}
        '''
        result = self._values.get("mongodbatlas")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMongodbatlas"]]], result)

    @builtins.property
    def mssql(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMssql"]]]:
        '''mssql block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#mssql DatabaseSecretsMount#mssql}
        '''
        result = self._values.get("mssql")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMssql"]]], result)

    @builtins.property
    def mysql(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMysql"]]]:
        '''mysql block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#mysql DatabaseSecretsMount#mysql}
        '''
        result = self._values.get("mysql")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMysql"]]], result)

    @builtins.property
    def mysql_aurora(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMysqlAurora"]]]:
        '''mysql_aurora block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#mysql_aurora DatabaseSecretsMount#mysql_aurora}
        '''
        result = self._values.get("mysql_aurora")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMysqlAurora"]]], result)

    @builtins.property
    def mysql_legacy(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMysqlLegacy"]]]:
        '''mysql_legacy block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#mysql_legacy DatabaseSecretsMount#mysql_legacy}
        '''
        result = self._values.get("mysql_legacy")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMysqlLegacy"]]], result)

    @builtins.property
    def mysql_rds(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMysqlRds"]]]:
        '''mysql_rds block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#mysql_rds DatabaseSecretsMount#mysql_rds}
        '''
        result = self._values.get("mysql_rds")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountMysqlRds"]]], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Target namespace. (requires Enterprise).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#namespace DatabaseSecretsMount#namespace}
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def options(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Specifies mount type specific options that are passed to the backend.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#options DatabaseSecretsMount#options}
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def oracle(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountOracle"]]]:
        '''oracle block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#oracle DatabaseSecretsMount#oracle}
        '''
        result = self._values.get("oracle")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountOracle"]]], result)

    @builtins.property
    def postgresql(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountPostgresql"]]]:
        '''postgresql block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#postgresql DatabaseSecretsMount#postgresql}
        '''
        result = self._values.get("postgresql")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountPostgresql"]]], result)

    @builtins.property
    def redis(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountRedis"]]]:
        '''redis block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#redis DatabaseSecretsMount#redis}
        '''
        result = self._values.get("redis")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountRedis"]]], result)

    @builtins.property
    def redis_elasticache(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountRedisElasticache"]]]:
        '''redis_elasticache block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#redis_elasticache DatabaseSecretsMount#redis_elasticache}
        '''
        result = self._values.get("redis_elasticache")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountRedisElasticache"]]], result)

    @builtins.property
    def redshift(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountRedshift"]]]:
        '''redshift block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#redshift DatabaseSecretsMount#redshift}
        '''
        result = self._values.get("redshift")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountRedshift"]]], result)

    @builtins.property
    def seal_wrap(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable seal wrapping for the mount, causing values stored by the mount to be wrapped by the seal's encryption capability.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#seal_wrap DatabaseSecretsMount#seal_wrap}
        '''
        result = self._values.get("seal_wrap")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def snowflake(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountSnowflake"]]]:
        '''snowflake block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#snowflake DatabaseSecretsMount#snowflake}
        '''
        result = self._values.get("snowflake")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DatabaseSecretsMountSnowflake"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseSecretsMountConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountCouchbase",
    jsii_struct_bases=[],
    name_mapping={
        "hosts": "hosts",
        "name": "name",
        "password": "password",
        "username": "username",
        "allowed_roles": "allowedRoles",
        "base64_pem": "base64Pem",
        "bucket_name": "bucketName",
        "data": "data",
        "insecure_tls": "insecureTls",
        "plugin_name": "pluginName",
        "root_rotation_statements": "rootRotationStatements",
        "tls": "tls",
        "username_template": "usernameTemplate",
        "verify_connection": "verifyConnection",
    },
)
class DatabaseSecretsMountCouchbase:
    def __init__(
        self,
        *,
        hosts: typing.Sequence[builtins.str],
        name: builtins.str,
        password: builtins.str,
        username: builtins.str,
        allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        base64_pem: typing.Optional[builtins.str] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        insecure_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        plugin_name: typing.Optional[builtins.str] = None,
        root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
        tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        username_template: typing.Optional[builtins.str] = None,
        verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param hosts: A set of Couchbase URIs to connect to. Must use ``couchbases://`` scheme if ``tls`` is ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#hosts DatabaseSecretsMount#hosts}
        :param name: Name of the database connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        :param password: Specifies the password corresponding to the given username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        :param username: Specifies the username for Vault to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        :param allowed_roles: A list of roles that are allowed to use this connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        :param base64_pem: Required if ``tls`` is ``true``. Specifies the certificate authority of the Couchbase server, as a PEM certificate that has been base64 encoded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#base64_pem DatabaseSecretsMount#base64_pem}
        :param bucket_name: Required for Couchbase versions prior to 6.5.0. This is only used to verify vault's connection to the server. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#bucket_name DatabaseSecretsMount#bucket_name}
        :param data: A map of sensitive data to pass to the endpoint. Useful for templated connection strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        :param insecure_tls: Specifies whether to skip verification of the server certificate when using TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#insecure_tls DatabaseSecretsMount#insecure_tls}
        :param plugin_name: Specifies the name of the plugin to use for this connection. Must be prefixed with the name of one of the supported database engine types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        :param root_rotation_statements: A list of database statements to be executed to rotate the root user's credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        :param tls: Specifies whether to use TLS when connecting to Couchbase. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#tls DatabaseSecretsMount#tls}
        :param username_template: Template describing how dynamic usernames are generated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username_template DatabaseSecretsMount#username_template}
        :param verify_connection: Specifies if the connection is verified during initial configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7708e191c336a208936984979fc4607456e4c8612daf9605d0214ea907b637fe)
            check_type(argname="argument hosts", value=hosts, expected_type=type_hints["hosts"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument allowed_roles", value=allowed_roles, expected_type=type_hints["allowed_roles"])
            check_type(argname="argument base64_pem", value=base64_pem, expected_type=type_hints["base64_pem"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument insecure_tls", value=insecure_tls, expected_type=type_hints["insecure_tls"])
            check_type(argname="argument plugin_name", value=plugin_name, expected_type=type_hints["plugin_name"])
            check_type(argname="argument root_rotation_statements", value=root_rotation_statements, expected_type=type_hints["root_rotation_statements"])
            check_type(argname="argument tls", value=tls, expected_type=type_hints["tls"])
            check_type(argname="argument username_template", value=username_template, expected_type=type_hints["username_template"])
            check_type(argname="argument verify_connection", value=verify_connection, expected_type=type_hints["verify_connection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hosts": hosts,
            "name": name,
            "password": password,
            "username": username,
        }
        if allowed_roles is not None:
            self._values["allowed_roles"] = allowed_roles
        if base64_pem is not None:
            self._values["base64_pem"] = base64_pem
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if data is not None:
            self._values["data"] = data
        if insecure_tls is not None:
            self._values["insecure_tls"] = insecure_tls
        if plugin_name is not None:
            self._values["plugin_name"] = plugin_name
        if root_rotation_statements is not None:
            self._values["root_rotation_statements"] = root_rotation_statements
        if tls is not None:
            self._values["tls"] = tls
        if username_template is not None:
            self._values["username_template"] = username_template
        if verify_connection is not None:
            self._values["verify_connection"] = verify_connection

    @builtins.property
    def hosts(self) -> typing.List[builtins.str]:
        '''A set of Couchbase URIs to connect to. Must use ``couchbases://`` scheme if ``tls`` is ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#hosts DatabaseSecretsMount#hosts}
        '''
        result = self._values.get("hosts")
        assert result is not None, "Required property 'hosts' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the database connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Specifies the password corresponding to the given username.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Specifies the username for Vault to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of roles that are allowed to use this connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        '''
        result = self._values.get("allowed_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def base64_pem(self) -> typing.Optional[builtins.str]:
        '''Required if ``tls`` is ``true``.

        Specifies the certificate authority of the Couchbase server, as a PEM certificate that has been base64 encoded.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#base64_pem DatabaseSecretsMount#base64_pem}
        '''
        result = self._values.get("base64_pem")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Required for Couchbase versions prior to 6.5.0. This is only used to verify vault's connection to the server.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#bucket_name DatabaseSecretsMount#bucket_name}
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of sensitive data to pass to the endpoint. Useful for templated connection strings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def insecure_tls(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to skip verification of the server certificate when using TLS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#insecure_tls DatabaseSecretsMount#insecure_tls}
        '''
        result = self._values.get("insecure_tls")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def plugin_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the plugin to use for this connection.

        Must be prefixed with the name of one of the supported database engine types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        '''
        result = self._values.get("plugin_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def root_rotation_statements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of database statements to be executed to rotate the root user's credentials.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        '''
        result = self._values.get("root_rotation_statements")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tls(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to use TLS when connecting to Couchbase.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#tls DatabaseSecretsMount#tls}
        '''
        result = self._values.get("tls")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def username_template(self) -> typing.Optional[builtins.str]:
        '''Template describing how dynamic usernames are generated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username_template DatabaseSecretsMount#username_template}
        '''
        result = self._values.get("username_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verify_connection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if the connection is verified during initial configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        result = self._values.get("verify_connection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseSecretsMountCouchbase(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseSecretsMountCouchbaseList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountCouchbaseList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a19cbbf1b22bddb7c4aa781cf1c5b1daa08b0b1c80dca2b790b8c336604a5de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DatabaseSecretsMountCouchbaseOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cacddaf7ed09a6806fdbc9fa287f308899b23facf566c9039c6f91b0b3846b88)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatabaseSecretsMountCouchbaseOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a790155b71d2ac0a8010046c81a8c241d5bbbee422885425d378947726e200d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f56bc92b1146cefa8a58f0c1e20e9622de176f839715246f44477d9601a4e15)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aef15ae232865eb9d1d5a8c160c83be7765166377302ecfc148704c6f0f216d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountCouchbase]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountCouchbase]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountCouchbase]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dadebd2164beb762fd416fdde9e02e74c255f5d00c141599831b80d656a52b0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatabaseSecretsMountCouchbaseOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountCouchbaseOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f9bf9949ec22093a9f50882c3bab20d663c672e8492c518969a3bea39847010)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllowedRoles")
    def reset_allowed_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedRoles", []))

    @jsii.member(jsii_name="resetBase64Pem")
    def reset_base64_pem(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBase64Pem", []))

    @jsii.member(jsii_name="resetBucketName")
    def reset_bucket_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketName", []))

    @jsii.member(jsii_name="resetData")
    def reset_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetData", []))

    @jsii.member(jsii_name="resetInsecureTls")
    def reset_insecure_tls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsecureTls", []))

    @jsii.member(jsii_name="resetPluginName")
    def reset_plugin_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginName", []))

    @jsii.member(jsii_name="resetRootRotationStatements")
    def reset_root_rotation_statements(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootRotationStatements", []))

    @jsii.member(jsii_name="resetTls")
    def reset_tls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTls", []))

    @jsii.member(jsii_name="resetUsernameTemplate")
    def reset_username_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsernameTemplate", []))

    @jsii.member(jsii_name="resetVerifyConnection")
    def reset_verify_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerifyConnection", []))

    @builtins.property
    @jsii.member(jsii_name="allowedRolesInput")
    def allowed_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="base64PemInput")
    def base64_pem_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "base64PemInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketNameInput")
    def bucket_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketNameInput"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="hostsInput")
    def hosts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "hostsInput"))

    @builtins.property
    @jsii.member(jsii_name="insecureTlsInput")
    def insecure_tls_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecureTlsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginNameInput")
    def plugin_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatementsInput")
    def root_rotation_statements_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rootRotationStatementsInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsInput")
    def tls_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tlsInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameTemplateInput")
    def username_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyConnectionInput")
    def verify_connection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verifyConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedRoles")
    def allowed_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedRoles"))

    @allowed_roles.setter
    def allowed_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53b06d2e4dbca8fe453f7381ef29fa14ef7bad44b90aa63670ea5bf6dfc7ba4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedRoles", value)

    @builtins.property
    @jsii.member(jsii_name="base64Pem")
    def base64_pem(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "base64Pem"))

    @base64_pem.setter
    def base64_pem(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b896808ced9c7480b20a0a0e88ca04bfb3d7ad1f705e5335f70d04f80ec782db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "base64Pem", value)

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @bucket_name.setter
    def bucket_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__722c1fe42d047ee9b2f79fbe1e40ec3916a9bf12319c27671106881c02c850d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketName", value)

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "data"))

    @data.setter
    def data(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__630008118cf0b7225a30ed242ab5fa94ef327b78ce8c639ee2cfea51c85aed83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value)

    @builtins.property
    @jsii.member(jsii_name="hosts")
    def hosts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "hosts"))

    @hosts.setter
    def hosts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48e64f2d63eaedaa148968b7fa4c0ed6b738b13bb7633fa3ed3429eced105c2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hosts", value)

    @builtins.property
    @jsii.member(jsii_name="insecureTls")
    def insecure_tls(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "insecureTls"))

    @insecure_tls.setter
    def insecure_tls(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__441aee4a588623845e30457828ea8c88f7ca31b0b51aa4c2bafdcb9902b1bc40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insecureTls", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e3c807913732fa8de30bd059b00e6c71e29dfd7b1950b220339af96d08383b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b95e8e5cc091ca3d9cdfec84e27112081394cb75552365d788dee7c2e86daff1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="pluginName")
    def plugin_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginName"))

    @plugin_name.setter
    def plugin_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac72efa5e53487a50ae34177b1c8927592b30e4a6d57227b13da129b521139e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginName", value)

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatements")
    def root_rotation_statements(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rootRotationStatements"))

    @root_rotation_statements.setter
    def root_rotation_statements(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2286db43c4b709bd70cff17f61bbd7fd5f8ce30384ac15decc315d62a823aa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootRotationStatements", value)

    @builtins.property
    @jsii.member(jsii_name="tls")
    def tls(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tls"))

    @tls.setter
    def tls(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__300cf6e7d6fd28665c4926c1d3b7477c857891936616b4fa58c496cea01614c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tls", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__500de1f7913eb2ecdbb873765905b939d56dd2df1fa9f0f0caabcaeba9fc8ccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="usernameTemplate")
    def username_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usernameTemplate"))

    @username_template.setter
    def username_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fb9148190d7cea1fa81687483bd902518469e5a152ddbb9b4005852a0fa01a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usernameTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="verifyConnection")
    def verify_connection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verifyConnection"))

    @verify_connection.setter
    def verify_connection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__197f0dc4eca573879ef532002213c0187f985c832c48bf35ad49127a9a22f1ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifyConnection", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountCouchbase]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountCouchbase]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountCouchbase]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecb60add22a7e61ce09d12abfe039b41ee3e3bf26674d9a618f8017f123a76ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountElasticsearch",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "password": "password",
        "url": "url",
        "username": "username",
        "allowed_roles": "allowedRoles",
        "ca_cert": "caCert",
        "ca_path": "caPath",
        "client_cert": "clientCert",
        "client_key": "clientKey",
        "data": "data",
        "insecure": "insecure",
        "plugin_name": "pluginName",
        "root_rotation_statements": "rootRotationStatements",
        "tls_server_name": "tlsServerName",
        "username_template": "usernameTemplate",
        "verify_connection": "verifyConnection",
    },
)
class DatabaseSecretsMountElasticsearch:
    def __init__(
        self,
        *,
        name: builtins.str,
        password: builtins.str,
        url: builtins.str,
        username: builtins.str,
        allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        ca_cert: typing.Optional[builtins.str] = None,
        ca_path: typing.Optional[builtins.str] = None,
        client_cert: typing.Optional[builtins.str] = None,
        client_key: typing.Optional[builtins.str] = None,
        data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        plugin_name: typing.Optional[builtins.str] = None,
        root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
        tls_server_name: typing.Optional[builtins.str] = None,
        username_template: typing.Optional[builtins.str] = None,
        verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Name of the database connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        :param password: The password to be used in the connection URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        :param url: The URL for Elasticsearch's API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#url DatabaseSecretsMount#url}
        :param username: The username to be used in the connection URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        :param allowed_roles: A list of roles that are allowed to use this connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        :param ca_cert: The path to a PEM-encoded CA cert file to use to verify the Elasticsearch server's identity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#ca_cert DatabaseSecretsMount#ca_cert}
        :param ca_path: The path to a directory of PEM-encoded CA cert files to use to verify the Elasticsearch server's identity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#ca_path DatabaseSecretsMount#ca_path}
        :param client_cert: The path to the certificate for the Elasticsearch client to present for communication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#client_cert DatabaseSecretsMount#client_cert}
        :param client_key: The path to the key for the Elasticsearch client to use for communication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#client_key DatabaseSecretsMount#client_key}
        :param data: A map of sensitive data to pass to the endpoint. Useful for templated connection strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        :param insecure: Whether to disable certificate verification. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#insecure DatabaseSecretsMount#insecure}
        :param plugin_name: Specifies the name of the plugin to use for this connection. Must be prefixed with the name of one of the supported database engine types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        :param root_rotation_statements: A list of database statements to be executed to rotate the root user's credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        :param tls_server_name: This, if set, is used to set the SNI host when connecting via TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#tls_server_name DatabaseSecretsMount#tls_server_name}
        :param username_template: Template describing how dynamic usernames are generated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username_template DatabaseSecretsMount#username_template}
        :param verify_connection: Specifies if the connection is verified during initial configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22399b1622dddcd6ba7f17d48590f4190246b50f1ef021a0987f0cc5fcb50063)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument allowed_roles", value=allowed_roles, expected_type=type_hints["allowed_roles"])
            check_type(argname="argument ca_cert", value=ca_cert, expected_type=type_hints["ca_cert"])
            check_type(argname="argument ca_path", value=ca_path, expected_type=type_hints["ca_path"])
            check_type(argname="argument client_cert", value=client_cert, expected_type=type_hints["client_cert"])
            check_type(argname="argument client_key", value=client_key, expected_type=type_hints["client_key"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument insecure", value=insecure, expected_type=type_hints["insecure"])
            check_type(argname="argument plugin_name", value=plugin_name, expected_type=type_hints["plugin_name"])
            check_type(argname="argument root_rotation_statements", value=root_rotation_statements, expected_type=type_hints["root_rotation_statements"])
            check_type(argname="argument tls_server_name", value=tls_server_name, expected_type=type_hints["tls_server_name"])
            check_type(argname="argument username_template", value=username_template, expected_type=type_hints["username_template"])
            check_type(argname="argument verify_connection", value=verify_connection, expected_type=type_hints["verify_connection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "password": password,
            "url": url,
            "username": username,
        }
        if allowed_roles is not None:
            self._values["allowed_roles"] = allowed_roles
        if ca_cert is not None:
            self._values["ca_cert"] = ca_cert
        if ca_path is not None:
            self._values["ca_path"] = ca_path
        if client_cert is not None:
            self._values["client_cert"] = client_cert
        if client_key is not None:
            self._values["client_key"] = client_key
        if data is not None:
            self._values["data"] = data
        if insecure is not None:
            self._values["insecure"] = insecure
        if plugin_name is not None:
            self._values["plugin_name"] = plugin_name
        if root_rotation_statements is not None:
            self._values["root_rotation_statements"] = root_rotation_statements
        if tls_server_name is not None:
            self._values["tls_server_name"] = tls_server_name
        if username_template is not None:
            self._values["username_template"] = username_template
        if verify_connection is not None:
            self._values["verify_connection"] = verify_connection

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the database connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''The password to be used in the connection URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''The URL for Elasticsearch's API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#url DatabaseSecretsMount#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''The username to be used in the connection URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of roles that are allowed to use this connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        '''
        result = self._values.get("allowed_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ca_cert(self) -> typing.Optional[builtins.str]:
        '''The path to a PEM-encoded CA cert file to use to verify the Elasticsearch server's identity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#ca_cert DatabaseSecretsMount#ca_cert}
        '''
        result = self._values.get("ca_cert")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ca_path(self) -> typing.Optional[builtins.str]:
        '''The path to a directory of PEM-encoded CA cert files to use to verify the Elasticsearch server's identity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#ca_path DatabaseSecretsMount#ca_path}
        '''
        result = self._values.get("ca_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_cert(self) -> typing.Optional[builtins.str]:
        '''The path to the certificate for the Elasticsearch client to present for communication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#client_cert DatabaseSecretsMount#client_cert}
        '''
        result = self._values.get("client_cert")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_key(self) -> typing.Optional[builtins.str]:
        '''The path to the key for the Elasticsearch client to use for communication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#client_key DatabaseSecretsMount#client_key}
        '''
        result = self._values.get("client_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of sensitive data to pass to the endpoint. Useful for templated connection strings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to disable certificate verification.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#insecure DatabaseSecretsMount#insecure}
        '''
        result = self._values.get("insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def plugin_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the plugin to use for this connection.

        Must be prefixed with the name of one of the supported database engine types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        '''
        result = self._values.get("plugin_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def root_rotation_statements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of database statements to be executed to rotate the root user's credentials.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        '''
        result = self._values.get("root_rotation_statements")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tls_server_name(self) -> typing.Optional[builtins.str]:
        '''This, if set, is used to set the SNI host when connecting via TLS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#tls_server_name DatabaseSecretsMount#tls_server_name}
        '''
        result = self._values.get("tls_server_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username_template(self) -> typing.Optional[builtins.str]:
        '''Template describing how dynamic usernames are generated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username_template DatabaseSecretsMount#username_template}
        '''
        result = self._values.get("username_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verify_connection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if the connection is verified during initial configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        result = self._values.get("verify_connection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseSecretsMountElasticsearch(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseSecretsMountElasticsearchList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountElasticsearchList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__61e46ce583c358fe2f35a51e2fb9f1aa3ae491d37adb7bdf83cb287e397a6c08)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatabaseSecretsMountElasticsearchOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e1fc9d64a4c8d24ed4d9d21050576fb46bd71604f69a16ab7f5a7e0b5195e3d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatabaseSecretsMountElasticsearchOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af04d92bc531014408e942c08af4e940103cc09504d5adddd0aefee48f0b65ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__484bd3ef5dcab8292cdd66c36e5144b61f335adc218c4af16478c39117619f79)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a09b63924f2618245cbd9fa0252e549d299b5ad208d39981c969027e61d3177)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountElasticsearch]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountElasticsearch]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountElasticsearch]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad64738c3cc62dbaf18687ed752a1de64d08db49274af8ffe653bb07907f00ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatabaseSecretsMountElasticsearchOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountElasticsearchOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c73bd7319d3fc38762515025dfee63a7d21bbc496056b162036f0771c3e24b96)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllowedRoles")
    def reset_allowed_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedRoles", []))

    @jsii.member(jsii_name="resetCaCert")
    def reset_ca_cert(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaCert", []))

    @jsii.member(jsii_name="resetCaPath")
    def reset_ca_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaPath", []))

    @jsii.member(jsii_name="resetClientCert")
    def reset_client_cert(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCert", []))

    @jsii.member(jsii_name="resetClientKey")
    def reset_client_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientKey", []))

    @jsii.member(jsii_name="resetData")
    def reset_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetData", []))

    @jsii.member(jsii_name="resetInsecure")
    def reset_insecure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsecure", []))

    @jsii.member(jsii_name="resetPluginName")
    def reset_plugin_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginName", []))

    @jsii.member(jsii_name="resetRootRotationStatements")
    def reset_root_rotation_statements(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootRotationStatements", []))

    @jsii.member(jsii_name="resetTlsServerName")
    def reset_tls_server_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsServerName", []))

    @jsii.member(jsii_name="resetUsernameTemplate")
    def reset_username_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsernameTemplate", []))

    @jsii.member(jsii_name="resetVerifyConnection")
    def reset_verify_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerifyConnection", []))

    @builtins.property
    @jsii.member(jsii_name="allowedRolesInput")
    def allowed_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="caCertInput")
    def ca_cert_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "caCertInput"))

    @builtins.property
    @jsii.member(jsii_name="caPathInput")
    def ca_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "caPathInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertInput")
    def client_cert_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertInput"))

    @builtins.property
    @jsii.member(jsii_name="clientKeyInput")
    def client_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="insecureInput")
    def insecure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecureInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginNameInput")
    def plugin_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatementsInput")
    def root_rotation_statements_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rootRotationStatementsInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsServerNameInput")
    def tls_server_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tlsServerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameTemplateInput")
    def username_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyConnectionInput")
    def verify_connection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verifyConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedRoles")
    def allowed_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedRoles"))

    @allowed_roles.setter
    def allowed_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e29a91425b2de754f635c1bfaa5a8496d8a211de67c5600b28cfb35d0097821)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedRoles", value)

    @builtins.property
    @jsii.member(jsii_name="caCert")
    def ca_cert(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caCert"))

    @ca_cert.setter
    def ca_cert(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a4576566527c701a8527bbec2a4815328dc6f6acfe66fc0564e0683c4a19f40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caCert", value)

    @builtins.property
    @jsii.member(jsii_name="caPath")
    def ca_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caPath"))

    @ca_path.setter
    def ca_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19b8f0cbc84d1b2bf814d3d5eecaef9bc060f487ab444e01a001d062a87b82f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caPath", value)

    @builtins.property
    @jsii.member(jsii_name="clientCert")
    def client_cert(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCert"))

    @client_cert.setter
    def client_cert(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7d6b1fc879b1409e5294df989048840db69ad7e26664d621974a2b6d4fe73a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCert", value)

    @builtins.property
    @jsii.member(jsii_name="clientKey")
    def client_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientKey"))

    @client_key.setter
    def client_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be0a0eae0658d518d029de43916f7a79efe33f9056856609d78039922605b508)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientKey", value)

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "data"))

    @data.setter
    def data(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed613105d65edc3495fcf73eb0ecc2c6feabb2710f0af0713c30c0a2a72ba15a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value)

    @builtins.property
    @jsii.member(jsii_name="insecure")
    def insecure(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "insecure"))

    @insecure.setter
    def insecure(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8486907f19823cc3068932c001acd514741835a8c63925dcecae59ba8d0d26a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insecure", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e2b25b2ea054c28bad926f5ed8bc3fb265c9b15080f157c988bd883461e4f29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfad744e7e4305970b0296cbebd8daf1ba2c7dd6d13721c4b486133d00d16f9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="pluginName")
    def plugin_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginName"))

    @plugin_name.setter
    def plugin_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ad8b19f4de30475a86f58d2c9a9a4f38e13a659c916f6ed329220a36b7a78f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginName", value)

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatements")
    def root_rotation_statements(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rootRotationStatements"))

    @root_rotation_statements.setter
    def root_rotation_statements(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da0cfa86f3cb063ef75af726daf6d939538bdad7f40e0f406add96620d67e2ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootRotationStatements", value)

    @builtins.property
    @jsii.member(jsii_name="tlsServerName")
    def tls_server_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tlsServerName"))

    @tls_server_name.setter
    def tls_server_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74d1579c7227ad84f54320e5e0220891a232e6715b6597bfa943b040debfc64c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsServerName", value)

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cb04e18ede7891f184f3b81d3185549de3eed152c65d2780e50606ea691b2bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc6cf5c9d6db453395c026c8fd211b5fada8b791d16d5629cd3004f5cd456dfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="usernameTemplate")
    def username_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usernameTemplate"))

    @username_template.setter
    def username_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d041036382f78a9d21b238854c4f69e335c07b97b51300fa3a230aee4d3de8f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usernameTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="verifyConnection")
    def verify_connection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verifyConnection"))

    @verify_connection.setter
    def verify_connection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__015a21c1a208d61ae1324208e008b49d84ace9b514e014c3982f6fff3b2d9a03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifyConnection", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountElasticsearch]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountElasticsearch]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountElasticsearch]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0ec083b6696c87109f43044750bfcff2776c0055485df4f010354ab415afe32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountHana",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "allowed_roles": "allowedRoles",
        "connection_url": "connectionUrl",
        "data": "data",
        "disable_escaping": "disableEscaping",
        "max_connection_lifetime": "maxConnectionLifetime",
        "max_idle_connections": "maxIdleConnections",
        "max_open_connections": "maxOpenConnections",
        "password": "password",
        "plugin_name": "pluginName",
        "root_rotation_statements": "rootRotationStatements",
        "username": "username",
        "verify_connection": "verifyConnection",
    },
)
class DatabaseSecretsMountHana:
    def __init__(
        self,
        *,
        name: builtins.str,
        allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection_url: typing.Optional[builtins.str] = None,
        data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        disable_escaping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_connection_lifetime: typing.Optional[jsii.Number] = None,
        max_idle_connections: typing.Optional[jsii.Number] = None,
        max_open_connections: typing.Optional[jsii.Number] = None,
        password: typing.Optional[builtins.str] = None,
        plugin_name: typing.Optional[builtins.str] = None,
        root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
        username: typing.Optional[builtins.str] = None,
        verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Name of the database connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        :param allowed_roles: A list of roles that are allowed to use this connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        :param connection_url: Connection string to use to connect to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#connection_url DatabaseSecretsMount#connection_url}
        :param data: A map of sensitive data to pass to the endpoint. Useful for templated connection strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        :param disable_escaping: Disable special character escaping in username and password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#disable_escaping DatabaseSecretsMount#disable_escaping}
        :param max_connection_lifetime: Maximum number of seconds a connection may be reused. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_connection_lifetime DatabaseSecretsMount#max_connection_lifetime}
        :param max_idle_connections: Maximum number of idle connections to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_idle_connections DatabaseSecretsMount#max_idle_connections}
        :param max_open_connections: Maximum number of open connections to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_open_connections DatabaseSecretsMount#max_open_connections}
        :param password: The root credential password used in the connection URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        :param plugin_name: Specifies the name of the plugin to use for this connection. Must be prefixed with the name of one of the supported database engine types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        :param root_rotation_statements: A list of database statements to be executed to rotate the root user's credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        :param username: The root credential username used in the connection URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        :param verify_connection: Specifies if the connection is verified during initial configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c72cd3caee2e9fbce76bb3aac1a434c9b1cf8b7c5657aad746c708df1a0d6fcc)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allowed_roles", value=allowed_roles, expected_type=type_hints["allowed_roles"])
            check_type(argname="argument connection_url", value=connection_url, expected_type=type_hints["connection_url"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument disable_escaping", value=disable_escaping, expected_type=type_hints["disable_escaping"])
            check_type(argname="argument max_connection_lifetime", value=max_connection_lifetime, expected_type=type_hints["max_connection_lifetime"])
            check_type(argname="argument max_idle_connections", value=max_idle_connections, expected_type=type_hints["max_idle_connections"])
            check_type(argname="argument max_open_connections", value=max_open_connections, expected_type=type_hints["max_open_connections"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument plugin_name", value=plugin_name, expected_type=type_hints["plugin_name"])
            check_type(argname="argument root_rotation_statements", value=root_rotation_statements, expected_type=type_hints["root_rotation_statements"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument verify_connection", value=verify_connection, expected_type=type_hints["verify_connection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if allowed_roles is not None:
            self._values["allowed_roles"] = allowed_roles
        if connection_url is not None:
            self._values["connection_url"] = connection_url
        if data is not None:
            self._values["data"] = data
        if disable_escaping is not None:
            self._values["disable_escaping"] = disable_escaping
        if max_connection_lifetime is not None:
            self._values["max_connection_lifetime"] = max_connection_lifetime
        if max_idle_connections is not None:
            self._values["max_idle_connections"] = max_idle_connections
        if max_open_connections is not None:
            self._values["max_open_connections"] = max_open_connections
        if password is not None:
            self._values["password"] = password
        if plugin_name is not None:
            self._values["plugin_name"] = plugin_name
        if root_rotation_statements is not None:
            self._values["root_rotation_statements"] = root_rotation_statements
        if username is not None:
            self._values["username"] = username
        if verify_connection is not None:
            self._values["verify_connection"] = verify_connection

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the database connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of roles that are allowed to use this connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        '''
        result = self._values.get("allowed_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def connection_url(self) -> typing.Optional[builtins.str]:
        '''Connection string to use to connect to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#connection_url DatabaseSecretsMount#connection_url}
        '''
        result = self._values.get("connection_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of sensitive data to pass to the endpoint. Useful for templated connection strings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def disable_escaping(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable special character escaping in username and password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#disable_escaping DatabaseSecretsMount#disable_escaping}
        '''
        result = self._values.get("disable_escaping")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_connection_lifetime(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of seconds a connection may be reused.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_connection_lifetime DatabaseSecretsMount#max_connection_lifetime}
        '''
        result = self._values.get("max_connection_lifetime")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_idle_connections(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of idle connections to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_idle_connections DatabaseSecretsMount#max_idle_connections}
        '''
        result = self._values.get("max_idle_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_open_connections(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of open connections to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_open_connections DatabaseSecretsMount#max_open_connections}
        '''
        result = self._values.get("max_open_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The root credential password used in the connection URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugin_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the plugin to use for this connection.

        Must be prefixed with the name of one of the supported database engine types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        '''
        result = self._values.get("plugin_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def root_rotation_statements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of database statements to be executed to rotate the root user's credentials.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        '''
        result = self._values.get("root_rotation_statements")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The root credential username used in the connection URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verify_connection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if the connection is verified during initial configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        result = self._values.get("verify_connection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseSecretsMountHana(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseSecretsMountHanaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountHanaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5250139ada5cba7b47662b5558b54bdefe8ba792fa2c5672e02acc0d99aaae21)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DatabaseSecretsMountHanaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba7a72d1b9221ae38317fc74a886842d2271f7a31d59b94be5abace55e0f5e85)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatabaseSecretsMountHanaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dd907eb1003d850ff183cd50aab480bb9e951d6e1730822b272aad38d3a4d35)
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
            type_hints = typing.get_type_hints(_typecheckingstub__de55da1bc944963c772de4dac94d93654de3caf047c5c8f0890ef7017203ac94)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c3ca28475641ad1050be442e62037c4f6f269bb07291ce72cf0714b89c6794f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountHana]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountHana]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountHana]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05ce00d9d06c6f11419432d4d3d2af5c173b679a313c7c2a159cd0588255c544)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatabaseSecretsMountHanaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountHanaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96e028b9d6364c47aada681b536f08d9c8932b69ae2c6ecddb331fd369078e78)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllowedRoles")
    def reset_allowed_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedRoles", []))

    @jsii.member(jsii_name="resetConnectionUrl")
    def reset_connection_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionUrl", []))

    @jsii.member(jsii_name="resetData")
    def reset_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetData", []))

    @jsii.member(jsii_name="resetDisableEscaping")
    def reset_disable_escaping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableEscaping", []))

    @jsii.member(jsii_name="resetMaxConnectionLifetime")
    def reset_max_connection_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConnectionLifetime", []))

    @jsii.member(jsii_name="resetMaxIdleConnections")
    def reset_max_idle_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxIdleConnections", []))

    @jsii.member(jsii_name="resetMaxOpenConnections")
    def reset_max_open_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxOpenConnections", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPluginName")
    def reset_plugin_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginName", []))

    @jsii.member(jsii_name="resetRootRotationStatements")
    def reset_root_rotation_statements(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootRotationStatements", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @jsii.member(jsii_name="resetVerifyConnection")
    def reset_verify_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerifyConnection", []))

    @builtins.property
    @jsii.member(jsii_name="allowedRolesInput")
    def allowed_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionUrlInput")
    def connection_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="disableEscapingInput")
    def disable_escaping_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableEscapingInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConnectionLifetimeInput")
    def max_connection_lifetime_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConnectionLifetimeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxIdleConnectionsInput")
    def max_idle_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxIdleConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxOpenConnectionsInput")
    def max_open_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxOpenConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginNameInput")
    def plugin_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatementsInput")
    def root_rotation_statements_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rootRotationStatementsInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyConnectionInput")
    def verify_connection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verifyConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedRoles")
    def allowed_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedRoles"))

    @allowed_roles.setter
    def allowed_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1501d09daacd9fb65c6a591a2833b1b4755f1fb6dd94fcc7559a007fbdb5bb52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedRoles", value)

    @builtins.property
    @jsii.member(jsii_name="connectionUrl")
    def connection_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionUrl"))

    @connection_url.setter
    def connection_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0ae6d90e54c9c160ab6fde304a573d69b570ce7dff2de5207ee6cc46cd1ecbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionUrl", value)

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "data"))

    @data.setter
    def data(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f85cac995e7e78ee6855c16212166e5f0ccf7c2e6966a733774814801e61b95a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value)

    @builtins.property
    @jsii.member(jsii_name="disableEscaping")
    def disable_escaping(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableEscaping"))

    @disable_escaping.setter
    def disable_escaping(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59b8a57f7e6219bb96c61976febe0e370103198a84552f038da29f1e076cd446)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableEscaping", value)

    @builtins.property
    @jsii.member(jsii_name="maxConnectionLifetime")
    def max_connection_lifetime(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConnectionLifetime"))

    @max_connection_lifetime.setter
    def max_connection_lifetime(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7f242fdc900e0f7407000df88ae0e32fb3321ac4ed4475195d441db243a765f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnectionLifetime", value)

    @builtins.property
    @jsii.member(jsii_name="maxIdleConnections")
    def max_idle_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIdleConnections"))

    @max_idle_connections.setter
    def max_idle_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9454bda6689929a5ff2676fda90327896cf511e53dd97b855bec8cc6aed8d87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxIdleConnections", value)

    @builtins.property
    @jsii.member(jsii_name="maxOpenConnections")
    def max_open_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxOpenConnections"))

    @max_open_connections.setter
    def max_open_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b5ba109e872894f136bb76a1ca1bdc1b766ed233928f47aff8b4e21caf0c3ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxOpenConnections", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__359688317530993184c77a332ab3422207b16562553b59ad0a6373375ff59a32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7c6339ad693e531e37dea3555caea2e4e500d8d509a549e7099a5afb5b3ac40)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="pluginName")
    def plugin_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginName"))

    @plugin_name.setter
    def plugin_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55d81f4799c1110e15031cb6fe5509f0887470810ea5fbec91ae369bbec53857)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginName", value)

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatements")
    def root_rotation_statements(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rootRotationStatements"))

    @root_rotation_statements.setter
    def root_rotation_statements(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31e2c495e04b0b3dd66a9582557d61c5f9f429ada847236b0644a529a8523bfe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootRotationStatements", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44adfe3a18bd1cb1259a20014f94c5291350157beb5e05c8e9ac2fd9cdc8be0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="verifyConnection")
    def verify_connection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verifyConnection"))

    @verify_connection.setter
    def verify_connection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87d76b2d2f19b41134f7d98b62fb002d5837440648dd87b771a48dda69dfed66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifyConnection", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountHana]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountHana]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountHana]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e10094e3626a24cdd99289dff5ca6f66ebc71fc41240fce91a19038f44c0017)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountInfluxdb",
    jsii_struct_bases=[],
    name_mapping={
        "host": "host",
        "name": "name",
        "password": "password",
        "username": "username",
        "allowed_roles": "allowedRoles",
        "connect_timeout": "connectTimeout",
        "data": "data",
        "insecure_tls": "insecureTls",
        "pem_bundle": "pemBundle",
        "pem_json": "pemJson",
        "plugin_name": "pluginName",
        "port": "port",
        "root_rotation_statements": "rootRotationStatements",
        "tls": "tls",
        "username_template": "usernameTemplate",
        "verify_connection": "verifyConnection",
    },
)
class DatabaseSecretsMountInfluxdb:
    def __init__(
        self,
        *,
        host: builtins.str,
        name: builtins.str,
        password: builtins.str,
        username: builtins.str,
        allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        connect_timeout: typing.Optional[jsii.Number] = None,
        data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        insecure_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        pem_bundle: typing.Optional[builtins.str] = None,
        pem_json: typing.Optional[builtins.str] = None,
        plugin_name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
        tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        username_template: typing.Optional[builtins.str] = None,
        verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param host: Influxdb host to connect to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#host DatabaseSecretsMount#host}
        :param name: Name of the database connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        :param password: Specifies the password corresponding to the given username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        :param username: Specifies the username to use for superuser access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        :param allowed_roles: A list of roles that are allowed to use this connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        :param connect_timeout: The number of seconds to use as a connection timeout. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#connect_timeout DatabaseSecretsMount#connect_timeout}
        :param data: A map of sensitive data to pass to the endpoint. Useful for templated connection strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        :param insecure_tls: Whether to skip verification of the server certificate when using TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#insecure_tls DatabaseSecretsMount#insecure_tls}
        :param pem_bundle: Concatenated PEM blocks containing a certificate and private key; a certificate, private key, and issuing CA certificate; or just a CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#pem_bundle DatabaseSecretsMount#pem_bundle}
        :param pem_json: Specifies JSON containing a certificate and private key; a certificate, private key, and issuing CA certificate; or just a CA certificate. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#pem_json DatabaseSecretsMount#pem_json}
        :param plugin_name: Specifies the name of the plugin to use for this connection. Must be prefixed with the name of one of the supported database engine types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        :param port: The transport port to use to connect to Influxdb. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#port DatabaseSecretsMount#port}
        :param root_rotation_statements: A list of database statements to be executed to rotate the root user's credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        :param tls: Whether to use TLS when connecting to Influxdb. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#tls DatabaseSecretsMount#tls}
        :param username_template: Template describing how dynamic usernames are generated. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username_template DatabaseSecretsMount#username_template}
        :param verify_connection: Specifies if the connection is verified during initial configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4f88548bcfd4868bd71841e883d92ebcbe2f06dbf858b520b78aba07d2056f6)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument allowed_roles", value=allowed_roles, expected_type=type_hints["allowed_roles"])
            check_type(argname="argument connect_timeout", value=connect_timeout, expected_type=type_hints["connect_timeout"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument insecure_tls", value=insecure_tls, expected_type=type_hints["insecure_tls"])
            check_type(argname="argument pem_bundle", value=pem_bundle, expected_type=type_hints["pem_bundle"])
            check_type(argname="argument pem_json", value=pem_json, expected_type=type_hints["pem_json"])
            check_type(argname="argument plugin_name", value=plugin_name, expected_type=type_hints["plugin_name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument root_rotation_statements", value=root_rotation_statements, expected_type=type_hints["root_rotation_statements"])
            check_type(argname="argument tls", value=tls, expected_type=type_hints["tls"])
            check_type(argname="argument username_template", value=username_template, expected_type=type_hints["username_template"])
            check_type(argname="argument verify_connection", value=verify_connection, expected_type=type_hints["verify_connection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host": host,
            "name": name,
            "password": password,
            "username": username,
        }
        if allowed_roles is not None:
            self._values["allowed_roles"] = allowed_roles
        if connect_timeout is not None:
            self._values["connect_timeout"] = connect_timeout
        if data is not None:
            self._values["data"] = data
        if insecure_tls is not None:
            self._values["insecure_tls"] = insecure_tls
        if pem_bundle is not None:
            self._values["pem_bundle"] = pem_bundle
        if pem_json is not None:
            self._values["pem_json"] = pem_json
        if plugin_name is not None:
            self._values["plugin_name"] = plugin_name
        if port is not None:
            self._values["port"] = port
        if root_rotation_statements is not None:
            self._values["root_rotation_statements"] = root_rotation_statements
        if tls is not None:
            self._values["tls"] = tls
        if username_template is not None:
            self._values["username_template"] = username_template
        if verify_connection is not None:
            self._values["verify_connection"] = verify_connection

    @builtins.property
    def host(self) -> builtins.str:
        '''Influxdb host to connect to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#host DatabaseSecretsMount#host}
        '''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the database connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Specifies the password corresponding to the given username.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Specifies the username to use for superuser access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of roles that are allowed to use this connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        '''
        result = self._values.get("allowed_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def connect_timeout(self) -> typing.Optional[jsii.Number]:
        '''The number of seconds to use as a connection timeout.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#connect_timeout DatabaseSecretsMount#connect_timeout}
        '''
        result = self._values.get("connect_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def data(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of sensitive data to pass to the endpoint. Useful for templated connection strings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def insecure_tls(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to skip verification of the server certificate when using TLS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#insecure_tls DatabaseSecretsMount#insecure_tls}
        '''
        result = self._values.get("insecure_tls")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def pem_bundle(self) -> typing.Optional[builtins.str]:
        '''Concatenated PEM blocks containing a certificate and private key;

        a certificate, private key, and issuing CA certificate; or just a CA certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#pem_bundle DatabaseSecretsMount#pem_bundle}
        '''
        result = self._values.get("pem_bundle")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pem_json(self) -> typing.Optional[builtins.str]:
        '''Specifies JSON containing a certificate and private key;

        a certificate, private key, and issuing CA certificate; or just a CA certificate.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#pem_json DatabaseSecretsMount#pem_json}
        '''
        result = self._values.get("pem_json")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugin_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the plugin to use for this connection.

        Must be prefixed with the name of one of the supported database engine types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        '''
        result = self._values.get("plugin_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The transport port to use to connect to Influxdb.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#port DatabaseSecretsMount#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def root_rotation_statements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of database statements to be executed to rotate the root user's credentials.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        '''
        result = self._values.get("root_rotation_statements")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tls(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to use TLS when connecting to Influxdb.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#tls DatabaseSecretsMount#tls}
        '''
        result = self._values.get("tls")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def username_template(self) -> typing.Optional[builtins.str]:
        '''Template describing how dynamic usernames are generated.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username_template DatabaseSecretsMount#username_template}
        '''
        result = self._values.get("username_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verify_connection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if the connection is verified during initial configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        result = self._values.get("verify_connection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseSecretsMountInfluxdb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseSecretsMountInfluxdbList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountInfluxdbList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cda7844152c8ceea020f7ac29642e552206209b55ada2ab11ba01bec460c8873)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DatabaseSecretsMountInfluxdbOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2c72d8edc3563e7629c22c13b61286463bfc988c1fa742b1eb5e2b40a3cca63)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatabaseSecretsMountInfluxdbOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f85ccd7d2a554da4ee834dda473544c15c0f7b930df7b1edaacf72daaa1bc4d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a056cf4077c41155c64e241ab38c7a5a999ec832b529d77817354424cc27574)
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
            type_hints = typing.get_type_hints(_typecheckingstub__75ce1d3cc040484b297057db1232de8fb807ac95e6edc8921051689ccffc5eb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountInfluxdb]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountInfluxdb]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountInfluxdb]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6a1472cdab98d605f68e6f5a6c6893a7772acb10dea878f3c3859ae897161ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatabaseSecretsMountInfluxdbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountInfluxdbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3010dc29103fa31f1320e0f554cdc6aa4056aa9e29a76319b72d282f8ffa71e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllowedRoles")
    def reset_allowed_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedRoles", []))

    @jsii.member(jsii_name="resetConnectTimeout")
    def reset_connect_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectTimeout", []))

    @jsii.member(jsii_name="resetData")
    def reset_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetData", []))

    @jsii.member(jsii_name="resetInsecureTls")
    def reset_insecure_tls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsecureTls", []))

    @jsii.member(jsii_name="resetPemBundle")
    def reset_pem_bundle(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPemBundle", []))

    @jsii.member(jsii_name="resetPemJson")
    def reset_pem_json(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPemJson", []))

    @jsii.member(jsii_name="resetPluginName")
    def reset_plugin_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginName", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetRootRotationStatements")
    def reset_root_rotation_statements(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootRotationStatements", []))

    @jsii.member(jsii_name="resetTls")
    def reset_tls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTls", []))

    @jsii.member(jsii_name="resetUsernameTemplate")
    def reset_username_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsernameTemplate", []))

    @jsii.member(jsii_name="resetVerifyConnection")
    def reset_verify_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerifyConnection", []))

    @builtins.property
    @jsii.member(jsii_name="allowedRolesInput")
    def allowed_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="connectTimeoutInput")
    def connect_timeout_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "connectTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="insecureTlsInput")
    def insecure_tls_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecureTlsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="pemBundleInput")
    def pem_bundle_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pemBundleInput"))

    @builtins.property
    @jsii.member(jsii_name="pemJsonInput")
    def pem_json_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pemJsonInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginNameInput")
    def plugin_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginNameInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatementsInput")
    def root_rotation_statements_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rootRotationStatementsInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsInput")
    def tls_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tlsInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameTemplateInput")
    def username_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyConnectionInput")
    def verify_connection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verifyConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedRoles")
    def allowed_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedRoles"))

    @allowed_roles.setter
    def allowed_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc44dbe3c4d70769a5011fe595a7ca9fbabf04daccd7dbea87f2f450020dad01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedRoles", value)

    @builtins.property
    @jsii.member(jsii_name="connectTimeout")
    def connect_timeout(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "connectTimeout"))

    @connect_timeout.setter
    def connect_timeout(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3a6bfeca7b5f45745b37eeb2b01eded4994debeacb4f326583c9d843c51d1f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectTimeout", value)

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "data"))

    @data.setter
    def data(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06202c703872010b6105e34155f654d254fbfcf0d34588920fe63cfc5a454701)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value)

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4103bf271f58247a504745e89df13bd02dad050e2d83dc5102503ae95f11dab8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value)

    @builtins.property
    @jsii.member(jsii_name="insecureTls")
    def insecure_tls(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "insecureTls"))

    @insecure_tls.setter
    def insecure_tls(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__371c360ef31460c05a5fa75ae168d0ec7bfae489af4f17f6f1e5e5769cbbbf63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insecureTls", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2d765c44be04437a00a2b2ffddb43c37954b9e8c173d5f3530c4c88b3e8f793)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e855c2aa625bf4c47eb0b8594afd478c78e86e42d8464ff9ee1c808239734ed5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="pemBundle")
    def pem_bundle(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pemBundle"))

    @pem_bundle.setter
    def pem_bundle(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23b135aada3f4184de209d584dcb2b5fec37d01cba7ce6cbba855b10d1080704)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pemBundle", value)

    @builtins.property
    @jsii.member(jsii_name="pemJson")
    def pem_json(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pemJson"))

    @pem_json.setter
    def pem_json(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e93a359314025b13ebef60306de979b3edc6c81e40d01ac320d6c4c210fe8892)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pemJson", value)

    @builtins.property
    @jsii.member(jsii_name="pluginName")
    def plugin_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginName"))

    @plugin_name.setter
    def plugin_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a005f70edb8d1d7f4b78e746c135470df13cba976e9bc0d4b13168abfd4aab57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginName", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30d16343326889797547a0c0939ddb73725abce2790a195af8d22a73e3e63d2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatements")
    def root_rotation_statements(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rootRotationStatements"))

    @root_rotation_statements.setter
    def root_rotation_statements(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__265d6c5edf4291bf5bb8d206d231cd668ee008a489d250dce48e6619cc5508bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootRotationStatements", value)

    @builtins.property
    @jsii.member(jsii_name="tls")
    def tls(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tls"))

    @tls.setter
    def tls(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8ac7615dd7668bd4ab4e7e5fc75fa0ab3317754b68cea04dbd58717e0172db6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tls", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57d17664221609e709a2ac3f3f78c874075fb368ed90d295d077b67e92bfd861)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="usernameTemplate")
    def username_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usernameTemplate"))

    @username_template.setter
    def username_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7de9cd771b44565734291cc1b585eb1da870a99df8c3536171702b28ecbe659)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usernameTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="verifyConnection")
    def verify_connection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verifyConnection"))

    @verify_connection.setter
    def verify_connection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0e95a2e5651ec13a129406ee70a4f9fd7a7b0fac70b072e99b3d38a0680a901)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifyConnection", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountInfluxdb]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountInfluxdb]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountInfluxdb]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99dca926d47321264a1873516dba08f40e6afc3c30816662d4d25db56c07014d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountMongodb",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "allowed_roles": "allowedRoles",
        "connection_url": "connectionUrl",
        "data": "data",
        "max_connection_lifetime": "maxConnectionLifetime",
        "max_idle_connections": "maxIdleConnections",
        "max_open_connections": "maxOpenConnections",
        "password": "password",
        "plugin_name": "pluginName",
        "root_rotation_statements": "rootRotationStatements",
        "username": "username",
        "username_template": "usernameTemplate",
        "verify_connection": "verifyConnection",
    },
)
class DatabaseSecretsMountMongodb:
    def __init__(
        self,
        *,
        name: builtins.str,
        allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection_url: typing.Optional[builtins.str] = None,
        data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_connection_lifetime: typing.Optional[jsii.Number] = None,
        max_idle_connections: typing.Optional[jsii.Number] = None,
        max_open_connections: typing.Optional[jsii.Number] = None,
        password: typing.Optional[builtins.str] = None,
        plugin_name: typing.Optional[builtins.str] = None,
        root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
        username: typing.Optional[builtins.str] = None,
        username_template: typing.Optional[builtins.str] = None,
        verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Name of the database connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        :param allowed_roles: A list of roles that are allowed to use this connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        :param connection_url: Connection string to use to connect to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#connection_url DatabaseSecretsMount#connection_url}
        :param data: A map of sensitive data to pass to the endpoint. Useful for templated connection strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        :param max_connection_lifetime: Maximum number of seconds a connection may be reused. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_connection_lifetime DatabaseSecretsMount#max_connection_lifetime}
        :param max_idle_connections: Maximum number of idle connections to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_idle_connections DatabaseSecretsMount#max_idle_connections}
        :param max_open_connections: Maximum number of open connections to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_open_connections DatabaseSecretsMount#max_open_connections}
        :param password: The root credential password used in the connection URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        :param plugin_name: Specifies the name of the plugin to use for this connection. Must be prefixed with the name of one of the supported database engine types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        :param root_rotation_statements: A list of database statements to be executed to rotate the root user's credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        :param username: The root credential username used in the connection URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        :param username_template: Username generation template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username_template DatabaseSecretsMount#username_template}
        :param verify_connection: Specifies if the connection is verified during initial configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5db3012e3b3241136c31ae686f9fe595043302c4d8fc2a53356c701037b58e23)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allowed_roles", value=allowed_roles, expected_type=type_hints["allowed_roles"])
            check_type(argname="argument connection_url", value=connection_url, expected_type=type_hints["connection_url"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument max_connection_lifetime", value=max_connection_lifetime, expected_type=type_hints["max_connection_lifetime"])
            check_type(argname="argument max_idle_connections", value=max_idle_connections, expected_type=type_hints["max_idle_connections"])
            check_type(argname="argument max_open_connections", value=max_open_connections, expected_type=type_hints["max_open_connections"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument plugin_name", value=plugin_name, expected_type=type_hints["plugin_name"])
            check_type(argname="argument root_rotation_statements", value=root_rotation_statements, expected_type=type_hints["root_rotation_statements"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument username_template", value=username_template, expected_type=type_hints["username_template"])
            check_type(argname="argument verify_connection", value=verify_connection, expected_type=type_hints["verify_connection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if allowed_roles is not None:
            self._values["allowed_roles"] = allowed_roles
        if connection_url is not None:
            self._values["connection_url"] = connection_url
        if data is not None:
            self._values["data"] = data
        if max_connection_lifetime is not None:
            self._values["max_connection_lifetime"] = max_connection_lifetime
        if max_idle_connections is not None:
            self._values["max_idle_connections"] = max_idle_connections
        if max_open_connections is not None:
            self._values["max_open_connections"] = max_open_connections
        if password is not None:
            self._values["password"] = password
        if plugin_name is not None:
            self._values["plugin_name"] = plugin_name
        if root_rotation_statements is not None:
            self._values["root_rotation_statements"] = root_rotation_statements
        if username is not None:
            self._values["username"] = username
        if username_template is not None:
            self._values["username_template"] = username_template
        if verify_connection is not None:
            self._values["verify_connection"] = verify_connection

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the database connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of roles that are allowed to use this connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        '''
        result = self._values.get("allowed_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def connection_url(self) -> typing.Optional[builtins.str]:
        '''Connection string to use to connect to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#connection_url DatabaseSecretsMount#connection_url}
        '''
        result = self._values.get("connection_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of sensitive data to pass to the endpoint. Useful for templated connection strings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def max_connection_lifetime(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of seconds a connection may be reused.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_connection_lifetime DatabaseSecretsMount#max_connection_lifetime}
        '''
        result = self._values.get("max_connection_lifetime")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_idle_connections(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of idle connections to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_idle_connections DatabaseSecretsMount#max_idle_connections}
        '''
        result = self._values.get("max_idle_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_open_connections(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of open connections to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_open_connections DatabaseSecretsMount#max_open_connections}
        '''
        result = self._values.get("max_open_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The root credential password used in the connection URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugin_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the plugin to use for this connection.

        Must be prefixed with the name of one of the supported database engine types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        '''
        result = self._values.get("plugin_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def root_rotation_statements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of database statements to be executed to rotate the root user's credentials.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        '''
        result = self._values.get("root_rotation_statements")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The root credential username used in the connection URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username_template(self) -> typing.Optional[builtins.str]:
        '''Username generation template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username_template DatabaseSecretsMount#username_template}
        '''
        result = self._values.get("username_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verify_connection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if the connection is verified during initial configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        result = self._values.get("verify_connection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseSecretsMountMongodb(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseSecretsMountMongodbList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountMongodbList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d2c4f5417e2c573f8b6f92b413918a40dc6d9acf495da532719a6547697a128)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DatabaseSecretsMountMongodbOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a0cc96c3d0fbae9529c633b9eed8aed0dbfd91b04f4e44c312f6713f6ae52af)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatabaseSecretsMountMongodbOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__658c9cc2b09da9eac458d0ab0601f12b9044f02b450c3bc1add74468a4e2a979)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f926281eb1201bbd308a1266e96191ca21f7a6d4e424b0de33e15280e5309c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a80a53de2216c5f70763ee3e8150ac4cbf739b9e23e3ac79ebfc3160da2d454)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMongodb]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMongodb]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMongodb]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8d08eb74c452f1ec730e1c3e54af41db1cf584512f3e56c0565e83eef4732a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatabaseSecretsMountMongodbOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountMongodbOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4087c891a593f6fd93f4e6ce268cb7e7fc5143d485ecef105e5a00d99f98ab7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllowedRoles")
    def reset_allowed_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedRoles", []))

    @jsii.member(jsii_name="resetConnectionUrl")
    def reset_connection_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionUrl", []))

    @jsii.member(jsii_name="resetData")
    def reset_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetData", []))

    @jsii.member(jsii_name="resetMaxConnectionLifetime")
    def reset_max_connection_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConnectionLifetime", []))

    @jsii.member(jsii_name="resetMaxIdleConnections")
    def reset_max_idle_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxIdleConnections", []))

    @jsii.member(jsii_name="resetMaxOpenConnections")
    def reset_max_open_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxOpenConnections", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPluginName")
    def reset_plugin_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginName", []))

    @jsii.member(jsii_name="resetRootRotationStatements")
    def reset_root_rotation_statements(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootRotationStatements", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @jsii.member(jsii_name="resetUsernameTemplate")
    def reset_username_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsernameTemplate", []))

    @jsii.member(jsii_name="resetVerifyConnection")
    def reset_verify_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerifyConnection", []))

    @builtins.property
    @jsii.member(jsii_name="allowedRolesInput")
    def allowed_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionUrlInput")
    def connection_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConnectionLifetimeInput")
    def max_connection_lifetime_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConnectionLifetimeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxIdleConnectionsInput")
    def max_idle_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxIdleConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxOpenConnectionsInput")
    def max_open_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxOpenConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginNameInput")
    def plugin_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatementsInput")
    def root_rotation_statements_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rootRotationStatementsInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameTemplateInput")
    def username_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyConnectionInput")
    def verify_connection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verifyConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedRoles")
    def allowed_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedRoles"))

    @allowed_roles.setter
    def allowed_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eca2329fbc7b2399195b34b941cdbd816983e5d8aa8e23ff681ff14a6e01d7a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedRoles", value)

    @builtins.property
    @jsii.member(jsii_name="connectionUrl")
    def connection_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionUrl"))

    @connection_url.setter
    def connection_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e55e63ee4c556db9a12a4e465d3a3bb87e3171db2f3b1ba7ef9c05e4cfa43d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionUrl", value)

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "data"))

    @data.setter
    def data(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa75de15fcd55525c91c35cbf0c2e030955776d1c143b2cf0be9aad96082fce0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value)

    @builtins.property
    @jsii.member(jsii_name="maxConnectionLifetime")
    def max_connection_lifetime(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConnectionLifetime"))

    @max_connection_lifetime.setter
    def max_connection_lifetime(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db816af2ef8852dae976791b83c8c2f0af935095331b67acb18dffa66ec80624)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnectionLifetime", value)

    @builtins.property
    @jsii.member(jsii_name="maxIdleConnections")
    def max_idle_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIdleConnections"))

    @max_idle_connections.setter
    def max_idle_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5100203e906f37688b45ff8a532f46db2db0413127483d46b9fdbe4e323f535)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxIdleConnections", value)

    @builtins.property
    @jsii.member(jsii_name="maxOpenConnections")
    def max_open_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxOpenConnections"))

    @max_open_connections.setter
    def max_open_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ad1c9a8b8f2358da061b81174bd51ac2aac8837cd8d64482c122737d4697a3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxOpenConnections", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10eabfc67564e83a3bf4e303b9ac11efb4cc9493b0e8773e937922259eeb1c6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff1dbce09e080db787f89da89418ddb4fa083b31c36e670703fb833192d5fc8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="pluginName")
    def plugin_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginName"))

    @plugin_name.setter
    def plugin_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56e68eeedb14f070e67555b4cb083a40e81123fb5f7842ce457619b1763d1a9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginName", value)

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatements")
    def root_rotation_statements(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rootRotationStatements"))

    @root_rotation_statements.setter
    def root_rotation_statements(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9def142611fab8c1f0c99217006f1382739a4fcb26bea621396672ae0e19b15c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootRotationStatements", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49afa36a8348d92dcd9d9a7a1025b44b758430f4dd159529736bc5e256cea2b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="usernameTemplate")
    def username_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usernameTemplate"))

    @username_template.setter
    def username_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ace1d294410d599ba613939d0aed9d75d9cfcd4fd11a5c4431c1d18e384b193)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usernameTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="verifyConnection")
    def verify_connection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verifyConnection"))

    @verify_connection.setter
    def verify_connection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5900c3784c53b1586a93beba32cc37932fa921bc3b8cb5889adb3a5c51d919d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifyConnection", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMongodb]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMongodb]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMongodb]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c58add0e2fe41e867cbe163d79d57574d6b070f31f54fe360f8c2c5a5e871d52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountMongodbatlas",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "private_key": "privateKey",
        "project_id": "projectId",
        "public_key": "publicKey",
        "allowed_roles": "allowedRoles",
        "data": "data",
        "plugin_name": "pluginName",
        "root_rotation_statements": "rootRotationStatements",
        "verify_connection": "verifyConnection",
    },
)
class DatabaseSecretsMountMongodbatlas:
    def __init__(
        self,
        *,
        name: builtins.str,
        private_key: builtins.str,
        project_id: builtins.str,
        public_key: builtins.str,
        allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        plugin_name: typing.Optional[builtins.str] = None,
        root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
        verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Name of the database connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        :param private_key: The Private Programmatic API Key used to connect with MongoDB Atlas API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#private_key DatabaseSecretsMount#private_key}
        :param project_id: The Project ID the Database User should be created within. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#project_id DatabaseSecretsMount#project_id}
        :param public_key: The Public Programmatic API Key used to authenticate with the MongoDB Atlas API. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#public_key DatabaseSecretsMount#public_key}
        :param allowed_roles: A list of roles that are allowed to use this connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        :param data: A map of sensitive data to pass to the endpoint. Useful for templated connection strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        :param plugin_name: Specifies the name of the plugin to use for this connection. Must be prefixed with the name of one of the supported database engine types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        :param root_rotation_statements: A list of database statements to be executed to rotate the root user's credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        :param verify_connection: Specifies if the connection is verified during initial configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aab914808d24e2d155521935ec3a9d4e9fb73097e6b32682d50b5233765529b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument public_key", value=public_key, expected_type=type_hints["public_key"])
            check_type(argname="argument allowed_roles", value=allowed_roles, expected_type=type_hints["allowed_roles"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument plugin_name", value=plugin_name, expected_type=type_hints["plugin_name"])
            check_type(argname="argument root_rotation_statements", value=root_rotation_statements, expected_type=type_hints["root_rotation_statements"])
            check_type(argname="argument verify_connection", value=verify_connection, expected_type=type_hints["verify_connection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "private_key": private_key,
            "project_id": project_id,
            "public_key": public_key,
        }
        if allowed_roles is not None:
            self._values["allowed_roles"] = allowed_roles
        if data is not None:
            self._values["data"] = data
        if plugin_name is not None:
            self._values["plugin_name"] = plugin_name
        if root_rotation_statements is not None:
            self._values["root_rotation_statements"] = root_rotation_statements
        if verify_connection is not None:
            self._values["verify_connection"] = verify_connection

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the database connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def private_key(self) -> builtins.str:
        '''The Private Programmatic API Key used to connect with MongoDB Atlas API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#private_key DatabaseSecretsMount#private_key}
        '''
        result = self._values.get("private_key")
        assert result is not None, "Required property 'private_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_id(self) -> builtins.str:
        '''The Project ID the Database User should be created within.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#project_id DatabaseSecretsMount#project_id}
        '''
        result = self._values.get("project_id")
        assert result is not None, "Required property 'project_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def public_key(self) -> builtins.str:
        '''The Public Programmatic API Key used to authenticate with the MongoDB Atlas API.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#public_key DatabaseSecretsMount#public_key}
        '''
        result = self._values.get("public_key")
        assert result is not None, "Required property 'public_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of roles that are allowed to use this connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        '''
        result = self._values.get("allowed_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def data(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of sensitive data to pass to the endpoint. Useful for templated connection strings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def plugin_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the plugin to use for this connection.

        Must be prefixed with the name of one of the supported database engine types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        '''
        result = self._values.get("plugin_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def root_rotation_statements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of database statements to be executed to rotate the root user's credentials.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        '''
        result = self._values.get("root_rotation_statements")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def verify_connection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if the connection is verified during initial configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        result = self._values.get("verify_connection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseSecretsMountMongodbatlas(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseSecretsMountMongodbatlasList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountMongodbatlasList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbb78b0cc86baa87e7244056c2aa3d0e6f3b9659268964a046c76bdb5478e444)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatabaseSecretsMountMongodbatlasOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cc0d602855f2d4d5c28ef870dbef3bd0c91d210ec8853d68e1be606061914e1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatabaseSecretsMountMongodbatlasOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a749ac288c80241be0bb7036253b9a4a88447d69a8a701c424708fe46c79047)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f82cce7b84e95252c7d0011c1db53170d9cca075f6f55d4d19e294c2dd2cac7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__10fa58e24ea4fb11451a3817a6c7c2b4a56a23393e969fca43eb74abd59d0cfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMongodbatlas]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMongodbatlas]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMongodbatlas]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc06a2d411d825cfa99896e26e5cbe0193f5ebf276351c26a41cd3e47dd1f829)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatabaseSecretsMountMongodbatlasOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountMongodbatlasOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf3ce5f4cc44c3bd987e9217492a49785244c83ed8327e9eb218179e73c85057)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllowedRoles")
    def reset_allowed_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedRoles", []))

    @jsii.member(jsii_name="resetData")
    def reset_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetData", []))

    @jsii.member(jsii_name="resetPluginName")
    def reset_plugin_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginName", []))

    @jsii.member(jsii_name="resetRootRotationStatements")
    def reset_root_rotation_statements(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootRotationStatements", []))

    @jsii.member(jsii_name="resetVerifyConnection")
    def reset_verify_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerifyConnection", []))

    @builtins.property
    @jsii.member(jsii_name="allowedRolesInput")
    def allowed_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginNameInput")
    def plugin_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginNameInput"))

    @builtins.property
    @jsii.member(jsii_name="privateKeyInput")
    def private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="projectIdInput")
    def project_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectIdInput"))

    @builtins.property
    @jsii.member(jsii_name="publicKeyInput")
    def public_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatementsInput")
    def root_rotation_statements_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rootRotationStatementsInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyConnectionInput")
    def verify_connection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verifyConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedRoles")
    def allowed_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedRoles"))

    @allowed_roles.setter
    def allowed_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c1218d34e82044da65e3c53796b35b6e83403d35f74d915d9bef0ecf9cbac5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedRoles", value)

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "data"))

    @data.setter
    def data(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd992fd2949590ebfa8874145925f82d025eb89076fb936950a2f9ac0d38a3d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac99ad508721783cc46f1e243cde238bb5a47141e4e3bfaf4978f11f14e256a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="pluginName")
    def plugin_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginName"))

    @plugin_name.setter
    def plugin_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__170162b8736b4c52fd6adc1bf68bfeb059d22410e53eb23c8fd14a69db51d02b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginName", value)

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73fcf89c66494d4f57edec8bf557502540edfa8a084a86c1f1a6858dfb7d7755)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value)

    @builtins.property
    @jsii.member(jsii_name="projectId")
    def project_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectId"))

    @project_id.setter
    def project_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71076eeba7b335415dd92e5c849dfabede1dc1620be61863ed33cfd57bb42e20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectId", value)

    @builtins.property
    @jsii.member(jsii_name="publicKey")
    def public_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publicKey"))

    @public_key.setter
    def public_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__743b3cf7fdb96905a1ae4701de2ea6fcbb50fd359ca330464fe320f8931fbb0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicKey", value)

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatements")
    def root_rotation_statements(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rootRotationStatements"))

    @root_rotation_statements.setter
    def root_rotation_statements(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a4f613029ccdb15e24d484c5bac7c62a87476ccf87bbb69ee5a3e968f881e52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootRotationStatements", value)

    @builtins.property
    @jsii.member(jsii_name="verifyConnection")
    def verify_connection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verifyConnection"))

    @verify_connection.setter
    def verify_connection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a33073120ad06bddb619c2632dc56f128aa5d25d9354f234f41819480deffb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifyConnection", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMongodbatlas]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMongodbatlas]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMongodbatlas]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27482a00ba84e5723953f91ac8ca49d835a611966d17559475f158610f82fa32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountMssql",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "allowed_roles": "allowedRoles",
        "connection_url": "connectionUrl",
        "contained_db": "containedDb",
        "data": "data",
        "disable_escaping": "disableEscaping",
        "max_connection_lifetime": "maxConnectionLifetime",
        "max_idle_connections": "maxIdleConnections",
        "max_open_connections": "maxOpenConnections",
        "password": "password",
        "plugin_name": "pluginName",
        "root_rotation_statements": "rootRotationStatements",
        "username": "username",
        "username_template": "usernameTemplate",
        "verify_connection": "verifyConnection",
    },
)
class DatabaseSecretsMountMssql:
    def __init__(
        self,
        *,
        name: builtins.str,
        allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection_url: typing.Optional[builtins.str] = None,
        contained_db: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        disable_escaping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_connection_lifetime: typing.Optional[jsii.Number] = None,
        max_idle_connections: typing.Optional[jsii.Number] = None,
        max_open_connections: typing.Optional[jsii.Number] = None,
        password: typing.Optional[builtins.str] = None,
        plugin_name: typing.Optional[builtins.str] = None,
        root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
        username: typing.Optional[builtins.str] = None,
        username_template: typing.Optional[builtins.str] = None,
        verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Name of the database connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        :param allowed_roles: A list of roles that are allowed to use this connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        :param connection_url: Connection string to use to connect to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#connection_url DatabaseSecretsMount#connection_url}
        :param contained_db: Set to true when the target is a Contained Database, e.g. AzureSQL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#contained_db DatabaseSecretsMount#contained_db}
        :param data: A map of sensitive data to pass to the endpoint. Useful for templated connection strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        :param disable_escaping: Disable special character escaping in username and password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#disable_escaping DatabaseSecretsMount#disable_escaping}
        :param max_connection_lifetime: Maximum number of seconds a connection may be reused. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_connection_lifetime DatabaseSecretsMount#max_connection_lifetime}
        :param max_idle_connections: Maximum number of idle connections to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_idle_connections DatabaseSecretsMount#max_idle_connections}
        :param max_open_connections: Maximum number of open connections to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_open_connections DatabaseSecretsMount#max_open_connections}
        :param password: The root credential password used in the connection URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        :param plugin_name: Specifies the name of the plugin to use for this connection. Must be prefixed with the name of one of the supported database engine types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        :param root_rotation_statements: A list of database statements to be executed to rotate the root user's credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        :param username: The root credential username used in the connection URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        :param username_template: Username generation template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username_template DatabaseSecretsMount#username_template}
        :param verify_connection: Specifies if the connection is verified during initial configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ca5ad366088df2425fdb1170cc75e211976f349ac8aa8e94d02534c5431db83)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allowed_roles", value=allowed_roles, expected_type=type_hints["allowed_roles"])
            check_type(argname="argument connection_url", value=connection_url, expected_type=type_hints["connection_url"])
            check_type(argname="argument contained_db", value=contained_db, expected_type=type_hints["contained_db"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument disable_escaping", value=disable_escaping, expected_type=type_hints["disable_escaping"])
            check_type(argname="argument max_connection_lifetime", value=max_connection_lifetime, expected_type=type_hints["max_connection_lifetime"])
            check_type(argname="argument max_idle_connections", value=max_idle_connections, expected_type=type_hints["max_idle_connections"])
            check_type(argname="argument max_open_connections", value=max_open_connections, expected_type=type_hints["max_open_connections"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument plugin_name", value=plugin_name, expected_type=type_hints["plugin_name"])
            check_type(argname="argument root_rotation_statements", value=root_rotation_statements, expected_type=type_hints["root_rotation_statements"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument username_template", value=username_template, expected_type=type_hints["username_template"])
            check_type(argname="argument verify_connection", value=verify_connection, expected_type=type_hints["verify_connection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if allowed_roles is not None:
            self._values["allowed_roles"] = allowed_roles
        if connection_url is not None:
            self._values["connection_url"] = connection_url
        if contained_db is not None:
            self._values["contained_db"] = contained_db
        if data is not None:
            self._values["data"] = data
        if disable_escaping is not None:
            self._values["disable_escaping"] = disable_escaping
        if max_connection_lifetime is not None:
            self._values["max_connection_lifetime"] = max_connection_lifetime
        if max_idle_connections is not None:
            self._values["max_idle_connections"] = max_idle_connections
        if max_open_connections is not None:
            self._values["max_open_connections"] = max_open_connections
        if password is not None:
            self._values["password"] = password
        if plugin_name is not None:
            self._values["plugin_name"] = plugin_name
        if root_rotation_statements is not None:
            self._values["root_rotation_statements"] = root_rotation_statements
        if username is not None:
            self._values["username"] = username
        if username_template is not None:
            self._values["username_template"] = username_template
        if verify_connection is not None:
            self._values["verify_connection"] = verify_connection

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the database connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of roles that are allowed to use this connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        '''
        result = self._values.get("allowed_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def connection_url(self) -> typing.Optional[builtins.str]:
        '''Connection string to use to connect to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#connection_url DatabaseSecretsMount#connection_url}
        '''
        result = self._values.get("connection_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def contained_db(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to true when the target is a Contained Database, e.g. AzureSQL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#contained_db DatabaseSecretsMount#contained_db}
        '''
        result = self._values.get("contained_db")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def data(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of sensitive data to pass to the endpoint. Useful for templated connection strings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def disable_escaping(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable special character escaping in username and password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#disable_escaping DatabaseSecretsMount#disable_escaping}
        '''
        result = self._values.get("disable_escaping")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_connection_lifetime(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of seconds a connection may be reused.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_connection_lifetime DatabaseSecretsMount#max_connection_lifetime}
        '''
        result = self._values.get("max_connection_lifetime")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_idle_connections(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of idle connections to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_idle_connections DatabaseSecretsMount#max_idle_connections}
        '''
        result = self._values.get("max_idle_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_open_connections(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of open connections to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_open_connections DatabaseSecretsMount#max_open_connections}
        '''
        result = self._values.get("max_open_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The root credential password used in the connection URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugin_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the plugin to use for this connection.

        Must be prefixed with the name of one of the supported database engine types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        '''
        result = self._values.get("plugin_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def root_rotation_statements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of database statements to be executed to rotate the root user's credentials.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        '''
        result = self._values.get("root_rotation_statements")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The root credential username used in the connection URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username_template(self) -> typing.Optional[builtins.str]:
        '''Username generation template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username_template DatabaseSecretsMount#username_template}
        '''
        result = self._values.get("username_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verify_connection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if the connection is verified during initial configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        result = self._values.get("verify_connection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseSecretsMountMssql(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseSecretsMountMssqlList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountMssqlList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04c042a60690181ac2884ad2ea0c8f87a72a65c853b8b776cd9886e814139b96)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DatabaseSecretsMountMssqlOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36428bedcd51ba172bd3da4410f826b8abd21ee2997e9d3717490ba3f786e4b1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatabaseSecretsMountMssqlOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54803089faa75286837b341f3f35c4c0c4139cd523e520365bd1ac3b9695e749)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1ce51a600b1c9bfde83f67fa384a7d0be8fc45d09c5dd4924d3da2c7e4dc0b8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d3e977de8455e97fd35b55f8aef19f28c5b06556316480da0bc17a549449093)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMssql]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMssql]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMssql]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39a449b226f353cb57d1e159925b0464c7e56285ae0a2526eb824fc419c43c9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatabaseSecretsMountMssqlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountMssqlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38a72e183dfa88e6c8c6813de5657bf8181ca00b4e44ca979ddf241c13a55ff2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllowedRoles")
    def reset_allowed_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedRoles", []))

    @jsii.member(jsii_name="resetConnectionUrl")
    def reset_connection_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionUrl", []))

    @jsii.member(jsii_name="resetContainedDb")
    def reset_contained_db(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainedDb", []))

    @jsii.member(jsii_name="resetData")
    def reset_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetData", []))

    @jsii.member(jsii_name="resetDisableEscaping")
    def reset_disable_escaping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableEscaping", []))

    @jsii.member(jsii_name="resetMaxConnectionLifetime")
    def reset_max_connection_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConnectionLifetime", []))

    @jsii.member(jsii_name="resetMaxIdleConnections")
    def reset_max_idle_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxIdleConnections", []))

    @jsii.member(jsii_name="resetMaxOpenConnections")
    def reset_max_open_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxOpenConnections", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPluginName")
    def reset_plugin_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginName", []))

    @jsii.member(jsii_name="resetRootRotationStatements")
    def reset_root_rotation_statements(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootRotationStatements", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @jsii.member(jsii_name="resetUsernameTemplate")
    def reset_username_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsernameTemplate", []))

    @jsii.member(jsii_name="resetVerifyConnection")
    def reset_verify_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerifyConnection", []))

    @builtins.property
    @jsii.member(jsii_name="allowedRolesInput")
    def allowed_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionUrlInput")
    def connection_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="containedDbInput")
    def contained_db_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "containedDbInput"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="disableEscapingInput")
    def disable_escaping_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableEscapingInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConnectionLifetimeInput")
    def max_connection_lifetime_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConnectionLifetimeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxIdleConnectionsInput")
    def max_idle_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxIdleConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxOpenConnectionsInput")
    def max_open_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxOpenConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginNameInput")
    def plugin_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatementsInput")
    def root_rotation_statements_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rootRotationStatementsInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameTemplateInput")
    def username_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyConnectionInput")
    def verify_connection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verifyConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedRoles")
    def allowed_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedRoles"))

    @allowed_roles.setter
    def allowed_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab98eb662a365876ee2e5081b66cdc20c15a9ff876512e9b70c76bf91b5423b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedRoles", value)

    @builtins.property
    @jsii.member(jsii_name="connectionUrl")
    def connection_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionUrl"))

    @connection_url.setter
    def connection_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77beada7d25145f6e7da8f2b819ee54e3fbe15ca3519f1adc6743da06d06e1c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionUrl", value)

    @builtins.property
    @jsii.member(jsii_name="containedDb")
    def contained_db(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "containedDb"))

    @contained_db.setter
    def contained_db(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9996fcfe749f66f76831bc410999f25e7e27521a77e7684e45228c18ce3b371f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containedDb", value)

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "data"))

    @data.setter
    def data(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba2107a22b94aee2ad1c669fea30c92982b7a26ffd10d6beb678e9f31f00706e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value)

    @builtins.property
    @jsii.member(jsii_name="disableEscaping")
    def disable_escaping(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableEscaping"))

    @disable_escaping.setter
    def disable_escaping(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5394bd93d6987233f19b7cd14db12d8f2275cb7296ce4a77582a3f55a6aa305c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableEscaping", value)

    @builtins.property
    @jsii.member(jsii_name="maxConnectionLifetime")
    def max_connection_lifetime(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConnectionLifetime"))

    @max_connection_lifetime.setter
    def max_connection_lifetime(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__572aa7756894477c27e977845ddc7ef28a769caacc426ddc3abb48d9df1d8ff3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnectionLifetime", value)

    @builtins.property
    @jsii.member(jsii_name="maxIdleConnections")
    def max_idle_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIdleConnections"))

    @max_idle_connections.setter
    def max_idle_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7da06741afc2a5884f807c59a259276aa67c347fead60f6e44ab262a178af6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxIdleConnections", value)

    @builtins.property
    @jsii.member(jsii_name="maxOpenConnections")
    def max_open_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxOpenConnections"))

    @max_open_connections.setter
    def max_open_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4da910eabf66178a984765e226ae888ee443205458014d569037787eb0c1b44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxOpenConnections", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e4232727cebc4c47b7d359ad26d830ac14673d3f4ffcae8d22f1b1898d45e51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5de6d4e7453c02ab5503b22360ce6ac79bc861726ae419d2bff510d2789b6284)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="pluginName")
    def plugin_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginName"))

    @plugin_name.setter
    def plugin_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb081b4e69623f0e24db306e78b800dbdca1c739cecb5cba2f2b54b61a1d896f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginName", value)

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatements")
    def root_rotation_statements(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rootRotationStatements"))

    @root_rotation_statements.setter
    def root_rotation_statements(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8383ca612d368521c10b87622f12222781009457c29cbb22adf88fde259ab98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootRotationStatements", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35169712a65a8bbd8987ed6577363e0c8b02d739a9c3831327b6baf7ad48d2e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="usernameTemplate")
    def username_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usernameTemplate"))

    @username_template.setter
    def username_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__879d06faab058cb97c2215b84e5d31f022af3be1d49a9c7f9d38a58a50bdba6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usernameTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="verifyConnection")
    def verify_connection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verifyConnection"))

    @verify_connection.setter
    def verify_connection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19a0d11d8ca37d146716bb9ae288db93773d9fb3a6469a9e7ea74a45b66fba15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifyConnection", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMssql]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMssql]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMssql]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aba4eef3f2e22ae2a004f2a9a11acf22370022fd32297b6b49c4bf51101fe57e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountMysql",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "allowed_roles": "allowedRoles",
        "connection_url": "connectionUrl",
        "data": "data",
        "max_connection_lifetime": "maxConnectionLifetime",
        "max_idle_connections": "maxIdleConnections",
        "max_open_connections": "maxOpenConnections",
        "password": "password",
        "plugin_name": "pluginName",
        "root_rotation_statements": "rootRotationStatements",
        "tls_ca": "tlsCa",
        "tls_certificate_key": "tlsCertificateKey",
        "username": "username",
        "username_template": "usernameTemplate",
        "verify_connection": "verifyConnection",
    },
)
class DatabaseSecretsMountMysql:
    def __init__(
        self,
        *,
        name: builtins.str,
        allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection_url: typing.Optional[builtins.str] = None,
        data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_connection_lifetime: typing.Optional[jsii.Number] = None,
        max_idle_connections: typing.Optional[jsii.Number] = None,
        max_open_connections: typing.Optional[jsii.Number] = None,
        password: typing.Optional[builtins.str] = None,
        plugin_name: typing.Optional[builtins.str] = None,
        root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
        tls_ca: typing.Optional[builtins.str] = None,
        tls_certificate_key: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
        username_template: typing.Optional[builtins.str] = None,
        verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Name of the database connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        :param allowed_roles: A list of roles that are allowed to use this connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        :param connection_url: Connection string to use to connect to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#connection_url DatabaseSecretsMount#connection_url}
        :param data: A map of sensitive data to pass to the endpoint. Useful for templated connection strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        :param max_connection_lifetime: Maximum number of seconds a connection may be reused. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_connection_lifetime DatabaseSecretsMount#max_connection_lifetime}
        :param max_idle_connections: Maximum number of idle connections to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_idle_connections DatabaseSecretsMount#max_idle_connections}
        :param max_open_connections: Maximum number of open connections to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_open_connections DatabaseSecretsMount#max_open_connections}
        :param password: The root credential password used in the connection URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        :param plugin_name: Specifies the name of the plugin to use for this connection. Must be prefixed with the name of one of the supported database engine types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        :param root_rotation_statements: A list of database statements to be executed to rotate the root user's credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        :param tls_ca: x509 CA file for validating the certificate presented by the MySQL server. Must be PEM encoded. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#tls_ca DatabaseSecretsMount#tls_ca}
        :param tls_certificate_key: x509 certificate for connecting to the database. This must be a PEM encoded version of the private key and the certificate combined. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#tls_certificate_key DatabaseSecretsMount#tls_certificate_key}
        :param username: The root credential username used in the connection URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        :param username_template: Username generation template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username_template DatabaseSecretsMount#username_template}
        :param verify_connection: Specifies if the connection is verified during initial configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__602c3f62440dd774c77c2feb86ae3dbecb381eec133e321afb73f8c2c1b6ea6a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allowed_roles", value=allowed_roles, expected_type=type_hints["allowed_roles"])
            check_type(argname="argument connection_url", value=connection_url, expected_type=type_hints["connection_url"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument max_connection_lifetime", value=max_connection_lifetime, expected_type=type_hints["max_connection_lifetime"])
            check_type(argname="argument max_idle_connections", value=max_idle_connections, expected_type=type_hints["max_idle_connections"])
            check_type(argname="argument max_open_connections", value=max_open_connections, expected_type=type_hints["max_open_connections"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument plugin_name", value=plugin_name, expected_type=type_hints["plugin_name"])
            check_type(argname="argument root_rotation_statements", value=root_rotation_statements, expected_type=type_hints["root_rotation_statements"])
            check_type(argname="argument tls_ca", value=tls_ca, expected_type=type_hints["tls_ca"])
            check_type(argname="argument tls_certificate_key", value=tls_certificate_key, expected_type=type_hints["tls_certificate_key"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument username_template", value=username_template, expected_type=type_hints["username_template"])
            check_type(argname="argument verify_connection", value=verify_connection, expected_type=type_hints["verify_connection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if allowed_roles is not None:
            self._values["allowed_roles"] = allowed_roles
        if connection_url is not None:
            self._values["connection_url"] = connection_url
        if data is not None:
            self._values["data"] = data
        if max_connection_lifetime is not None:
            self._values["max_connection_lifetime"] = max_connection_lifetime
        if max_idle_connections is not None:
            self._values["max_idle_connections"] = max_idle_connections
        if max_open_connections is not None:
            self._values["max_open_connections"] = max_open_connections
        if password is not None:
            self._values["password"] = password
        if plugin_name is not None:
            self._values["plugin_name"] = plugin_name
        if root_rotation_statements is not None:
            self._values["root_rotation_statements"] = root_rotation_statements
        if tls_ca is not None:
            self._values["tls_ca"] = tls_ca
        if tls_certificate_key is not None:
            self._values["tls_certificate_key"] = tls_certificate_key
        if username is not None:
            self._values["username"] = username
        if username_template is not None:
            self._values["username_template"] = username_template
        if verify_connection is not None:
            self._values["verify_connection"] = verify_connection

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the database connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of roles that are allowed to use this connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        '''
        result = self._values.get("allowed_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def connection_url(self) -> typing.Optional[builtins.str]:
        '''Connection string to use to connect to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#connection_url DatabaseSecretsMount#connection_url}
        '''
        result = self._values.get("connection_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of sensitive data to pass to the endpoint. Useful for templated connection strings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def max_connection_lifetime(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of seconds a connection may be reused.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_connection_lifetime DatabaseSecretsMount#max_connection_lifetime}
        '''
        result = self._values.get("max_connection_lifetime")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_idle_connections(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of idle connections to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_idle_connections DatabaseSecretsMount#max_idle_connections}
        '''
        result = self._values.get("max_idle_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_open_connections(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of open connections to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_open_connections DatabaseSecretsMount#max_open_connections}
        '''
        result = self._values.get("max_open_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The root credential password used in the connection URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugin_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the plugin to use for this connection.

        Must be prefixed with the name of one of the supported database engine types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        '''
        result = self._values.get("plugin_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def root_rotation_statements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of database statements to be executed to rotate the root user's credentials.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        '''
        result = self._values.get("root_rotation_statements")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tls_ca(self) -> typing.Optional[builtins.str]:
        '''x509 CA file for validating the certificate presented by the MySQL server. Must be PEM encoded.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#tls_ca DatabaseSecretsMount#tls_ca}
        '''
        result = self._values.get("tls_ca")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tls_certificate_key(self) -> typing.Optional[builtins.str]:
        '''x509 certificate for connecting to the database.

        This must be a PEM encoded version of the private key and the certificate combined.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#tls_certificate_key DatabaseSecretsMount#tls_certificate_key}
        '''
        result = self._values.get("tls_certificate_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The root credential username used in the connection URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username_template(self) -> typing.Optional[builtins.str]:
        '''Username generation template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username_template DatabaseSecretsMount#username_template}
        '''
        result = self._values.get("username_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verify_connection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if the connection is verified during initial configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        result = self._values.get("verify_connection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseSecretsMountMysql(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountMysqlAurora",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "allowed_roles": "allowedRoles",
        "connection_url": "connectionUrl",
        "data": "data",
        "max_connection_lifetime": "maxConnectionLifetime",
        "max_idle_connections": "maxIdleConnections",
        "max_open_connections": "maxOpenConnections",
        "password": "password",
        "plugin_name": "pluginName",
        "root_rotation_statements": "rootRotationStatements",
        "username": "username",
        "username_template": "usernameTemplate",
        "verify_connection": "verifyConnection",
    },
)
class DatabaseSecretsMountMysqlAurora:
    def __init__(
        self,
        *,
        name: builtins.str,
        allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection_url: typing.Optional[builtins.str] = None,
        data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_connection_lifetime: typing.Optional[jsii.Number] = None,
        max_idle_connections: typing.Optional[jsii.Number] = None,
        max_open_connections: typing.Optional[jsii.Number] = None,
        password: typing.Optional[builtins.str] = None,
        plugin_name: typing.Optional[builtins.str] = None,
        root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
        username: typing.Optional[builtins.str] = None,
        username_template: typing.Optional[builtins.str] = None,
        verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Name of the database connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        :param allowed_roles: A list of roles that are allowed to use this connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        :param connection_url: Connection string to use to connect to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#connection_url DatabaseSecretsMount#connection_url}
        :param data: A map of sensitive data to pass to the endpoint. Useful for templated connection strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        :param max_connection_lifetime: Maximum number of seconds a connection may be reused. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_connection_lifetime DatabaseSecretsMount#max_connection_lifetime}
        :param max_idle_connections: Maximum number of idle connections to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_idle_connections DatabaseSecretsMount#max_idle_connections}
        :param max_open_connections: Maximum number of open connections to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_open_connections DatabaseSecretsMount#max_open_connections}
        :param password: The root credential password used in the connection URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        :param plugin_name: Specifies the name of the plugin to use for this connection. Must be prefixed with the name of one of the supported database engine types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        :param root_rotation_statements: A list of database statements to be executed to rotate the root user's credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        :param username: The root credential username used in the connection URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        :param username_template: Username generation template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username_template DatabaseSecretsMount#username_template}
        :param verify_connection: Specifies if the connection is verified during initial configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82c06db88c427c5286f5e891a1d58d37870d0195a8fc8002b7515ee88cfb418f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allowed_roles", value=allowed_roles, expected_type=type_hints["allowed_roles"])
            check_type(argname="argument connection_url", value=connection_url, expected_type=type_hints["connection_url"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument max_connection_lifetime", value=max_connection_lifetime, expected_type=type_hints["max_connection_lifetime"])
            check_type(argname="argument max_idle_connections", value=max_idle_connections, expected_type=type_hints["max_idle_connections"])
            check_type(argname="argument max_open_connections", value=max_open_connections, expected_type=type_hints["max_open_connections"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument plugin_name", value=plugin_name, expected_type=type_hints["plugin_name"])
            check_type(argname="argument root_rotation_statements", value=root_rotation_statements, expected_type=type_hints["root_rotation_statements"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument username_template", value=username_template, expected_type=type_hints["username_template"])
            check_type(argname="argument verify_connection", value=verify_connection, expected_type=type_hints["verify_connection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if allowed_roles is not None:
            self._values["allowed_roles"] = allowed_roles
        if connection_url is not None:
            self._values["connection_url"] = connection_url
        if data is not None:
            self._values["data"] = data
        if max_connection_lifetime is not None:
            self._values["max_connection_lifetime"] = max_connection_lifetime
        if max_idle_connections is not None:
            self._values["max_idle_connections"] = max_idle_connections
        if max_open_connections is not None:
            self._values["max_open_connections"] = max_open_connections
        if password is not None:
            self._values["password"] = password
        if plugin_name is not None:
            self._values["plugin_name"] = plugin_name
        if root_rotation_statements is not None:
            self._values["root_rotation_statements"] = root_rotation_statements
        if username is not None:
            self._values["username"] = username
        if username_template is not None:
            self._values["username_template"] = username_template
        if verify_connection is not None:
            self._values["verify_connection"] = verify_connection

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the database connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of roles that are allowed to use this connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        '''
        result = self._values.get("allowed_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def connection_url(self) -> typing.Optional[builtins.str]:
        '''Connection string to use to connect to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#connection_url DatabaseSecretsMount#connection_url}
        '''
        result = self._values.get("connection_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of sensitive data to pass to the endpoint. Useful for templated connection strings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def max_connection_lifetime(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of seconds a connection may be reused.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_connection_lifetime DatabaseSecretsMount#max_connection_lifetime}
        '''
        result = self._values.get("max_connection_lifetime")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_idle_connections(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of idle connections to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_idle_connections DatabaseSecretsMount#max_idle_connections}
        '''
        result = self._values.get("max_idle_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_open_connections(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of open connections to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_open_connections DatabaseSecretsMount#max_open_connections}
        '''
        result = self._values.get("max_open_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The root credential password used in the connection URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugin_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the plugin to use for this connection.

        Must be prefixed with the name of one of the supported database engine types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        '''
        result = self._values.get("plugin_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def root_rotation_statements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of database statements to be executed to rotate the root user's credentials.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        '''
        result = self._values.get("root_rotation_statements")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The root credential username used in the connection URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username_template(self) -> typing.Optional[builtins.str]:
        '''Username generation template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username_template DatabaseSecretsMount#username_template}
        '''
        result = self._values.get("username_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verify_connection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if the connection is verified during initial configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        result = self._values.get("verify_connection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseSecretsMountMysqlAurora(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseSecretsMountMysqlAuroraList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountMysqlAuroraList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__89638ad8a971f4fd92492b3c5d4178227b2c320b0f38f1f5601290847639b19d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatabaseSecretsMountMysqlAuroraOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__133188ce48fd5c9a7f67de9972e00fd2d71a56cde2dd0f523f5cfb2358bac35b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatabaseSecretsMountMysqlAuroraOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__178ebde17cd3dfe51cd4b00db90eb7395e594fa73d0f38962db31c24012c4f01)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c37996e034a94d3a9fa341d99d4922e596a879e7bfce8440be1419d100624f9b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db3d4d9e30713fe06cff2f37c4b2c73b0c7d071d86b9b2ed7caa5e51b2b6392e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMysqlAurora]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMysqlAurora]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMysqlAurora]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6386b64a8183f9bc8c0573d8ab47ddec5254c159a91615128ac075dc789a8265)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatabaseSecretsMountMysqlAuroraOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountMysqlAuroraOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73e0811f1742c3e4d1bff7f8852a8dcb8b40e2608493b2f1aef54457a1f57d03)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllowedRoles")
    def reset_allowed_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedRoles", []))

    @jsii.member(jsii_name="resetConnectionUrl")
    def reset_connection_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionUrl", []))

    @jsii.member(jsii_name="resetData")
    def reset_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetData", []))

    @jsii.member(jsii_name="resetMaxConnectionLifetime")
    def reset_max_connection_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConnectionLifetime", []))

    @jsii.member(jsii_name="resetMaxIdleConnections")
    def reset_max_idle_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxIdleConnections", []))

    @jsii.member(jsii_name="resetMaxOpenConnections")
    def reset_max_open_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxOpenConnections", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPluginName")
    def reset_plugin_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginName", []))

    @jsii.member(jsii_name="resetRootRotationStatements")
    def reset_root_rotation_statements(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootRotationStatements", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @jsii.member(jsii_name="resetUsernameTemplate")
    def reset_username_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsernameTemplate", []))

    @jsii.member(jsii_name="resetVerifyConnection")
    def reset_verify_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerifyConnection", []))

    @builtins.property
    @jsii.member(jsii_name="allowedRolesInput")
    def allowed_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionUrlInput")
    def connection_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConnectionLifetimeInput")
    def max_connection_lifetime_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConnectionLifetimeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxIdleConnectionsInput")
    def max_idle_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxIdleConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxOpenConnectionsInput")
    def max_open_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxOpenConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginNameInput")
    def plugin_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatementsInput")
    def root_rotation_statements_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rootRotationStatementsInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameTemplateInput")
    def username_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyConnectionInput")
    def verify_connection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verifyConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedRoles")
    def allowed_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedRoles"))

    @allowed_roles.setter
    def allowed_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a03cae021c9230f4647ee46f373ef5dde1b33c8c9c7cdb3b7a0ce4b2437a3443)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedRoles", value)

    @builtins.property
    @jsii.member(jsii_name="connectionUrl")
    def connection_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionUrl"))

    @connection_url.setter
    def connection_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f7c5ecae8821b06c7051d1bd3924f42bc7789258dfb0759ae378bf466efb908)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionUrl", value)

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "data"))

    @data.setter
    def data(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5afa207e77cd4e373f4a3fa03a360133f693162cd0d043ad4c69c95bab6380e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value)

    @builtins.property
    @jsii.member(jsii_name="maxConnectionLifetime")
    def max_connection_lifetime(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConnectionLifetime"))

    @max_connection_lifetime.setter
    def max_connection_lifetime(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02abded6b82a894d5835c74736c19c3c291001175c96e333332e265c2db0e96d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnectionLifetime", value)

    @builtins.property
    @jsii.member(jsii_name="maxIdleConnections")
    def max_idle_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIdleConnections"))

    @max_idle_connections.setter
    def max_idle_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d38d4b242aeee44af7f3cd8663b455320206dfb29fa0ed4f8e7ad8a59df63325)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxIdleConnections", value)

    @builtins.property
    @jsii.member(jsii_name="maxOpenConnections")
    def max_open_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxOpenConnections"))

    @max_open_connections.setter
    def max_open_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09ec6b2d54303d4998d603411267e2638c755f73421c1307ae697d95f9bec755)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxOpenConnections", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a7fd67f528b64aa41b0de469393e696b562acffed49462d01f2668be4ad1749)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5eb219cb703aa8a2ae83a99f7097099a272ecc9acdffad1a2b37e11c9f22baa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="pluginName")
    def plugin_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginName"))

    @plugin_name.setter
    def plugin_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d2a7d93cd9180a48f576e03e707c79f627746ba6cefb4cd0e0f0968f4fe5569)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginName", value)

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatements")
    def root_rotation_statements(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rootRotationStatements"))

    @root_rotation_statements.setter
    def root_rotation_statements(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e05ad578ac9d3992ed519bbf565fccc89ae244da7b53c1dae429b6a01d6a972)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootRotationStatements", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86397e06f52f83013e640b6467e4a36a05ceadd2ecf98303c52141ae11cd1d06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="usernameTemplate")
    def username_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usernameTemplate"))

    @username_template.setter
    def username_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b65515683946ce13120d23208dffa0c54c4a083c2c52c8b7ad70f49f4f21ff2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usernameTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="verifyConnection")
    def verify_connection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verifyConnection"))

    @verify_connection.setter
    def verify_connection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__996ee4532ffcbbfa4e682ab32843feac0dfc44d5c34a1fcf7e907bb07443ad41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifyConnection", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMysqlAurora]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMysqlAurora]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMysqlAurora]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bd2660e4ee10ae879679703bf982cf5ef670db80ecf53d7b103108306dd0f4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountMysqlLegacy",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "allowed_roles": "allowedRoles",
        "connection_url": "connectionUrl",
        "data": "data",
        "max_connection_lifetime": "maxConnectionLifetime",
        "max_idle_connections": "maxIdleConnections",
        "max_open_connections": "maxOpenConnections",
        "password": "password",
        "plugin_name": "pluginName",
        "root_rotation_statements": "rootRotationStatements",
        "username": "username",
        "username_template": "usernameTemplate",
        "verify_connection": "verifyConnection",
    },
)
class DatabaseSecretsMountMysqlLegacy:
    def __init__(
        self,
        *,
        name: builtins.str,
        allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection_url: typing.Optional[builtins.str] = None,
        data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_connection_lifetime: typing.Optional[jsii.Number] = None,
        max_idle_connections: typing.Optional[jsii.Number] = None,
        max_open_connections: typing.Optional[jsii.Number] = None,
        password: typing.Optional[builtins.str] = None,
        plugin_name: typing.Optional[builtins.str] = None,
        root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
        username: typing.Optional[builtins.str] = None,
        username_template: typing.Optional[builtins.str] = None,
        verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Name of the database connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        :param allowed_roles: A list of roles that are allowed to use this connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        :param connection_url: Connection string to use to connect to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#connection_url DatabaseSecretsMount#connection_url}
        :param data: A map of sensitive data to pass to the endpoint. Useful for templated connection strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        :param max_connection_lifetime: Maximum number of seconds a connection may be reused. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_connection_lifetime DatabaseSecretsMount#max_connection_lifetime}
        :param max_idle_connections: Maximum number of idle connections to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_idle_connections DatabaseSecretsMount#max_idle_connections}
        :param max_open_connections: Maximum number of open connections to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_open_connections DatabaseSecretsMount#max_open_connections}
        :param password: The root credential password used in the connection URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        :param plugin_name: Specifies the name of the plugin to use for this connection. Must be prefixed with the name of one of the supported database engine types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        :param root_rotation_statements: A list of database statements to be executed to rotate the root user's credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        :param username: The root credential username used in the connection URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        :param username_template: Username generation template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username_template DatabaseSecretsMount#username_template}
        :param verify_connection: Specifies if the connection is verified during initial configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4e8faa9285539891551e8d833691913780353032beac2c982898e5a8791ef54)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allowed_roles", value=allowed_roles, expected_type=type_hints["allowed_roles"])
            check_type(argname="argument connection_url", value=connection_url, expected_type=type_hints["connection_url"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument max_connection_lifetime", value=max_connection_lifetime, expected_type=type_hints["max_connection_lifetime"])
            check_type(argname="argument max_idle_connections", value=max_idle_connections, expected_type=type_hints["max_idle_connections"])
            check_type(argname="argument max_open_connections", value=max_open_connections, expected_type=type_hints["max_open_connections"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument plugin_name", value=plugin_name, expected_type=type_hints["plugin_name"])
            check_type(argname="argument root_rotation_statements", value=root_rotation_statements, expected_type=type_hints["root_rotation_statements"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument username_template", value=username_template, expected_type=type_hints["username_template"])
            check_type(argname="argument verify_connection", value=verify_connection, expected_type=type_hints["verify_connection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if allowed_roles is not None:
            self._values["allowed_roles"] = allowed_roles
        if connection_url is not None:
            self._values["connection_url"] = connection_url
        if data is not None:
            self._values["data"] = data
        if max_connection_lifetime is not None:
            self._values["max_connection_lifetime"] = max_connection_lifetime
        if max_idle_connections is not None:
            self._values["max_idle_connections"] = max_idle_connections
        if max_open_connections is not None:
            self._values["max_open_connections"] = max_open_connections
        if password is not None:
            self._values["password"] = password
        if plugin_name is not None:
            self._values["plugin_name"] = plugin_name
        if root_rotation_statements is not None:
            self._values["root_rotation_statements"] = root_rotation_statements
        if username is not None:
            self._values["username"] = username
        if username_template is not None:
            self._values["username_template"] = username_template
        if verify_connection is not None:
            self._values["verify_connection"] = verify_connection

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the database connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of roles that are allowed to use this connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        '''
        result = self._values.get("allowed_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def connection_url(self) -> typing.Optional[builtins.str]:
        '''Connection string to use to connect to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#connection_url DatabaseSecretsMount#connection_url}
        '''
        result = self._values.get("connection_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of sensitive data to pass to the endpoint. Useful for templated connection strings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def max_connection_lifetime(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of seconds a connection may be reused.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_connection_lifetime DatabaseSecretsMount#max_connection_lifetime}
        '''
        result = self._values.get("max_connection_lifetime")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_idle_connections(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of idle connections to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_idle_connections DatabaseSecretsMount#max_idle_connections}
        '''
        result = self._values.get("max_idle_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_open_connections(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of open connections to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_open_connections DatabaseSecretsMount#max_open_connections}
        '''
        result = self._values.get("max_open_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The root credential password used in the connection URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugin_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the plugin to use for this connection.

        Must be prefixed with the name of one of the supported database engine types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        '''
        result = self._values.get("plugin_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def root_rotation_statements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of database statements to be executed to rotate the root user's credentials.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        '''
        result = self._values.get("root_rotation_statements")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The root credential username used in the connection URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username_template(self) -> typing.Optional[builtins.str]:
        '''Username generation template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username_template DatabaseSecretsMount#username_template}
        '''
        result = self._values.get("username_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verify_connection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if the connection is verified during initial configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        result = self._values.get("verify_connection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseSecretsMountMysqlLegacy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseSecretsMountMysqlLegacyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountMysqlLegacyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2dfa14560f4c0d7d4e886f5acb39d5cc9b2be197bf6054e532414ad20242c4f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatabaseSecretsMountMysqlLegacyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69251deeefba5c4def210df82efcf8c93eb42f96c39418e33c365ba6abc53e64)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatabaseSecretsMountMysqlLegacyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efddb0e7472a863d01ee46a090491dd41ae3933162ac2087ee16db9d707741ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5a88e237a3deaa82a25de5d568146e1b634e0d18bf0da57efd1176a15afab57)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3112fc01ef6c1cdea0ddd23998101b06409b5774956f82b9d2d9a67c54d2847)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMysqlLegacy]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMysqlLegacy]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMysqlLegacy]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76ece26ae3243424419f227b9ce117ae62cac538fc039e6ed68ff9abe677c2e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatabaseSecretsMountMysqlLegacyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountMysqlLegacyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4115494fca69ad24f4e9738296bf2ba8c4c337eef036acbc46cabc824d5722e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllowedRoles")
    def reset_allowed_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedRoles", []))

    @jsii.member(jsii_name="resetConnectionUrl")
    def reset_connection_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionUrl", []))

    @jsii.member(jsii_name="resetData")
    def reset_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetData", []))

    @jsii.member(jsii_name="resetMaxConnectionLifetime")
    def reset_max_connection_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConnectionLifetime", []))

    @jsii.member(jsii_name="resetMaxIdleConnections")
    def reset_max_idle_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxIdleConnections", []))

    @jsii.member(jsii_name="resetMaxOpenConnections")
    def reset_max_open_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxOpenConnections", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPluginName")
    def reset_plugin_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginName", []))

    @jsii.member(jsii_name="resetRootRotationStatements")
    def reset_root_rotation_statements(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootRotationStatements", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @jsii.member(jsii_name="resetUsernameTemplate")
    def reset_username_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsernameTemplate", []))

    @jsii.member(jsii_name="resetVerifyConnection")
    def reset_verify_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerifyConnection", []))

    @builtins.property
    @jsii.member(jsii_name="allowedRolesInput")
    def allowed_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionUrlInput")
    def connection_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConnectionLifetimeInput")
    def max_connection_lifetime_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConnectionLifetimeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxIdleConnectionsInput")
    def max_idle_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxIdleConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxOpenConnectionsInput")
    def max_open_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxOpenConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginNameInput")
    def plugin_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatementsInput")
    def root_rotation_statements_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rootRotationStatementsInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameTemplateInput")
    def username_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyConnectionInput")
    def verify_connection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verifyConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedRoles")
    def allowed_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedRoles"))

    @allowed_roles.setter
    def allowed_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a83bfacc9591d36f95cba51b53ef2216a4bbd70d894f48a95854a9cd037b291f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedRoles", value)

    @builtins.property
    @jsii.member(jsii_name="connectionUrl")
    def connection_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionUrl"))

    @connection_url.setter
    def connection_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74b8affac7ede2b593f116540b65feab0d0922129f05f3ac051e763837b6084a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionUrl", value)

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "data"))

    @data.setter
    def data(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fffaf186cf1e49a6b7f3d6704ea4b7a921d617a50ec6ec9994d0598ae880abea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value)

    @builtins.property
    @jsii.member(jsii_name="maxConnectionLifetime")
    def max_connection_lifetime(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConnectionLifetime"))

    @max_connection_lifetime.setter
    def max_connection_lifetime(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7627827954f817d87c7d49f892ec6dac857fa4837dc856f4127a0043d55c92e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnectionLifetime", value)

    @builtins.property
    @jsii.member(jsii_name="maxIdleConnections")
    def max_idle_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIdleConnections"))

    @max_idle_connections.setter
    def max_idle_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9482a0d673bb69ab3df2196de40f5832fcb86e97a200c7937ea79c7a386427b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxIdleConnections", value)

    @builtins.property
    @jsii.member(jsii_name="maxOpenConnections")
    def max_open_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxOpenConnections"))

    @max_open_connections.setter
    def max_open_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23244d56b3059dd1097ecf95a79fde41f9769dc385d35b31a2415e060a763bbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxOpenConnections", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22cbd4e72dbf026b8997081c73f69a13a0b157d19ebcb1b5aa0e7b0c5bf4954b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffa873e2b97762436a1b28d599e717961eaeadee47c37fa62d1cf3450e235073)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="pluginName")
    def plugin_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginName"))

    @plugin_name.setter
    def plugin_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__764c994158011342a5dda1c0d7fe31c475c9da8d52957804724768f253a38823)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginName", value)

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatements")
    def root_rotation_statements(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rootRotationStatements"))

    @root_rotation_statements.setter
    def root_rotation_statements(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f2aa5ee6c3afd0e5213389678cffd219e694601d008fbec5322cfc76b2faa51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootRotationStatements", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__836ea320cbcce7ea9e3e77f883aeef8421b8cb4b0a94f490f16e4936b357ba2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="usernameTemplate")
    def username_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usernameTemplate"))

    @username_template.setter
    def username_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e0824973da860f6e782b3efb04299ced0f5714b4cdb24bfb73c6d4d7f44abc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usernameTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="verifyConnection")
    def verify_connection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verifyConnection"))

    @verify_connection.setter
    def verify_connection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3536a2ec3af03ed5827b4a7ada25a57dbebd7516912233eb3943958301b23003)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifyConnection", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMysqlLegacy]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMysqlLegacy]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMysqlLegacy]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a2f9b0e146f8966bbcdb8fe870694df3240fc0eb78d3d9d83deb77b5a69f7cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatabaseSecretsMountMysqlList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountMysqlList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1a4a03998a3c3adbf4b8d36dcb5e60515b55bdaf3973fab63d0a478f667bc29)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DatabaseSecretsMountMysqlOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8e8a210355b019ad0c848fcb001d12d9a6a0c9d9bb7f5e792ba64edbe94fb54)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatabaseSecretsMountMysqlOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f92f3965c79edd40b38fb4a6ea33dcb7c0c483b1cf45e1c2bd8690396876d355)
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
            type_hints = typing.get_type_hints(_typecheckingstub__27a2e9b04749d7a2c42405094ab41f1fa4684929e6f20480dc468a4f4a4d4bdd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be5b02f91b8e776620408d73c948b6d7700036afffb6776e7577a112534ef688)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMysql]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMysql]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMysql]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f43fb86633a27d0ff180019b25a449581da2cfb0be38f269fba87f5580b0b74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatabaseSecretsMountMysqlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountMysqlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__77ff54283c045cb34de85d67345d1ce86e75761fe06492d775ba8939339189a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllowedRoles")
    def reset_allowed_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedRoles", []))

    @jsii.member(jsii_name="resetConnectionUrl")
    def reset_connection_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionUrl", []))

    @jsii.member(jsii_name="resetData")
    def reset_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetData", []))

    @jsii.member(jsii_name="resetMaxConnectionLifetime")
    def reset_max_connection_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConnectionLifetime", []))

    @jsii.member(jsii_name="resetMaxIdleConnections")
    def reset_max_idle_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxIdleConnections", []))

    @jsii.member(jsii_name="resetMaxOpenConnections")
    def reset_max_open_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxOpenConnections", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPluginName")
    def reset_plugin_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginName", []))

    @jsii.member(jsii_name="resetRootRotationStatements")
    def reset_root_rotation_statements(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootRotationStatements", []))

    @jsii.member(jsii_name="resetTlsCa")
    def reset_tls_ca(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsCa", []))

    @jsii.member(jsii_name="resetTlsCertificateKey")
    def reset_tls_certificate_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsCertificateKey", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @jsii.member(jsii_name="resetUsernameTemplate")
    def reset_username_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsernameTemplate", []))

    @jsii.member(jsii_name="resetVerifyConnection")
    def reset_verify_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerifyConnection", []))

    @builtins.property
    @jsii.member(jsii_name="allowedRolesInput")
    def allowed_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionUrlInput")
    def connection_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConnectionLifetimeInput")
    def max_connection_lifetime_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConnectionLifetimeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxIdleConnectionsInput")
    def max_idle_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxIdleConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxOpenConnectionsInput")
    def max_open_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxOpenConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginNameInput")
    def plugin_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatementsInput")
    def root_rotation_statements_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rootRotationStatementsInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsCaInput")
    def tls_ca_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tlsCaInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsCertificateKeyInput")
    def tls_certificate_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tlsCertificateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameTemplateInput")
    def username_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyConnectionInput")
    def verify_connection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verifyConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedRoles")
    def allowed_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedRoles"))

    @allowed_roles.setter
    def allowed_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3383b68475f903cf1e24df80a5d74c579c111d3c42dd7d5622dc6b5277da95e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedRoles", value)

    @builtins.property
    @jsii.member(jsii_name="connectionUrl")
    def connection_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionUrl"))

    @connection_url.setter
    def connection_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb5a5b7bfca09cab0c9f8904ee9b2b00d70e1509e79aa6d2fa4f0f29d1b6003d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionUrl", value)

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "data"))

    @data.setter
    def data(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da1d483f2d9af12e3cd9577420180f972baba82571cadf42ade2a5b232d43eb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value)

    @builtins.property
    @jsii.member(jsii_name="maxConnectionLifetime")
    def max_connection_lifetime(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConnectionLifetime"))

    @max_connection_lifetime.setter
    def max_connection_lifetime(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d20e14e98ab9b40ad4275334794d73ecde3bba7a5c973cff36ed508667d7abe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnectionLifetime", value)

    @builtins.property
    @jsii.member(jsii_name="maxIdleConnections")
    def max_idle_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIdleConnections"))

    @max_idle_connections.setter
    def max_idle_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cc3bd578c3be6b6a3600bd0275e70c26b19a32c6f0140c84b928d16e85b9a22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxIdleConnections", value)

    @builtins.property
    @jsii.member(jsii_name="maxOpenConnections")
    def max_open_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxOpenConnections"))

    @max_open_connections.setter
    def max_open_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8140154a134efa2d1ca1d10b73a5173cc83182b73a832acf72e879d95f25776f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxOpenConnections", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab524a502f95c5c18b4482aad5c39d6e0abd0c0f87392cdd3d95be3b46daff50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c18ecfdb9ba4fde2a5975b1d6f2d1ec704072eef6507b11177fdf03a8e93130)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="pluginName")
    def plugin_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginName"))

    @plugin_name.setter
    def plugin_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__116b08800223ebb013bf3983adb4988b8cadc59c7a6f491a6b128c07f1d797d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginName", value)

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatements")
    def root_rotation_statements(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rootRotationStatements"))

    @root_rotation_statements.setter
    def root_rotation_statements(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec62e721bd2a00dec8394409fb603e0936886c57167a3ee9f1ff4ca3183f8f9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootRotationStatements", value)

    @builtins.property
    @jsii.member(jsii_name="tlsCa")
    def tls_ca(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tlsCa"))

    @tls_ca.setter
    def tls_ca(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__620b0a0aa85bd6ef9c4410d1f3474f9ef2127667847c3fe32c9b90e933ba92d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsCa", value)

    @builtins.property
    @jsii.member(jsii_name="tlsCertificateKey")
    def tls_certificate_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tlsCertificateKey"))

    @tls_certificate_key.setter
    def tls_certificate_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__051fbede64d14c82fa674d7a19d5f7af7e1009d2ac097f973bbb83be8e6d2c51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsCertificateKey", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07855d8342ff781d0f8ece6b1d71edd2edf17f65b284ba4adda17d3ee3766d97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="usernameTemplate")
    def username_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usernameTemplate"))

    @username_template.setter
    def username_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acc076f9f672da5dc53c78e1fdd4451bc335ebb694077e946ef14ad5b77c7d84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usernameTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="verifyConnection")
    def verify_connection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verifyConnection"))

    @verify_connection.setter
    def verify_connection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6b0a60a6d22a1010902b8660f90a75871f015fc15ed0690077cf820f81871c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifyConnection", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMysql]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMysql]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMysql]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f08dc3bb92b36b998c24e3d44ab3c127b86d48a44f730f935eca49ce99a7cc2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountMysqlRds",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "allowed_roles": "allowedRoles",
        "connection_url": "connectionUrl",
        "data": "data",
        "max_connection_lifetime": "maxConnectionLifetime",
        "max_idle_connections": "maxIdleConnections",
        "max_open_connections": "maxOpenConnections",
        "password": "password",
        "plugin_name": "pluginName",
        "root_rotation_statements": "rootRotationStatements",
        "username": "username",
        "username_template": "usernameTemplate",
        "verify_connection": "verifyConnection",
    },
)
class DatabaseSecretsMountMysqlRds:
    def __init__(
        self,
        *,
        name: builtins.str,
        allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection_url: typing.Optional[builtins.str] = None,
        data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_connection_lifetime: typing.Optional[jsii.Number] = None,
        max_idle_connections: typing.Optional[jsii.Number] = None,
        max_open_connections: typing.Optional[jsii.Number] = None,
        password: typing.Optional[builtins.str] = None,
        plugin_name: typing.Optional[builtins.str] = None,
        root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
        username: typing.Optional[builtins.str] = None,
        username_template: typing.Optional[builtins.str] = None,
        verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Name of the database connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        :param allowed_roles: A list of roles that are allowed to use this connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        :param connection_url: Connection string to use to connect to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#connection_url DatabaseSecretsMount#connection_url}
        :param data: A map of sensitive data to pass to the endpoint. Useful for templated connection strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        :param max_connection_lifetime: Maximum number of seconds a connection may be reused. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_connection_lifetime DatabaseSecretsMount#max_connection_lifetime}
        :param max_idle_connections: Maximum number of idle connections to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_idle_connections DatabaseSecretsMount#max_idle_connections}
        :param max_open_connections: Maximum number of open connections to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_open_connections DatabaseSecretsMount#max_open_connections}
        :param password: The root credential password used in the connection URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        :param plugin_name: Specifies the name of the plugin to use for this connection. Must be prefixed with the name of one of the supported database engine types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        :param root_rotation_statements: A list of database statements to be executed to rotate the root user's credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        :param username: The root credential username used in the connection URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        :param username_template: Username generation template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username_template DatabaseSecretsMount#username_template}
        :param verify_connection: Specifies if the connection is verified during initial configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94e56133dea2b462dff7a58564d06e8463f1098fda031de337b569d321f06751)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allowed_roles", value=allowed_roles, expected_type=type_hints["allowed_roles"])
            check_type(argname="argument connection_url", value=connection_url, expected_type=type_hints["connection_url"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument max_connection_lifetime", value=max_connection_lifetime, expected_type=type_hints["max_connection_lifetime"])
            check_type(argname="argument max_idle_connections", value=max_idle_connections, expected_type=type_hints["max_idle_connections"])
            check_type(argname="argument max_open_connections", value=max_open_connections, expected_type=type_hints["max_open_connections"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument plugin_name", value=plugin_name, expected_type=type_hints["plugin_name"])
            check_type(argname="argument root_rotation_statements", value=root_rotation_statements, expected_type=type_hints["root_rotation_statements"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument username_template", value=username_template, expected_type=type_hints["username_template"])
            check_type(argname="argument verify_connection", value=verify_connection, expected_type=type_hints["verify_connection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if allowed_roles is not None:
            self._values["allowed_roles"] = allowed_roles
        if connection_url is not None:
            self._values["connection_url"] = connection_url
        if data is not None:
            self._values["data"] = data
        if max_connection_lifetime is not None:
            self._values["max_connection_lifetime"] = max_connection_lifetime
        if max_idle_connections is not None:
            self._values["max_idle_connections"] = max_idle_connections
        if max_open_connections is not None:
            self._values["max_open_connections"] = max_open_connections
        if password is not None:
            self._values["password"] = password
        if plugin_name is not None:
            self._values["plugin_name"] = plugin_name
        if root_rotation_statements is not None:
            self._values["root_rotation_statements"] = root_rotation_statements
        if username is not None:
            self._values["username"] = username
        if username_template is not None:
            self._values["username_template"] = username_template
        if verify_connection is not None:
            self._values["verify_connection"] = verify_connection

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the database connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of roles that are allowed to use this connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        '''
        result = self._values.get("allowed_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def connection_url(self) -> typing.Optional[builtins.str]:
        '''Connection string to use to connect to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#connection_url DatabaseSecretsMount#connection_url}
        '''
        result = self._values.get("connection_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of sensitive data to pass to the endpoint. Useful for templated connection strings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def max_connection_lifetime(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of seconds a connection may be reused.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_connection_lifetime DatabaseSecretsMount#max_connection_lifetime}
        '''
        result = self._values.get("max_connection_lifetime")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_idle_connections(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of idle connections to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_idle_connections DatabaseSecretsMount#max_idle_connections}
        '''
        result = self._values.get("max_idle_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_open_connections(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of open connections to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_open_connections DatabaseSecretsMount#max_open_connections}
        '''
        result = self._values.get("max_open_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The root credential password used in the connection URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugin_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the plugin to use for this connection.

        Must be prefixed with the name of one of the supported database engine types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        '''
        result = self._values.get("plugin_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def root_rotation_statements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of database statements to be executed to rotate the root user's credentials.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        '''
        result = self._values.get("root_rotation_statements")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The root credential username used in the connection URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username_template(self) -> typing.Optional[builtins.str]:
        '''Username generation template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username_template DatabaseSecretsMount#username_template}
        '''
        result = self._values.get("username_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verify_connection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if the connection is verified during initial configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        result = self._values.get("verify_connection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseSecretsMountMysqlRds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseSecretsMountMysqlRdsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountMysqlRdsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__460534ce8afae1dba0f75d6c4d8628d8f0310d4a07921d55d7e21a930f85e365)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DatabaseSecretsMountMysqlRdsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__856cc45ef3c17291b9fef98129d23364b9ab7ed30cb67a10193656e3892d4be3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatabaseSecretsMountMysqlRdsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39df93693f4654b19951d8536c93dc41ee4858f70a9f249384c4f1bff38b42bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9da60f88beaafbeff040b687e0cf105a5d28e28653ecc41f070b9dcdeb0ccb30)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0520d7f1be5bc104be4ba14eb8da5b70f8bb6b8cf8fc2ef06ee9d83fffa8d54)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMysqlRds]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMysqlRds]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMysqlRds]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d5923081e363f91271925125b968b59cc0e2e9741c71989c070f7b5f215dd47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatabaseSecretsMountMysqlRdsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountMysqlRdsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e63362f0ef5fbda6eafcc8f2a68646e5da957329e9d32070c6f6cafe13948da8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllowedRoles")
    def reset_allowed_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedRoles", []))

    @jsii.member(jsii_name="resetConnectionUrl")
    def reset_connection_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionUrl", []))

    @jsii.member(jsii_name="resetData")
    def reset_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetData", []))

    @jsii.member(jsii_name="resetMaxConnectionLifetime")
    def reset_max_connection_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConnectionLifetime", []))

    @jsii.member(jsii_name="resetMaxIdleConnections")
    def reset_max_idle_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxIdleConnections", []))

    @jsii.member(jsii_name="resetMaxOpenConnections")
    def reset_max_open_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxOpenConnections", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPluginName")
    def reset_plugin_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginName", []))

    @jsii.member(jsii_name="resetRootRotationStatements")
    def reset_root_rotation_statements(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootRotationStatements", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @jsii.member(jsii_name="resetUsernameTemplate")
    def reset_username_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsernameTemplate", []))

    @jsii.member(jsii_name="resetVerifyConnection")
    def reset_verify_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerifyConnection", []))

    @builtins.property
    @jsii.member(jsii_name="allowedRolesInput")
    def allowed_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionUrlInput")
    def connection_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConnectionLifetimeInput")
    def max_connection_lifetime_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConnectionLifetimeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxIdleConnectionsInput")
    def max_idle_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxIdleConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxOpenConnectionsInput")
    def max_open_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxOpenConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginNameInput")
    def plugin_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatementsInput")
    def root_rotation_statements_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rootRotationStatementsInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameTemplateInput")
    def username_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyConnectionInput")
    def verify_connection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verifyConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedRoles")
    def allowed_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedRoles"))

    @allowed_roles.setter
    def allowed_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dab9a76f20fd6a32ad71841b5f6ba408b1c5d9f75cbc13508cae98065950fce2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedRoles", value)

    @builtins.property
    @jsii.member(jsii_name="connectionUrl")
    def connection_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionUrl"))

    @connection_url.setter
    def connection_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9d8270da4212b450f813e77dbcd736892fb8a98aeb7ff8aaa5486a4381bcbef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionUrl", value)

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "data"))

    @data.setter
    def data(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5a9cd0212967e64d951c0f713f2fdebd90cf6e73244a8f4f1de44d9452d74c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value)

    @builtins.property
    @jsii.member(jsii_name="maxConnectionLifetime")
    def max_connection_lifetime(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConnectionLifetime"))

    @max_connection_lifetime.setter
    def max_connection_lifetime(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c494319e3b4f8138f36c53e7a9a4ab2f287cb77f345aab4e80664698c26bd2ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnectionLifetime", value)

    @builtins.property
    @jsii.member(jsii_name="maxIdleConnections")
    def max_idle_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIdleConnections"))

    @max_idle_connections.setter
    def max_idle_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c30ebb165d3dd28faabf036abfa8b7e69f8fd449a534fdc7f63f8fbb5cfc6f38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxIdleConnections", value)

    @builtins.property
    @jsii.member(jsii_name="maxOpenConnections")
    def max_open_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxOpenConnections"))

    @max_open_connections.setter
    def max_open_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aa151bb31ecce05cc4f52802273280c53401c7a60642e7d726c5e2bd748342c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxOpenConnections", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d68a02ca92be3e38ec514b8e26f4876794acccd1d228ae1353ae278856548165)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ee738c1bf4d2f8ee241b3f1f6a4b3d95466b335ca0851985faa70b53df35117)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="pluginName")
    def plugin_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginName"))

    @plugin_name.setter
    def plugin_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0917c5d0a7fe0b8328dce7ebed4c8b64c2ec7450e4cf579a82a4ac19b2b8d61d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginName", value)

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatements")
    def root_rotation_statements(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rootRotationStatements"))

    @root_rotation_statements.setter
    def root_rotation_statements(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8978091f9f81d68ffa24c5b8d5359b63131a1d3c7e1f3f209c4e2bff2f5ea3ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootRotationStatements", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adaecaaef22ed67c281f17b54fa5089e093f437179f7883c53e6d71dd5da748f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="usernameTemplate")
    def username_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usernameTemplate"))

    @username_template.setter
    def username_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__519a1a7bcfde4afed0b1538b0685b783cd9234b43294138b2597603644089580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usernameTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="verifyConnection")
    def verify_connection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verifyConnection"))

    @verify_connection.setter
    def verify_connection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cf08774f890ba69a4ad3bf5776f7dc755561f6e49002afc56e819d08b44b49b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifyConnection", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMysqlRds]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMysqlRds]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMysqlRds]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96ca2cabe2a637c3852a25173086717903dc8f2330b830dedbb02f5bc68924cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountOracle",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "allowed_roles": "allowedRoles",
        "connection_url": "connectionUrl",
        "data": "data",
        "max_connection_lifetime": "maxConnectionLifetime",
        "max_idle_connections": "maxIdleConnections",
        "max_open_connections": "maxOpenConnections",
        "password": "password",
        "plugin_name": "pluginName",
        "root_rotation_statements": "rootRotationStatements",
        "username": "username",
        "username_template": "usernameTemplate",
        "verify_connection": "verifyConnection",
    },
)
class DatabaseSecretsMountOracle:
    def __init__(
        self,
        *,
        name: builtins.str,
        allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection_url: typing.Optional[builtins.str] = None,
        data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_connection_lifetime: typing.Optional[jsii.Number] = None,
        max_idle_connections: typing.Optional[jsii.Number] = None,
        max_open_connections: typing.Optional[jsii.Number] = None,
        password: typing.Optional[builtins.str] = None,
        plugin_name: typing.Optional[builtins.str] = None,
        root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
        username: typing.Optional[builtins.str] = None,
        username_template: typing.Optional[builtins.str] = None,
        verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Name of the database connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        :param allowed_roles: A list of roles that are allowed to use this connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        :param connection_url: Connection string to use to connect to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#connection_url DatabaseSecretsMount#connection_url}
        :param data: A map of sensitive data to pass to the endpoint. Useful for templated connection strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        :param max_connection_lifetime: Maximum number of seconds a connection may be reused. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_connection_lifetime DatabaseSecretsMount#max_connection_lifetime}
        :param max_idle_connections: Maximum number of idle connections to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_idle_connections DatabaseSecretsMount#max_idle_connections}
        :param max_open_connections: Maximum number of open connections to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_open_connections DatabaseSecretsMount#max_open_connections}
        :param password: The root credential password used in the connection URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        :param plugin_name: Specifies the name of the plugin to use for this connection. Must be prefixed with the name of one of the supported database engine types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        :param root_rotation_statements: A list of database statements to be executed to rotate the root user's credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        :param username: The root credential username used in the connection URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        :param username_template: Username generation template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username_template DatabaseSecretsMount#username_template}
        :param verify_connection: Specifies if the connection is verified during initial configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65491de5558996136bec008c06366a08b38751687c4fb1303c5c54059711eb9c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allowed_roles", value=allowed_roles, expected_type=type_hints["allowed_roles"])
            check_type(argname="argument connection_url", value=connection_url, expected_type=type_hints["connection_url"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument max_connection_lifetime", value=max_connection_lifetime, expected_type=type_hints["max_connection_lifetime"])
            check_type(argname="argument max_idle_connections", value=max_idle_connections, expected_type=type_hints["max_idle_connections"])
            check_type(argname="argument max_open_connections", value=max_open_connections, expected_type=type_hints["max_open_connections"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument plugin_name", value=plugin_name, expected_type=type_hints["plugin_name"])
            check_type(argname="argument root_rotation_statements", value=root_rotation_statements, expected_type=type_hints["root_rotation_statements"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument username_template", value=username_template, expected_type=type_hints["username_template"])
            check_type(argname="argument verify_connection", value=verify_connection, expected_type=type_hints["verify_connection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if allowed_roles is not None:
            self._values["allowed_roles"] = allowed_roles
        if connection_url is not None:
            self._values["connection_url"] = connection_url
        if data is not None:
            self._values["data"] = data
        if max_connection_lifetime is not None:
            self._values["max_connection_lifetime"] = max_connection_lifetime
        if max_idle_connections is not None:
            self._values["max_idle_connections"] = max_idle_connections
        if max_open_connections is not None:
            self._values["max_open_connections"] = max_open_connections
        if password is not None:
            self._values["password"] = password
        if plugin_name is not None:
            self._values["plugin_name"] = plugin_name
        if root_rotation_statements is not None:
            self._values["root_rotation_statements"] = root_rotation_statements
        if username is not None:
            self._values["username"] = username
        if username_template is not None:
            self._values["username_template"] = username_template
        if verify_connection is not None:
            self._values["verify_connection"] = verify_connection

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the database connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of roles that are allowed to use this connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        '''
        result = self._values.get("allowed_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def connection_url(self) -> typing.Optional[builtins.str]:
        '''Connection string to use to connect to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#connection_url DatabaseSecretsMount#connection_url}
        '''
        result = self._values.get("connection_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of sensitive data to pass to the endpoint. Useful for templated connection strings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def max_connection_lifetime(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of seconds a connection may be reused.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_connection_lifetime DatabaseSecretsMount#max_connection_lifetime}
        '''
        result = self._values.get("max_connection_lifetime")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_idle_connections(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of idle connections to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_idle_connections DatabaseSecretsMount#max_idle_connections}
        '''
        result = self._values.get("max_idle_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_open_connections(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of open connections to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_open_connections DatabaseSecretsMount#max_open_connections}
        '''
        result = self._values.get("max_open_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The root credential password used in the connection URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugin_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the plugin to use for this connection.

        Must be prefixed with the name of one of the supported database engine types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        '''
        result = self._values.get("plugin_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def root_rotation_statements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of database statements to be executed to rotate the root user's credentials.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        '''
        result = self._values.get("root_rotation_statements")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The root credential username used in the connection URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username_template(self) -> typing.Optional[builtins.str]:
        '''Username generation template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username_template DatabaseSecretsMount#username_template}
        '''
        result = self._values.get("username_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verify_connection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if the connection is verified during initial configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        result = self._values.get("verify_connection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseSecretsMountOracle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseSecretsMountOracleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountOracleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aab452671df63799ef1f4c8cb024d1d8e82c4e258b856489782bc5b9eaf52282)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DatabaseSecretsMountOracleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c184402a3d09264ab4bd1c1d95630b385fc347a79d444c392522669d7824d312)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatabaseSecretsMountOracleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a8f447fe214fff11f16ef64fdfadae51cdae899395965ee75876bb570bf8d1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6513457ac3877effc01a64bbd7fae5d279eda6b7aba688e6a277c3bc3b2c2105)
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
            type_hints = typing.get_type_hints(_typecheckingstub__10ae89194eb74c82517aeecc5275312d854372e1bf02996b2d529188e3024664)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountOracle]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountOracle]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountOracle]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9a65f0acfcfa7932c5a5dc9ae49c755b897052f6476cb507785d4539b7b8ae8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatabaseSecretsMountOracleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountOracleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7dc035229bfcb02f513a1c002fca846f8ac711ed70f19c466d519b10424b969)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllowedRoles")
    def reset_allowed_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedRoles", []))

    @jsii.member(jsii_name="resetConnectionUrl")
    def reset_connection_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionUrl", []))

    @jsii.member(jsii_name="resetData")
    def reset_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetData", []))

    @jsii.member(jsii_name="resetMaxConnectionLifetime")
    def reset_max_connection_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConnectionLifetime", []))

    @jsii.member(jsii_name="resetMaxIdleConnections")
    def reset_max_idle_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxIdleConnections", []))

    @jsii.member(jsii_name="resetMaxOpenConnections")
    def reset_max_open_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxOpenConnections", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPluginName")
    def reset_plugin_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginName", []))

    @jsii.member(jsii_name="resetRootRotationStatements")
    def reset_root_rotation_statements(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootRotationStatements", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @jsii.member(jsii_name="resetUsernameTemplate")
    def reset_username_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsernameTemplate", []))

    @jsii.member(jsii_name="resetVerifyConnection")
    def reset_verify_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerifyConnection", []))

    @builtins.property
    @jsii.member(jsii_name="allowedRolesInput")
    def allowed_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionUrlInput")
    def connection_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConnectionLifetimeInput")
    def max_connection_lifetime_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConnectionLifetimeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxIdleConnectionsInput")
    def max_idle_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxIdleConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxOpenConnectionsInput")
    def max_open_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxOpenConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginNameInput")
    def plugin_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatementsInput")
    def root_rotation_statements_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rootRotationStatementsInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameTemplateInput")
    def username_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyConnectionInput")
    def verify_connection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verifyConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedRoles")
    def allowed_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedRoles"))

    @allowed_roles.setter
    def allowed_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f39ac996373996d57095071ac6b97a8d8e04b6a8b0653db6cf77e0bae14978d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedRoles", value)

    @builtins.property
    @jsii.member(jsii_name="connectionUrl")
    def connection_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionUrl"))

    @connection_url.setter
    def connection_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e317f84131a0d91e271aaea8d46a6a97fc8ae83e20c53fd361afa090075cff5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionUrl", value)

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "data"))

    @data.setter
    def data(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc5166d99994d42c2c6e25c5ee5215e090db2e97f1fef0c5e989c80f272a7d8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value)

    @builtins.property
    @jsii.member(jsii_name="maxConnectionLifetime")
    def max_connection_lifetime(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConnectionLifetime"))

    @max_connection_lifetime.setter
    def max_connection_lifetime(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d24c589c31b29959f0e516d9982b753a96ce7486d0891dbaad058f2918072ebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnectionLifetime", value)

    @builtins.property
    @jsii.member(jsii_name="maxIdleConnections")
    def max_idle_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIdleConnections"))

    @max_idle_connections.setter
    def max_idle_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45c1196fb54ff2d6e1a810079901a1dacbe3c266557c38c3706897e1483109fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxIdleConnections", value)

    @builtins.property
    @jsii.member(jsii_name="maxOpenConnections")
    def max_open_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxOpenConnections"))

    @max_open_connections.setter
    def max_open_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3de7c373c5bf1087efead7eb4a9404ef6cf9662ec2736693e1c186cc25daa94f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxOpenConnections", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c64858f3fed32707a126cf78b4dfad7a47922229704fcba8661aed5760a4bbac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07c18d6b34468b0c7d4017b0d94746f9096c2e9bd6f481e991751cb1ebb81f17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="pluginName")
    def plugin_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginName"))

    @plugin_name.setter
    def plugin_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f6ae0eca1f49e9a8fdb3369e99d8a1b82965b190766f453c549b71757a0aca5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginName", value)

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatements")
    def root_rotation_statements(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rootRotationStatements"))

    @root_rotation_statements.setter
    def root_rotation_statements(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b75145ce45d0a15331f591f47332910176997e9d250d7e08dd501fa8e10b2cdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootRotationStatements", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31b54f8fc2ad2d07f769f5c709846679735fed77937c46c676ef3da1dce1110f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="usernameTemplate")
    def username_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usernameTemplate"))

    @username_template.setter
    def username_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f4dfd2564e2f26ef70b84b9cae789f14059680a39ad8e60393fd51bae9b18a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usernameTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="verifyConnection")
    def verify_connection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verifyConnection"))

    @verify_connection.setter
    def verify_connection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfb28b170c38be09e4d7ba752dea522c24c5656030fd0d51a6d35f547b071f8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifyConnection", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountOracle]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountOracle]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountOracle]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c2e100ce197c33684c1ff9fcdbe0e971004480a533af822f3e3c50a8984dcfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountPostgresql",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "allowed_roles": "allowedRoles",
        "connection_url": "connectionUrl",
        "data": "data",
        "disable_escaping": "disableEscaping",
        "max_connection_lifetime": "maxConnectionLifetime",
        "max_idle_connections": "maxIdleConnections",
        "max_open_connections": "maxOpenConnections",
        "password": "password",
        "plugin_name": "pluginName",
        "root_rotation_statements": "rootRotationStatements",
        "username": "username",
        "username_template": "usernameTemplate",
        "verify_connection": "verifyConnection",
    },
)
class DatabaseSecretsMountPostgresql:
    def __init__(
        self,
        *,
        name: builtins.str,
        allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection_url: typing.Optional[builtins.str] = None,
        data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        disable_escaping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_connection_lifetime: typing.Optional[jsii.Number] = None,
        max_idle_connections: typing.Optional[jsii.Number] = None,
        max_open_connections: typing.Optional[jsii.Number] = None,
        password: typing.Optional[builtins.str] = None,
        plugin_name: typing.Optional[builtins.str] = None,
        root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
        username: typing.Optional[builtins.str] = None,
        username_template: typing.Optional[builtins.str] = None,
        verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Name of the database connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        :param allowed_roles: A list of roles that are allowed to use this connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        :param connection_url: Connection string to use to connect to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#connection_url DatabaseSecretsMount#connection_url}
        :param data: A map of sensitive data to pass to the endpoint. Useful for templated connection strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        :param disable_escaping: Disable special character escaping in username and password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#disable_escaping DatabaseSecretsMount#disable_escaping}
        :param max_connection_lifetime: Maximum number of seconds a connection may be reused. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_connection_lifetime DatabaseSecretsMount#max_connection_lifetime}
        :param max_idle_connections: Maximum number of idle connections to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_idle_connections DatabaseSecretsMount#max_idle_connections}
        :param max_open_connections: Maximum number of open connections to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_open_connections DatabaseSecretsMount#max_open_connections}
        :param password: The root credential password used in the connection URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        :param plugin_name: Specifies the name of the plugin to use for this connection. Must be prefixed with the name of one of the supported database engine types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        :param root_rotation_statements: A list of database statements to be executed to rotate the root user's credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        :param username: The root credential username used in the connection URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        :param username_template: Username generation template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username_template DatabaseSecretsMount#username_template}
        :param verify_connection: Specifies if the connection is verified during initial configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1313db13b346cc66400dedb70fa9ace00b847fdcaea9d7e18d073b7b071db0d2)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allowed_roles", value=allowed_roles, expected_type=type_hints["allowed_roles"])
            check_type(argname="argument connection_url", value=connection_url, expected_type=type_hints["connection_url"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument disable_escaping", value=disable_escaping, expected_type=type_hints["disable_escaping"])
            check_type(argname="argument max_connection_lifetime", value=max_connection_lifetime, expected_type=type_hints["max_connection_lifetime"])
            check_type(argname="argument max_idle_connections", value=max_idle_connections, expected_type=type_hints["max_idle_connections"])
            check_type(argname="argument max_open_connections", value=max_open_connections, expected_type=type_hints["max_open_connections"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument plugin_name", value=plugin_name, expected_type=type_hints["plugin_name"])
            check_type(argname="argument root_rotation_statements", value=root_rotation_statements, expected_type=type_hints["root_rotation_statements"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument username_template", value=username_template, expected_type=type_hints["username_template"])
            check_type(argname="argument verify_connection", value=verify_connection, expected_type=type_hints["verify_connection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if allowed_roles is not None:
            self._values["allowed_roles"] = allowed_roles
        if connection_url is not None:
            self._values["connection_url"] = connection_url
        if data is not None:
            self._values["data"] = data
        if disable_escaping is not None:
            self._values["disable_escaping"] = disable_escaping
        if max_connection_lifetime is not None:
            self._values["max_connection_lifetime"] = max_connection_lifetime
        if max_idle_connections is not None:
            self._values["max_idle_connections"] = max_idle_connections
        if max_open_connections is not None:
            self._values["max_open_connections"] = max_open_connections
        if password is not None:
            self._values["password"] = password
        if plugin_name is not None:
            self._values["plugin_name"] = plugin_name
        if root_rotation_statements is not None:
            self._values["root_rotation_statements"] = root_rotation_statements
        if username is not None:
            self._values["username"] = username
        if username_template is not None:
            self._values["username_template"] = username_template
        if verify_connection is not None:
            self._values["verify_connection"] = verify_connection

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the database connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of roles that are allowed to use this connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        '''
        result = self._values.get("allowed_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def connection_url(self) -> typing.Optional[builtins.str]:
        '''Connection string to use to connect to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#connection_url DatabaseSecretsMount#connection_url}
        '''
        result = self._values.get("connection_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of sensitive data to pass to the endpoint. Useful for templated connection strings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def disable_escaping(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable special character escaping in username and password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#disable_escaping DatabaseSecretsMount#disable_escaping}
        '''
        result = self._values.get("disable_escaping")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_connection_lifetime(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of seconds a connection may be reused.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_connection_lifetime DatabaseSecretsMount#max_connection_lifetime}
        '''
        result = self._values.get("max_connection_lifetime")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_idle_connections(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of idle connections to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_idle_connections DatabaseSecretsMount#max_idle_connections}
        '''
        result = self._values.get("max_idle_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_open_connections(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of open connections to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_open_connections DatabaseSecretsMount#max_open_connections}
        '''
        result = self._values.get("max_open_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The root credential password used in the connection URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugin_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the plugin to use for this connection.

        Must be prefixed with the name of one of the supported database engine types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        '''
        result = self._values.get("plugin_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def root_rotation_statements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of database statements to be executed to rotate the root user's credentials.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        '''
        result = self._values.get("root_rotation_statements")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The root credential username used in the connection URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username_template(self) -> typing.Optional[builtins.str]:
        '''Username generation template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username_template DatabaseSecretsMount#username_template}
        '''
        result = self._values.get("username_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verify_connection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if the connection is verified during initial configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        result = self._values.get("verify_connection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseSecretsMountPostgresql(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseSecretsMountPostgresqlList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountPostgresqlList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__28cda09f1a5b0363c5816cb8e7cffe15e5fc17db6b526a526d20778e2ca40e55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatabaseSecretsMountPostgresqlOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__433b329437e71d41787244ac538e35ebc90f5ff29e9eb4bfe9effc79c218513d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatabaseSecretsMountPostgresqlOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4d1061a847076d56edb56012f81db7e7a68eed5b658f74362af2d3276092191)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcffb7a206bea0932798d0450553f8dc6cbcf1240a3f4575d365a3f7b90c15eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__03ae6ea713454ab8d8b9ccd5c57051782ecd52142b2393da60fa2a52471b8de6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountPostgresql]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountPostgresql]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountPostgresql]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0977e4a3870df929df48947dc844a7de1859c788073cd0ea99d1a25cfa066a8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatabaseSecretsMountPostgresqlOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountPostgresqlOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__987e3411fa0d5652b5e39d7cc7337a2a5903871fc0776056350d7b54c834e7be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllowedRoles")
    def reset_allowed_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedRoles", []))

    @jsii.member(jsii_name="resetConnectionUrl")
    def reset_connection_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionUrl", []))

    @jsii.member(jsii_name="resetData")
    def reset_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetData", []))

    @jsii.member(jsii_name="resetDisableEscaping")
    def reset_disable_escaping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableEscaping", []))

    @jsii.member(jsii_name="resetMaxConnectionLifetime")
    def reset_max_connection_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConnectionLifetime", []))

    @jsii.member(jsii_name="resetMaxIdleConnections")
    def reset_max_idle_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxIdleConnections", []))

    @jsii.member(jsii_name="resetMaxOpenConnections")
    def reset_max_open_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxOpenConnections", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPluginName")
    def reset_plugin_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginName", []))

    @jsii.member(jsii_name="resetRootRotationStatements")
    def reset_root_rotation_statements(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootRotationStatements", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @jsii.member(jsii_name="resetUsernameTemplate")
    def reset_username_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsernameTemplate", []))

    @jsii.member(jsii_name="resetVerifyConnection")
    def reset_verify_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerifyConnection", []))

    @builtins.property
    @jsii.member(jsii_name="allowedRolesInput")
    def allowed_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionUrlInput")
    def connection_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="disableEscapingInput")
    def disable_escaping_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableEscapingInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConnectionLifetimeInput")
    def max_connection_lifetime_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConnectionLifetimeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxIdleConnectionsInput")
    def max_idle_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxIdleConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxOpenConnectionsInput")
    def max_open_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxOpenConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginNameInput")
    def plugin_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatementsInput")
    def root_rotation_statements_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rootRotationStatementsInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameTemplateInput")
    def username_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyConnectionInput")
    def verify_connection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verifyConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedRoles")
    def allowed_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedRoles"))

    @allowed_roles.setter
    def allowed_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4937bfa39de1b6e144abbe7ec8ad542f37ef6f44ae83d4e3c3e7cbd25d68fc15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedRoles", value)

    @builtins.property
    @jsii.member(jsii_name="connectionUrl")
    def connection_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionUrl"))

    @connection_url.setter
    def connection_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d66de9892ef2a8d785fe18484b4bcec564244bdae1955b5fb534c6fa8768f247)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionUrl", value)

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "data"))

    @data.setter
    def data(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa6913493865f7da2c3e949a2bb893b34dca9b45dda343d3b02eeb353f6ff44b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value)

    @builtins.property
    @jsii.member(jsii_name="disableEscaping")
    def disable_escaping(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableEscaping"))

    @disable_escaping.setter
    def disable_escaping(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caea0b3bffc4d641a4bbc399f7ca4746cac387582f88e86fd5412e79c22c495b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableEscaping", value)

    @builtins.property
    @jsii.member(jsii_name="maxConnectionLifetime")
    def max_connection_lifetime(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConnectionLifetime"))

    @max_connection_lifetime.setter
    def max_connection_lifetime(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90d0cabe019a4b3caf12480f643e4a87be30957ea44ebb70f67bdcf9f30d6f38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnectionLifetime", value)

    @builtins.property
    @jsii.member(jsii_name="maxIdleConnections")
    def max_idle_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIdleConnections"))

    @max_idle_connections.setter
    def max_idle_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f856629d3817cb465c94acde465df8a122c4e06a5612cf450d02c346f41073d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxIdleConnections", value)

    @builtins.property
    @jsii.member(jsii_name="maxOpenConnections")
    def max_open_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxOpenConnections"))

    @max_open_connections.setter
    def max_open_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c73903e34881e5c0487198b1b47dd591ffb01b058238ad0a762f5df94b0f16e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxOpenConnections", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7a621dd1c03f8f533010db5c0e1ceec39815e495c84f04a0e35efc6b9aeeb4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8c0a6eff7b6889ae0a32d0dd4aaef9460a124c376c4ed22e7b150d23f50a0e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="pluginName")
    def plugin_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginName"))

    @plugin_name.setter
    def plugin_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64781763e1f253fae768be269a44b2233704864f57ce51270da7d10a9fc02d7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginName", value)

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatements")
    def root_rotation_statements(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rootRotationStatements"))

    @root_rotation_statements.setter
    def root_rotation_statements(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0992b7fdb5a53c82d8b08f4424c18ec1d224a586c4775c944b857ed89a405d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootRotationStatements", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c33bc4b6d28e17773ad37467035fb4bbd76245749ff4728b1effd774bb6a496)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="usernameTemplate")
    def username_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usernameTemplate"))

    @username_template.setter
    def username_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7247b0668c35e1362a25756d5782c828a01fc617e16e8728ca1a89a31e1db3d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usernameTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="verifyConnection")
    def verify_connection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verifyConnection"))

    @verify_connection.setter
    def verify_connection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b61d479d7ad0cf227da5cea3f1dab01b2455f510467d740512822642ffac8a5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifyConnection", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountPostgresql]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountPostgresql]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountPostgresql]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec33e8a00860fb323c1a979e335975a388008832ca9aefbc89627fcbb62552b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountRedis",
    jsii_struct_bases=[],
    name_mapping={
        "host": "host",
        "name": "name",
        "password": "password",
        "username": "username",
        "allowed_roles": "allowedRoles",
        "ca_cert": "caCert",
        "data": "data",
        "insecure_tls": "insecureTls",
        "plugin_name": "pluginName",
        "port": "port",
        "root_rotation_statements": "rootRotationStatements",
        "tls": "tls",
        "verify_connection": "verifyConnection",
    },
)
class DatabaseSecretsMountRedis:
    def __init__(
        self,
        *,
        host: builtins.str,
        name: builtins.str,
        password: builtins.str,
        username: builtins.str,
        allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        ca_cert: typing.Optional[builtins.str] = None,
        data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        insecure_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        plugin_name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
        tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param host: Specifies the host to connect to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#host DatabaseSecretsMount#host}
        :param name: Name of the database connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        :param password: Specifies the password corresponding to the given username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        :param username: Specifies the username for Vault to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        :param allowed_roles: A list of roles that are allowed to use this connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        :param ca_cert: The contents of a PEM-encoded CA cert file to use to verify the Redis server's identity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#ca_cert DatabaseSecretsMount#ca_cert}
        :param data: A map of sensitive data to pass to the endpoint. Useful for templated connection strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        :param insecure_tls: Specifies whether to skip verification of the server certificate when using TLS. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#insecure_tls DatabaseSecretsMount#insecure_tls}
        :param plugin_name: Specifies the name of the plugin to use for this connection. Must be prefixed with the name of one of the supported database engine types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        :param port: The transport port to use to connect to Redis. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#port DatabaseSecretsMount#port}
        :param root_rotation_statements: A list of database statements to be executed to rotate the root user's credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        :param tls: Specifies whether to use TLS when connecting to Redis. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#tls DatabaseSecretsMount#tls}
        :param verify_connection: Specifies if the connection is verified during initial configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd74ef1d018c28c33d6bb68363675273db4bf2da3296873908e3d8e1525bb490)
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument allowed_roles", value=allowed_roles, expected_type=type_hints["allowed_roles"])
            check_type(argname="argument ca_cert", value=ca_cert, expected_type=type_hints["ca_cert"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument insecure_tls", value=insecure_tls, expected_type=type_hints["insecure_tls"])
            check_type(argname="argument plugin_name", value=plugin_name, expected_type=type_hints["plugin_name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument root_rotation_statements", value=root_rotation_statements, expected_type=type_hints["root_rotation_statements"])
            check_type(argname="argument tls", value=tls, expected_type=type_hints["tls"])
            check_type(argname="argument verify_connection", value=verify_connection, expected_type=type_hints["verify_connection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host": host,
            "name": name,
            "password": password,
            "username": username,
        }
        if allowed_roles is not None:
            self._values["allowed_roles"] = allowed_roles
        if ca_cert is not None:
            self._values["ca_cert"] = ca_cert
        if data is not None:
            self._values["data"] = data
        if insecure_tls is not None:
            self._values["insecure_tls"] = insecure_tls
        if plugin_name is not None:
            self._values["plugin_name"] = plugin_name
        if port is not None:
            self._values["port"] = port
        if root_rotation_statements is not None:
            self._values["root_rotation_statements"] = root_rotation_statements
        if tls is not None:
            self._values["tls"] = tls
        if verify_connection is not None:
            self._values["verify_connection"] = verify_connection

    @builtins.property
    def host(self) -> builtins.str:
        '''Specifies the host to connect to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#host DatabaseSecretsMount#host}
        '''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the database connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Specifies the password corresponding to the given username.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Specifies the username for Vault to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of roles that are allowed to use this connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        '''
        result = self._values.get("allowed_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ca_cert(self) -> typing.Optional[builtins.str]:
        '''The contents of a PEM-encoded CA cert file to use to verify the Redis server's identity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#ca_cert DatabaseSecretsMount#ca_cert}
        '''
        result = self._values.get("ca_cert")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of sensitive data to pass to the endpoint. Useful for templated connection strings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def insecure_tls(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to skip verification of the server certificate when using TLS.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#insecure_tls DatabaseSecretsMount#insecure_tls}
        '''
        result = self._values.get("insecure_tls")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def plugin_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the plugin to use for this connection.

        Must be prefixed with the name of one of the supported database engine types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        '''
        result = self._values.get("plugin_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The transport port to use to connect to Redis.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#port DatabaseSecretsMount#port}
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def root_rotation_statements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of database statements to be executed to rotate the root user's credentials.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        '''
        result = self._values.get("root_rotation_statements")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tls(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies whether to use TLS when connecting to Redis.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#tls DatabaseSecretsMount#tls}
        '''
        result = self._values.get("tls")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def verify_connection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if the connection is verified during initial configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        result = self._values.get("verify_connection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseSecretsMountRedis(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountRedisElasticache",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "url": "url",
        "allowed_roles": "allowedRoles",
        "data": "data",
        "password": "password",
        "plugin_name": "pluginName",
        "region": "region",
        "root_rotation_statements": "rootRotationStatements",
        "username": "username",
        "verify_connection": "verifyConnection",
    },
)
class DatabaseSecretsMountRedisElasticache:
    def __init__(
        self,
        *,
        name: builtins.str,
        url: builtins.str,
        allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        password: typing.Optional[builtins.str] = None,
        plugin_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
        username: typing.Optional[builtins.str] = None,
        verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Name of the database connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        :param url: The configuration endpoint for the ElastiCache cluster to connect to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#url DatabaseSecretsMount#url}
        :param allowed_roles: A list of roles that are allowed to use this connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        :param data: A map of sensitive data to pass to the endpoint. Useful for templated connection strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        :param password: The AWS secret key id to use to talk to ElastiCache. If omitted the credentials chain provider is used instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        :param plugin_name: Specifies the name of the plugin to use for this connection. Must be prefixed with the name of one of the supported database engine types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        :param region: The AWS region where the ElastiCache cluster is hosted. If omitted the plugin tries to infer the region from the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#region DatabaseSecretsMount#region}
        :param root_rotation_statements: A list of database statements to be executed to rotate the root user's credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        :param username: The AWS access key id to use to talk to ElastiCache. If omitted the credentials chain provider is used instead. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        :param verify_connection: Specifies if the connection is verified during initial configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81a5ccd1bcd0c89a82fbb3ee877551440220d55536cf39b944ea8ffb010c613f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument allowed_roles", value=allowed_roles, expected_type=type_hints["allowed_roles"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument plugin_name", value=plugin_name, expected_type=type_hints["plugin_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument root_rotation_statements", value=root_rotation_statements, expected_type=type_hints["root_rotation_statements"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument verify_connection", value=verify_connection, expected_type=type_hints["verify_connection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "url": url,
        }
        if allowed_roles is not None:
            self._values["allowed_roles"] = allowed_roles
        if data is not None:
            self._values["data"] = data
        if password is not None:
            self._values["password"] = password
        if plugin_name is not None:
            self._values["plugin_name"] = plugin_name
        if region is not None:
            self._values["region"] = region
        if root_rotation_statements is not None:
            self._values["root_rotation_statements"] = root_rotation_statements
        if username is not None:
            self._values["username"] = username
        if verify_connection is not None:
            self._values["verify_connection"] = verify_connection

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the database connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''The configuration endpoint for the ElastiCache cluster to connect to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#url DatabaseSecretsMount#url}
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of roles that are allowed to use this connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        '''
        result = self._values.get("allowed_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def data(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of sensitive data to pass to the endpoint. Useful for templated connection strings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The AWS secret key id to use to talk to ElastiCache.

        If omitted the credentials chain provider is used instead.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugin_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the plugin to use for this connection.

        Must be prefixed with the name of one of the supported database engine types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        '''
        result = self._values.get("plugin_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region where the ElastiCache cluster is hosted.

        If omitted the plugin tries to infer the region from the environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#region DatabaseSecretsMount#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def root_rotation_statements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of database statements to be executed to rotate the root user's credentials.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        '''
        result = self._values.get("root_rotation_statements")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The AWS access key id to use to talk to ElastiCache.

        If omitted the credentials chain provider is used instead.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verify_connection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if the connection is verified during initial configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        result = self._values.get("verify_connection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseSecretsMountRedisElasticache(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseSecretsMountRedisElasticacheList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountRedisElasticacheList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__921938093bd0779396a82fd95df04f004ee52eca333af63b082e42c96e7f4484)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DatabaseSecretsMountRedisElasticacheOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d224e78a50303205fb0e30957a50a9744eb28fdcab4ff76cb4f0b39c799196cc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatabaseSecretsMountRedisElasticacheOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40530eb93a5eb2f934774bb9b296bb029b438605e3167de726471f2150b90593)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2331c7cba8f488ca86a1e0220ae5360227be063e8531e6360f0f6127912b7c5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6798afc1e44e012959054a1507176c4995c86a30edecd3144b2c42b0d1cca9d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountRedisElasticache]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountRedisElasticache]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountRedisElasticache]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9205d31520857c1a57803269245118f71e4d95565438d8e353657d6e8d74c35d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatabaseSecretsMountRedisElasticacheOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountRedisElasticacheOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16b1f56bf0fbc286f1ceae8a3a5b3394aa7b4e0fdc9858596219b2e60484b90d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllowedRoles")
    def reset_allowed_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedRoles", []))

    @jsii.member(jsii_name="resetData")
    def reset_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetData", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPluginName")
    def reset_plugin_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginName", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRootRotationStatements")
    def reset_root_rotation_statements(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootRotationStatements", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @jsii.member(jsii_name="resetVerifyConnection")
    def reset_verify_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerifyConnection", []))

    @builtins.property
    @jsii.member(jsii_name="allowedRolesInput")
    def allowed_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginNameInput")
    def plugin_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginNameInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatementsInput")
    def root_rotation_statements_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rootRotationStatementsInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyConnectionInput")
    def verify_connection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verifyConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedRoles")
    def allowed_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedRoles"))

    @allowed_roles.setter
    def allowed_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4972651314622eec55c83e17298e7a292d3df05db70a211653831530bf37bb3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedRoles", value)

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "data"))

    @data.setter
    def data(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff81d92f33f44d0401873a77635454dc4a32d2d163453499d4a55fe0272aa2ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31c203e132fef874aa539e47b36ff5c311030110bb326f036ff9185cce1caf3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9251fc6261a5048feec4ca554c1dbe8767e479526309a436b026a7bcd5447b1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="pluginName")
    def plugin_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginName"))

    @plugin_name.setter
    def plugin_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8ce60e46501da7f71bb537402b6d28539917757f1f17e3e4cee988f9dd44110)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginName", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50b691b4882d428e33d4a3fdc7261c002e29152f11fbd0ef6669cae888b56d50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatements")
    def root_rotation_statements(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rootRotationStatements"))

    @root_rotation_statements.setter
    def root_rotation_statements(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab2b3a13cc8e8193a4280ca53e066b489aea5b36dd7d72d7d426ab22bba1923d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootRotationStatements", value)

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__818b31e7b6b0ca7e86ddcc8a75a910af0a8721a9926fba0e36657f529342424b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7425224cf4f63a501c313c500038c5e501591ec2219bcf81fdd571659b1663c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="verifyConnection")
    def verify_connection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verifyConnection"))

    @verify_connection.setter
    def verify_connection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c79f6d65e41787a95e58461d1e5c43269fa8dd3f2b26dac06725302821b38b90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifyConnection", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountRedisElasticache]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountRedisElasticache]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountRedisElasticache]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__431f1d8e710f641a7d2e5b2b330e92f6d9a999c34f0f48798fea0f643268592f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatabaseSecretsMountRedisList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountRedisList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8038393689bece62b282204023d36bcd0cea5f4463cac800d0eea9e8dcb29e47)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DatabaseSecretsMountRedisOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c41753c9524f3adccecba1846e0365d02101a186f5b47069ac357825f43abfe1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatabaseSecretsMountRedisOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbf2092d13dd3a793a5fd71d268d30a796ae529096c2a39c837f5719134b8929)
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
            type_hints = typing.get_type_hints(_typecheckingstub__79e25f4b0c1ebf352570b10cfc6e7c94d17fb7f7de62542eb1ca23691deb0ac5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__170221ea270f4208ef11d51946b1751476f4e628984f07dde80726466e5eba6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountRedis]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountRedis]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountRedis]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93dbccf06c353d37e6b2fac6549b5160fc91f43aa2777ac392d4c143135251cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatabaseSecretsMountRedisOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountRedisOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ec15fc1eae349b7b84ceb2f59851aa1dce9a333f383e62300dcf5727973cc6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllowedRoles")
    def reset_allowed_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedRoles", []))

    @jsii.member(jsii_name="resetCaCert")
    def reset_ca_cert(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaCert", []))

    @jsii.member(jsii_name="resetData")
    def reset_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetData", []))

    @jsii.member(jsii_name="resetInsecureTls")
    def reset_insecure_tls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsecureTls", []))

    @jsii.member(jsii_name="resetPluginName")
    def reset_plugin_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginName", []))

    @jsii.member(jsii_name="resetPort")
    def reset_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPort", []))

    @jsii.member(jsii_name="resetRootRotationStatements")
    def reset_root_rotation_statements(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootRotationStatements", []))

    @jsii.member(jsii_name="resetTls")
    def reset_tls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTls", []))

    @jsii.member(jsii_name="resetVerifyConnection")
    def reset_verify_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerifyConnection", []))

    @builtins.property
    @jsii.member(jsii_name="allowedRolesInput")
    def allowed_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="caCertInput")
    def ca_cert_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "caCertInput"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="insecureTlsInput")
    def insecure_tls_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecureTlsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginNameInput")
    def plugin_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginNameInput"))

    @builtins.property
    @jsii.member(jsii_name="portInput")
    def port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "portInput"))

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatementsInput")
    def root_rotation_statements_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rootRotationStatementsInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsInput")
    def tls_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tlsInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyConnectionInput")
    def verify_connection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verifyConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedRoles")
    def allowed_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedRoles"))

    @allowed_roles.setter
    def allowed_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02969329ee4677e165f15b28ffab3baa58c74458a1d46194d42f5d24587b8db9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedRoles", value)

    @builtins.property
    @jsii.member(jsii_name="caCert")
    def ca_cert(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caCert"))

    @ca_cert.setter
    def ca_cert(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ab6edd16e82f20545dc498ac3aa542479cada3db180cdee6115ada6358acfc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caCert", value)

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "data"))

    @data.setter
    def data(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c12ac6afbd7f1e0ca7ebc691115f4ba938ebe36ca13bcc4a9aff8e82aa36937)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value)

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ea13b86099ffad3ee4eadefa39dbca13371916b0546745f5b7e0140e7932ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value)

    @builtins.property
    @jsii.member(jsii_name="insecureTls")
    def insecure_tls(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "insecureTls"))

    @insecure_tls.setter
    def insecure_tls(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__900a20b1da6b45b1a40f9c4ad57058d1ca7d9abd7ffe88e19ec6bf6316341b0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insecureTls", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f32416472cf7419746e1a67eb4e13c2ecb318e570812b353912d2af8d4b1c75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10953eb9881740c9f7b394d946575e9613659349efd696a7876155a8efb2197d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="pluginName")
    def plugin_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginName"))

    @plugin_name.setter
    def plugin_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e2ed6fa4bdb9ccfe8a2243bc09e076c08f779a80ef4135a550ac5dafac91875)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginName", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @port.setter
    def port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fb9a15192a648007db46042183af609b442db5d8856d15bc2b6746507735167)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatements")
    def root_rotation_statements(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rootRotationStatements"))

    @root_rotation_statements.setter
    def root_rotation_statements(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__995268070c02ba706851c483dd0cf862db2b4bb8092858016a029984272debc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootRotationStatements", value)

    @builtins.property
    @jsii.member(jsii_name="tls")
    def tls(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tls"))

    @tls.setter
    def tls(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28fa347e60e4e5c9a5c3a254bb36831c686973aa32dce57cb164a4dfcdaa6ea7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tls", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e3405aa5f8703ebdbd3f504af3171332838b195b15ace648190aee122a302ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="verifyConnection")
    def verify_connection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verifyConnection"))

    @verify_connection.setter
    def verify_connection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0d8a60b444f39ce52f7c3f83df4bd2e2121d5c17809231e27d4024ad14d2b82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifyConnection", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountRedis]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountRedis]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountRedis]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8f8794938eca69670ebcd29de0e1fd59b92681623994d7d76ecd42630f53547)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountRedshift",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "allowed_roles": "allowedRoles",
        "connection_url": "connectionUrl",
        "data": "data",
        "disable_escaping": "disableEscaping",
        "max_connection_lifetime": "maxConnectionLifetime",
        "max_idle_connections": "maxIdleConnections",
        "max_open_connections": "maxOpenConnections",
        "password": "password",
        "plugin_name": "pluginName",
        "root_rotation_statements": "rootRotationStatements",
        "username": "username",
        "username_template": "usernameTemplate",
        "verify_connection": "verifyConnection",
    },
)
class DatabaseSecretsMountRedshift:
    def __init__(
        self,
        *,
        name: builtins.str,
        allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection_url: typing.Optional[builtins.str] = None,
        data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        disable_escaping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        max_connection_lifetime: typing.Optional[jsii.Number] = None,
        max_idle_connections: typing.Optional[jsii.Number] = None,
        max_open_connections: typing.Optional[jsii.Number] = None,
        password: typing.Optional[builtins.str] = None,
        plugin_name: typing.Optional[builtins.str] = None,
        root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
        username: typing.Optional[builtins.str] = None,
        username_template: typing.Optional[builtins.str] = None,
        verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Name of the database connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        :param allowed_roles: A list of roles that are allowed to use this connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        :param connection_url: Connection string to use to connect to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#connection_url DatabaseSecretsMount#connection_url}
        :param data: A map of sensitive data to pass to the endpoint. Useful for templated connection strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        :param disable_escaping: Disable special character escaping in username and password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#disable_escaping DatabaseSecretsMount#disable_escaping}
        :param max_connection_lifetime: Maximum number of seconds a connection may be reused. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_connection_lifetime DatabaseSecretsMount#max_connection_lifetime}
        :param max_idle_connections: Maximum number of idle connections to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_idle_connections DatabaseSecretsMount#max_idle_connections}
        :param max_open_connections: Maximum number of open connections to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_open_connections DatabaseSecretsMount#max_open_connections}
        :param password: The root credential password used in the connection URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        :param plugin_name: Specifies the name of the plugin to use for this connection. Must be prefixed with the name of one of the supported database engine types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        :param root_rotation_statements: A list of database statements to be executed to rotate the root user's credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        :param username: The root credential username used in the connection URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        :param username_template: Username generation template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username_template DatabaseSecretsMount#username_template}
        :param verify_connection: Specifies if the connection is verified during initial configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8924b28c9b7d4db003afc64e9791a61fe5a17214504b14480646b4812716b2fd)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allowed_roles", value=allowed_roles, expected_type=type_hints["allowed_roles"])
            check_type(argname="argument connection_url", value=connection_url, expected_type=type_hints["connection_url"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument disable_escaping", value=disable_escaping, expected_type=type_hints["disable_escaping"])
            check_type(argname="argument max_connection_lifetime", value=max_connection_lifetime, expected_type=type_hints["max_connection_lifetime"])
            check_type(argname="argument max_idle_connections", value=max_idle_connections, expected_type=type_hints["max_idle_connections"])
            check_type(argname="argument max_open_connections", value=max_open_connections, expected_type=type_hints["max_open_connections"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument plugin_name", value=plugin_name, expected_type=type_hints["plugin_name"])
            check_type(argname="argument root_rotation_statements", value=root_rotation_statements, expected_type=type_hints["root_rotation_statements"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument username_template", value=username_template, expected_type=type_hints["username_template"])
            check_type(argname="argument verify_connection", value=verify_connection, expected_type=type_hints["verify_connection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if allowed_roles is not None:
            self._values["allowed_roles"] = allowed_roles
        if connection_url is not None:
            self._values["connection_url"] = connection_url
        if data is not None:
            self._values["data"] = data
        if disable_escaping is not None:
            self._values["disable_escaping"] = disable_escaping
        if max_connection_lifetime is not None:
            self._values["max_connection_lifetime"] = max_connection_lifetime
        if max_idle_connections is not None:
            self._values["max_idle_connections"] = max_idle_connections
        if max_open_connections is not None:
            self._values["max_open_connections"] = max_open_connections
        if password is not None:
            self._values["password"] = password
        if plugin_name is not None:
            self._values["plugin_name"] = plugin_name
        if root_rotation_statements is not None:
            self._values["root_rotation_statements"] = root_rotation_statements
        if username is not None:
            self._values["username"] = username
        if username_template is not None:
            self._values["username_template"] = username_template
        if verify_connection is not None:
            self._values["verify_connection"] = verify_connection

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the database connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of roles that are allowed to use this connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        '''
        result = self._values.get("allowed_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def connection_url(self) -> typing.Optional[builtins.str]:
        '''Connection string to use to connect to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#connection_url DatabaseSecretsMount#connection_url}
        '''
        result = self._values.get("connection_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of sensitive data to pass to the endpoint. Useful for templated connection strings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def disable_escaping(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable special character escaping in username and password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#disable_escaping DatabaseSecretsMount#disable_escaping}
        '''
        result = self._values.get("disable_escaping")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def max_connection_lifetime(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of seconds a connection may be reused.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_connection_lifetime DatabaseSecretsMount#max_connection_lifetime}
        '''
        result = self._values.get("max_connection_lifetime")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_idle_connections(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of idle connections to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_idle_connections DatabaseSecretsMount#max_idle_connections}
        '''
        result = self._values.get("max_idle_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_open_connections(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of open connections to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_open_connections DatabaseSecretsMount#max_open_connections}
        '''
        result = self._values.get("max_open_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The root credential password used in the connection URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugin_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the plugin to use for this connection.

        Must be prefixed with the name of one of the supported database engine types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        '''
        result = self._values.get("plugin_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def root_rotation_statements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of database statements to be executed to rotate the root user's credentials.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        '''
        result = self._values.get("root_rotation_statements")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The root credential username used in the connection URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username_template(self) -> typing.Optional[builtins.str]:
        '''Username generation template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username_template DatabaseSecretsMount#username_template}
        '''
        result = self._values.get("username_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verify_connection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if the connection is verified during initial configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        result = self._values.get("verify_connection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseSecretsMountRedshift(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseSecretsMountRedshiftList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountRedshiftList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6db3faaa35a2320614fee787b8d92846002a747df0b14762cde8dec6954dfc1b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DatabaseSecretsMountRedshiftOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1f0de23009b256c96abff9637f963ea6e8e969ec288ad90b4a3cc24c576cf09)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatabaseSecretsMountRedshiftOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef99faf6acf134f8b4e0796ab1cac1a3384d1f0a9c83743c4fb0cc1af9cee0ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dec099000d033a9d38feed119d3e865634517e333f492c1cd4bbbc96bf41bd53)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfefc03844b087f6bef9546d8d99adb31aa06342f655d54ec9b6295c11e92132)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountRedshift]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountRedshift]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountRedshift]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4549c24036d4775f6c31d799049e071909630bd20ee1ce01de4f636cf59bf06b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatabaseSecretsMountRedshiftOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountRedshiftOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d124eadbabce102a36103b6270b1378cafe5c9509897f9a2c8dd52b4d8d931d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllowedRoles")
    def reset_allowed_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedRoles", []))

    @jsii.member(jsii_name="resetConnectionUrl")
    def reset_connection_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionUrl", []))

    @jsii.member(jsii_name="resetData")
    def reset_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetData", []))

    @jsii.member(jsii_name="resetDisableEscaping")
    def reset_disable_escaping(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableEscaping", []))

    @jsii.member(jsii_name="resetMaxConnectionLifetime")
    def reset_max_connection_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConnectionLifetime", []))

    @jsii.member(jsii_name="resetMaxIdleConnections")
    def reset_max_idle_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxIdleConnections", []))

    @jsii.member(jsii_name="resetMaxOpenConnections")
    def reset_max_open_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxOpenConnections", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPluginName")
    def reset_plugin_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginName", []))

    @jsii.member(jsii_name="resetRootRotationStatements")
    def reset_root_rotation_statements(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootRotationStatements", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @jsii.member(jsii_name="resetUsernameTemplate")
    def reset_username_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsernameTemplate", []))

    @jsii.member(jsii_name="resetVerifyConnection")
    def reset_verify_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerifyConnection", []))

    @builtins.property
    @jsii.member(jsii_name="allowedRolesInput")
    def allowed_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionUrlInput")
    def connection_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="disableEscapingInput")
    def disable_escaping_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableEscapingInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConnectionLifetimeInput")
    def max_connection_lifetime_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConnectionLifetimeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxIdleConnectionsInput")
    def max_idle_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxIdleConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxOpenConnectionsInput")
    def max_open_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxOpenConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginNameInput")
    def plugin_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatementsInput")
    def root_rotation_statements_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rootRotationStatementsInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameTemplateInput")
    def username_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyConnectionInput")
    def verify_connection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verifyConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedRoles")
    def allowed_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedRoles"))

    @allowed_roles.setter
    def allowed_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c35cc6011cd998a58a8b521e59fa856130a110c0b15133a3bd53d7376a73c795)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedRoles", value)

    @builtins.property
    @jsii.member(jsii_name="connectionUrl")
    def connection_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionUrl"))

    @connection_url.setter
    def connection_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7544b2389a6f7a5c9c4e2803a5736664d22dbad092a91ad97dcd24aef98d5a99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionUrl", value)

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "data"))

    @data.setter
    def data(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff96e92d242f06ede50de26ce02b2fe1f88f9f33529ad70e6fe97542a5a175f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value)

    @builtins.property
    @jsii.member(jsii_name="disableEscaping")
    def disable_escaping(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableEscaping"))

    @disable_escaping.setter
    def disable_escaping(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80f25d34b0e38f083abe44bc5beefd388730658d830de2882c54df00fd5cbd3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableEscaping", value)

    @builtins.property
    @jsii.member(jsii_name="maxConnectionLifetime")
    def max_connection_lifetime(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConnectionLifetime"))

    @max_connection_lifetime.setter
    def max_connection_lifetime(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ab470d35a8c2ed866f0eac784625fcc7f9d1cc6ca12ff3f4f953b3785c08643)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnectionLifetime", value)

    @builtins.property
    @jsii.member(jsii_name="maxIdleConnections")
    def max_idle_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIdleConnections"))

    @max_idle_connections.setter
    def max_idle_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39d9fde83a2cbfa5e468fbfcb7945d604ea1016bcda9e281ea5711497a5fe438)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxIdleConnections", value)

    @builtins.property
    @jsii.member(jsii_name="maxOpenConnections")
    def max_open_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxOpenConnections"))

    @max_open_connections.setter
    def max_open_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a4837e3b5fc41bcb00c42d95a740c35c74d36e97dc6884b8fb8289a2b84c98b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxOpenConnections", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__102e0a70e8df3bc7e0454a41bc76d754c196793967f5b1854631f97fe5fb3c62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6121ead6e5709f014746416b339b281a97160e5a428bc31bdc8a1150ba194e60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="pluginName")
    def plugin_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginName"))

    @plugin_name.setter
    def plugin_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c356d63336e583c5d1fb4c3457d2c59994fbc747876a6052dbb01e161d0dd89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginName", value)

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatements")
    def root_rotation_statements(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rootRotationStatements"))

    @root_rotation_statements.setter
    def root_rotation_statements(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5f0be15e64ee46acd286fd334881bbdd6ab53e90d45c898977a93e85e356ee4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootRotationStatements", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d4769b7e4298816da852c9cc7d82d3afbd13e285f14d5bd93e4c44a6c69f751)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="usernameTemplate")
    def username_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usernameTemplate"))

    @username_template.setter
    def username_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41ba7ff90d250e606837abc0cfce88362e607dc6d9bc207d76873b03fc65e803)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usernameTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="verifyConnection")
    def verify_connection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verifyConnection"))

    @verify_connection.setter
    def verify_connection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d266a894aa0c2f9990b03946d55ee1c327a02cc0e30847aae7ab4a066749264b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifyConnection", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountRedshift]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountRedshift]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountRedshift]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2b41f433408c6fd6eaf947ce11e2e61318d1417cbad0320ccc4e4631a71dee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountSnowflake",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "allowed_roles": "allowedRoles",
        "connection_url": "connectionUrl",
        "data": "data",
        "max_connection_lifetime": "maxConnectionLifetime",
        "max_idle_connections": "maxIdleConnections",
        "max_open_connections": "maxOpenConnections",
        "password": "password",
        "plugin_name": "pluginName",
        "root_rotation_statements": "rootRotationStatements",
        "username": "username",
        "username_template": "usernameTemplate",
        "verify_connection": "verifyConnection",
    },
)
class DatabaseSecretsMountSnowflake:
    def __init__(
        self,
        *,
        name: builtins.str,
        allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection_url: typing.Optional[builtins.str] = None,
        data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        max_connection_lifetime: typing.Optional[jsii.Number] = None,
        max_idle_connections: typing.Optional[jsii.Number] = None,
        max_open_connections: typing.Optional[jsii.Number] = None,
        password: typing.Optional[builtins.str] = None,
        plugin_name: typing.Optional[builtins.str] = None,
        root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
        username: typing.Optional[builtins.str] = None,
        username_template: typing.Optional[builtins.str] = None,
        verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Name of the database connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        :param allowed_roles: A list of roles that are allowed to use this connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        :param connection_url: Connection string to use to connect to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#connection_url DatabaseSecretsMount#connection_url}
        :param data: A map of sensitive data to pass to the endpoint. Useful for templated connection strings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        :param max_connection_lifetime: Maximum number of seconds a connection may be reused. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_connection_lifetime DatabaseSecretsMount#max_connection_lifetime}
        :param max_idle_connections: Maximum number of idle connections to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_idle_connections DatabaseSecretsMount#max_idle_connections}
        :param max_open_connections: Maximum number of open connections to the database. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_open_connections DatabaseSecretsMount#max_open_connections}
        :param password: The root credential password used in the connection URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        :param plugin_name: Specifies the name of the plugin to use for this connection. Must be prefixed with the name of one of the supported database engine types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        :param root_rotation_statements: A list of database statements to be executed to rotate the root user's credentials. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        :param username: The root credential username used in the connection URL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        :param username_template: Username generation template. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username_template DatabaseSecretsMount#username_template}
        :param verify_connection: Specifies if the connection is verified during initial configuration. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f69284a6cae7f9a93e2d78b68c96325f99de2c92d57cd8ecd635dc0f0c084b0)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument allowed_roles", value=allowed_roles, expected_type=type_hints["allowed_roles"])
            check_type(argname="argument connection_url", value=connection_url, expected_type=type_hints["connection_url"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument max_connection_lifetime", value=max_connection_lifetime, expected_type=type_hints["max_connection_lifetime"])
            check_type(argname="argument max_idle_connections", value=max_idle_connections, expected_type=type_hints["max_idle_connections"])
            check_type(argname="argument max_open_connections", value=max_open_connections, expected_type=type_hints["max_open_connections"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument plugin_name", value=plugin_name, expected_type=type_hints["plugin_name"])
            check_type(argname="argument root_rotation_statements", value=root_rotation_statements, expected_type=type_hints["root_rotation_statements"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument username_template", value=username_template, expected_type=type_hints["username_template"])
            check_type(argname="argument verify_connection", value=verify_connection, expected_type=type_hints["verify_connection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if allowed_roles is not None:
            self._values["allowed_roles"] = allowed_roles
        if connection_url is not None:
            self._values["connection_url"] = connection_url
        if data is not None:
            self._values["data"] = data
        if max_connection_lifetime is not None:
            self._values["max_connection_lifetime"] = max_connection_lifetime
        if max_idle_connections is not None:
            self._values["max_idle_connections"] = max_idle_connections
        if max_open_connections is not None:
            self._values["max_open_connections"] = max_open_connections
        if password is not None:
            self._values["password"] = password
        if plugin_name is not None:
            self._values["plugin_name"] = plugin_name
        if root_rotation_statements is not None:
            self._values["root_rotation_statements"] = root_rotation_statements
        if username is not None:
            self._values["username"] = username
        if username_template is not None:
            self._values["username_template"] = username_template
        if verify_connection is not None:
            self._values["verify_connection"] = verify_connection

    @builtins.property
    def name(self) -> builtins.str:
        '''Name of the database connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#name DatabaseSecretsMount#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of roles that are allowed to use this connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#allowed_roles DatabaseSecretsMount#allowed_roles}
        '''
        result = self._values.get("allowed_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def connection_url(self) -> typing.Optional[builtins.str]:
        '''Connection string to use to connect to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#connection_url DatabaseSecretsMount#connection_url}
        '''
        result = self._values.get("connection_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of sensitive data to pass to the endpoint. Useful for templated connection strings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#data DatabaseSecretsMount#data}
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def max_connection_lifetime(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of seconds a connection may be reused.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_connection_lifetime DatabaseSecretsMount#max_connection_lifetime}
        '''
        result = self._values.get("max_connection_lifetime")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_idle_connections(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of idle connections to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_idle_connections DatabaseSecretsMount#max_idle_connections}
        '''
        result = self._values.get("max_idle_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_open_connections(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of open connections to the database.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#max_open_connections DatabaseSecretsMount#max_open_connections}
        '''
        result = self._values.get("max_open_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The root credential password used in the connection URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#password DatabaseSecretsMount#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugin_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the plugin to use for this connection.

        Must be prefixed with the name of one of the supported database engine types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#plugin_name DatabaseSecretsMount#plugin_name}
        '''
        result = self._values.get("plugin_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def root_rotation_statements(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of database statements to be executed to rotate the root user's credentials.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#root_rotation_statements DatabaseSecretsMount#root_rotation_statements}
        '''
        result = self._values.get("root_rotation_statements")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The root credential username used in the connection URL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username DatabaseSecretsMount#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username_template(self) -> typing.Optional[builtins.str]:
        '''Username generation template.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#username_template DatabaseSecretsMount#username_template}
        '''
        result = self._values.get("username_template")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verify_connection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if the connection is verified during initial configuration.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/vault/3.19.0/docs/resources/database_secrets_mount#verify_connection DatabaseSecretsMount#verify_connection}
        '''
        result = self._values.get("verify_connection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseSecretsMountSnowflake(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseSecretsMountSnowflakeList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountSnowflakeList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2398d68acd89728fdf2ffca6f56eeae10ff7109806747197f539733a80e04e5a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DatabaseSecretsMountSnowflakeOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2549cd03910419417a057c0471a411319bc304f6f9b2f42cf3120e3d027340e1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DatabaseSecretsMountSnowflakeOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d40a6f286ae3c2be2b7b2912275d1a22b37bdd37e5895f6204561d4d3443c245)
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
            type_hints = typing.get_type_hints(_typecheckingstub__46185847c25339c14c6040388d130b12507c084c1a2201617eeec07285542d87)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cf1afbb16827f7ae95f2f3cb14f921408cab1ca3cd79205263bd7af6c7c4ccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountSnowflake]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountSnowflake]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountSnowflake]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e083567f6ca41d8c48f32a9d057e49f6413e1be629b84f24955696ef4acf7e17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DatabaseSecretsMountSnowflakeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-vault.databaseSecretsMount.DatabaseSecretsMountSnowflakeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f47d988f5970ddc89a0688164c50df541b2f2b4d14adcb17f4bd7a429a0fa4a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllowedRoles")
    def reset_allowed_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedRoles", []))

    @jsii.member(jsii_name="resetConnectionUrl")
    def reset_connection_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionUrl", []))

    @jsii.member(jsii_name="resetData")
    def reset_data(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetData", []))

    @jsii.member(jsii_name="resetMaxConnectionLifetime")
    def reset_max_connection_lifetime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxConnectionLifetime", []))

    @jsii.member(jsii_name="resetMaxIdleConnections")
    def reset_max_idle_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxIdleConnections", []))

    @jsii.member(jsii_name="resetMaxOpenConnections")
    def reset_max_open_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxOpenConnections", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPluginName")
    def reset_plugin_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginName", []))

    @jsii.member(jsii_name="resetRootRotationStatements")
    def reset_root_rotation_statements(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRootRotationStatements", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @jsii.member(jsii_name="resetUsernameTemplate")
    def reset_username_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsernameTemplate", []))

    @jsii.member(jsii_name="resetVerifyConnection")
    def reset_verify_connection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerifyConnection", []))

    @builtins.property
    @jsii.member(jsii_name="allowedRolesInput")
    def allowed_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionUrlInput")
    def connection_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="dataInput")
    def data_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "dataInput"))

    @builtins.property
    @jsii.member(jsii_name="maxConnectionLifetimeInput")
    def max_connection_lifetime_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxConnectionLifetimeInput"))

    @builtins.property
    @jsii.member(jsii_name="maxIdleConnectionsInput")
    def max_idle_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxIdleConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxOpenConnectionsInput")
    def max_open_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxOpenConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginNameInput")
    def plugin_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginNameInput"))

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatementsInput")
    def root_rotation_statements_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "rootRotationStatementsInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameTemplateInput")
    def username_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="verifyConnectionInput")
    def verify_connection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verifyConnectionInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedRoles")
    def allowed_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedRoles"))

    @allowed_roles.setter
    def allowed_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27f6a237c25d179fb2dc599b0e2fb2d6d2db3b767c91a69a969557747bb2f14c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedRoles", value)

    @builtins.property
    @jsii.member(jsii_name="connectionUrl")
    def connection_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionUrl"))

    @connection_url.setter
    def connection_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f9c34570d5cec6c47ba220be91751c80f637d84aab39611f2c9e3cabfef41c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionUrl", value)

    @builtins.property
    @jsii.member(jsii_name="data")
    def data(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "data"))

    @data.setter
    def data(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e166de2f457b145ad6dffb3a05601e7a377204b583bba23eb440b111932ffb47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "data", value)

    @builtins.property
    @jsii.member(jsii_name="maxConnectionLifetime")
    def max_connection_lifetime(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxConnectionLifetime"))

    @max_connection_lifetime.setter
    def max_connection_lifetime(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66d9e24e9139ef8a4caf88bac01696df8828a63b7211e4d32b29a8134b7a4791)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxConnectionLifetime", value)

    @builtins.property
    @jsii.member(jsii_name="maxIdleConnections")
    def max_idle_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxIdleConnections"))

    @max_idle_connections.setter
    def max_idle_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1064b7cf6c3c4a5ca4c795ed35bc97ee461f665c42f66b589dd6ccc891f0b212)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxIdleConnections", value)

    @builtins.property
    @jsii.member(jsii_name="maxOpenConnections")
    def max_open_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxOpenConnections"))

    @max_open_connections.setter
    def max_open_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__248fe56aaafa5e5f75b94292e6f2d1b0e48195438a710cc228b2e5d6c3386d2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxOpenConnections", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7ab70d4f4cd04795d8921b6f785380dc50e69b2ddc953b776cca2dfafc7d7cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e0833dca66d9da8c482ca58f7e2f368ace6cb2f2c52a90480441626df9b00e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="pluginName")
    def plugin_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginName"))

    @plugin_name.setter
    def plugin_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ddf60b128ae6c4d546625278c3b7825fcda2355c10c8bb2a6dc522ccfa2ccd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginName", value)

    @builtins.property
    @jsii.member(jsii_name="rootRotationStatements")
    def root_rotation_statements(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rootRotationStatements"))

    @root_rotation_statements.setter
    def root_rotation_statements(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25fdf0d0b61412c820dda72d214cefce8468a537134e4b77b87a2b6393fc9ce1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rootRotationStatements", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2db1d0ac223df8ee2c1cf4c8870aa56be5283c75939ae6d4c60021d3128cb76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="usernameTemplate")
    def username_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "usernameTemplate"))

    @username_template.setter
    def username_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f0513d4ae563396bab70bac6c048198bbdd728b34f17e9f4c1b6e6f473fd68f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usernameTemplate", value)

    @builtins.property
    @jsii.member(jsii_name="verifyConnection")
    def verify_connection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verifyConnection"))

    @verify_connection.setter
    def verify_connection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa9541c6edef7da4a14b776f076365a23b08787e23c04636e8f4f9e34a5ac30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verifyConnection", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountSnowflake]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountSnowflake]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountSnowflake]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9b7e0a72578edce80d6c54649e7a4484958ab830ae4119644cdded65a09ae41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DatabaseSecretsMount",
    "DatabaseSecretsMountCassandra",
    "DatabaseSecretsMountCassandraList",
    "DatabaseSecretsMountCassandraOutputReference",
    "DatabaseSecretsMountConfig",
    "DatabaseSecretsMountCouchbase",
    "DatabaseSecretsMountCouchbaseList",
    "DatabaseSecretsMountCouchbaseOutputReference",
    "DatabaseSecretsMountElasticsearch",
    "DatabaseSecretsMountElasticsearchList",
    "DatabaseSecretsMountElasticsearchOutputReference",
    "DatabaseSecretsMountHana",
    "DatabaseSecretsMountHanaList",
    "DatabaseSecretsMountHanaOutputReference",
    "DatabaseSecretsMountInfluxdb",
    "DatabaseSecretsMountInfluxdbList",
    "DatabaseSecretsMountInfluxdbOutputReference",
    "DatabaseSecretsMountMongodb",
    "DatabaseSecretsMountMongodbList",
    "DatabaseSecretsMountMongodbOutputReference",
    "DatabaseSecretsMountMongodbatlas",
    "DatabaseSecretsMountMongodbatlasList",
    "DatabaseSecretsMountMongodbatlasOutputReference",
    "DatabaseSecretsMountMssql",
    "DatabaseSecretsMountMssqlList",
    "DatabaseSecretsMountMssqlOutputReference",
    "DatabaseSecretsMountMysql",
    "DatabaseSecretsMountMysqlAurora",
    "DatabaseSecretsMountMysqlAuroraList",
    "DatabaseSecretsMountMysqlAuroraOutputReference",
    "DatabaseSecretsMountMysqlLegacy",
    "DatabaseSecretsMountMysqlLegacyList",
    "DatabaseSecretsMountMysqlLegacyOutputReference",
    "DatabaseSecretsMountMysqlList",
    "DatabaseSecretsMountMysqlOutputReference",
    "DatabaseSecretsMountMysqlRds",
    "DatabaseSecretsMountMysqlRdsList",
    "DatabaseSecretsMountMysqlRdsOutputReference",
    "DatabaseSecretsMountOracle",
    "DatabaseSecretsMountOracleList",
    "DatabaseSecretsMountOracleOutputReference",
    "DatabaseSecretsMountPostgresql",
    "DatabaseSecretsMountPostgresqlList",
    "DatabaseSecretsMountPostgresqlOutputReference",
    "DatabaseSecretsMountRedis",
    "DatabaseSecretsMountRedisElasticache",
    "DatabaseSecretsMountRedisElasticacheList",
    "DatabaseSecretsMountRedisElasticacheOutputReference",
    "DatabaseSecretsMountRedisList",
    "DatabaseSecretsMountRedisOutputReference",
    "DatabaseSecretsMountRedshift",
    "DatabaseSecretsMountRedshiftList",
    "DatabaseSecretsMountRedshiftOutputReference",
    "DatabaseSecretsMountSnowflake",
    "DatabaseSecretsMountSnowflakeList",
    "DatabaseSecretsMountSnowflakeOutputReference",
]

publication.publish()

def _typecheckingstub__ac8f62cbd006ac2878530cb2f917cded0ae67aa667f7ca0cc17e2d8ab8d8ef03(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    path: builtins.str,
    allowed_managed_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    audit_non_hmac_request_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    audit_non_hmac_response_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    cassandra: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountCassandra, typing.Dict[builtins.str, typing.Any]]]]] = None,
    couchbase: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountCouchbase, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_lease_ttl_seconds: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    elasticsearch: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountElasticsearch, typing.Dict[builtins.str, typing.Any]]]]] = None,
    external_entropy_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hana: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountHana, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    influxdb: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountInfluxdb, typing.Dict[builtins.str, typing.Any]]]]] = None,
    local: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_lease_ttl_seconds: typing.Optional[jsii.Number] = None,
    mongodb: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountMongodb, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mongodbatlas: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountMongodbatlas, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mssql: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountMssql, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mysql: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountMysql, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mysql_aurora: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountMysqlAurora, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mysql_legacy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountMysqlLegacy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mysql_rds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountMysqlRds, typing.Dict[builtins.str, typing.Any]]]]] = None,
    namespace: typing.Optional[builtins.str] = None,
    options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    oracle: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountOracle, typing.Dict[builtins.str, typing.Any]]]]] = None,
    postgresql: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountPostgresql, typing.Dict[builtins.str, typing.Any]]]]] = None,
    redis: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountRedis, typing.Dict[builtins.str, typing.Any]]]]] = None,
    redis_elasticache: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountRedisElasticache, typing.Dict[builtins.str, typing.Any]]]]] = None,
    redshift: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountRedshift, typing.Dict[builtins.str, typing.Any]]]]] = None,
    seal_wrap: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    snowflake: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountSnowflake, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__35437877e9f9e1bfe0a8c81c67337c8265a1ab0a6e6462067a6b376087f463b5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountCassandra, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e04cad43ad1e2016b0b8e72fb21259fa3cc4ac867dfffcd0e8da76924d550b39(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountCouchbase, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae2ffcbe755867ca7aba40c068e2a96c2c0fe9f02a5e266fbea50b8c3f91d767(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountElasticsearch, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd960c87cff028125fc432d38ec1c6c70524323a1f4d9818acc430158ffff876(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountHana, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d960c9fcf95941970bb01cefb0115ea6da4b9e9a1ae565aee5bdde0b7a72db30(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountInfluxdb, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd82b7062e0cfef43cb591382826d6d0e946004467c6644e14fc5d2b30815767(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountMongodb, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bc789f2500e3bde017fa0fa961ec73e8a9f346686c1e55133f28692215dc7fa(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountMongodbatlas, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a77e037b4b32699d4f8f89f91c8f1cb794f0381cdb90c3075dda6186ad078546(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountMssql, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e6d2fb2d8857883722f1368c78e7c7b3e323c1d1c0c9f8421ab30e1a1de5d63(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountMysql, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__806d0361fb5f220bb806976857a5e12d6c255d124755f8038b7e0e56be68a184(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountMysqlAurora, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5df8a73042d21375ba940d4cc69deed09bec7c8546ab93271b61719d7704675(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountMysqlLegacy, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f0489ae0700063ee1dfd357c0f571b779ccb6a8c3c4e6d9fa53d54ee36a37b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountMysqlRds, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fedef04bc561e841934a42b3b8a664a3379f343ba6fa213bab59b7bac26893b9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountOracle, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c07124bc8298bc07cc53ce0d7a167eb5be31b26ee530e055a7b3b0f93856ce7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountPostgresql, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dd109a922cdcb189aff490613d3516f5355a370e1aea01e231dc786750d41d5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountRedis, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8298f39af04e163ece85c640509417705ea1510c8e5577d5c1ff2f2642453f9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountRedisElasticache, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60a159973f513373d3335d5f4300f29562f50d3185c75a2c9e989175ce72a01b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountRedshift, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cda27a3c69ecbdf0e425e853e9bfc3b3bc7bbb772788d1946c83976adcae84e3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountSnowflake, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e261229ad4936afeca04a28a468b6b0b1ff54c6bf57fa1062a6c3b91cfe87ca(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bb289b9d4777709effeeb03308fb7c1b2cb68dbcd6e16abe74524e84708c352(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ead257c41f35a41688108eed3b5fb0d17b9724a026266f8c552063117838ce3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2853819a74919c31d315f1e83f6c2d087a75b5ca020431c6d2495dd6e614a4a8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4991794f327924d1c5ca8e42c5c9d1740e01ba2e9e837d5992e001e97c9fc42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7b7bb250b16bbd9af2fdcbf2ed60d4806d90ce4a1738fdbf5176b5d2905af13(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86995ff3f3a92992024991bb0544ee1912cfec14a8727e552f5f3204299c48e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e5ce497808449c5065cf788d98e3b89257e927dc3ff83826f19f2e448e8a6d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d57fad8b014ac341c538941158880c7567b6b533e40db86872a0c0e35e902ae1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acb029bd2219c6244522bffce6bcef6d695dc12a34bd09b60afd9502e65f8124(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e6c6b4147de2bd4cd413db7eaebcc7e8789983be3a214198e5eacdee095868(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99fdcdd08aecfbb7eb70b558a3be81d9346d21cc6337bd80a0d0576bc80a98fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b745a6bb72ac25b3e608f62e44ed7241168056fa433aaed7c3a0abea67820b64(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bc0e2a228a7d8cabe8ffaeb8d3f171391408a88a2f11fd9d6bfc524f249f8b5(
    *,
    name: builtins.str,
    allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    connect_timeout: typing.Optional[jsii.Number] = None,
    data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    hosts: typing.Optional[typing.Sequence[builtins.str]] = None,
    insecure_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password: typing.Optional[builtins.str] = None,
    pem_bundle: typing.Optional[builtins.str] = None,
    pem_json: typing.Optional[builtins.str] = None,
    plugin_name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol_version: typing.Optional[jsii.Number] = None,
    root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
    tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    username: typing.Optional[builtins.str] = None,
    verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__610357533e7a5ff7d26271410ae37932900dc171385da75b5fe5bce46fbce020(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ee00824f7c2395df86ccfc5f55436cab80014d10c8e97cc89da42d79c802e82(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6631d5423c7baf3edfffa83e0c2a9b127b9762e48d0b903e00a48192f0320f23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a34a2343c762ea22858e4a720cd0395d2a566f446593c6917f77c2d403b96bf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__221362b61450727741ea18c807a2b422081670fe2c2d45e28bd7429ead9f328e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa8cc00add67c5b9c1a6843a24fbb4e53633d2c9c13ea0f791ba1e50a59af4f1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountCassandra]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c43d508a3fd1ed41e0f23d5f1eb4fced939a573ca449d550bc04228e60ad7cf7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e9373ca52d9aa9fa11656f9badb19e89596f128f0e0f6d60fcf9b6a816ff1a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f79ced0a79e2097daf4fce7eb84d2a9bb0d0b632f81ff39f25b5fc45a36a6d96(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c66c617f5d732db9480038d1fdbed647d3bcc10f669bb92d950d52d95b8b43e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb5fde135c1d2db43a4440770380618ba3b2adf253c39a01617140a68ffd58fb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8e340f58d30fe0d361239131695503687067f679cfd36e554f475e1351d06a4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ce9ef962c419bde13b5ad363482d00e638dc930f7eea671ac3e838710117a62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68502b209a4cc2e4b0157641d79acd25ed5a659d0c0694e3405cad356b1d9649(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__773a7eb8510d77a382c2ff53eef08a8d89cea1d1ab0228bb979734e8af5d6ffc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__062caac504306d28494c413d575a9045fadad2d18073bd3144745f83bff46854(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81fa21156d6df39a222a9670648f0b1cb2c3b33f867cbac0da77f99d8fed2b39(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f1d8debf2621b4f32c6f2378fe7b0d70fd299599090fa2ae5e2bd895e8f1c5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed438a3e5ae3d8b2eb51c13202a9be4fa4ff0765da051e3ca71f68935f1066ed(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3ad1cea42b41579fec239f8d43b53304fdfb2da34cd4cbdc24f93df90212358(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce448508530c290e34d02444be2eb9b14fff71839731e1d4b9598117af5dd01c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d8a5a26792fea0845f76807393fcc332d09e8cc0c165c0c92ff2d0b66bc7e3e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b728eb45f0fb428c22078ed0eb01f605cc5d8fe7b2496eec761fb5d086c23a3f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5b43eca688bab6857cf2cb3780de51f6ca375602874e0b547e69f37002452ac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountCassandra]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e0a282c97b99e84c8991454c3106a78d4d2f27824bc5990a8abf3546c7278fe(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    path: builtins.str,
    allowed_managed_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    audit_non_hmac_request_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    audit_non_hmac_response_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    cassandra: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountCassandra, typing.Dict[builtins.str, typing.Any]]]]] = None,
    couchbase: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountCouchbase, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_lease_ttl_seconds: typing.Optional[jsii.Number] = None,
    description: typing.Optional[builtins.str] = None,
    elasticsearch: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountElasticsearch, typing.Dict[builtins.str, typing.Any]]]]] = None,
    external_entropy_access: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    hana: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountHana, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    influxdb: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountInfluxdb, typing.Dict[builtins.str, typing.Any]]]]] = None,
    local: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_lease_ttl_seconds: typing.Optional[jsii.Number] = None,
    mongodb: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountMongodb, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mongodbatlas: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountMongodbatlas, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mssql: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountMssql, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mysql: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountMysql, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mysql_aurora: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountMysqlAurora, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mysql_legacy: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountMysqlLegacy, typing.Dict[builtins.str, typing.Any]]]]] = None,
    mysql_rds: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountMysqlRds, typing.Dict[builtins.str, typing.Any]]]]] = None,
    namespace: typing.Optional[builtins.str] = None,
    options: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    oracle: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountOracle, typing.Dict[builtins.str, typing.Any]]]]] = None,
    postgresql: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountPostgresql, typing.Dict[builtins.str, typing.Any]]]]] = None,
    redis: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountRedis, typing.Dict[builtins.str, typing.Any]]]]] = None,
    redis_elasticache: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountRedisElasticache, typing.Dict[builtins.str, typing.Any]]]]] = None,
    redshift: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountRedshift, typing.Dict[builtins.str, typing.Any]]]]] = None,
    seal_wrap: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    snowflake: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DatabaseSecretsMountSnowflake, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7708e191c336a208936984979fc4607456e4c8612daf9605d0214ea907b637fe(
    *,
    hosts: typing.Sequence[builtins.str],
    name: builtins.str,
    password: builtins.str,
    username: builtins.str,
    allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    base64_pem: typing.Optional[builtins.str] = None,
    bucket_name: typing.Optional[builtins.str] = None,
    data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    insecure_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    plugin_name: typing.Optional[builtins.str] = None,
    root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
    tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    username_template: typing.Optional[builtins.str] = None,
    verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a19cbbf1b22bddb7c4aa781cf1c5b1daa08b0b1c80dca2b790b8c336604a5de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cacddaf7ed09a6806fdbc9fa287f308899b23facf566c9039c6f91b0b3846b88(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a790155b71d2ac0a8010046c81a8c241d5bbbee422885425d378947726e200d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f56bc92b1146cefa8a58f0c1e20e9622de176f839715246f44477d9601a4e15(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aef15ae232865eb9d1d5a8c160c83be7765166377302ecfc148704c6f0f216d0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dadebd2164beb762fd416fdde9e02e74c255f5d00c141599831b80d656a52b0e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountCouchbase]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f9bf9949ec22093a9f50882c3bab20d663c672e8492c518969a3bea39847010(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53b06d2e4dbca8fe453f7381ef29fa14ef7bad44b90aa63670ea5bf6dfc7ba4a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b896808ced9c7480b20a0a0e88ca04bfb3d7ad1f705e5335f70d04f80ec782db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__722c1fe42d047ee9b2f79fbe1e40ec3916a9bf12319c27671106881c02c850d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__630008118cf0b7225a30ed242ab5fa94ef327b78ce8c639ee2cfea51c85aed83(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48e64f2d63eaedaa148968b7fa4c0ed6b738b13bb7633fa3ed3429eced105c2c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__441aee4a588623845e30457828ea8c88f7ca31b0b51aa4c2bafdcb9902b1bc40(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e3c807913732fa8de30bd059b00e6c71e29dfd7b1950b220339af96d08383b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b95e8e5cc091ca3d9cdfec84e27112081394cb75552365d788dee7c2e86daff1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac72efa5e53487a50ae34177b1c8927592b30e4a6d57227b13da129b521139e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2286db43c4b709bd70cff17f61bbd7fd5f8ce30384ac15decc315d62a823aa6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__300cf6e7d6fd28665c4926c1d3b7477c857891936616b4fa58c496cea01614c7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__500de1f7913eb2ecdbb873765905b939d56dd2df1fa9f0f0caabcaeba9fc8ccf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb9148190d7cea1fa81687483bd902518469e5a152ddbb9b4005852a0fa01a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__197f0dc4eca573879ef532002213c0187f985c832c48bf35ad49127a9a22f1ac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecb60add22a7e61ce09d12abfe039b41ee3e3bf26674d9a618f8017f123a76ec(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountCouchbase]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22399b1622dddcd6ba7f17d48590f4190246b50f1ef021a0987f0cc5fcb50063(
    *,
    name: builtins.str,
    password: builtins.str,
    url: builtins.str,
    username: builtins.str,
    allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ca_cert: typing.Optional[builtins.str] = None,
    ca_path: typing.Optional[builtins.str] = None,
    client_cert: typing.Optional[builtins.str] = None,
    client_key: typing.Optional[builtins.str] = None,
    data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    plugin_name: typing.Optional[builtins.str] = None,
    root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
    tls_server_name: typing.Optional[builtins.str] = None,
    username_template: typing.Optional[builtins.str] = None,
    verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61e46ce583c358fe2f35a51e2fb9f1aa3ae491d37adb7bdf83cb287e397a6c08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e1fc9d64a4c8d24ed4d9d21050576fb46bd71604f69a16ab7f5a7e0b5195e3d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af04d92bc531014408e942c08af4e940103cc09504d5adddd0aefee48f0b65ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__484bd3ef5dcab8292cdd66c36e5144b61f335adc218c4af16478c39117619f79(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a09b63924f2618245cbd9fa0252e549d299b5ad208d39981c969027e61d3177(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad64738c3cc62dbaf18687ed752a1de64d08db49274af8ffe653bb07907f00ee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountElasticsearch]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c73bd7319d3fc38762515025dfee63a7d21bbc496056b162036f0771c3e24b96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e29a91425b2de754f635c1bfaa5a8496d8a211de67c5600b28cfb35d0097821(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a4576566527c701a8527bbec2a4815328dc6f6acfe66fc0564e0683c4a19f40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19b8f0cbc84d1b2bf814d3d5eecaef9bc060f487ab444e01a001d062a87b82f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7d6b1fc879b1409e5294df989048840db69ad7e26664d621974a2b6d4fe73a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be0a0eae0658d518d029de43916f7a79efe33f9056856609d78039922605b508(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed613105d65edc3495fcf73eb0ecc2c6feabb2710f0af0713c30c0a2a72ba15a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8486907f19823cc3068932c001acd514741835a8c63925dcecae59ba8d0d26a6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e2b25b2ea054c28bad926f5ed8bc3fb265c9b15080f157c988bd883461e4f29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfad744e7e4305970b0296cbebd8daf1ba2c7dd6d13721c4b486133d00d16f9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ad8b19f4de30475a86f58d2c9a9a4f38e13a659c916f6ed329220a36b7a78f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da0cfa86f3cb063ef75af726daf6d939538bdad7f40e0f406add96620d67e2ce(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74d1579c7227ad84f54320e5e0220891a232e6715b6597bfa943b040debfc64c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb04e18ede7891f184f3b81d3185549de3eed152c65d2780e50606ea691b2bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc6cf5c9d6db453395c026c8fd211b5fada8b791d16d5629cd3004f5cd456dfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d041036382f78a9d21b238854c4f69e335c07b97b51300fa3a230aee4d3de8f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015a21c1a208d61ae1324208e008b49d84ace9b514e014c3982f6fff3b2d9a03(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0ec083b6696c87109f43044750bfcff2776c0055485df4f010354ab415afe32(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountElasticsearch]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c72cd3caee2e9fbce76bb3aac1a434c9b1cf8b7c5657aad746c708df1a0d6fcc(
    *,
    name: builtins.str,
    allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    connection_url: typing.Optional[builtins.str] = None,
    data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    disable_escaping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_connection_lifetime: typing.Optional[jsii.Number] = None,
    max_idle_connections: typing.Optional[jsii.Number] = None,
    max_open_connections: typing.Optional[jsii.Number] = None,
    password: typing.Optional[builtins.str] = None,
    plugin_name: typing.Optional[builtins.str] = None,
    root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
    username: typing.Optional[builtins.str] = None,
    verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5250139ada5cba7b47662b5558b54bdefe8ba792fa2c5672e02acc0d99aaae21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba7a72d1b9221ae38317fc74a886842d2271f7a31d59b94be5abace55e0f5e85(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd907eb1003d850ff183cd50aab480bb9e951d6e1730822b272aad38d3a4d35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de55da1bc944963c772de4dac94d93654de3caf047c5c8f0890ef7017203ac94(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3ca28475641ad1050be442e62037c4f6f269bb07291ce72cf0714b89c6794f8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05ce00d9d06c6f11419432d4d3d2af5c173b679a313c7c2a159cd0588255c544(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountHana]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e028b9d6364c47aada681b536f08d9c8932b69ae2c6ecddb331fd369078e78(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1501d09daacd9fb65c6a591a2833b1b4755f1fb6dd94fcc7559a007fbdb5bb52(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ae6d90e54c9c160ab6fde304a573d69b570ce7dff2de5207ee6cc46cd1ecbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f85cac995e7e78ee6855c16212166e5f0ccf7c2e6966a733774814801e61b95a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59b8a57f7e6219bb96c61976febe0e370103198a84552f038da29f1e076cd446(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7f242fdc900e0f7407000df88ae0e32fb3321ac4ed4475195d441db243a765f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9454bda6689929a5ff2676fda90327896cf511e53dd97b855bec8cc6aed8d87(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b5ba109e872894f136bb76a1ca1bdc1b766ed233928f47aff8b4e21caf0c3ad(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__359688317530993184c77a332ab3422207b16562553b59ad0a6373375ff59a32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7c6339ad693e531e37dea3555caea2e4e500d8d509a549e7099a5afb5b3ac40(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55d81f4799c1110e15031cb6fe5509f0887470810ea5fbec91ae369bbec53857(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31e2c495e04b0b3dd66a9582557d61c5f9f429ada847236b0644a529a8523bfe(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44adfe3a18bd1cb1259a20014f94c5291350157beb5e05c8e9ac2fd9cdc8be0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d76b2d2f19b41134f7d98b62fb002d5837440648dd87b771a48dda69dfed66(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e10094e3626a24cdd99289dff5ca6f66ebc71fc41240fce91a19038f44c0017(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountHana]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4f88548bcfd4868bd71841e883d92ebcbe2f06dbf858b520b78aba07d2056f6(
    *,
    host: builtins.str,
    name: builtins.str,
    password: builtins.str,
    username: builtins.str,
    allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    connect_timeout: typing.Optional[jsii.Number] = None,
    data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    insecure_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    pem_bundle: typing.Optional[builtins.str] = None,
    pem_json: typing.Optional[builtins.str] = None,
    plugin_name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
    tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    username_template: typing.Optional[builtins.str] = None,
    verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cda7844152c8ceea020f7ac29642e552206209b55ada2ab11ba01bec460c8873(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2c72d8edc3563e7629c22c13b61286463bfc988c1fa742b1eb5e2b40a3cca63(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f85ccd7d2a554da4ee834dda473544c15c0f7b930df7b1edaacf72daaa1bc4d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a056cf4077c41155c64e241ab38c7a5a999ec832b529d77817354424cc27574(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75ce1d3cc040484b297057db1232de8fb807ac95e6edc8921051689ccffc5eb9(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6a1472cdab98d605f68e6f5a6c6893a7772acb10dea878f3c3859ae897161ea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountInfluxdb]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3010dc29103fa31f1320e0f554cdc6aa4056aa9e29a76319b72d282f8ffa71e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc44dbe3c4d70769a5011fe595a7ca9fbabf04daccd7dbea87f2f450020dad01(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3a6bfeca7b5f45745b37eeb2b01eded4994debeacb4f326583c9d843c51d1f4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06202c703872010b6105e34155f654d254fbfcf0d34588920fe63cfc5a454701(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4103bf271f58247a504745e89df13bd02dad050e2d83dc5102503ae95f11dab8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__371c360ef31460c05a5fa75ae168d0ec7bfae489af4f17f6f1e5e5769cbbbf63(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2d765c44be04437a00a2b2ffddb43c37954b9e8c173d5f3530c4c88b3e8f793(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e855c2aa625bf4c47eb0b8594afd478c78e86e42d8464ff9ee1c808239734ed5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23b135aada3f4184de209d584dcb2b5fec37d01cba7ce6cbba855b10d1080704(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e93a359314025b13ebef60306de979b3edc6c81e40d01ac320d6c4c210fe8892(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a005f70edb8d1d7f4b78e746c135470df13cba976e9bc0d4b13168abfd4aab57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30d16343326889797547a0c0939ddb73725abce2790a195af8d22a73e3e63d2d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__265d6c5edf4291bf5bb8d206d231cd668ee008a489d250dce48e6619cc5508bc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ac7615dd7668bd4ab4e7e5fc75fa0ab3317754b68cea04dbd58717e0172db6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57d17664221609e709a2ac3f3f78c874075fb368ed90d295d077b67e92bfd861(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7de9cd771b44565734291cc1b585eb1da870a99df8c3536171702b28ecbe659(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0e95a2e5651ec13a129406ee70a4f9fd7a7b0fac70b072e99b3d38a0680a901(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99dca926d47321264a1873516dba08f40e6afc3c30816662d4d25db56c07014d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountInfluxdb]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5db3012e3b3241136c31ae686f9fe595043302c4d8fc2a53356c701037b58e23(
    *,
    name: builtins.str,
    allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    connection_url: typing.Optional[builtins.str] = None,
    data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    max_connection_lifetime: typing.Optional[jsii.Number] = None,
    max_idle_connections: typing.Optional[jsii.Number] = None,
    max_open_connections: typing.Optional[jsii.Number] = None,
    password: typing.Optional[builtins.str] = None,
    plugin_name: typing.Optional[builtins.str] = None,
    root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
    username: typing.Optional[builtins.str] = None,
    username_template: typing.Optional[builtins.str] = None,
    verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d2c4f5417e2c573f8b6f92b413918a40dc6d9acf495da532719a6547697a128(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a0cc96c3d0fbae9529c633b9eed8aed0dbfd91b04f4e44c312f6713f6ae52af(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__658c9cc2b09da9eac458d0ab0601f12b9044f02b450c3bc1add74468a4e2a979(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f926281eb1201bbd308a1266e96191ca21f7a6d4e424b0de33e15280e5309c5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a80a53de2216c5f70763ee3e8150ac4cbf739b9e23e3ac79ebfc3160da2d454(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8d08eb74c452f1ec730e1c3e54af41db1cf584512f3e56c0565e83eef4732a7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMongodb]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4087c891a593f6fd93f4e6ce268cb7e7fc5143d485ecef105e5a00d99f98ab7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eca2329fbc7b2399195b34b941cdbd816983e5d8aa8e23ff681ff14a6e01d7a2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e55e63ee4c556db9a12a4e465d3a3bb87e3171db2f3b1ba7ef9c05e4cfa43d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa75de15fcd55525c91c35cbf0c2e030955776d1c143b2cf0be9aad96082fce0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db816af2ef8852dae976791b83c8c2f0af935095331b67acb18dffa66ec80624(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5100203e906f37688b45ff8a532f46db2db0413127483d46b9fdbe4e323f535(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ad1c9a8b8f2358da061b81174bd51ac2aac8837cd8d64482c122737d4697a3d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10eabfc67564e83a3bf4e303b9ac11efb4cc9493b0e8773e937922259eeb1c6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff1dbce09e080db787f89da89418ddb4fa083b31c36e670703fb833192d5fc8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56e68eeedb14f070e67555b4cb083a40e81123fb5f7842ce457619b1763d1a9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9def142611fab8c1f0c99217006f1382739a4fcb26bea621396672ae0e19b15c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49afa36a8348d92dcd9d9a7a1025b44b758430f4dd159529736bc5e256cea2b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ace1d294410d599ba613939d0aed9d75d9cfcd4fd11a5c4431c1d18e384b193(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5900c3784c53b1586a93beba32cc37932fa921bc3b8cb5889adb3a5c51d919d2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58add0e2fe41e867cbe163d79d57574d6b070f31f54fe360f8c2c5a5e871d52(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMongodb]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aab914808d24e2d155521935ec3a9d4e9fb73097e6b32682d50b5233765529b(
    *,
    name: builtins.str,
    private_key: builtins.str,
    project_id: builtins.str,
    public_key: builtins.str,
    allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    plugin_name: typing.Optional[builtins.str] = None,
    root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
    verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb78b0cc86baa87e7244056c2aa3d0e6f3b9659268964a046c76bdb5478e444(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cc0d602855f2d4d5c28ef870dbef3bd0c91d210ec8853d68e1be606061914e1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a749ac288c80241be0bb7036253b9a4a88447d69a8a701c424708fe46c79047(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f82cce7b84e95252c7d0011c1db53170d9cca075f6f55d4d19e294c2dd2cac7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10fa58e24ea4fb11451a3817a6c7c2b4a56a23393e969fca43eb74abd59d0cfa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc06a2d411d825cfa99896e26e5cbe0193f5ebf276351c26a41cd3e47dd1f829(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMongodbatlas]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf3ce5f4cc44c3bd987e9217492a49785244c83ed8327e9eb218179e73c85057(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c1218d34e82044da65e3c53796b35b6e83403d35f74d915d9bef0ecf9cbac5a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd992fd2949590ebfa8874145925f82d025eb89076fb936950a2f9ac0d38a3d8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac99ad508721783cc46f1e243cde238bb5a47141e4e3bfaf4978f11f14e256a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__170162b8736b4c52fd6adc1bf68bfeb059d22410e53eb23c8fd14a69db51d02b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73fcf89c66494d4f57edec8bf557502540edfa8a084a86c1f1a6858dfb7d7755(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71076eeba7b335415dd92e5c849dfabede1dc1620be61863ed33cfd57bb42e20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__743b3cf7fdb96905a1ae4701de2ea6fcbb50fd359ca330464fe320f8931fbb0a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4f613029ccdb15e24d484c5bac7c62a87476ccf87bbb69ee5a3e968f881e52(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a33073120ad06bddb619c2632dc56f128aa5d25d9354f234f41819480deffb0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27482a00ba84e5723953f91ac8ca49d835a611966d17559475f158610f82fa32(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMongodbatlas]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca5ad366088df2425fdb1170cc75e211976f349ac8aa8e94d02534c5431db83(
    *,
    name: builtins.str,
    allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    connection_url: typing.Optional[builtins.str] = None,
    contained_db: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    disable_escaping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_connection_lifetime: typing.Optional[jsii.Number] = None,
    max_idle_connections: typing.Optional[jsii.Number] = None,
    max_open_connections: typing.Optional[jsii.Number] = None,
    password: typing.Optional[builtins.str] = None,
    plugin_name: typing.Optional[builtins.str] = None,
    root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
    username: typing.Optional[builtins.str] = None,
    username_template: typing.Optional[builtins.str] = None,
    verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c042a60690181ac2884ad2ea0c8f87a72a65c853b8b776cd9886e814139b96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36428bedcd51ba172bd3da4410f826b8abd21ee2997e9d3717490ba3f786e4b1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54803089faa75286837b341f3f35c4c0c4139cd523e520365bd1ac3b9695e749(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1ce51a600b1c9bfde83f67fa384a7d0be8fc45d09c5dd4924d3da2c7e4dc0b8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d3e977de8455e97fd35b55f8aef19f28c5b06556316480da0bc17a549449093(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39a449b226f353cb57d1e159925b0464c7e56285ae0a2526eb824fc419c43c9b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMssql]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a72e183dfa88e6c8c6813de5657bf8181ca00b4e44ca979ddf241c13a55ff2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab98eb662a365876ee2e5081b66cdc20c15a9ff876512e9b70c76bf91b5423b8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77beada7d25145f6e7da8f2b819ee54e3fbe15ca3519f1adc6743da06d06e1c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9996fcfe749f66f76831bc410999f25e7e27521a77e7684e45228c18ce3b371f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba2107a22b94aee2ad1c669fea30c92982b7a26ffd10d6beb678e9f31f00706e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5394bd93d6987233f19b7cd14db12d8f2275cb7296ce4a77582a3f55a6aa305c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__572aa7756894477c27e977845ddc7ef28a769caacc426ddc3abb48d9df1d8ff3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7da06741afc2a5884f807c59a259276aa67c347fead60f6e44ab262a178af6a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4da910eabf66178a984765e226ae888ee443205458014d569037787eb0c1b44(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e4232727cebc4c47b7d359ad26d830ac14673d3f4ffcae8d22f1b1898d45e51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5de6d4e7453c02ab5503b22360ce6ac79bc861726ae419d2bff510d2789b6284(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb081b4e69623f0e24db306e78b800dbdca1c739cecb5cba2f2b54b61a1d896f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8383ca612d368521c10b87622f12222781009457c29cbb22adf88fde259ab98(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35169712a65a8bbd8987ed6577363e0c8b02d739a9c3831327b6baf7ad48d2e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__879d06faab058cb97c2215b84e5d31f022af3be1d49a9c7f9d38a58a50bdba6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19a0d11d8ca37d146716bb9ae288db93773d9fb3a6469a9e7ea74a45b66fba15(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aba4eef3f2e22ae2a004f2a9a11acf22370022fd32297b6b49c4bf51101fe57e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMssql]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__602c3f62440dd774c77c2feb86ae3dbecb381eec133e321afb73f8c2c1b6ea6a(
    *,
    name: builtins.str,
    allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    connection_url: typing.Optional[builtins.str] = None,
    data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    max_connection_lifetime: typing.Optional[jsii.Number] = None,
    max_idle_connections: typing.Optional[jsii.Number] = None,
    max_open_connections: typing.Optional[jsii.Number] = None,
    password: typing.Optional[builtins.str] = None,
    plugin_name: typing.Optional[builtins.str] = None,
    root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
    tls_ca: typing.Optional[builtins.str] = None,
    tls_certificate_key: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
    username_template: typing.Optional[builtins.str] = None,
    verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82c06db88c427c5286f5e891a1d58d37870d0195a8fc8002b7515ee88cfb418f(
    *,
    name: builtins.str,
    allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    connection_url: typing.Optional[builtins.str] = None,
    data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    max_connection_lifetime: typing.Optional[jsii.Number] = None,
    max_idle_connections: typing.Optional[jsii.Number] = None,
    max_open_connections: typing.Optional[jsii.Number] = None,
    password: typing.Optional[builtins.str] = None,
    plugin_name: typing.Optional[builtins.str] = None,
    root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
    username: typing.Optional[builtins.str] = None,
    username_template: typing.Optional[builtins.str] = None,
    verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89638ad8a971f4fd92492b3c5d4178227b2c320b0f38f1f5601290847639b19d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__133188ce48fd5c9a7f67de9972e00fd2d71a56cde2dd0f523f5cfb2358bac35b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__178ebde17cd3dfe51cd4b00db90eb7395e594fa73d0f38962db31c24012c4f01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c37996e034a94d3a9fa341d99d4922e596a879e7bfce8440be1419d100624f9b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db3d4d9e30713fe06cff2f37c4b2c73b0c7d071d86b9b2ed7caa5e51b2b6392e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6386b64a8183f9bc8c0573d8ab47ddec5254c159a91615128ac075dc789a8265(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMysqlAurora]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e0811f1742c3e4d1bff7f8852a8dcb8b40e2608493b2f1aef54457a1f57d03(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a03cae021c9230f4647ee46f373ef5dde1b33c8c9c7cdb3b7a0ce4b2437a3443(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f7c5ecae8821b06c7051d1bd3924f42bc7789258dfb0759ae378bf466efb908(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5afa207e77cd4e373f4a3fa03a360133f693162cd0d043ad4c69c95bab6380e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02abded6b82a894d5835c74736c19c3c291001175c96e333332e265c2db0e96d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d38d4b242aeee44af7f3cd8663b455320206dfb29fa0ed4f8e7ad8a59df63325(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ec6b2d54303d4998d603411267e2638c755f73421c1307ae697d95f9bec755(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a7fd67f528b64aa41b0de469393e696b562acffed49462d01f2668be4ad1749(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5eb219cb703aa8a2ae83a99f7097099a272ecc9acdffad1a2b37e11c9f22baa2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d2a7d93cd9180a48f576e03e707c79f627746ba6cefb4cd0e0f0968f4fe5569(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e05ad578ac9d3992ed519bbf565fccc89ae244da7b53c1dae429b6a01d6a972(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86397e06f52f83013e640b6467e4a36a05ceadd2ecf98303c52141ae11cd1d06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b65515683946ce13120d23208dffa0c54c4a083c2c52c8b7ad70f49f4f21ff2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__996ee4532ffcbbfa4e682ab32843feac0dfc44d5c34a1fcf7e907bb07443ad41(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bd2660e4ee10ae879679703bf982cf5ef670db80ecf53d7b103108306dd0f4a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMysqlAurora]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4e8faa9285539891551e8d833691913780353032beac2c982898e5a8791ef54(
    *,
    name: builtins.str,
    allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    connection_url: typing.Optional[builtins.str] = None,
    data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    max_connection_lifetime: typing.Optional[jsii.Number] = None,
    max_idle_connections: typing.Optional[jsii.Number] = None,
    max_open_connections: typing.Optional[jsii.Number] = None,
    password: typing.Optional[builtins.str] = None,
    plugin_name: typing.Optional[builtins.str] = None,
    root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
    username: typing.Optional[builtins.str] = None,
    username_template: typing.Optional[builtins.str] = None,
    verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2dfa14560f4c0d7d4e886f5acb39d5cc9b2be197bf6054e532414ad20242c4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69251deeefba5c4def210df82efcf8c93eb42f96c39418e33c365ba6abc53e64(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efddb0e7472a863d01ee46a090491dd41ae3933162ac2087ee16db9d707741ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5a88e237a3deaa82a25de5d568146e1b634e0d18bf0da57efd1176a15afab57(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3112fc01ef6c1cdea0ddd23998101b06409b5774956f82b9d2d9a67c54d2847(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76ece26ae3243424419f227b9ce117ae62cac538fc039e6ed68ff9abe677c2e8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMysqlLegacy]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4115494fca69ad24f4e9738296bf2ba8c4c337eef036acbc46cabc824d5722e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a83bfacc9591d36f95cba51b53ef2216a4bbd70d894f48a95854a9cd037b291f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74b8affac7ede2b593f116540b65feab0d0922129f05f3ac051e763837b6084a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fffaf186cf1e49a6b7f3d6704ea4b7a921d617a50ec6ec9994d0598ae880abea(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7627827954f817d87c7d49f892ec6dac857fa4837dc856f4127a0043d55c92e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9482a0d673bb69ab3df2196de40f5832fcb86e97a200c7937ea79c7a386427b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23244d56b3059dd1097ecf95a79fde41f9769dc385d35b31a2415e060a763bbf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22cbd4e72dbf026b8997081c73f69a13a0b157d19ebcb1b5aa0e7b0c5bf4954b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa873e2b97762436a1b28d599e717961eaeadee47c37fa62d1cf3450e235073(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__764c994158011342a5dda1c0d7fe31c475c9da8d52957804724768f253a38823(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f2aa5ee6c3afd0e5213389678cffd219e694601d008fbec5322cfc76b2faa51(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__836ea320cbcce7ea9e3e77f883aeef8421b8cb4b0a94f490f16e4936b357ba2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e0824973da860f6e782b3efb04299ced0f5714b4cdb24bfb73c6d4d7f44abc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3536a2ec3af03ed5827b4a7ada25a57dbebd7516912233eb3943958301b23003(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a2f9b0e146f8966bbcdb8fe870694df3240fc0eb78d3d9d83deb77b5a69f7cb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMysqlLegacy]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a4a03998a3c3adbf4b8d36dcb5e60515b55bdaf3973fab63d0a478f667bc29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8e8a210355b019ad0c848fcb001d12d9a6a0c9d9bb7f5e792ba64edbe94fb54(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f92f3965c79edd40b38fb4a6ea33dcb7c0c483b1cf45e1c2bd8690396876d355(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27a2e9b04749d7a2c42405094ab41f1fa4684929e6f20480dc468a4f4a4d4bdd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be5b02f91b8e776620408d73c948b6d7700036afffb6776e7577a112534ef688(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f43fb86633a27d0ff180019b25a449581da2cfb0be38f269fba87f5580b0b74(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMysql]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77ff54283c045cb34de85d67345d1ce86e75761fe06492d775ba8939339189a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3383b68475f903cf1e24df80a5d74c579c111d3c42dd7d5622dc6b5277da95e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb5a5b7bfca09cab0c9f8904ee9b2b00d70e1509e79aa6d2fa4f0f29d1b6003d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da1d483f2d9af12e3cd9577420180f972baba82571cadf42ade2a5b232d43eb6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d20e14e98ab9b40ad4275334794d73ecde3bba7a5c973cff36ed508667d7abe1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cc3bd578c3be6b6a3600bd0275e70c26b19a32c6f0140c84b928d16e85b9a22(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8140154a134efa2d1ca1d10b73a5173cc83182b73a832acf72e879d95f25776f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab524a502f95c5c18b4482aad5c39d6e0abd0c0f87392cdd3d95be3b46daff50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c18ecfdb9ba4fde2a5975b1d6f2d1ec704072eef6507b11177fdf03a8e93130(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__116b08800223ebb013bf3983adb4988b8cadc59c7a6f491a6b128c07f1d797d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec62e721bd2a00dec8394409fb603e0936886c57167a3ee9f1ff4ca3183f8f9f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__620b0a0aa85bd6ef9c4410d1f3474f9ef2127667847c3fe32c9b90e933ba92d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__051fbede64d14c82fa674d7a19d5f7af7e1009d2ac097f973bbb83be8e6d2c51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07855d8342ff781d0f8ece6b1d71edd2edf17f65b284ba4adda17d3ee3766d97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acc076f9f672da5dc53c78e1fdd4451bc335ebb694077e946ef14ad5b77c7d84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6b0a60a6d22a1010902b8660f90a75871f015fc15ed0690077cf820f81871c6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f08dc3bb92b36b998c24e3d44ab3c127b86d48a44f730f935eca49ce99a7cc2f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMysql]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94e56133dea2b462dff7a58564d06e8463f1098fda031de337b569d321f06751(
    *,
    name: builtins.str,
    allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    connection_url: typing.Optional[builtins.str] = None,
    data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    max_connection_lifetime: typing.Optional[jsii.Number] = None,
    max_idle_connections: typing.Optional[jsii.Number] = None,
    max_open_connections: typing.Optional[jsii.Number] = None,
    password: typing.Optional[builtins.str] = None,
    plugin_name: typing.Optional[builtins.str] = None,
    root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
    username: typing.Optional[builtins.str] = None,
    username_template: typing.Optional[builtins.str] = None,
    verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__460534ce8afae1dba0f75d6c4d8628d8f0310d4a07921d55d7e21a930f85e365(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__856cc45ef3c17291b9fef98129d23364b9ab7ed30cb67a10193656e3892d4be3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39df93693f4654b19951d8536c93dc41ee4858f70a9f249384c4f1bff38b42bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9da60f88beaafbeff040b687e0cf105a5d28e28653ecc41f070b9dcdeb0ccb30(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0520d7f1be5bc104be4ba14eb8da5b70f8bb6b8cf8fc2ef06ee9d83fffa8d54(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5923081e363f91271925125b968b59cc0e2e9741c71989c070f7b5f215dd47(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountMysqlRds]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e63362f0ef5fbda6eafcc8f2a68646e5da957329e9d32070c6f6cafe13948da8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dab9a76f20fd6a32ad71841b5f6ba408b1c5d9f75cbc13508cae98065950fce2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9d8270da4212b450f813e77dbcd736892fb8a98aeb7ff8aaa5486a4381bcbef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a9cd0212967e64d951c0f713f2fdebd90cf6e73244a8f4f1de44d9452d74c4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c494319e3b4f8138f36c53e7a9a4ab2f287cb77f345aab4e80664698c26bd2ca(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c30ebb165d3dd28faabf036abfa8b7e69f8fd449a534fdc7f63f8fbb5cfc6f38(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aa151bb31ecce05cc4f52802273280c53401c7a60642e7d726c5e2bd748342c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d68a02ca92be3e38ec514b8e26f4876794acccd1d228ae1353ae278856548165(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ee738c1bf4d2f8ee241b3f1f6a4b3d95466b335ca0851985faa70b53df35117(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0917c5d0a7fe0b8328dce7ebed4c8b64c2ec7450e4cf579a82a4ac19b2b8d61d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8978091f9f81d68ffa24c5b8d5359b63131a1d3c7e1f3f209c4e2bff2f5ea3ab(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adaecaaef22ed67c281f17b54fa5089e093f437179f7883c53e6d71dd5da748f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__519a1a7bcfde4afed0b1538b0685b783cd9234b43294138b2597603644089580(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cf08774f890ba69a4ad3bf5776f7dc755561f6e49002afc56e819d08b44b49b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96ca2cabe2a637c3852a25173086717903dc8f2330b830dedbb02f5bc68924cb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountMysqlRds]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65491de5558996136bec008c06366a08b38751687c4fb1303c5c54059711eb9c(
    *,
    name: builtins.str,
    allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    connection_url: typing.Optional[builtins.str] = None,
    data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    max_connection_lifetime: typing.Optional[jsii.Number] = None,
    max_idle_connections: typing.Optional[jsii.Number] = None,
    max_open_connections: typing.Optional[jsii.Number] = None,
    password: typing.Optional[builtins.str] = None,
    plugin_name: typing.Optional[builtins.str] = None,
    root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
    username: typing.Optional[builtins.str] = None,
    username_template: typing.Optional[builtins.str] = None,
    verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aab452671df63799ef1f4c8cb024d1d8e82c4e258b856489782bc5b9eaf52282(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c184402a3d09264ab4bd1c1d95630b385fc347a79d444c392522669d7824d312(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a8f447fe214fff11f16ef64fdfadae51cdae899395965ee75876bb570bf8d1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6513457ac3877effc01a64bbd7fae5d279eda6b7aba688e6a277c3bc3b2c2105(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10ae89194eb74c82517aeecc5275312d854372e1bf02996b2d529188e3024664(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9a65f0acfcfa7932c5a5dc9ae49c755b897052f6476cb507785d4539b7b8ae8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountOracle]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7dc035229bfcb02f513a1c002fca846f8ac711ed70f19c466d519b10424b969(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f39ac996373996d57095071ac6b97a8d8e04b6a8b0653db6cf77e0bae14978d3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e317f84131a0d91e271aaea8d46a6a97fc8ae83e20c53fd361afa090075cff5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc5166d99994d42c2c6e25c5ee5215e090db2e97f1fef0c5e989c80f272a7d8c(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d24c589c31b29959f0e516d9982b753a96ce7486d0891dbaad058f2918072ebf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45c1196fb54ff2d6e1a810079901a1dacbe3c266557c38c3706897e1483109fc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3de7c373c5bf1087efead7eb4a9404ef6cf9662ec2736693e1c186cc25daa94f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c64858f3fed32707a126cf78b4dfad7a47922229704fcba8661aed5760a4bbac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c18d6b34468b0c7d4017b0d94746f9096c2e9bd6f481e991751cb1ebb81f17(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f6ae0eca1f49e9a8fdb3369e99d8a1b82965b190766f453c549b71757a0aca5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b75145ce45d0a15331f591f47332910176997e9d250d7e08dd501fa8e10b2cdb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31b54f8fc2ad2d07f769f5c709846679735fed77937c46c676ef3da1dce1110f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f4dfd2564e2f26ef70b84b9cae789f14059680a39ad8e60393fd51bae9b18a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfb28b170c38be09e4d7ba752dea522c24c5656030fd0d51a6d35f547b071f8a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c2e100ce197c33684c1ff9fcdbe0e971004480a533af822f3e3c50a8984dcfa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountOracle]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1313db13b346cc66400dedb70fa9ace00b847fdcaea9d7e18d073b7b071db0d2(
    *,
    name: builtins.str,
    allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    connection_url: typing.Optional[builtins.str] = None,
    data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    disable_escaping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_connection_lifetime: typing.Optional[jsii.Number] = None,
    max_idle_connections: typing.Optional[jsii.Number] = None,
    max_open_connections: typing.Optional[jsii.Number] = None,
    password: typing.Optional[builtins.str] = None,
    plugin_name: typing.Optional[builtins.str] = None,
    root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
    username: typing.Optional[builtins.str] = None,
    username_template: typing.Optional[builtins.str] = None,
    verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28cda09f1a5b0363c5816cb8e7cffe15e5fc17db6b526a526d20778e2ca40e55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__433b329437e71d41787244ac538e35ebc90f5ff29e9eb4bfe9effc79c218513d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4d1061a847076d56edb56012f81db7e7a68eed5b658f74362af2d3276092191(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcffb7a206bea0932798d0450553f8dc6cbcf1240a3f4575d365a3f7b90c15eb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03ae6ea713454ab8d8b9ccd5c57051782ecd52142b2393da60fa2a52471b8de6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0977e4a3870df929df48947dc844a7de1859c788073cd0ea99d1a25cfa066a8c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountPostgresql]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__987e3411fa0d5652b5e39d7cc7337a2a5903871fc0776056350d7b54c834e7be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4937bfa39de1b6e144abbe7ec8ad542f37ef6f44ae83d4e3c3e7cbd25d68fc15(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d66de9892ef2a8d785fe18484b4bcec564244bdae1955b5fb534c6fa8768f247(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa6913493865f7da2c3e949a2bb893b34dca9b45dda343d3b02eeb353f6ff44b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caea0b3bffc4d641a4bbc399f7ca4746cac387582f88e86fd5412e79c22c495b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90d0cabe019a4b3caf12480f643e4a87be30957ea44ebb70f67bdcf9f30d6f38(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f856629d3817cb465c94acde465df8a122c4e06a5612cf450d02c346f41073d7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c73903e34881e5c0487198b1b47dd591ffb01b058238ad0a762f5df94b0f16e8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7a621dd1c03f8f533010db5c0e1ceec39815e495c84f04a0e35efc6b9aeeb4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8c0a6eff7b6889ae0a32d0dd4aaef9460a124c376c4ed22e7b150d23f50a0e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64781763e1f253fae768be269a44b2233704864f57ce51270da7d10a9fc02d7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0992b7fdb5a53c82d8b08f4424c18ec1d224a586c4775c944b857ed89a405d4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c33bc4b6d28e17773ad37467035fb4bbd76245749ff4728b1effd774bb6a496(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7247b0668c35e1362a25756d5782c828a01fc617e16e8728ca1a89a31e1db3d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b61d479d7ad0cf227da5cea3f1dab01b2455f510467d740512822642ffac8a5e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec33e8a00860fb323c1a979e335975a388008832ca9aefbc89627fcbb62552b1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountPostgresql]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd74ef1d018c28c33d6bb68363675273db4bf2da3296873908e3d8e1525bb490(
    *,
    host: builtins.str,
    name: builtins.str,
    password: builtins.str,
    username: builtins.str,
    allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ca_cert: typing.Optional[builtins.str] = None,
    data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    insecure_tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    plugin_name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
    tls: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81a5ccd1bcd0c89a82fbb3ee877551440220d55536cf39b944ea8ffb010c613f(
    *,
    name: builtins.str,
    url: builtins.str,
    allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    password: typing.Optional[builtins.str] = None,
    plugin_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
    username: typing.Optional[builtins.str] = None,
    verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__921938093bd0779396a82fd95df04f004ee52eca333af63b082e42c96e7f4484(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d224e78a50303205fb0e30957a50a9744eb28fdcab4ff76cb4f0b39c799196cc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40530eb93a5eb2f934774bb9b296bb029b438605e3167de726471f2150b90593(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2331c7cba8f488ca86a1e0220ae5360227be063e8531e6360f0f6127912b7c5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6798afc1e44e012959054a1507176c4995c86a30edecd3144b2c42b0d1cca9d6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9205d31520857c1a57803269245118f71e4d95565438d8e353657d6e8d74c35d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountRedisElasticache]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b1f56bf0fbc286f1ceae8a3a5b3394aa7b4e0fdc9858596219b2e60484b90d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4972651314622eec55c83e17298e7a292d3df05db70a211653831530bf37bb3b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff81d92f33f44d0401873a77635454dc4a32d2d163453499d4a55fe0272aa2ad(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c203e132fef874aa539e47b36ff5c311030110bb326f036ff9185cce1caf3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9251fc6261a5048feec4ca554c1dbe8767e479526309a436b026a7bcd5447b1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ce60e46501da7f71bb537402b6d28539917757f1f17e3e4cee988f9dd44110(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50b691b4882d428e33d4a3fdc7261c002e29152f11fbd0ef6669cae888b56d50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab2b3a13cc8e8193a4280ca53e066b489aea5b36dd7d72d7d426ab22bba1923d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__818b31e7b6b0ca7e86ddcc8a75a910af0a8721a9926fba0e36657f529342424b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7425224cf4f63a501c313c500038c5e501591ec2219bcf81fdd571659b1663c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c79f6d65e41787a95e58461d1e5c43269fa8dd3f2b26dac06725302821b38b90(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__431f1d8e710f641a7d2e5b2b330e92f6d9a999c34f0f48798fea0f643268592f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountRedisElasticache]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8038393689bece62b282204023d36bcd0cea5f4463cac800d0eea9e8dcb29e47(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c41753c9524f3adccecba1846e0365d02101a186f5b47069ac357825f43abfe1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbf2092d13dd3a793a5fd71d268d30a796ae529096c2a39c837f5719134b8929(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79e25f4b0c1ebf352570b10cfc6e7c94d17fb7f7de62542eb1ca23691deb0ac5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__170221ea270f4208ef11d51946b1751476f4e628984f07dde80726466e5eba6c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93dbccf06c353d37e6b2fac6549b5160fc91f43aa2777ac392d4c143135251cb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountRedis]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec15fc1eae349b7b84ceb2f59851aa1dce9a333f383e62300dcf5727973cc6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02969329ee4677e165f15b28ffab3baa58c74458a1d46194d42f5d24587b8db9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ab6edd16e82f20545dc498ac3aa542479cada3db180cdee6115ada6358acfc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c12ac6afbd7f1e0ca7ebc691115f4ba938ebe36ca13bcc4a9aff8e82aa36937(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ea13b86099ffad3ee4eadefa39dbca13371916b0546745f5b7e0140e7932ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__900a20b1da6b45b1a40f9c4ad57058d1ca7d9abd7ffe88e19ec6bf6316341b0a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f32416472cf7419746e1a67eb4e13c2ecb318e570812b353912d2af8d4b1c75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10953eb9881740c9f7b394d946575e9613659349efd696a7876155a8efb2197d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e2ed6fa4bdb9ccfe8a2243bc09e076c08f779a80ef4135a550ac5dafac91875(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fb9a15192a648007db46042183af609b442db5d8856d15bc2b6746507735167(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__995268070c02ba706851c483dd0cf862db2b4bb8092858016a029984272debc4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28fa347e60e4e5c9a5c3a254bb36831c686973aa32dce57cb164a4dfcdaa6ea7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e3405aa5f8703ebdbd3f504af3171332838b195b15ace648190aee122a302ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d8a60b444f39ce52f7c3f83df4bd2e2121d5c17809231e27d4024ad14d2b82(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8f8794938eca69670ebcd29de0e1fd59b92681623994d7d76ecd42630f53547(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountRedis]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8924b28c9b7d4db003afc64e9791a61fe5a17214504b14480646b4812716b2fd(
    *,
    name: builtins.str,
    allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    connection_url: typing.Optional[builtins.str] = None,
    data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    disable_escaping: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    max_connection_lifetime: typing.Optional[jsii.Number] = None,
    max_idle_connections: typing.Optional[jsii.Number] = None,
    max_open_connections: typing.Optional[jsii.Number] = None,
    password: typing.Optional[builtins.str] = None,
    plugin_name: typing.Optional[builtins.str] = None,
    root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
    username: typing.Optional[builtins.str] = None,
    username_template: typing.Optional[builtins.str] = None,
    verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6db3faaa35a2320614fee787b8d92846002a747df0b14762cde8dec6954dfc1b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1f0de23009b256c96abff9637f963ea6e8e969ec288ad90b4a3cc24c576cf09(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef99faf6acf134f8b4e0796ab1cac1a3384d1f0a9c83743c4fb0cc1af9cee0ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec099000d033a9d38feed119d3e865634517e333f492c1cd4bbbc96bf41bd53(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfefc03844b087f6bef9546d8d99adb31aa06342f655d54ec9b6295c11e92132(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4549c24036d4775f6c31d799049e071909630bd20ee1ce01de4f636cf59bf06b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountRedshift]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d124eadbabce102a36103b6270b1378cafe5c9509897f9a2c8dd52b4d8d931d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c35cc6011cd998a58a8b521e59fa856130a110c0b15133a3bd53d7376a73c795(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7544b2389a6f7a5c9c4e2803a5736664d22dbad092a91ad97dcd24aef98d5a99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff96e92d242f06ede50de26ce02b2fe1f88f9f33529ad70e6fe97542a5a175f8(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80f25d34b0e38f083abe44bc5beefd388730658d830de2882c54df00fd5cbd3f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ab470d35a8c2ed866f0eac784625fcc7f9d1cc6ca12ff3f4f953b3785c08643(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d9fde83a2cbfa5e468fbfcb7945d604ea1016bcda9e281ea5711497a5fe438(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a4837e3b5fc41bcb00c42d95a740c35c74d36e97dc6884b8fb8289a2b84c98b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__102e0a70e8df3bc7e0454a41bc76d754c196793967f5b1854631f97fe5fb3c62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6121ead6e5709f014746416b339b281a97160e5a428bc31bdc8a1150ba194e60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c356d63336e583c5d1fb4c3457d2c59994fbc747876a6052dbb01e161d0dd89(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5f0be15e64ee46acd286fd334881bbdd6ab53e90d45c898977a93e85e356ee4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d4769b7e4298816da852c9cc7d82d3afbd13e285f14d5bd93e4c44a6c69f751(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ba7ff90d250e606837abc0cfce88362e607dc6d9bc207d76873b03fc65e803(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d266a894aa0c2f9990b03946d55ee1c327a02cc0e30847aae7ab4a066749264b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2b41f433408c6fd6eaf947ce11e2e61318d1417cbad0320ccc4e4631a71dee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountRedshift]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f69284a6cae7f9a93e2d78b68c96325f99de2c92d57cd8ecd635dc0f0c084b0(
    *,
    name: builtins.str,
    allowed_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    connection_url: typing.Optional[builtins.str] = None,
    data: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    max_connection_lifetime: typing.Optional[jsii.Number] = None,
    max_idle_connections: typing.Optional[jsii.Number] = None,
    max_open_connections: typing.Optional[jsii.Number] = None,
    password: typing.Optional[builtins.str] = None,
    plugin_name: typing.Optional[builtins.str] = None,
    root_rotation_statements: typing.Optional[typing.Sequence[builtins.str]] = None,
    username: typing.Optional[builtins.str] = None,
    username_template: typing.Optional[builtins.str] = None,
    verify_connection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2398d68acd89728fdf2ffca6f56eeae10ff7109806747197f539733a80e04e5a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2549cd03910419417a057c0471a411319bc304f6f9b2f42cf3120e3d027340e1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d40a6f286ae3c2be2b7b2912275d1a22b37bdd37e5895f6204561d4d3443c245(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46185847c25339c14c6040388d130b12507c084c1a2201617eeec07285542d87(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cf1afbb16827f7ae95f2f3cb14f921408cab1ca3cd79205263bd7af6c7c4ccf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e083567f6ca41d8c48f32a9d057e49f6413e1be629b84f24955696ef4acf7e17(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DatabaseSecretsMountSnowflake]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f47d988f5970ddc89a0688164c50df541b2f2b4d14adcb17f4bd7a429a0fa4a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27f6a237c25d179fb2dc599b0e2fb2d6d2db3b767c91a69a969557747bb2f14c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f9c34570d5cec6c47ba220be91751c80f637d84aab39611f2c9e3cabfef41c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e166de2f457b145ad6dffb3a05601e7a377204b583bba23eb440b111932ffb47(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66d9e24e9139ef8a4caf88bac01696df8828a63b7211e4d32b29a8134b7a4791(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1064b7cf6c3c4a5ca4c795ed35bc97ee461f665c42f66b589dd6ccc891f0b212(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__248fe56aaafa5e5f75b94292e6f2d1b0e48195438a710cc228b2e5d6c3386d2c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ab70d4f4cd04795d8921b6f785380dc50e69b2ddc953b776cca2dfafc7d7cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e0833dca66d9da8c482ca58f7e2f368ace6cb2f2c52a90480441626df9b00e0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ddf60b128ae6c4d546625278c3b7825fcda2355c10c8bb2a6dc522ccfa2ccd7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25fdf0d0b61412c820dda72d214cefce8468a537134e4b77b87a2b6393fc9ce1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2db1d0ac223df8ee2c1cf4c8870aa56be5283c75939ae6d4c60021d3128cb76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f0513d4ae563396bab70bac6c048198bbdd728b34f17e9f4c1b6e6f473fd68f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa9541c6edef7da4a14b776f076365a23b08787e23c04636e8f4f9e34a5ac30(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9b7e0a72578edce80d6c54649e7a4484958ab830ae4119644cdded65a09ae41(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DatabaseSecretsMountSnowflake]],
) -> None:
    """Type checking stubs"""
    pass
