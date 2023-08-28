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

import constructs as _constructs_77d1e7e8


@jsii.enum(jsii_type="aws-pdk.cdk_graph.CdkConstructIds")
class CdkConstructIds(enum.Enum):
    '''Common cdk construct ids.'''

    DEFAULT = "DEFAULT"
    RESOURCE = "RESOURCE"
    EXPORTS = "EXPORTS"


class CdkGraph(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-pdk.cdk_graph.CdkGraph",
):
    '''CdkGraph construct is the cdk-graph framework controller that is responsible for computing the graph, storing serialized graph, and instrumenting plugins per the plugin contract.'''

    def __init__(
        self,
        root: _constructs_77d1e7e8.Construct,
        *,
        plugins: typing.Optional[typing.Sequence["ICdkGraphPlugin"]] = None,
    ) -> None:
        '''
        :param root: -
        :param plugins: List of plugins to extends the graph. Plugins are invoked at each phases in fifo order.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27c0cd401dadd0588452f1c1fae52718266f81e977ff9050ff78dcccfc0061d2)
            check_type(argname="argument root", value=root, expected_type=type_hints["root"])
        props = ICdkGraphProps(plugins=plugins)

        jsii.create(self.__class__, self, [root, props])

    @jsii.member(jsii_name="report")
    def report(self) -> None:
        '''Asynchronous report generation. This operation enables running expensive and non-synchronous report generation by plugins post synthesis.

        If a given plugin requires performing asynchronous operations or is general expensive, it should
        utilize ``report`` rather than ``synthesize``.
        '''
        return typing.cast(None, jsii.ainvoke(self, "report", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ID")
    def ID(cls) -> builtins.str:
        '''Fixed CdkGraph construct id.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ID"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="VERSION")
    def VERSION(cls) -> builtins.str:
        '''Current CdkGraph semantic version.'''
        return typing.cast(builtins.str, jsii.sget(cls, "VERSION"))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''Config.'''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="plugins")
    def plugins(self) -> typing.List["ICdkGraphPlugin"]:
        '''List of plugins registered with this instance.'''
        return typing.cast(typing.List["ICdkGraphPlugin"], jsii.get(self, "plugins"))

    @builtins.property
    @jsii.member(jsii_name="root")
    def root(self) -> _constructs_77d1e7e8.Construct:
        return typing.cast(_constructs_77d1e7e8.Construct, jsii.get(self, "root"))

    @builtins.property
    @jsii.member(jsii_name="graphContext")
    def graph_context(self) -> typing.Optional["CdkGraphContext"]:
        '''Get the context for the graph instance.

        This will be ``undefined`` before construct synthesis has initiated.
        '''
        return typing.cast(typing.Optional["CdkGraphContext"], jsii.get(self, "graphContext"))


@jsii.data_type(
    jsii_type="aws-pdk.cdk_graph.CdkGraphArtifact",
    jsii_struct_bases=[],
    name_mapping={
        "filename": "filename",
        "filepath": "filepath",
        "id": "id",
        "source": "source",
        "description": "description",
    },
)
class CdkGraphArtifact:
    def __init__(
        self,
        *,
        filename: builtins.str,
        filepath: builtins.str,
        id: builtins.str,
        source: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''CdkGraph artifact definition.

        :param filename: Filename of the artifact.
        :param filepath: Full path where artifact is stored.
        :param id: The unique type of the artifact.
        :param source: The source of the artifact (such as plugin, or core system, etc).
        :param description: Description of artifact.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5d82cab11551fcff2f6299519c75d5a93c746fbe6dfe8fbde7907683afd2b05)
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
            check_type(argname="argument filepath", value=filepath, expected_type=type_hints["filepath"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filename": filename,
            "filepath": filepath,
            "id": id,
            "source": source,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def filename(self) -> builtins.str:
        '''Filename of the artifact.'''
        result = self._values.get("filename")
        assert result is not None, "Required property 'filename' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filepath(self) -> builtins.str:
        '''Full path where artifact is stored.'''
        result = self._values.get("filepath")
        assert result is not None, "Required property 'filepath' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''The unique type of the artifact.'''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''The source of the artifact (such as plugin, or core system, etc).'''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description of artifact.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkGraphArtifact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-pdk.cdk_graph.CdkGraphArtifacts")
class CdkGraphArtifacts(enum.Enum):
    '''CdkGraph core artifacts.'''

    GRAPH_METADATA = "GRAPH_METADATA"
    GRAPH = "GRAPH"


class CdkGraphContext(
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-pdk.cdk_graph.CdkGraphContext",
):
    '''CdkGraph context.'''

    def __init__(self, store: "Store", outdir: builtins.str) -> None:
        '''
        :param store: -
        :param outdir: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81d647d056df85d7e9a08428ddffd79e799c8b938e7fc1bef8c7d407f82c6a04)
            check_type(argname="argument store", value=store, expected_type=type_hints["store"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
        jsii.create(self.__class__, self, [store, outdir])

    @jsii.member(jsii_name="getArtifact")
    def get_artifact(self, id: builtins.str) -> CdkGraphArtifact:
        '''Get CdkGraph artifact by id.

        :param id: -

        :throws: Error is artifact does not exist
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e16b57de7ebe5b23f364abe4879e95b0dd49cd7e83223e6b491ce5e40118f00)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(CdkGraphArtifact, jsii.invoke(self, "getArtifact", [id]))

    @jsii.member(jsii_name="hasArtifactFile")
    def has_artifact_file(self, filename: builtins.str) -> builtins.bool:
        '''Indicates if context has an artifact with *filename* defined.

        :param filename: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf66d947af8fa192724e3f4300774ff37a03388b3e4aea4074df2e2f4090770d)
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
        return typing.cast(builtins.bool, jsii.invoke(self, "hasArtifactFile", [filename]))

    @jsii.member(jsii_name="logArtifact")
    def log_artifact(
        self,
        source: typing.Union[CdkGraph, "ICdkGraphPlugin"],
        id: builtins.str,
        filepath: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> CdkGraphArtifact:
        '''Logs an artifact entry.

        In general this should not be called directly, as ``writeArtifact`` should be utilized
        to perform writing and logging artifacts. However some plugins utilize other tools that generate the artifacts,
        in which case the plugin would call this method to log the entry.

        :param source: The source of the artifact, such as the name of plugin.
        :param id: Unique id of the artifact.
        :param filepath: Full path where the artifact is stored.
        :param description: Description of the artifact.

        :throws: Error is artifact id or filename already exists
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cf12c69a297801d655846dae260d45c9d599a7622f2a7f45c4d3c8a23b4ece6)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument filepath", value=filepath, expected_type=type_hints["filepath"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        return typing.cast(CdkGraphArtifact, jsii.invoke(self, "logArtifact", [source, id, filepath, description]))

    @jsii.member(jsii_name="writeArtifact")
    def write_artifact(
        self,
        source: typing.Union[CdkGraph, "ICdkGraphPlugin"],
        id: builtins.str,
        filename: builtins.str,
        data: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> CdkGraphArtifact:
        '''Writes artifact data to outdir and logs the entry.

        :param source: The source of the artifact, such as the name of plugin.
        :param id: Unique id of the artifact.
        :param filename: Relative name of the file.
        :param data: -
        :param description: Description of the artifact.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5b3da94247e169bc2d88970ff455d7a307e1e3b605f1fdff0b9a65746e6f714)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        return typing.cast(CdkGraphArtifact, jsii.invoke(self, "writeArtifact", [source, id, filename, data, description]))

    @builtins.property
    @jsii.member(jsii_name="artifacts")
    def artifacts(self) -> typing.Mapping[builtins.str, CdkGraphArtifact]:
        '''Get record of all graph artifacts keyed by artifact id.'''
        return typing.cast(typing.Mapping[builtins.str, CdkGraphArtifact], jsii.get(self, "artifacts"))

    @builtins.property
    @jsii.member(jsii_name="graphJson")
    def graph_json(self) -> CdkGraphArtifact:
        '''Get CdkGraph core ``graph.json`` artifact.'''
        return typing.cast(CdkGraphArtifact, jsii.get(self, "graphJson"))

    @builtins.property
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outdir"))

    @builtins.property
    @jsii.member(jsii_name="store")
    def store(self) -> "Store":
        return typing.cast("Store", jsii.get(self, "store"))


@jsii.enum(jsii_type="aws-pdk.cdk_graph.CfnAttributesEnum")
class CfnAttributesEnum(enum.Enum):
    '''Common cfn attribute keys.'''

    TYPE = "TYPE"
    PROPS = "PROPS"


@jsii.data_type(
    jsii_type="aws-pdk.cdk_graph.ConstructInfo",
    jsii_struct_bases=[],
    name_mapping={"fqn": "fqn", "version": "version"},
)
class ConstructInfo:
    def __init__(self, *, fqn: builtins.str, version: builtins.str) -> None:
        '''Source information on a construct (class fqn and version).

        :param fqn: 
        :param version: 

        :see: https://github.com/aws/aws-cdk/blob/cea1039e3664fdfa89c6f00cdaeb1a0185a12678/packages/%40aws-cdk/core/lib/private/runtime-info.ts#L22
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__195e54720f463a462c44f63ad105f7349df2eee3da6f49d9ba35c8c0319ac6bb)
            check_type(argname="argument fqn", value=fqn, expected_type=type_hints["fqn"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fqn": fqn,
            "version": version,
        }

    @builtins.property
    def fqn(self) -> builtins.str:
        result = self._values.get("fqn")
        assert result is not None, "Required property 'fqn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConstructInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-pdk.cdk_graph.ConstructInfoFqnEnum")
class ConstructInfoFqnEnum(enum.Enum):
    '''Commonly used cdk construct info fqn (jsii fully-qualified ids).'''

    APP = "APP"
    PDKAPP_MONO = "PDKAPP_MONO"
    PDKAPP = "PDKAPP"
    STAGE = "STAGE"
    STACK = "STACK"
    NESTED_STACK = "NESTED_STACK"
    CFN_STACK = "CFN_STACK"
    CFN_OUTPUT = "CFN_OUTPUT"
    CFN_PARAMETER = "CFN_PARAMETER"
    CUSTOM_RESOURCE = "CUSTOM_RESOURCE"
    AWS_CUSTOM_RESOURCE = "AWS_CUSTOM_RESOURCE"
    CUSTOM_RESOURCE_PROVIDER = "CUSTOM_RESOURCE_PROVIDER"
    CUSTOM_RESOURCE_PROVIDER_2 = "CUSTOM_RESOURCE_PROVIDER_2"
    LAMBDA = "LAMBDA"
    CFN_LAMBDA = "CFN_LAMBDA"
    LAMBDA_LAYER_VERSION = "LAMBDA_LAYER_VERSION"
    CFN_LAMBDA_LAYER_VERSION = "CFN_LAMBDA_LAYER_VERSION"
    LAMBDA_ALIAS = "LAMBDA_ALIAS"
    CFN_LAMBDA_ALIAS = "CFN_LAMBDA_ALIAS"
    LAMBDA_BASE = "LAMBDA_BASE"
    LAMBDA_SINGLETON = "LAMBDA_SINGLETON"
    LAMBDA_LAYER_AWSCLI = "LAMBDA_LAYER_AWSCLI"
    CFN_LAMBDA_PERMISSIONS = "CFN_LAMBDA_PERMISSIONS"
    ASSET_STAGING = "ASSET_STAGING"
    S3_ASSET = "S3_ASSET"
    ECR_TARBALL_ASSET = "ECR_TARBALL_ASSET"
    EC2_INSTANCE = "EC2_INSTANCE"
    CFN_EC2_INSTANCE = "CFN_EC2_INSTANCE"
    SECURITY_GROUP = "SECURITY_GROUP"
    CFN_SECURITY_GROUP = "CFN_SECURITY_GROUP"
    VPC = "VPC"
    CFN_VPC = "CFN_VPC"
    PRIVATE_SUBNET = "PRIVATE_SUBNET"
    CFN_PRIVATE_SUBNET = "CFN_PRIVATE_SUBNET"
    PUBLIC_SUBNET = "PUBLIC_SUBNET"
    CFN_PUBLIC_SUBNET = "CFN_PUBLIC_SUBNET"
    IAM_ROLE = "IAM_ROLE"


@jsii.enum(jsii_type="aws-pdk.cdk_graph.EdgeDirectionEnum")
class EdgeDirectionEnum(enum.Enum):
    '''EdgeDirection specifies in which direction the edge is directed or if it is undirected.'''

    NONE = "NONE"
    '''Indicates that edge is *undirected*;

    meaning there is no directional relationship between the **source** and **target**.
    '''
    FORWARD = "FORWARD"
    '''Indicates the edge is *directed* from the **source** to the **target**.'''
    BACK = "BACK"
    '''Indicates the edge is *directed* from the **target** to the **source**.'''
    BOTH = "BOTH"
    '''Indicates the edge is *bi-directional*.'''


@jsii.enum(jsii_type="aws-pdk.cdk_graph.EdgeTypeEnum")
class EdgeTypeEnum(enum.Enum):
    '''Edge types handles by the graph.'''

    CUSTOM = "CUSTOM"
    '''Custom edge.'''
    REFERENCE = "REFERENCE"
    '''Reference edge (Ref, Fn::GetAtt, Fn::ImportValue).'''
    DEPENDENCY = "DEPENDENCY"
    '''CloudFormation dependency edge.'''


@jsii.enum(jsii_type="aws-pdk.cdk_graph.FilterPreset")
class FilterPreset(enum.Enum):
    '''Filter presets.'''

    COMPACT = "COMPACT"
    '''Collapses extraneous nodes to parent and cdk created nodes on themselves, and prunes extraneous edges.

    This most closely represents the developers code for the current application
    and reduces the noise one expects.
    '''
    NON_EXTRANEOUS = "NON_EXTRANEOUS"
    '''Collapses extraneous nodes to parent and prunes extraneous edges.'''
    NONE = "NONE"
    '''No filtering is performed which will output **verbose** graph.'''


@jsii.enum(jsii_type="aws-pdk.cdk_graph.FilterStrategy")
class FilterStrategy(enum.Enum):
    '''Filter strategy to apply to filter matches.'''

    PRUNE = "PRUNE"
    '''Remove filtered entity and all its edges.'''
    COLLAPSE = "COLLAPSE"
    '''Collapse all child entities of filtered entity into filtered entity;

    and hoist all edges.
    '''
    COLLAPSE_TO_PARENT = "COLLAPSE_TO_PARENT"
    '''Collapse all filtered entities into their parent entity;

    and hoist its edges to parent.
    '''


@jsii.data_type(
    jsii_type="aws-pdk.cdk_graph.FilterValue",
    jsii_struct_bases=[],
    name_mapping={"regex": "regex", "value": "value"},
)
class FilterValue:
    def __init__(
        self,
        *,
        regex: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Filter value to use.

        :param regex: String representation of a regex.
        :param value: Raw value.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0695bb07e020bdbc6bac5a911e6ab1f1502e5347a5cb9e050d281bf05be5941b)
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if regex is not None:
            self._values["regex"] = regex
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''String representation of a regex.'''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Raw value.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FilterValue(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Filters(metaclass=jsii.JSIIMeta, jsii_type="aws-pdk.cdk_graph.Filters"):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="collapseCdkOwnedResources")
    @builtins.classmethod
    def collapse_cdk_owned_resources(cls) -> "IGraphStoreFilter":
        '''Collapses all Cdk Owned containers, which more closely mirrors the application code by removing resources that are automatically created by cdk.'''
        return typing.cast("IGraphStoreFilter", jsii.sinvoke(cls, "collapseCdkOwnedResources", []))

    @jsii.member(jsii_name="collapseCdkWrappers")
    @builtins.classmethod
    def collapse_cdk_wrappers(cls) -> "IGraphStoreFilter":
        '''Collapses all Cdk Resource wrappers that wrap directly wrap a CfnResource.

        Example, s3.Bucket wraps s3.CfnBucket.
        '''
        return typing.cast("IGraphStoreFilter", jsii.sinvoke(cls, "collapseCdkWrappers", []))

    @jsii.member(jsii_name="collapseCustomResources")
    @builtins.classmethod
    def collapse_custom_resources(cls) -> "IGraphStoreFilter":
        '''Collapses Custom Resource nodes to a single node.'''
        return typing.cast("IGraphStoreFilter", jsii.sinvoke(cls, "collapseCustomResources", []))

    @jsii.member(jsii_name="compact")
    @builtins.classmethod
    def compact(cls) -> "IGraphStoreFilter":
        '''Collapses extraneous nodes to parent and cdk created nodes on themselves, and prunes extraneous edges.

        This most closely represents the developers code for the current application
        and reduces the noise one expects.

        Invokes:
        1.

        1. pruneExtraneous()(store);
        2. collapseCdkOwnedResources()(store);
        3. collapseCdkWrappers()(store);
        4. collapseCustomResources()(store);
        5. ~pruneCustomResources()(store);~
        6. pruneEmptyContainers()(store);

        :destructive: true
        :throws: Error if store is not filterable
        '''
        return typing.cast("IGraphStoreFilter", jsii.sinvoke(cls, "compact", []))

    @jsii.member(jsii_name="excludeCfnType")
    @builtins.classmethod
    def exclude_cfn_type(
        cls,
        cfn_types: typing.Sequence[typing.Union[FilterValue, typing.Dict[builtins.str, typing.Any]]],
    ) -> "IGraphFilter":
        '''Prune all {@link Graph.ResourceNode} and {@link Graph.CfnResourceNode} nodes *matching* specified list of CloudFormation types.

        :param cfn_types: -

        :destructive: true
        :throws: Error if store is not filterable
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8629401beba8ab9f067d55546a5ee55a1c37335f829a6c553e3b96d8cf88e2bc)
            check_type(argname="argument cfn_types", value=cfn_types, expected_type=type_hints["cfn_types"])
        return typing.cast("IGraphFilter", jsii.sinvoke(cls, "excludeCfnType", [cfn_types]))

    @jsii.member(jsii_name="excludeNodeType")
    @builtins.classmethod
    def exclude_node_type(
        cls,
        node_types: typing.Sequence[typing.Union[FilterValue, typing.Dict[builtins.str, typing.Any]]],
    ) -> "IGraphStoreFilter":
        '''Prune all {@link Graph.Node}s *matching* specified list.

        This filter targets all nodes (except root) - {@link IGraphFilter.allNodes}

        :param node_types: -

        :destructive: true
        :throws: Error if store is not filterable
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a81614a43e7cf62541648ca269c11c3a23f8573738aa72ba6f7bed7ba9a641e9)
            check_type(argname="argument node_types", value=node_types, expected_type=type_hints["node_types"])
        return typing.cast("IGraphStoreFilter", jsii.sinvoke(cls, "excludeNodeType", [node_types]))

    @jsii.member(jsii_name="includeCfnType")
    @builtins.classmethod
    def include_cfn_type(
        cls,
        cfn_types: typing.Sequence[typing.Union[FilterValue, typing.Dict[builtins.str, typing.Any]]],
    ) -> "IGraphFilter":
        '''Prune all {@link Graph.ResourceNode} and {@link Graph.CfnResourceNode} nodes *except those matching* specified list of CloudFormation types.

        :param cfn_types: -

        :destructive: true
        :throws: Error if store is not filterable
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcceca9ffcce9781c83f4f4fea91d82aeb5a4ac97cc7cfed47b1f20180e05b3a)
            check_type(argname="argument cfn_types", value=cfn_types, expected_type=type_hints["cfn_types"])
        return typing.cast("IGraphFilter", jsii.sinvoke(cls, "includeCfnType", [cfn_types]))

    @jsii.member(jsii_name="includeNodeType")
    @builtins.classmethod
    def include_node_type(
        cls,
        node_types: typing.Sequence[typing.Union[FilterValue, typing.Dict[builtins.str, typing.Any]]],
    ) -> "IGraphStoreFilter":
        '''Prune all {@link Graph.Node}s *except those matching* specified list.

        This filter targets all nodes (except root) - {@link IGraphFilter.allNodes}

        :param node_types: -

        :destructive: true
        :throws: Error if store is not filterable
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08a61543609b4769faeba386592504091bbd2467ea05f2b8b438803edf2c72e6)
            check_type(argname="argument node_types", value=node_types, expected_type=type_hints["node_types"])
        return typing.cast("IGraphStoreFilter", jsii.sinvoke(cls, "includeNodeType", [node_types]))

    @jsii.member(jsii_name="pruneCustomResources")
    @builtins.classmethod
    def prune_custom_resources(cls) -> "IGraphStoreFilter":
        '''Prune Custom Resource nodes.'''
        return typing.cast("IGraphStoreFilter", jsii.sinvoke(cls, "pruneCustomResources", []))

    @jsii.member(jsii_name="pruneEmptyContainers")
    @builtins.classmethod
    def prune_empty_containers(cls) -> "IGraphStoreFilter":
        '''Prune empty containers, which are non-resource default nodes without any children.

        Generally L3 constructs in which all children have already been pruned, which
        would be useful as containers, but without children are considered extraneous.
        '''
        return typing.cast("IGraphStoreFilter", jsii.sinvoke(cls, "pruneEmptyContainers", []))

    @jsii.member(jsii_name="pruneExtraneous")
    @builtins.classmethod
    def prune_extraneous(cls) -> "IGraphStoreFilter":
        '''Prune **extraneous** nodes and edges.

        :destructive: true
        :throws: Error if store is not filterable
        '''
        return typing.cast("IGraphStoreFilter", jsii.sinvoke(cls, "pruneExtraneous", []))

    @jsii.member(jsii_name="uncluster")
    @builtins.classmethod
    def uncluster(
        cls,
        cluster_types: typing.Optional[typing.Sequence["NodeTypeEnum"]] = None,
    ) -> "IGraphStoreFilter":
        '''Remove clusters by hoisting their children to the parent of the cluster and collapsing the cluster itself to its parent.

        :param cluster_types: -

        :see: {@link Graph.Node.mutateUncluster }
        :destructive: true
        :throws: Error if store is not filterable
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3265a83360e0a421b9bff4299ba5e2032b313b98a8b232cb2f39c2fd87deee7)
            check_type(argname="argument cluster_types", value=cluster_types, expected_type=type_hints["cluster_types"])
        return typing.cast("IGraphStoreFilter", jsii.sinvoke(cls, "uncluster", [cluster_types]))

    @jsii.member(jsii_name="verifyFilterable")
    @builtins.classmethod
    def verify_filterable(cls, store: "Store") -> None:
        '''Verify that store is filterable, meaning it allows destructive mutations.

        :param store: -

        :throws: Error if store is not filterable
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e7145a4cf4d60e5ecd33563cbc93b575d2b0cb54a29ed65bd480f3cfced5b06)
            check_type(argname="argument store", value=store, expected_type=type_hints["store"])
        return typing.cast(None, jsii.sinvoke(cls, "verifyFilterable", [store]))


@jsii.enum(jsii_type="aws-pdk.cdk_graph.FlagEnum")
class FlagEnum(enum.Enum):
    '''Graph flags.'''

    CLUSTER = "CLUSTER"
    '''Indicates that node is a cluster (container) and treated like an emphasized subgraph.'''
    GRAPH_CONTAINER = "GRAPH_CONTAINER"
    '''Indicates that node is non-resource container (Root, App) and used for structural purpose in the graph only.'''
    EXTRANEOUS = "EXTRANEOUS"
    '''Indicates that the entity is extraneous and considered collapsible to parent without impact of intent.'''
    ASSET = "ASSET"
    '''Indicates node is considered a CDK Asset (Lambda Code, Docker Image, etc).'''
    CDK_OWNED = "CDK_OWNED"
    '''Indicates that node was created by CDK.

    :see: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.Resource.html#static-iswbrownedwbrresourceconstruct
    '''
    CFN_FQN = "CFN_FQN"
    '''Indicates node ConstructInfoFqn denotes a ``aws-cdk-lib.*.Cfn*`` construct.'''
    CLOSED_EDGE = "CLOSED_EDGE"
    '''Indicates that edge is closed;

    meaning ``source === target``. This flag only gets applied on creation of edge, not during mutations to maintain initial intent.
    '''
    MUTATED = "MUTATED"
    '''Indicates that entity was mutated;

    meaning a mutation was performed to change originally computed graph value.
    '''
    IMPORT = "IMPORT"
    '''Indicates that resource is imported into CDK (eg: ``lambda.Function.fromFunctionName()``, ``s3.Bucket.fromBucketArn()``).'''
    CUSTOM_RESOURCE = "CUSTOM_RESOURCE"
    '''Indicates if node is a CustomResource.

    :see: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.custom_resources-readme.html
    '''
    AWS_CUSTOM_RESOURCE = "AWS_CUSTOM_RESOURCE"
    '''Indicates if node is an AwsCustomResource, which is a custom resource that simply calls the AWS SDK API via singleton provider.

    :see: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.custom_resources.AwsCustomResource.html
    '''
    AWS_API_CALL_LAMBDA = "AWS_API_CALL_LAMBDA"
    '''Indicates if lambda function resource is a singleton AWS API call lambda for AwsCustomResources.

    :see: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.custom_resources.AwsCustomResource.html
    '''


@jsii.interface(jsii_type="aws-pdk.cdk_graph.IBaseEntityDataProps")
class IBaseEntityDataProps(typing_extensions.Protocol):
    '''Base interface for all store entities **data** props.'''

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, "PlainObject", typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, "PlainObject"]]]]]:
        '''Attributes.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="flags")
    def flags(self) -> typing.Optional[typing.List[FlagEnum]]:
        '''Flags.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(
        self,
    ) -> typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]]:
        '''Metadata entries.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags.'''
        ...


class _IBaseEntityDataPropsProxy:
    '''Base interface for all store entities **data** props.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.IBaseEntityDataProps"

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, "PlainObject", typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, "PlainObject"]]]]]:
        '''Attributes.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, "PlainObject", typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, "PlainObject"]]]]], jsii.get(self, "attributes"))

    @builtins.property
    @jsii.member(jsii_name="flags")
    def flags(self) -> typing.Optional[typing.List[FlagEnum]]:
        '''Flags.'''
        return typing.cast(typing.Optional[typing.List[FlagEnum]], jsii.get(self, "flags"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(
        self,
    ) -> typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]]:
        '''Metadata entries.'''
        return typing.cast(typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]], jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Tags.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tags"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBaseEntityDataProps).__jsii_proxy_class__ = lambda : _IBaseEntityDataPropsProxy


@jsii.interface(jsii_type="aws-pdk.cdk_graph.IBaseEntityProps")
class IBaseEntityProps(IBaseEntityDataProps, typing_extensions.Protocol):
    '''Base interface for all store entities props.'''

    @builtins.property
    @jsii.member(jsii_name="store")
    def store(self) -> "Store":
        '''Store.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        '''UUID.'''
        ...


class _IBaseEntityPropsProxy(
    jsii.proxy_for(IBaseEntityDataProps), # type: ignore[misc]
):
    '''Base interface for all store entities props.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.IBaseEntityProps"

    @builtins.property
    @jsii.member(jsii_name="store")
    def store(self) -> "Store":
        '''Store.'''
        return typing.cast("Store", jsii.get(self, "store"))

    @builtins.property
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        '''UUID.'''
        return typing.cast(builtins.str, jsii.get(self, "uuid"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBaseEntityProps).__jsii_proxy_class__ = lambda : _IBaseEntityPropsProxy


@jsii.interface(jsii_type="aws-pdk.cdk_graph.ICdkGraphPlugin")
class ICdkGraphPlugin(typing_extensions.Protocol):
    '''CdkGraph **Plugin** interface.'''

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''Unique identifier for this plugin.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''Plugin version.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="dependencies")
    def dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of plugins this plugin depends on, including optional semver version (eg: ["foo", "bar@1.2"]).'''
        ...

    @builtins.property
    @jsii.member(jsii_name="bind")
    def bind(self) -> "IGraphPluginBindCallback":
        '''Binds the plugin to the CdkGraph instance.

        Enables plugins to receive base configs.
        '''
        ...

    @bind.setter
    def bind(self, value: "IGraphPluginBindCallback") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="inspect")
    def inspect(self) -> typing.Optional["IGraphVisitorCallback"]:
        '''Node visitor callback for construct tree traversal.

        This follows IAspect.visit pattern, but the order
        of visitor traversal in managed by the CdkGraph.
        '''
        ...

    @inspect.setter
    def inspect(self, value: typing.Optional["IGraphVisitorCallback"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="report")
    def report(self) -> typing.Optional["IGraphReportCallback"]:
        '''Generate asynchronous reports based on the graph.

        This is not automatically called when synthesizing CDK.
        Developer must explicitly add ``await graphInstance.report()`` to the CDK bin or invoke this outside
        of the CDK synth. In either case, the plugin receives the in-memory graph interface when invoked, as the
        CdkGraph will deserialize the graph prior to invoking the plugin report.
        '''
        ...

    @report.setter
    def report(self, value: typing.Optional["IGraphReportCallback"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="synthesize")
    def synthesize(self) -> typing.Optional["IGraphSynthesizeCallback"]:
        '''Called during CDK synthesize to generate synchronous artifacts based on the in-memory graph passed to the plugin.

        This is called in fifo order of plugins.
        '''
        ...

    @synthesize.setter
    def synthesize(self, value: typing.Optional["IGraphSynthesizeCallback"]) -> None:
        ...


class _ICdkGraphPluginProxy:
    '''CdkGraph **Plugin** interface.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.ICdkGraphPlugin"

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''Unique identifier for this plugin.'''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''Plugin version.'''
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="dependencies")
    def dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of plugins this plugin depends on, including optional semver version (eg: ["foo", "bar@1.2"]).'''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dependencies"))

    @builtins.property
    @jsii.member(jsii_name="bind")
    def bind(self) -> "IGraphPluginBindCallback":
        '''Binds the plugin to the CdkGraph instance.

        Enables plugins to receive base configs.
        '''
        return typing.cast("IGraphPluginBindCallback", jsii.get(self, "bind"))

    @bind.setter
    def bind(self, value: "IGraphPluginBindCallback") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cec3ef32f6ccb0052708916e41815fb90eef21f2a6a4166f10f81355024fc3ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bind", value)

    @builtins.property
    @jsii.member(jsii_name="inspect")
    def inspect(self) -> typing.Optional["IGraphVisitorCallback"]:
        '''Node visitor callback for construct tree traversal.

        This follows IAspect.visit pattern, but the order
        of visitor traversal in managed by the CdkGraph.
        '''
        return typing.cast(typing.Optional["IGraphVisitorCallback"], jsii.get(self, "inspect"))

    @inspect.setter
    def inspect(self, value: typing.Optional["IGraphVisitorCallback"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10f09faa94a1e661dc734f7fe17dd01bc53a6d99cdd7cb89c29b22872f935c3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inspect", value)

    @builtins.property
    @jsii.member(jsii_name="report")
    def report(self) -> typing.Optional["IGraphReportCallback"]:
        '''Generate asynchronous reports based on the graph.

        This is not automatically called when synthesizing CDK.
        Developer must explicitly add ``await graphInstance.report()`` to the CDK bin or invoke this outside
        of the CDK synth. In either case, the plugin receives the in-memory graph interface when invoked, as the
        CdkGraph will deserialize the graph prior to invoking the plugin report.
        '''
        return typing.cast(typing.Optional["IGraphReportCallback"], jsii.get(self, "report"))

    @report.setter
    def report(self, value: typing.Optional["IGraphReportCallback"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fce80a55da3622644d29ec84456917eb0beec770e0518163aa866c07a74e63c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "report", value)

    @builtins.property
    @jsii.member(jsii_name="synthesize")
    def synthesize(self) -> typing.Optional["IGraphSynthesizeCallback"]:
        '''Called during CDK synthesize to generate synchronous artifacts based on the in-memory graph passed to the plugin.

        This is called in fifo order of plugins.
        '''
        return typing.cast(typing.Optional["IGraphSynthesizeCallback"], jsii.get(self, "synthesize"))

    @synthesize.setter
    def synthesize(self, value: typing.Optional["IGraphSynthesizeCallback"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__327e61b18f62c219319411532c743a133ca4ccf49b67778fe14192f2d7d48295)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "synthesize", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICdkGraphPlugin).__jsii_proxy_class__ = lambda : _ICdkGraphPluginProxy


@jsii.data_type(
    jsii_type="aws-pdk.cdk_graph.ICdkGraphProps",
    jsii_struct_bases=[],
    name_mapping={"plugins": "plugins"},
)
class ICdkGraphProps:
    def __init__(
        self,
        *,
        plugins: typing.Optional[typing.Sequence[ICdkGraphPlugin]] = None,
    ) -> None:
        '''{@link CdkGraph} props.

        :param plugins: List of plugins to extends the graph. Plugins are invoked at each phases in fifo order.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f41f7d3ea20834a84a5383430600b13d06568854f927c95f668f009d4b6b3eec)
            check_type(argname="argument plugins", value=plugins, expected_type=type_hints["plugins"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if plugins is not None:
            self._values["plugins"] = plugins

    @builtins.property
    def plugins(self) -> typing.Optional[typing.List[ICdkGraphPlugin]]:
        '''List of plugins to extends the graph.

        Plugins are invoked at each phases in fifo order.
        '''
        result = self._values.get("plugins")
        return typing.cast(typing.Optional[typing.List[ICdkGraphPlugin]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ICdkGraphProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="aws-pdk.cdk_graph.IEdgePredicate")
class IEdgePredicate(typing_extensions.Protocol):
    '''Predicate to match edge.'''

    @jsii.member(jsii_name="filter")
    def filter(self, edge: "Edge") -> builtins.bool:
        '''
        :param edge: -
        '''
        ...


class _IEdgePredicateProxy:
    '''Predicate to match edge.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.IEdgePredicate"

    @jsii.member(jsii_name="filter")
    def filter(self, edge: "Edge") -> builtins.bool:
        '''
        :param edge: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5104b846228daa4b8c1327d05b0f107eccc2bc188eadb4c78f3bf8d9f1966b09)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(builtins.bool, jsii.invoke(self, "filter", [edge]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEdgePredicate).__jsii_proxy_class__ = lambda : _IEdgePredicateProxy


@jsii.data_type(
    jsii_type="aws-pdk.cdk_graph.IFilter",
    jsii_struct_bases=[],
    name_mapping={"graph": "graph", "store": "store"},
)
class IFilter:
    def __init__(
        self,
        *,
        graph: typing.Optional[typing.Union["IGraphFilter", typing.Dict[builtins.str, typing.Any]]] = None,
        store: typing.Optional["IGraphStoreFilter"] = None,
    ) -> None:
        '''A filter than can be applied to the graph.

        :param graph: Graph Filter.
        :param store: Store Filter.
        '''
        if isinstance(graph, dict):
            graph = IGraphFilter(**graph)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e372c28af11eeb9c028663f92cca63cb2113a713369c52ab35590d6c7aac4a94)
            check_type(argname="argument graph", value=graph, expected_type=type_hints["graph"])
            check_type(argname="argument store", value=store, expected_type=type_hints["store"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if graph is not None:
            self._values["graph"] = graph
        if store is not None:
            self._values["store"] = store

    @builtins.property
    def graph(self) -> typing.Optional["IGraphFilter"]:
        '''Graph Filter.'''
        result = self._values.get("graph")
        return typing.cast(typing.Optional["IGraphFilter"], result)

    @builtins.property
    def store(self) -> typing.Optional["IGraphStoreFilter"]:
        '''Store Filter.'''
        result = self._values.get("store")
        return typing.cast(typing.Optional["IGraphStoreFilter"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="aws-pdk.cdk_graph.IFilterFocusCallback")
class IFilterFocusCallback(typing_extensions.Protocol):
    '''Determines focus node of filter plan.'''

    @jsii.member(jsii_name="filter")
    def filter(self, store: "Store") -> "Node":
        '''
        :param store: -
        '''
        ...


class _IFilterFocusCallbackProxy:
    '''Determines focus node of filter plan.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.IFilterFocusCallback"

    @jsii.member(jsii_name="filter")
    def filter(self, store: "Store") -> "Node":
        '''
        :param store: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7461ffa3e5819d67add5a1801ca2dc33b32fe7c91ac20ab346e8f1a4583dd300)
            check_type(argname="argument store", value=store, expected_type=type_hints["store"])
        return typing.cast("Node", jsii.invoke(self, "filter", [store]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFilterFocusCallback).__jsii_proxy_class__ = lambda : _IFilterFocusCallbackProxy


@jsii.interface(jsii_type="aws-pdk.cdk_graph.IFindEdgeOptions")
class IFindEdgeOptions(typing_extensions.Protocol):
    '''Options for edge based search operations.'''

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> typing.Optional[_constructs_77d1e7e8.ConstructOrder]:
        '''The order of traversal during search path.'''
        ...

    @order.setter
    def order(
        self,
        value: typing.Optional[_constructs_77d1e7e8.ConstructOrder],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="predicate")
    def predicate(self) -> typing.Optional[IEdgePredicate]:
        '''The predicate to match edges(s).'''
        ...

    @predicate.setter
    def predicate(self, value: typing.Optional[IEdgePredicate]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="reverse")
    def reverse(self) -> typing.Optional[builtins.bool]:
        '''Indicates reverse order.'''
        ...

    @reverse.setter
    def reverse(self, value: typing.Optional[builtins.bool]) -> None:
        ...


class _IFindEdgeOptionsProxy:
    '''Options for edge based search operations.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.IFindEdgeOptions"

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> typing.Optional[_constructs_77d1e7e8.ConstructOrder]:
        '''The order of traversal during search path.'''
        return typing.cast(typing.Optional[_constructs_77d1e7e8.ConstructOrder], jsii.get(self, "order"))

    @order.setter
    def order(
        self,
        value: typing.Optional[_constructs_77d1e7e8.ConstructOrder],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be88ede9716eae25ace453020f7c5b190ff0cdc34d57f31ced2e412d4b3c8da8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "order", value)

    @builtins.property
    @jsii.member(jsii_name="predicate")
    def predicate(self) -> typing.Optional[IEdgePredicate]:
        '''The predicate to match edges(s).'''
        return typing.cast(typing.Optional[IEdgePredicate], jsii.get(self, "predicate"))

    @predicate.setter
    def predicate(self, value: typing.Optional[IEdgePredicate]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dffad915d3f4eece0462979b246e33b227765e2e3c13712ab80a2caad005998a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "predicate", value)

    @builtins.property
    @jsii.member(jsii_name="reverse")
    def reverse(self) -> typing.Optional[builtins.bool]:
        '''Indicates reverse order.'''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "reverse"))

    @reverse.setter
    def reverse(self, value: typing.Optional[builtins.bool]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__111fb97b7ffc01e9032f0bfd6f545b8285bb3d991e206bf3d9ce52b6e13cca09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reverse", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFindEdgeOptions).__jsii_proxy_class__ = lambda : _IFindEdgeOptionsProxy


@jsii.interface(jsii_type="aws-pdk.cdk_graph.IFindNodeOptions")
class IFindNodeOptions(typing_extensions.Protocol):
    '''Options for node based search operations.'''

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> typing.Optional[_constructs_77d1e7e8.ConstructOrder]:
        '''The order of traversal during search path.'''
        ...

    @order.setter
    def order(
        self,
        value: typing.Optional[_constructs_77d1e7e8.ConstructOrder],
    ) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="predicate")
    def predicate(self) -> typing.Optional["INodePredicate"]:
        '''The predicate to match node(s).'''
        ...

    @predicate.setter
    def predicate(self, value: typing.Optional["INodePredicate"]) -> None:
        ...


class _IFindNodeOptionsProxy:
    '''Options for node based search operations.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.IFindNodeOptions"

    @builtins.property
    @jsii.member(jsii_name="order")
    def order(self) -> typing.Optional[_constructs_77d1e7e8.ConstructOrder]:
        '''The order of traversal during search path.'''
        return typing.cast(typing.Optional[_constructs_77d1e7e8.ConstructOrder], jsii.get(self, "order"))

    @order.setter
    def order(
        self,
        value: typing.Optional[_constructs_77d1e7e8.ConstructOrder],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81452004140db3cdc6d913f09e8a0cad6783c636889e27996cd92075d886026d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "order", value)

    @builtins.property
    @jsii.member(jsii_name="predicate")
    def predicate(self) -> typing.Optional["INodePredicate"]:
        '''The predicate to match node(s).'''
        return typing.cast(typing.Optional["INodePredicate"], jsii.get(self, "predicate"))

    @predicate.setter
    def predicate(self, value: typing.Optional["INodePredicate"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ab65295afddf6807d1aaa7a7feefb126d17fb6c48a4ff4876355df9276f1104)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "predicate", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFindNodeOptions).__jsii_proxy_class__ = lambda : _IFindNodeOptionsProxy


@jsii.data_type(
    jsii_type="aws-pdk.cdk_graph.IGraphFilter",
    jsii_struct_bases=[],
    name_mapping={
        "all_nodes": "allNodes",
        "edge": "edge",
        "inverse": "inverse",
        "node": "node",
        "strategy": "strategy",
    },
)
class IGraphFilter:
    def __init__(
        self,
        *,
        all_nodes: typing.Optional[builtins.bool] = None,
        edge: typing.Optional[IEdgePredicate] = None,
        inverse: typing.Optional[builtins.bool] = None,
        node: typing.Optional["INodePredicate"] = None,
        strategy: typing.Optional[FilterStrategy] = None,
    ) -> None:
        '''Graph filter.

        :param all_nodes: Indicates that all nodes will be filtered, rather than just Resource and CfnResource nodes. By enabling this, all Stages, Stacks, and structural construct boundaries will be filtered as well. In general, most users intent is to operate against resources and desire to preserve structural groupings, which is common in most Cfn/Cdk based filtering where inputs are "include" lists. Defaults to value of containing {@link IGraphFilterPlan.allNodes}
        :param edge: Predicate to match edges. Edges are evaluated after nodes are filtered.
        :param inverse: Indicates that matches will be filtered, as opposed to non-matches. The default follows common `Javascript Array.filter <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter>`_ precedence of preserving matches during filtering, while pruning non-matches. Default: false - Preserve matches, and filter out non-matches.
        :param node: Predicate to match nodes.
        :param strategy: Filter strategy to apply to matching nodes. Edges do not have a strategy, they are always pruned. Default: {FilterStrategy.PRUNE}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__840da42ae2fc1e59d55f4dfbb9303d1aa93fee75f0d64b0effb1b828bb2e79bf)
            check_type(argname="argument all_nodes", value=all_nodes, expected_type=type_hints["all_nodes"])
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
            check_type(argname="argument inverse", value=inverse, expected_type=type_hints["inverse"])
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if all_nodes is not None:
            self._values["all_nodes"] = all_nodes
        if edge is not None:
            self._values["edge"] = edge
        if inverse is not None:
            self._values["inverse"] = inverse
        if node is not None:
            self._values["node"] = node
        if strategy is not None:
            self._values["strategy"] = strategy

    @builtins.property
    def all_nodes(self) -> typing.Optional[builtins.bool]:
        '''Indicates that all nodes will be filtered, rather than just Resource and CfnResource nodes.

        By enabling this, all Stages, Stacks, and structural construct boundaries will be filtered as well.
        In general, most users intent is to operate against resources and desire to preserve structural groupings,
        which is common in most Cfn/Cdk based filtering where inputs are "include" lists.

        Defaults to value of containing {@link IGraphFilterPlan.allNodes}
        '''
        result = self._values.get("all_nodes")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def edge(self) -> typing.Optional[IEdgePredicate]:
        '''Predicate to match edges.

        Edges are evaluated after nodes are filtered.
        '''
        result = self._values.get("edge")
        return typing.cast(typing.Optional[IEdgePredicate], result)

    @builtins.property
    def inverse(self) -> typing.Optional[builtins.bool]:
        '''Indicates that matches will be filtered, as opposed to non-matches.

        The default follows common `Javascript Array.filter <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter>`_
        precedence of preserving matches during filtering, while pruning non-matches.

        :default: false - Preserve matches, and filter out non-matches.
        '''
        result = self._values.get("inverse")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def node(self) -> typing.Optional["INodePredicate"]:
        '''Predicate to match nodes.'''
        result = self._values.get("node")
        return typing.cast(typing.Optional["INodePredicate"], result)

    @builtins.property
    def strategy(self) -> typing.Optional[FilterStrategy]:
        '''Filter strategy to apply to matching nodes.

        Edges do not have a strategy, they are always pruned.

        :default: {FilterStrategy.PRUNE}
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional[FilterStrategy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IGraphFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-pdk.cdk_graph.IGraphFilterPlan",
    jsii_struct_bases=[],
    name_mapping={
        "all_nodes": "allNodes",
        "filters": "filters",
        "focus": "focus",
        "order": "order",
        "preset": "preset",
    },
)
class IGraphFilterPlan:
    def __init__(
        self,
        *,
        all_nodes: typing.Optional[builtins.bool] = None,
        filters: typing.Optional[typing.Sequence[typing.Union[IFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
        focus: typing.Optional[typing.Union["IGraphFilterPlanFocusConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        order: typing.Optional[_constructs_77d1e7e8.ConstructOrder] = None,
        preset: typing.Optional[FilterPreset] = None,
    ) -> None:
        '''Graph filter plan.

        :param all_nodes: Indicates that all nodes will be filtered, rather than just Resource and CfnResource nodes. By enabling this, all Stages, Stacks, and structural construct boundaries will be filtered as well. In general, most users intent is to operate against resources and desire to preserve structural groupings, which is common in most Cfn/Cdk based filtering where inputs are "include" lists. Default: false By default only Resource and CfnResource nodes are filtered.
        :param filters: Ordered list of {@link IGraphFilter} and {@link IGraphStoreFilter} filters to apply to the store. - Filters are applied *after* the preset filtering is applied if present. - Filters are applied sequentially against all nodes, as opposed to IAspect.visitor pattern which are sequentially applied per node.
        :param focus: Config to focus the graph on specific node.
        :param order: The order to visit nodes and edges during filtering. Default: {ConstructOrder.PREORDER}
        :param preset: Optional preset filter to apply before other filters.
        '''
        if isinstance(focus, dict):
            focus = IGraphFilterPlanFocusConfig(**focus)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ccb6194666839ca5d5cb519d9346bdf8d90cb2b378883da4fe080c7887dc09c)
            check_type(argname="argument all_nodes", value=all_nodes, expected_type=type_hints["all_nodes"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument focus", value=focus, expected_type=type_hints["focus"])
            check_type(argname="argument order", value=order, expected_type=type_hints["order"])
            check_type(argname="argument preset", value=preset, expected_type=type_hints["preset"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if all_nodes is not None:
            self._values["all_nodes"] = all_nodes
        if filters is not None:
            self._values["filters"] = filters
        if focus is not None:
            self._values["focus"] = focus
        if order is not None:
            self._values["order"] = order
        if preset is not None:
            self._values["preset"] = preset

    @builtins.property
    def all_nodes(self) -> typing.Optional[builtins.bool]:
        '''Indicates that all nodes will be filtered, rather than just Resource and CfnResource nodes.

        By enabling this, all Stages, Stacks, and structural construct boundaries will be filtered as well.
        In general, most users intent is to operate against resources and desire to preserve structural groupings,
        which is common in most Cfn/Cdk based filtering where inputs are "include" lists.

        :default: false By default only Resource and CfnResource nodes are filtered.
        '''
        result = self._values.get("all_nodes")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def filters(self) -> typing.Optional[typing.List[IFilter]]:
        '''Ordered list of {@link IGraphFilter} and {@link IGraphStoreFilter} filters to apply to the store.

        - Filters are applied *after* the preset filtering is applied if present.
        - Filters are applied sequentially against all nodes, as opposed to IAspect.visitor pattern
          which are sequentially applied per node.
        '''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.List[IFilter]], result)

    @builtins.property
    def focus(self) -> typing.Optional["IGraphFilterPlanFocusConfig"]:
        '''Config to focus the graph on specific node.'''
        result = self._values.get("focus")
        return typing.cast(typing.Optional["IGraphFilterPlanFocusConfig"], result)

    @builtins.property
    def order(self) -> typing.Optional[_constructs_77d1e7e8.ConstructOrder]:
        '''The order to visit nodes and edges during filtering.

        :default: {ConstructOrder.PREORDER}
        '''
        result = self._values.get("order")
        return typing.cast(typing.Optional[_constructs_77d1e7e8.ConstructOrder], result)

    @builtins.property
    def preset(self) -> typing.Optional[FilterPreset]:
        '''Optional preset filter to apply before other filters.'''
        result = self._values.get("preset")
        return typing.cast(typing.Optional[FilterPreset], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IGraphFilterPlan(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-pdk.cdk_graph.IGraphFilterPlanFocusConfig",
    jsii_struct_bases=[],
    name_mapping={"filter": "filter", "no_hoist": "noHoist"},
)
class IGraphFilterPlanFocusConfig:
    def __init__(
        self,
        *,
        filter: IFilterFocusCallback,
        no_hoist: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param filter: The node or resolver to determine the node to focus on.
        :param no_hoist: Indicates if ancestral containers are preserved (eg: Stages, Stack). If ``false``, the "focused node" will be hoisted to the graph root and all ancestors will be pruned. If ``true``, the "focused" will be left in-place, while all siblings and non-scope ancestors will be pruned. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e394bd3f78468d03deb74b83a2ce7cf9270776ac045d8a8e9f3ed619d1070559)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument no_hoist", value=no_hoist, expected_type=type_hints["no_hoist"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter": filter,
        }
        if no_hoist is not None:
            self._values["no_hoist"] = no_hoist

    @builtins.property
    def filter(self) -> IFilterFocusCallback:
        '''The node or resolver to determine the node to focus on.'''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast(IFilterFocusCallback, result)

    @builtins.property
    def no_hoist(self) -> typing.Optional[builtins.bool]:
        '''Indicates if ancestral containers are preserved (eg: Stages, Stack).

        If ``false``, the "focused node" will be hoisted to the graph root and all ancestors will be pruned.
        If ``true``, the "focused" will be left in-place, while all siblings and non-scope ancestors will be pruned.

        :default: true
        '''
        result = self._values.get("no_hoist")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IGraphFilterPlanFocusConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="aws-pdk.cdk_graph.IGraphPluginBindCallback")
class IGraphPluginBindCallback(typing_extensions.Protocol):
    '''Callback signature for graph ``Plugin.bind`` operation.'''

    pass


class _IGraphPluginBindCallbackProxy:
    '''Callback signature for graph ``Plugin.bind`` operation.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.IGraphPluginBindCallback"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphPluginBindCallback).__jsii_proxy_class__ = lambda : _IGraphPluginBindCallbackProxy


@jsii.interface(jsii_type="aws-pdk.cdk_graph.IGraphReportCallback")
class IGraphReportCallback(typing_extensions.Protocol):
    '''Callback signature for graph ``Plugin.report`` operation.'''

    pass


class _IGraphReportCallbackProxy:
    '''Callback signature for graph ``Plugin.report`` operation.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.IGraphReportCallback"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphReportCallback).__jsii_proxy_class__ = lambda : _IGraphReportCallbackProxy


@jsii.interface(jsii_type="aws-pdk.cdk_graph.IGraphStoreFilter")
class IGraphStoreFilter(typing_extensions.Protocol):
    '''Store filter callback interface used to perform filtering operations directly against the store, as opposed to using {@link IGraphFilter} definitions.'''

    @jsii.member(jsii_name="filter")
    def filter(self, store: "Store") -> None:
        '''
        :param store: -
        '''
        ...


class _IGraphStoreFilterProxy:
    '''Store filter callback interface used to perform filtering operations directly against the store, as opposed to using {@link IGraphFilter} definitions.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.IGraphStoreFilter"

    @jsii.member(jsii_name="filter")
    def filter(self, store: "Store") -> None:
        '''
        :param store: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9410ad2f608ab5a52bfc6304fa30426823a4b1855524b07676969f9da1dc191e)
            check_type(argname="argument store", value=store, expected_type=type_hints["store"])
        return typing.cast(None, jsii.invoke(self, "filter", [store]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphStoreFilter).__jsii_proxy_class__ = lambda : _IGraphStoreFilterProxy


@jsii.interface(jsii_type="aws-pdk.cdk_graph.IGraphSynthesizeCallback")
class IGraphSynthesizeCallback(typing_extensions.Protocol):
    '''Callback signature for graph ``Plugin.synthesize`` operation.'''

    pass


class _IGraphSynthesizeCallbackProxy:
    '''Callback signature for graph ``Plugin.synthesize`` operation.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.IGraphSynthesizeCallback"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphSynthesizeCallback).__jsii_proxy_class__ = lambda : _IGraphSynthesizeCallbackProxy


@jsii.interface(jsii_type="aws-pdk.cdk_graph.IGraphVisitorCallback")
class IGraphVisitorCallback(typing_extensions.Protocol):
    '''Callback signature for graph ``Plugin.inspect`` operation.'''

    pass


class _IGraphVisitorCallbackProxy:
    '''Callback signature for graph ``Plugin.inspect`` operation.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.IGraphVisitorCallback"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGraphVisitorCallback).__jsii_proxy_class__ = lambda : _IGraphVisitorCallbackProxy


@jsii.interface(jsii_type="aws-pdk.cdk_graph.INodePredicate")
class INodePredicate(typing_extensions.Protocol):
    '''Predicate to match node.'''

    @jsii.member(jsii_name="filter")
    def filter(self, node: "Node") -> builtins.bool:
        '''
        :param node: -
        '''
        ...


class _INodePredicateProxy:
    '''Predicate to match node.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.INodePredicate"

    @jsii.member(jsii_name="filter")
    def filter(self, node: "Node") -> builtins.bool:
        '''
        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad4271c60ee6c959db9db1ea974a08da8f6ec89f3fc7ddf8a7d8d52f99d5ed98)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.invoke(self, "filter", [node]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INodePredicate).__jsii_proxy_class__ = lambda : _INodePredicateProxy


@jsii.interface(jsii_type="aws-pdk.cdk_graph.ISerializableEdge")
class ISerializableEdge(typing_extensions.Protocol):
    '''Interface for serializable graph edge entity.'''

    pass


class _ISerializableEdgeProxy:
    '''Interface for serializable graph edge entity.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.ISerializableEdge"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISerializableEdge).__jsii_proxy_class__ = lambda : _ISerializableEdgeProxy


@jsii.interface(jsii_type="aws-pdk.cdk_graph.ISerializableEntity")
class ISerializableEntity(typing_extensions.Protocol):
    '''Interface for serializable graph entities.'''

    pass


class _ISerializableEntityProxy:
    '''Interface for serializable graph entities.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.ISerializableEntity"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISerializableEntity).__jsii_proxy_class__ = lambda : _ISerializableEntityProxy


@jsii.interface(jsii_type="aws-pdk.cdk_graph.ISerializableGraphStore")
class ISerializableGraphStore(typing_extensions.Protocol):
    '''Interface for serializable graph store.'''

    @jsii.member(jsii_name="serialize")
    def serialize(self) -> "SGGraphStore":
        ...


class _ISerializableGraphStoreProxy:
    '''Interface for serializable graph store.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.ISerializableGraphStore"

    @jsii.member(jsii_name="serialize")
    def serialize(self) -> "SGGraphStore":
        return typing.cast("SGGraphStore", jsii.invoke(self, "serialize", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISerializableGraphStore).__jsii_proxy_class__ = lambda : _ISerializableGraphStoreProxy


@jsii.interface(jsii_type="aws-pdk.cdk_graph.ISerializableNode")
class ISerializableNode(typing_extensions.Protocol):
    '''Interface for serializable graph node entity.'''

    pass


class _ISerializableNodeProxy:
    '''Interface for serializable graph node entity.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.ISerializableNode"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISerializableNode).__jsii_proxy_class__ = lambda : _ISerializableNodeProxy


@jsii.interface(jsii_type="aws-pdk.cdk_graph.IStoreCounts")
class IStoreCounts(typing_extensions.Protocol):
    '''Interface for store counts.'''

    @builtins.property
    @jsii.member(jsii_name="cfnResources")
    def cfn_resources(self) -> typing.Mapping[builtins.str, jsii.Number]:
        '''Returns {@link ICounterRecord} containing total number of each *cfnResourceType*.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="edges")
    def edges(self) -> jsii.Number:
        '''Counts total number of edges in the store.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="edgeTypes")
    def edge_types(self) -> typing.Mapping[builtins.str, jsii.Number]:
        '''Returns {@link ICounterRecord} containing total number of each *edge type* ({@link EdgeTypeEnum}).'''
        ...

    @builtins.property
    @jsii.member(jsii_name="nodes")
    def nodes(self) -> jsii.Number:
        '''Counts total number of nodes in the store.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="nodeTypes")
    def node_types(self) -> typing.Mapping[builtins.str, jsii.Number]:
        '''Returns {@link ICounterRecord} containing total number of each *node type* ({@link NodeTypeEnum}).'''
        ...

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> jsii.Number:
        '''Counts total number of stacks in the store.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="stages")
    def stages(self) -> jsii.Number:
        '''Counts total number of stages in the store.'''
        ...


class _IStoreCountsProxy:
    '''Interface for store counts.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.IStoreCounts"

    @builtins.property
    @jsii.member(jsii_name="cfnResources")
    def cfn_resources(self) -> typing.Mapping[builtins.str, jsii.Number]:
        '''Returns {@link ICounterRecord} containing total number of each *cfnResourceType*.'''
        return typing.cast(typing.Mapping[builtins.str, jsii.Number], jsii.get(self, "cfnResources"))

    @builtins.property
    @jsii.member(jsii_name="edges")
    def edges(self) -> jsii.Number:
        '''Counts total number of edges in the store.'''
        return typing.cast(jsii.Number, jsii.get(self, "edges"))

    @builtins.property
    @jsii.member(jsii_name="edgeTypes")
    def edge_types(self) -> typing.Mapping[builtins.str, jsii.Number]:
        '''Returns {@link ICounterRecord} containing total number of each *edge type* ({@link EdgeTypeEnum}).'''
        return typing.cast(typing.Mapping[builtins.str, jsii.Number], jsii.get(self, "edgeTypes"))

    @builtins.property
    @jsii.member(jsii_name="nodes")
    def nodes(self) -> jsii.Number:
        '''Counts total number of nodes in the store.'''
        return typing.cast(jsii.Number, jsii.get(self, "nodes"))

    @builtins.property
    @jsii.member(jsii_name="nodeTypes")
    def node_types(self) -> typing.Mapping[builtins.str, jsii.Number]:
        '''Returns {@link ICounterRecord} containing total number of each *node type* ({@link NodeTypeEnum}).'''
        return typing.cast(typing.Mapping[builtins.str, jsii.Number], jsii.get(self, "nodeTypes"))

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> jsii.Number:
        '''Counts total number of stacks in the store.'''
        return typing.cast(jsii.Number, jsii.get(self, "stacks"))

    @builtins.property
    @jsii.member(jsii_name="stages")
    def stages(self) -> jsii.Number:
        '''Counts total number of stages in the store.'''
        return typing.cast(jsii.Number, jsii.get(self, "stages"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IStoreCounts).__jsii_proxy_class__ = lambda : _IStoreCountsProxy


@jsii.interface(jsii_type="aws-pdk.cdk_graph.ITypedEdgeProps")
class ITypedEdgeProps(IBaseEntityProps, typing_extensions.Protocol):
    '''Base edge props agnostic to edge type.

    Used for extending per edge class with type specifics.
    '''

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "Node":
        '''Edge **source** is the node that defines the edge (tail).'''
        ...

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "Node":
        '''Edge **target** is the node being referenced by the **source** (head).'''
        ...


class _ITypedEdgePropsProxy(
    jsii.proxy_for(IBaseEntityProps), # type: ignore[misc]
):
    '''Base edge props agnostic to edge type.

    Used for extending per edge class with type specifics.
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.ITypedEdgeProps"

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "Node":
        '''Edge **source** is the node that defines the edge (tail).'''
        return typing.cast("Node", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "Node":
        '''Edge **target** is the node being referenced by the **source** (head).'''
        return typing.cast("Node", jsii.get(self, "target"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITypedEdgeProps).__jsii_proxy_class__ = lambda : _ITypedEdgePropsProxy


@jsii.interface(jsii_type="aws-pdk.cdk_graph.ITypedNodeProps")
class ITypedNodeProps(IBaseEntityProps, typing_extensions.Protocol):
    '''Base node props agnostic to node type.

    Used for extending per node class with type specifics.
    '''

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''Node id, which is unique within parent scope.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        '''Path of the node.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="cfnType")
    def cfn_type(self) -> typing.Optional[builtins.str]:
        '''Type of CloudFormation resource.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="constructInfo")
    def construct_info(self) -> typing.Optional[ConstructInfo]:
        '''Synthesized construct information defining jii resolution data.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="logicalId")
    def logical_id(self) -> typing.Optional[builtins.str]:
        '''Logical id of the node, which is only unique within containing stack.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> typing.Optional["Node"]:
        '''Parent node.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> typing.Optional["StackNode"]:
        '''Stack the node is contained.'''
        ...


class _ITypedNodePropsProxy(
    jsii.proxy_for(IBaseEntityProps), # type: ignore[misc]
):
    '''Base node props agnostic to node type.

    Used for extending per node class with type specifics.
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.ITypedNodeProps"

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''Node id, which is unique within parent scope.'''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        '''Path of the node.'''
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="cfnType")
    def cfn_type(self) -> typing.Optional[builtins.str]:
        '''Type of CloudFormation resource.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cfnType"))

    @builtins.property
    @jsii.member(jsii_name="constructInfo")
    def construct_info(self) -> typing.Optional[ConstructInfo]:
        '''Synthesized construct information defining jii resolution data.'''
        return typing.cast(typing.Optional[ConstructInfo], jsii.get(self, "constructInfo"))

    @builtins.property
    @jsii.member(jsii_name="logicalId")
    def logical_id(self) -> typing.Optional[builtins.str]:
        '''Logical id of the node, which is only unique within containing stack.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logicalId"))

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> typing.Optional["Node"]:
        '''Parent node.'''
        return typing.cast(typing.Optional["Node"], jsii.get(self, "parent"))

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> typing.Optional["StackNode"]:
        '''Stack the node is contained.'''
        return typing.cast(typing.Optional["StackNode"], jsii.get(self, "stack"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITypedNodeProps).__jsii_proxy_class__ = lambda : _ITypedNodePropsProxy


@jsii.enum(jsii_type="aws-pdk.cdk_graph.MetadataTypeEnum")
class MetadataTypeEnum(enum.Enum):
    '''Common cdk metadata types.'''

    LOGICAL_ID = "LOGICAL_ID"


@jsii.enum(jsii_type="aws-pdk.cdk_graph.NodeTypeEnum")
class NodeTypeEnum(enum.Enum):
    '''Node types handled by the graph.'''

    DEFAULT = "DEFAULT"
    '''Default node type - used for all nodes that don't have explicit type defined.'''
    CFN_RESOURCE = "CFN_RESOURCE"
    '''L1 cfn resource node.'''
    RESOURCE = "RESOURCE"
    '''L2 cdk resource node.'''
    CUSTOM_RESOURCE = "CUSTOM_RESOURCE"
    '''Cdk customer resource node.'''
    ROOT = "ROOT"
    '''Graph root node.'''
    APP = "APP"
    '''Cdk App node.'''
    STAGE = "STAGE"
    '''Cdk Stage node.'''
    STACK = "STACK"
    '''Cdk Stack node.'''
    NESTED_STACK = "NESTED_STACK"
    '''Cdk NestedStack node.'''
    OUTPUT = "OUTPUT"
    '''CfnOutput node.'''
    PARAMETER = "PARAMETER"
    '''CfnParameter node.'''
    ASSET = "ASSET"
    '''Cdk asset node.'''


@jsii.data_type(
    jsii_type="aws-pdk.cdk_graph.PlainObject",
    jsii_struct_bases=[],
    name_mapping={},
)
class PlainObject:
    def __init__(self) -> None:
        '''Serializable plain object value (JSII supported).'''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PlainObject(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-pdk.cdk_graph.ReferenceTypeEnum")
class ReferenceTypeEnum(enum.Enum):
    '''Reference edge types.'''

    REF = "REF"
    '''CloudFormation **Ref** reference.'''
    ATTRIBUTE = "ATTRIBUTE"
    '''CloudFormation **Fn::GetAtt** reference.'''
    IMPORT = "IMPORT"
    '''CloudFormation **Fn::ImportValue** reference.'''
    IMPORT_ARN = "IMPORT_ARN"
    '''CloudFormation **Fn::Join** reference of imported resourced (eg: ``s3.Bucket.fromBucketArn()``).'''


@jsii.data_type(
    jsii_type="aws-pdk.cdk_graph.SGEntity",
    jsii_struct_bases=[],
    name_mapping={
        "uuid": "uuid",
        "attributes": "attributes",
        "flags": "flags",
        "metadata": "metadata",
        "tags": "tags",
    },
)
class SGEntity:
    def __init__(
        self,
        *,
        uuid: builtins.str,
        attributes: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]]] = None,
        flags: typing.Optional[typing.Sequence[FlagEnum]] = None,
        metadata: typing.Optional[typing.Sequence[typing.Union[_constructs_77d1e7e8.MetadataEntry, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Serializable graph entity.

        :param uuid: Universally unique identity.
        :param attributes: Serializable entity attributes.
        :param flags: Serializable entity flags.
        :param metadata: Serializable entity metadata.
        :param tags: Serializable entity tags.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c4298dbc4d14316130bfb52fe6d8e564a020dfe8b99ce11a210e9bb9c552173)
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument flags", value=flags, expected_type=type_hints["flags"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uuid": uuid,
        }
        if attributes is not None:
            self._values["attributes"] = attributes
        if flags is not None:
            self._values["flags"] = flags
        if metadata is not None:
            self._values["metadata"] = metadata
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def uuid(self) -> builtins.str:
        '''Universally unique identity.'''
        result = self._values.get("uuid")
        assert result is not None, "Required property 'uuid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]]:
        '''Serializable entity attributes.

        :see: {@link Attributes }
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]], result)

    @builtins.property
    def flags(self) -> typing.Optional[typing.List[FlagEnum]]:
        '''Serializable entity flags.

        :see: {@link FlagEnum }
        '''
        result = self._values.get("flags")
        return typing.cast(typing.Optional[typing.List[FlagEnum]], result)

    @builtins.property
    def metadata(
        self,
    ) -> typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]]:
        '''Serializable entity metadata.

        :see: {@link Metadata }
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Serializable entity tags.

        :see: {@link Tags }
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SGEntity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-pdk.cdk_graph.SGGraphStore",
    jsii_struct_bases=[],
    name_mapping={"edges": "edges", "tree": "tree", "version": "version"},
)
class SGGraphStore:
    def __init__(
        self,
        *,
        edges: typing.Sequence[typing.Union["SGEdge", typing.Dict[builtins.str, typing.Any]]],
        tree: typing.Union["SGNode", typing.Dict[builtins.str, typing.Any]],
        version: builtins.str,
    ) -> None:
        '''Serializable graph store.

        :param edges: List of edges.
        :param tree: Node tree.
        :param version: Store version.
        '''
        if isinstance(tree, dict):
            tree = SGNode(**tree)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34a52c739dad71eb3b97fd79836a41dbfb17d6e665d15dc52ab667582094ffae)
            check_type(argname="argument edges", value=edges, expected_type=type_hints["edges"])
            check_type(argname="argument tree", value=tree, expected_type=type_hints["tree"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "edges": edges,
            "tree": tree,
            "version": version,
        }

    @builtins.property
    def edges(self) -> typing.List["SGEdge"]:
        '''List of edges.'''
        result = self._values.get("edges")
        assert result is not None, "Required property 'edges' is missing"
        return typing.cast(typing.List["SGEdge"], result)

    @builtins.property
    def tree(self) -> "SGNode":
        '''Node tree.'''
        result = self._values.get("tree")
        assert result is not None, "Required property 'tree' is missing"
        return typing.cast("SGNode", result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Store version.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SGGraphStore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-pdk.cdk_graph.SGNode",
    jsii_struct_bases=[SGEntity],
    name_mapping={
        "uuid": "uuid",
        "attributes": "attributes",
        "flags": "flags",
        "metadata": "metadata",
        "tags": "tags",
        "id": "id",
        "node_type": "nodeType",
        "path": "path",
        "cfn_type": "cfnType",
        "children": "children",
        "construct_info": "constructInfo",
        "edges": "edges",
        "logical_id": "logicalId",
        "parent": "parent",
        "stack": "stack",
    },
)
class SGNode(SGEntity):
    def __init__(
        self,
        *,
        uuid: builtins.str,
        attributes: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]]] = None,
        flags: typing.Optional[typing.Sequence[FlagEnum]] = None,
        metadata: typing.Optional[typing.Sequence[typing.Union[_constructs_77d1e7e8.MetadataEntry, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: builtins.str,
        node_type: NodeTypeEnum,
        path: builtins.str,
        cfn_type: typing.Optional[builtins.str] = None,
        children: typing.Optional[typing.Mapping[builtins.str, typing.Union["SGNode", typing.Dict[builtins.str, typing.Any]]]] = None,
        construct_info: typing.Optional[typing.Union[ConstructInfo, typing.Dict[builtins.str, typing.Any]]] = None,
        edges: typing.Optional[typing.Sequence[builtins.str]] = None,
        logical_id: typing.Optional[builtins.str] = None,
        parent: typing.Optional[builtins.str] = None,
        stack: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Serializable graph node entity.

        :param uuid: Universally unique identity.
        :param attributes: Serializable entity attributes.
        :param flags: Serializable entity flags.
        :param metadata: Serializable entity metadata.
        :param tags: Serializable entity tags.
        :param id: Node id within parent (unique only between parent child nodes).
        :param node_type: Node type.
        :param path: Node path.
        :param cfn_type: CloudFormation resource type for this node.
        :param children: Child node record.
        :param construct_info: Synthesized construct information defining jii resolution data.
        :param edges: List of edge UUIDs where this node is the **source**.
        :param logical_id: Logical id of the node, which is only unique within containing stack.
        :param parent: UUID of node parent.
        :param stack: UUID of node stack.
        '''
        if isinstance(construct_info, dict):
            construct_info = ConstructInfo(**construct_info)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d435ebf5b1908bfd33e7828e8120584949ceff2333073d1ffcfc51a86ef85dd4)
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument flags", value=flags, expected_type=type_hints["flags"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument node_type", value=node_type, expected_type=type_hints["node_type"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument cfn_type", value=cfn_type, expected_type=type_hints["cfn_type"])
            check_type(argname="argument children", value=children, expected_type=type_hints["children"])
            check_type(argname="argument construct_info", value=construct_info, expected_type=type_hints["construct_info"])
            check_type(argname="argument edges", value=edges, expected_type=type_hints["edges"])
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uuid": uuid,
            "id": id,
            "node_type": node_type,
            "path": path,
        }
        if attributes is not None:
            self._values["attributes"] = attributes
        if flags is not None:
            self._values["flags"] = flags
        if metadata is not None:
            self._values["metadata"] = metadata
        if tags is not None:
            self._values["tags"] = tags
        if cfn_type is not None:
            self._values["cfn_type"] = cfn_type
        if children is not None:
            self._values["children"] = children
        if construct_info is not None:
            self._values["construct_info"] = construct_info
        if edges is not None:
            self._values["edges"] = edges
        if logical_id is not None:
            self._values["logical_id"] = logical_id
        if parent is not None:
            self._values["parent"] = parent
        if stack is not None:
            self._values["stack"] = stack

    @builtins.property
    def uuid(self) -> builtins.str:
        '''Universally unique identity.'''
        result = self._values.get("uuid")
        assert result is not None, "Required property 'uuid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]]:
        '''Serializable entity attributes.

        :see: {@link Attributes }
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]], result)

    @builtins.property
    def flags(self) -> typing.Optional[typing.List[FlagEnum]]:
        '''Serializable entity flags.

        :see: {@link FlagEnum }
        '''
        result = self._values.get("flags")
        return typing.cast(typing.Optional[typing.List[FlagEnum]], result)

    @builtins.property
    def metadata(
        self,
    ) -> typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]]:
        '''Serializable entity metadata.

        :see: {@link Metadata }
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Serializable entity tags.

        :see: {@link Tags }
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def id(self) -> builtins.str:
        '''Node id within parent (unique only between parent child nodes).'''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_type(self) -> NodeTypeEnum:
        '''Node type.'''
        result = self._values.get("node_type")
        assert result is not None, "Required property 'node_type' is missing"
        return typing.cast(NodeTypeEnum, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''Node path.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cfn_type(self) -> typing.Optional[builtins.str]:
        '''CloudFormation resource type for this node.'''
        result = self._values.get("cfn_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def children(self) -> typing.Optional[typing.Mapping[builtins.str, "SGNode"]]:
        '''Child node record.'''
        result = self._values.get("children")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "SGNode"]], result)

    @builtins.property
    def construct_info(self) -> typing.Optional[ConstructInfo]:
        '''Synthesized construct information defining jii resolution data.'''
        result = self._values.get("construct_info")
        return typing.cast(typing.Optional[ConstructInfo], result)

    @builtins.property
    def edges(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of edge UUIDs where this node is the **source**.'''
        result = self._values.get("edges")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def logical_id(self) -> typing.Optional[builtins.str]:
        '''Logical id of the node, which is only unique within containing stack.'''
        result = self._values.get("logical_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent(self) -> typing.Optional[builtins.str]:
        '''UUID of node parent.'''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stack(self) -> typing.Optional[builtins.str]:
        '''UUID of node stack.'''
        result = self._values.get("stack")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SGNode(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-pdk.cdk_graph.SGUnresolvedReference",
    jsii_struct_bases=[],
    name_mapping={
        "reference_type": "referenceType",
        "source": "source",
        "target": "target",
        "value": "value",
    },
)
class SGUnresolvedReference:
    def __init__(
        self,
        *,
        reference_type: ReferenceTypeEnum,
        source: builtins.str,
        target: builtins.str,
        value: typing.Optional[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Unresolved reference struct.

        During graph computation references are unresolved and stored in this struct.

        :param reference_type: 
        :param source: 
        :param target: 
        :param value: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aa3d2ca6809903d0c1c1007c08a3af3aa7c7b0d99bfe4ddd6b7fecde5920a22)
            check_type(argname="argument reference_type", value=reference_type, expected_type=type_hints["reference_type"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "reference_type": reference_type,
            "source": source,
            "target": target,
        }
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def reference_type(self) -> ReferenceTypeEnum:
        result = self._values.get("reference_type")
        assert result is not None, "Required property 'reference_type' is missing"
        return typing.cast(ReferenceTypeEnum, result)

    @builtins.property
    def source(self) -> builtins.str:
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]:
        result = self._values.get("value")
        return typing.cast(typing.Optional[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SGUnresolvedReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ISerializableGraphStore)
class Store(metaclass=jsii.JSIIMeta, jsii_type="aws-pdk.cdk_graph.Store"):
    '''Store class provides the in-memory database-like interface for managing all entities in the graph.'''

    def __init__(
        self,
        allow_destructive_mutations: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param allow_destructive_mutations: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c45d72e0054b126e56496c4ce2a10ee06961c134ccbf0faecfb2f64d5d156523)
            check_type(argname="argument allow_destructive_mutations", value=allow_destructive_mutations, expected_type=type_hints["allow_destructive_mutations"])
        jsii.create(self.__class__, self, [allow_destructive_mutations])

    @jsii.member(jsii_name="fromSerializedStore")
    @builtins.classmethod
    def from_serialized_store(
        cls,
        *,
        edges: typing.Sequence[typing.Union["SGEdge", typing.Dict[builtins.str, typing.Any]]],
        tree: typing.Union[SGNode, typing.Dict[builtins.str, typing.Any]],
        version: builtins.str,
    ) -> "Store":
        '''Builds store from serialized store data.

        :param edges: List of edges.
        :param tree: Node tree.
        :param version: Store version.
        '''
        serialized_store = SGGraphStore(edges=edges, tree=tree, version=version)

        return typing.cast("Store", jsii.sinvoke(cls, "fromSerializedStore", [serialized_store]))

    @jsii.member(jsii_name="addEdge")
    def add_edge(self, edge: "Edge") -> None:
        '''Add **edge** to the store.

        :param edge: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__335c616a8314affc9fe4b7086b907b674a8da8b27da8d2f63a766b87dcffde22)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(None, jsii.invoke(self, "addEdge", [edge]))

    @jsii.member(jsii_name="addNode")
    def add_node(self, node: "Node") -> None:
        '''Add **node** to the store.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa1a099a580cbeb023b54267c1b9878d7f478c99bb20555bf165780237d8a619)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "addNode", [node]))

    @jsii.member(jsii_name="addStack")
    def add_stack(self, stack: "StackNode") -> None:
        '''Add **stack** node to the store.

        :param stack: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__588ba0c5a3a0dac34251b68e97e9c44c67932aac318a97061378db2f1d23c965)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(None, jsii.invoke(self, "addStack", [stack]))

    @jsii.member(jsii_name="addStage")
    def add_stage(self, stage: "StageNode") -> None:
        '''Add **stage** to the store.

        :param stage: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb7569264399acfbfb90d5aa050eeff17baed229adae68b4dcf2ac2d71e522a6)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        return typing.cast(None, jsii.invoke(self, "addStage", [stage]))

    @jsii.member(jsii_name="clone")
    def clone(
        self,
        allow_destructive_mutations: typing.Optional[builtins.bool] = None,
    ) -> "Store":
        '''Clone the store to allow destructive mutations.

        :param allow_destructive_mutations: Indicates if destructive mutations are allowed; defaults to ``true``

        :return: Returns a clone of the store that allows destructive mutations
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed18acd48a1a5beb1bb89d3eee9d8f0a0285253129176d9fcbc2b25516eddbe3)
            check_type(argname="argument allow_destructive_mutations", value=allow_destructive_mutations, expected_type=type_hints["allow_destructive_mutations"])
        return typing.cast("Store", jsii.invoke(self, "clone", [allow_destructive_mutations]))

    @jsii.member(jsii_name="computeLogicalUniversalId")
    def compute_logical_universal_id(
        self,
        stack: "StackNode",
        logical_id: builtins.str,
    ) -> builtins.str:
        '''Compute **universal** *logicalId* based on parent stack and construct *logicalId* (``<stack>:<logicalId>``).

        Construct *logicalIds are only unique within their containing stack, so to use *logicalId*
        lookups universally (like resolving references) we need a universal key.

        :param stack: -
        :param logical_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0ea44fc5d181e0cf068fa4129788a74ff74367b6d4f463978405b6d267b7d87)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
        return typing.cast(builtins.str, jsii.invoke(self, "computeLogicalUniversalId", [stack, logical_id]))

    @jsii.member(jsii_name="findNodeByImportArn")
    def find_node_by_import_arn(self, value: typing.Any) -> typing.Optional["Node"]:
        '''Attempts to lookup the {@link Node} associated with a given *import arn token*.

        :param value: Import arn value, which is either object to tokenize or already tokenized string.

        :return: Returns matching {@link Node } if found, otherwise undefined.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__582eed54711f17977a95af99dbe2108fbf969bcf9385fffc44f1677b386ace2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(typing.Optional["Node"], jsii.invoke(self, "findNodeByImportArn", [value]))

    @jsii.member(jsii_name="findNodeByLogicalId")
    def find_node_by_logical_id(
        self,
        stack: "StackNode",
        logical_id: builtins.str,
    ) -> "Node":
        '''Find node within given **stack** with given *logicalId*.

        :param stack: -
        :param logical_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec309c80416841f360acb7624800ed5cdddedec2dd6c57f30a8317d67d0b4cd2)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
        return typing.cast("Node", jsii.invoke(self, "findNodeByLogicalId", [stack, logical_id]))

    @jsii.member(jsii_name="findNodeByLogicalUniversalId")
    def find_node_by_logical_universal_id(self, uid: builtins.str) -> "Node":
        '''Find node by **universal** *logicalId* (``<stack>:<logicalId>``).

        :param uid: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e37ae0302916f9100547ab1f26b6ceedf23ba65bc23b3f2b7653559479191544)
            check_type(argname="argument uid", value=uid, expected_type=type_hints["uid"])
        return typing.cast("Node", jsii.invoke(self, "findNodeByLogicalUniversalId", [uid]))

    @jsii.member(jsii_name="getEdge")
    def get_edge(self, uuid: builtins.str) -> "Edge":
        '''Get stored **edge** by UUID.

        :param uuid: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98bb3d9a7f041be77d073f12f70b7408b4b8fa058939343f6b01b1b2c5074316)
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
        return typing.cast("Edge", jsii.invoke(self, "getEdge", [uuid]))

    @jsii.member(jsii_name="getNode")
    def get_node(self, uuid: builtins.str) -> "Node":
        '''Get stored **node** by UUID.

        :param uuid: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a9df12223d11a345cbcb9cb57a082c1ef151d6f3f2fd59b572f58b3b5612a32)
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
        return typing.cast("Node", jsii.invoke(self, "getNode", [uuid]))

    @jsii.member(jsii_name="getStack")
    def get_stack(self, uuid: builtins.str) -> "StackNode":
        '''Get stored **stack** node by UUID.

        :param uuid: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31fb4e2eff7befd95a27ebc6715d47be47b3550641a63c2a3d60d5ced1760df8)
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
        return typing.cast("StackNode", jsii.invoke(self, "getStack", [uuid]))

    @jsii.member(jsii_name="getStage")
    def get_stage(self, uuid: builtins.str) -> "StageNode":
        '''Get stored **stage** node by UUID.

        :param uuid: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcf168d106c59be24c47311b2428c41642e7c2c969148c39596ac1ab07b945f4)
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
        return typing.cast("StageNode", jsii.invoke(self, "getStage", [uuid]))

    @jsii.member(jsii_name="mutateRemoveEdge")
    def mutate_remove_edge(self, edge: "Edge") -> builtins.bool:
        '''Remove **edge** from the store.

        :param edge: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f520ec94ffdd0afa2ce964d73a479ea7130635d3bc90e7d70366b068b725afb)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveEdge", [edge]))

    @jsii.member(jsii_name="mutateRemoveNode")
    def mutate_remove_node(self, node: "Node") -> builtins.bool:
        '''Remove **node** from the store.

        :param node: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ec35cd5062bb3b84eba76df1785554984bfef15367cf3af5a9f9765f9b9c80d)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveNode", [node]))

    @jsii.member(jsii_name="recordImportArn")
    def record_import_arn(self, arn_token: builtins.str, resource: "Node") -> None:
        '''Records arn tokens from imported resources (eg: ``s3.Bucket.fromBucketArn()``) that are used for resolving references.

        :param arn_token: -
        :param resource: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4555fcf416c414465d91a9a0b679ed2f5cca937866e3b6cbe6c2067a93d2b682)
            check_type(argname="argument arn_token", value=arn_token, expected_type=type_hints["arn_token"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(None, jsii.invoke(self, "recordImportArn", [arn_token, resource]))

    @jsii.member(jsii_name="recordLogicalId")
    def record_logical_id(
        self,
        stack: "StackNode",
        logical_id: builtins.str,
        resource: "Node",
    ) -> None:
        '''Record a **universal** *logicalId* to node mapping in the store.

        :param stack: -
        :param logical_id: -
        :param resource: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8580bf6d78ed80f02af00ee71fda2b1988ed2847a318f3320d727cd7de2e54a)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(None, jsii.invoke(self, "recordLogicalId", [stack, logical_id, resource]))

    @jsii.member(jsii_name="serialize")
    def serialize(self) -> SGGraphStore:
        '''Serialize the store.'''
        return typing.cast(SGGraphStore, jsii.invoke(self, "serialize", []))

    @jsii.member(jsii_name="verifyDestructiveMutationAllowed")
    def verify_destructive_mutation_allowed(self) -> None:
        '''Verifies that the store allows destructive mutations.

        :throws: Error is store does **not** allow mutations
        '''
        return typing.cast(None, jsii.invoke(self, "verifyDestructiveMutationAllowed", []))

    @builtins.property
    @jsii.member(jsii_name="allowDestructiveMutations")
    def allow_destructive_mutations(self) -> builtins.bool:
        '''Indicates if the store allows destructive mutations.

        Destructive mutations are only allowed on clones of the store to prevent plugins and filters from
        mutating the store for downstream plugins.

        All ``mutate*`` methods are only allowed on stores that allow destructive mutations.

        This behavior may change in the future if the need arises for plugins to pass mutated stores
        to downstream plugins. But it will be done cautiously with ensuring the intent of
        downstream plugin is to receive the mutated store.
        '''
        return typing.cast(builtins.bool, jsii.get(self, "allowDestructiveMutations"))

    @builtins.property
    @jsii.member(jsii_name="counts")
    def counts(self) -> IStoreCounts:
        '''Get record of all store counters.'''
        return typing.cast(IStoreCounts, jsii.get(self, "counts"))

    @builtins.property
    @jsii.member(jsii_name="edges")
    def edges(self) -> typing.List["Edge"]:
        '''Gets all stored **edges**.

        :type: ReadonlyArray
        '''
        return typing.cast(typing.List["Edge"], jsii.get(self, "edges"))

    @builtins.property
    @jsii.member(jsii_name="nodes")
    def nodes(self) -> typing.List["Node"]:
        '''Gets all stored **nodes**.

        :type: ReadonlyArray
        '''
        return typing.cast(typing.List["Node"], jsii.get(self, "nodes"))

    @builtins.property
    @jsii.member(jsii_name="root")
    def root(self) -> "RootNode":
        '''Root node in the store.

        The **root** node is not the computed root, but the graph root
        which is auto-generated and can not be mutated.
        '''
        return typing.cast("RootNode", jsii.get(self, "root"))

    @builtins.property
    @jsii.member(jsii_name="rootStacks")
    def root_stacks(self) -> typing.List["StackNode"]:
        '''Gets all stored **root stack** nodes.

        :type: ReadonlyArray
        '''
        return typing.cast(typing.List["StackNode"], jsii.get(self, "rootStacks"))

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List["StackNode"]:
        '''Gets all stored **stack** nodes.

        :type: ReadonlyArray
        '''
        return typing.cast(typing.List["StackNode"], jsii.get(self, "stacks"))

    @builtins.property
    @jsii.member(jsii_name="stages")
    def stages(self) -> typing.List["StageNode"]:
        '''Gets all stored **stage** nodes.

        :type: ReadonlyArray
        '''
        return typing.cast(typing.List["StageNode"], jsii.get(self, "stages"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''Current SemVer version of the store.'''
        return typing.cast(builtins.str, jsii.get(self, "version"))


@jsii.implements(ISerializableEntity)
class BaseEntity(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="aws-pdk.cdk_graph.BaseEntity",
):
    '''Base class for all store entities (Node and Edges).'''

    def __init__(self, props: IBaseEntityProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66b940bd9a4a4c2d38a71391c1d42165194cc345bb0824366700599aae6db3e1)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="addAttribute")
    def add_attribute(self, key: builtins.str, value: typing.Any) -> None:
        '''Add attribute.

        :param key: -
        :param value: -

        :throws: Error if attribute for key already exists
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b1c4c627b858975af0e5487ad5e1acc512ce053447f149f2a167c14443a359c)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addAttribute", [key, value]))

    @jsii.member(jsii_name="addFlag")
    def add_flag(self, flag: FlagEnum) -> None:
        '''Add flag.

        :param flag: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49650010b6731e36ec20882aec595ef28b66f6840da8cfcb86ea68423c55fb0e)
            check_type(argname="argument flag", value=flag, expected_type=type_hints["flag"])
        return typing.cast(None, jsii.invoke(self, "addFlag", [flag]))

    @jsii.member(jsii_name="addMetadata")
    def add_metadata(self, metadata_type: builtins.str, data: typing.Any) -> None:
        '''Add metadata entry.

        :param metadata_type: -
        :param data: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18c27ec4f07f61e9a6c86f2f37905e3c29b62e16547c0c9626e9cfa1e1edd8aa)
            check_type(argname="argument metadata_type", value=metadata_type, expected_type=type_hints["metadata_type"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        return typing.cast(None, jsii.invoke(self, "addMetadata", [metadata_type, data]))

    @jsii.member(jsii_name="addTag")
    def add_tag(self, key: builtins.str, value: builtins.str) -> None:
        '''Add tag.

        :param key: -
        :param value: -

        :throws: Throws Error is tag for key already exists
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02a58d59b46c96be9085ed903fa96d25a78036d69b02b701bebc8e424970dc36)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addTag", [key, value]))

    @jsii.member(jsii_name="applyData")
    def apply_data(
        self,
        data: IBaseEntityDataProps,
        overwrite: typing.Optional[builtins.bool] = None,
        apply_flags: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Applies data (attributes, metadata, tags, flag) to entity.

        Generally used only for mutations such as collapse and consume to retain data.

        :param data: - The data to apply.
        :param overwrite: -
        :param apply_flags: - Indicates if data is overwritten - Indicates if flags should be applied.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f76c419e91f82c7f73ec1de78a72e72fca4fe5de6ab303fdec9954eaa54a29b)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument overwrite", value=overwrite, expected_type=type_hints["overwrite"])
            check_type(argname="argument apply_flags", value=apply_flags, expected_type=type_hints["apply_flags"])
        return typing.cast(None, jsii.invoke(self, "applyData", [data, overwrite, apply_flags]))

    @jsii.member(jsii_name="findMetadata")
    def find_metadata(
        self,
        metadata_type: builtins.str,
    ) -> typing.List[_constructs_77d1e7e8.MetadataEntry]:
        '''Retrieves all metadata entries of a given type.

        :param metadata_type: -

        :type: Readonly<SerializedGraph.Metadata>
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__778d54204d04976cbf2decdd42cdc6b13714d26edd6fd4b74fc70164d0158bdf)
            check_type(argname="argument metadata_type", value=metadata_type, expected_type=type_hints["metadata_type"])
        return typing.cast(typing.List[_constructs_77d1e7e8.MetadataEntry], jsii.invoke(self, "findMetadata", [metadata_type]))

    @jsii.member(jsii_name="getAttribute")
    def get_attribute(self, key: builtins.str) -> typing.Any:
        '''Get attribute by key.

        :param key: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b9e505ed524dbf121193f8044949f9e28ee8641817667e03e7084dfe003ad13)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(typing.Any, jsii.invoke(self, "getAttribute", [key]))

    @jsii.member(jsii_name="getTag")
    def get_tag(self, key: builtins.str) -> typing.Optional[builtins.str]:
        '''Get tag by key.

        :param key: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64987e8e7e28f42c60371e62806aa0197ee7cd9a02af8c3327d1a3cb1c8f20d3)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "getTag", [key]))

    @jsii.member(jsii_name="hasAttribute")
    def has_attribute(
        self,
        key: builtins.str,
        value: typing.Any = None,
    ) -> builtins.bool:
        '''Indicates if entity has a given attribute defined, and optionally with a specific value.

        :param key: -
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4af255296cac152f625d15dd62ab4c241ce5fc919bd994a038e78cb5947c9bae)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.bool, jsii.invoke(self, "hasAttribute", [key, value]))

    @jsii.member(jsii_name="hasFlag")
    def has_flag(self, flag: FlagEnum) -> builtins.bool:
        '''Indicates if entity has a given flag.

        :param flag: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6be01caa1b4b8b4e3d74fc44cbe6cc4c197a9e89b837b14fec578250b0ab0519)
            check_type(argname="argument flag", value=flag, expected_type=type_hints["flag"])
        return typing.cast(builtins.bool, jsii.invoke(self, "hasFlag", [flag]))

    @jsii.member(jsii_name="hasMetadata")
    def has_metadata(
        self,
        metadata_type: builtins.str,
        data: typing.Any,
    ) -> builtins.bool:
        '''Indicates if entity has matching metadata entry.

        :param metadata_type: -
        :param data: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77b017330c657e60671de0a279b75114d7fe3ab2420a36da7d33bcc8b7829c6d)
            check_type(argname="argument metadata_type", value=metadata_type, expected_type=type_hints["metadata_type"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        return typing.cast(builtins.bool, jsii.invoke(self, "hasMetadata", [metadata_type, data]))

    @jsii.member(jsii_name="hasTag")
    def has_tag(
        self,
        key: builtins.str,
        value: typing.Optional[builtins.str] = None,
    ) -> builtins.bool:
        '''Indicates if entity has tag, optionally verifying tag value.

        :param key: -
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a66cabe9a9fdf3171e68dfe81dfe7ec7f026ad9a63f45ff970771501fa193fbb)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.bool, jsii.invoke(self, "hasTag", [key, value]))

    @jsii.member(jsii_name="mutateDestroy")
    @abc.abstractmethod
    def mutate_destroy(self, strict: typing.Optional[builtins.bool] = None) -> None:
        '''Destroy the entity be removing all references and removing from store.

        :param strict: - If ``strict``, then entity must not have any references remaining when attempting to destroy.

        :destructive: true
        '''
        ...

    @jsii.member(jsii_name="setAttribute")
    def set_attribute(self, key: builtins.str, value: typing.Any) -> None:
        '''Set attribute.

        This will overwrite existing attribute.

        :param key: -
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__247b9f93aba2c1ac53d20f2c7a52841da482b5ddcbb73e6a22b5f6ef671e3a2d)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "setAttribute", [key, value]))

    @jsii.member(jsii_name="setTag")
    def set_tag(self, key: builtins.str, value: builtins.str) -> None:
        '''Set tag.

        Will overwrite existing tag.

        :param key: -
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__debfcb941751c761cb39b0745cb3cff09acdf97df6b8257c6edd9ce3515254dc)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "setTag", [key, value]))

    @builtins.property
    @jsii.member(jsii_name="attributes")
    def attributes(
        self,
    ) -> typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]:
        '''Get *readonly* record of all attributes.

        :type: Readonly<SerializedGraph.Attributes>
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]], jsii.get(self, "attributes"))

    @builtins.property
    @jsii.member(jsii_name="flags")
    def flags(self) -> typing.List[FlagEnum]:
        '''Get *readonly* list of all flags.

        :type: ReadonlyArray
        '''
        return typing.cast(typing.List[FlagEnum], jsii.get(self, "flags"))

    @builtins.property
    @jsii.member(jsii_name="isDestroyed")
    def is_destroyed(self) -> builtins.bool:
        '''Indicates if the entity has been destroyed (eg: removed from store).'''
        return typing.cast(builtins.bool, jsii.get(self, "isDestroyed"))

    @builtins.property
    @jsii.member(jsii_name="isMutated")
    def is_mutated(self) -> builtins.bool:
        '''Indicates if the entity has had destructive mutations applied.'''
        return typing.cast(builtins.bool, jsii.get(self, "isMutated"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> typing.List[_constructs_77d1e7e8.MetadataEntry]:
        '''Get *readonly* list of all metadata entries.

        :type: Readonly<SerializedGraph.Metadata>
        '''
        return typing.cast(typing.List[_constructs_77d1e7e8.MetadataEntry], jsii.get(self, "metadata"))

    @builtins.property
    @jsii.member(jsii_name="store")
    def store(self) -> Store:
        '''Reference to the store.'''
        return typing.cast(Store, jsii.get(self, "store"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''Get *readonly* record of all tags.

        :type: Readonly<SerializedGraph.Tags>
        '''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="uuid")
    def uuid(self) -> builtins.str:
        '''Universally unique identifier.'''
        return typing.cast(builtins.str, jsii.get(self, "uuid"))


class _BaseEntityProxy(BaseEntity):
    @jsii.member(jsii_name="mutateDestroy")
    def mutate_destroy(self, strict: typing.Optional[builtins.bool] = None) -> None:
        '''Destroy the entity be removing all references and removing from store.

        :param strict: - If ``strict``, then entity must not have any references remaining when attempting to destroy.

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99ee3f72791f8a9a48462c55518e9749803916a029b9443c7170ddceb15b9d5c)
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
        return typing.cast(None, jsii.invoke(self, "mutateDestroy", [strict]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, BaseEntity).__jsii_proxy_class__ = lambda : _BaseEntityProxy


@jsii.implements(ISerializableEdge)
class Edge(BaseEntity, metaclass=jsii.JSIIMeta, jsii_type="aws-pdk.cdk_graph.Edge"):
    '''Edge class defines a link (relationship) between nodes, as in standard `graph theory <https://en.wikipedia.org/wiki/Graph_theory>`_.'''

    def __init__(self, props: "IEdgeProps") -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c923c62f7fba1f4e39d79d6fc22d32315d3a1533a31dfe82ea42349955f26253)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="findAllInChain")
    @builtins.classmethod
    def find_all_in_chain(
        cls,
        chain: typing.Sequence[typing.Any],
        predicate: IEdgePredicate,
    ) -> typing.List["Edge"]:
        '''Find all matching edges based on predicate within an EdgeChain.

        :param chain: -
        :param predicate: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41aa4c7fc4c2053cfa79e7e4048a16c8445adda20e2f1674f69dbaaca4c85a60)
            check_type(argname="argument chain", value=chain, expected_type=type_hints["chain"])
            check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
        return typing.cast(typing.List["Edge"], jsii.sinvoke(cls, "findAllInChain", [chain, predicate]))

    @jsii.member(jsii_name="findInChain")
    @builtins.classmethod
    def find_in_chain(
        cls,
        chain: typing.Sequence[typing.Any],
        predicate: IEdgePredicate,
    ) -> typing.Optional["Edge"]:
        '''Find first edge matching predicate within an EdgeChain.

        :param chain: -
        :param predicate: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8df4c980e3b05dd72ec3bdfd846ccc9f5ce648bdf083abf26da71bb79d157a73)
            check_type(argname="argument chain", value=chain, expected_type=type_hints["chain"])
            check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
        return typing.cast(typing.Optional["Edge"], jsii.sinvoke(cls, "findInChain", [chain, predicate]))

    @jsii.member(jsii_name="isEquivalent")
    def is_equivalent(self, edge: "Edge") -> builtins.bool:
        '''Indicates if this edge is equivalent to another edge.

        Edges are considered equivalent if they share same type, source, and target.

        :param edge: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae9ce2c39f795eb5043aa7e58c1c19469412ce091e346f78d50de410987f935d)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isEquivalent", [edge]))

    @jsii.member(jsii_name="mutateConsume")
    def mutate_consume(self, edge: "Edge") -> None:
        '''Merge an equivalent edge's data into this edge and destroy the other edge.

        Used during filtering operations to consolidate equivalent edges.

        :param edge: - The edge to consume.

        :destructive: true
        :throws: Error is edge is not *equivalent*
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2c577a6bd65d6a64d26ce8586979f63c6bd2853876f21b37ac7e128296bdfd7)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(None, jsii.invoke(self, "mutateConsume", [edge]))

    @jsii.member(jsii_name="mutateDestroy")
    def mutate_destroy(self, _strict: typing.Optional[builtins.bool] = None) -> None:
        '''Destroy the edge.

        Remove all references and remove from store.

        :param _strict: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6617bb51d2ca010bd03c333ffb5ce299f8d9139e9584ffd57d62d604a1f808f)
            check_type(argname="argument _strict", value=_strict, expected_type=type_hints["_strict"])
        return typing.cast(None, jsii.invoke(self, "mutateDestroy", [_strict]))

    @jsii.member(jsii_name="mutateDirection")
    def mutate_direction(self, direction: EdgeDirectionEnum) -> None:
        '''Change the edge **direction**.

        :param direction: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__153a587294604c6162e3494be66889c2f74337a568c0c304a0e9bbdf1278326a)
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
        return typing.cast(None, jsii.invoke(self, "mutateDirection", [direction]))

    @jsii.member(jsii_name="mutateSource")
    def mutate_source(self, node: "Node") -> None:
        '''Change the edge **source**.

        :param node: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ae65196193cf0a9355730fd93ac666a87554187ec519ded9d28790f2b7bdc0b)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "mutateSource", [node]))

    @jsii.member(jsii_name="mutateTarget")
    def mutate_target(self, node: "Node") -> None:
        '''Change the edge **target**.

        :param node: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e71af489fe71f57f9d69977b2d17497bd61be3099e05ad7b4fa2dfcac709ca3)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "mutateTarget", [node]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Get string representation of this edge.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="allowDestructiveMutations")
    def allow_destructive_mutations(self) -> builtins.bool:
        '''Indicates if edge allows destructive mutations.'''
        return typing.cast(builtins.bool, jsii.get(self, "allowDestructiveMutations"))

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> EdgeDirectionEnum:
        '''Indicates the direction in which the edge is directed.'''
        return typing.cast(EdgeDirectionEnum, jsii.get(self, "direction"))

    @builtins.property
    @jsii.member(jsii_name="edgeType")
    def edge_type(self) -> EdgeTypeEnum:
        '''Type of edge.'''
        return typing.cast(EdgeTypeEnum, jsii.get(self, "edgeType"))

    @builtins.property
    @jsii.member(jsii_name="isClosed")
    def is_closed(self) -> builtins.bool:
        '''Indicates if the Edge's **source** and **target** are the same, or were the same when it was created (prior to mutations).

        To check whether it was originally closed, use ``hasFlag(FlagEnum.CLOSED_EDGE)`` instead.
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isClosed"))

    @builtins.property
    @jsii.member(jsii_name="isCrossStack")
    def is_cross_stack(self) -> builtins.bool:
        '''Indicates if **source** and **target** nodes reside in different *root* stacks.'''
        return typing.cast(builtins.bool, jsii.get(self, "isCrossStack"))

    @builtins.property
    @jsii.member(jsii_name="isExtraneous")
    def is_extraneous(self) -> builtins.bool:
        '''Indicates if edge is extraneous which is determined by explicitly having *EXTRANEOUS* flag added and/or being a closed loop (source===target).'''
        return typing.cast(builtins.bool, jsii.get(self, "isExtraneous"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> "Node":
        '''Edge **source** is the node that defines the edge (tail).'''
        return typing.cast("Node", jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> "Node":
        '''Edge **target** is the node being referenced by the **source** (head).'''
        return typing.cast("Node", jsii.get(self, "target"))


@jsii.interface(jsii_type="aws-pdk.cdk_graph.IAppNodeProps")
class IAppNodeProps(IBaseEntityDataProps, typing_extensions.Protocol):
    '''{@link AppNode} props.'''

    @builtins.property
    @jsii.member(jsii_name="store")
    def store(self) -> Store:
        '''Store.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="cfnType")
    def cfn_type(self) -> typing.Optional[builtins.str]:
        '''Type of CloudFormation resource.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="constructInfo")
    def construct_info(self) -> typing.Optional[ConstructInfo]:
        '''Synthesized construct information defining jii resolution data.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="logicalId")
    def logical_id(self) -> typing.Optional[builtins.str]:
        '''Logical id of the node, which is only unique within containing stack.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> typing.Optional["Node"]:
        '''Parent node.'''
        ...


class _IAppNodePropsProxy(
    jsii.proxy_for(IBaseEntityDataProps), # type: ignore[misc]
):
    '''{@link AppNode} props.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.IAppNodeProps"

    @builtins.property
    @jsii.member(jsii_name="store")
    def store(self) -> Store:
        '''Store.'''
        return typing.cast(Store, jsii.get(self, "store"))

    @builtins.property
    @jsii.member(jsii_name="cfnType")
    def cfn_type(self) -> typing.Optional[builtins.str]:
        '''Type of CloudFormation resource.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cfnType"))

    @builtins.property
    @jsii.member(jsii_name="constructInfo")
    def construct_info(self) -> typing.Optional[ConstructInfo]:
        '''Synthesized construct information defining jii resolution data.'''
        return typing.cast(typing.Optional[ConstructInfo], jsii.get(self, "constructInfo"))

    @builtins.property
    @jsii.member(jsii_name="logicalId")
    def logical_id(self) -> typing.Optional[builtins.str]:
        '''Logical id of the node, which is only unique within containing stack.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logicalId"))

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> typing.Optional["Node"]:
        '''Parent node.'''
        return typing.cast(typing.Optional["Node"], jsii.get(self, "parent"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAppNodeProps).__jsii_proxy_class__ = lambda : _IAppNodePropsProxy


@jsii.interface(jsii_type="aws-pdk.cdk_graph.IAttributeReferenceProps")
class IAttributeReferenceProps(ITypedEdgeProps, typing_extensions.Protocol):
    '''Attribute type reference props.'''

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(
        self,
    ) -> typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]:
        '''Resolved attribute value.'''
        ...

    @value.setter
    def value(
        self,
        value: typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]],
    ) -> None:
        ...


class _IAttributeReferencePropsProxy(
    jsii.proxy_for(ITypedEdgeProps), # type: ignore[misc]
):
    '''Attribute type reference props.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.IAttributeReferenceProps"

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(
        self,
    ) -> typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]:
        '''Resolved attribute value.'''
        return typing.cast(typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]], jsii.get(self, "value"))

    @value.setter
    def value(
        self,
        value: typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cb4455c6155f299476a670d0e997b71808f20671144d43b0bee567bac569469)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAttributeReferenceProps).__jsii_proxy_class__ = lambda : _IAttributeReferencePropsProxy


@jsii.interface(jsii_type="aws-pdk.cdk_graph.ICfnResourceNodeProps")
class ICfnResourceNodeProps(ITypedNodeProps, typing_extensions.Protocol):
    '''CfnResourceNode props.'''

    @builtins.property
    @jsii.member(jsii_name="importArnToken")
    def import_arn_token(self) -> typing.Optional[builtins.str]:
        ...

    @import_arn_token.setter
    def import_arn_token(self, value: typing.Optional[builtins.str]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> typing.Optional[NodeTypeEnum]:
        ...

    @node_type.setter
    def node_type(self, value: typing.Optional[NodeTypeEnum]) -> None:
        ...


class _ICfnResourceNodePropsProxy(
    jsii.proxy_for(ITypedNodeProps), # type: ignore[misc]
):
    '''CfnResourceNode props.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.ICfnResourceNodeProps"

    @builtins.property
    @jsii.member(jsii_name="importArnToken")
    def import_arn_token(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "importArnToken"))

    @import_arn_token.setter
    def import_arn_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be6be7326a849c07dcb81fa86dc40a866bea3e67d81c9cb2af912bc8abf833aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "importArnToken", value)

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> typing.Optional[NodeTypeEnum]:
        return typing.cast(typing.Optional[NodeTypeEnum], jsii.get(self, "nodeType"))

    @node_type.setter
    def node_type(self, value: typing.Optional[NodeTypeEnum]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e96a1c36c84cd0c68af3453ab9f4614eda7c4ff0396c1167687cf813b028f08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeType", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICfnResourceNodeProps).__jsii_proxy_class__ = lambda : _ICfnResourceNodePropsProxy


@jsii.interface(jsii_type="aws-pdk.cdk_graph.IEdgeProps")
class IEdgeProps(ITypedEdgeProps, typing_extensions.Protocol):
    '''Edge props interface.'''

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> EdgeDirectionEnum:
        '''Indicates the direction in which the edge is directed.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="edgeType")
    def edge_type(self) -> EdgeTypeEnum:
        '''Type of edge.'''
        ...


class _IEdgePropsProxy(
    jsii.proxy_for(ITypedEdgeProps), # type: ignore[misc]
):
    '''Edge props interface.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.IEdgeProps"

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> EdgeDirectionEnum:
        '''Indicates the direction in which the edge is directed.'''
        return typing.cast(EdgeDirectionEnum, jsii.get(self, "direction"))

    @builtins.property
    @jsii.member(jsii_name="edgeType")
    def edge_type(self) -> EdgeTypeEnum:
        '''Type of edge.'''
        return typing.cast(EdgeTypeEnum, jsii.get(self, "edgeType"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEdgeProps).__jsii_proxy_class__ = lambda : _IEdgePropsProxy


@jsii.interface(jsii_type="aws-pdk.cdk_graph.INodeProps")
class INodeProps(ITypedNodeProps, typing_extensions.Protocol):
    '''Node props.'''

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> NodeTypeEnum:
        '''Type of node.'''
        ...


class _INodePropsProxy(
    jsii.proxy_for(ITypedNodeProps), # type: ignore[misc]
):
    '''Node props.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.INodeProps"

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> NodeTypeEnum:
        '''Type of node.'''
        return typing.cast(NodeTypeEnum, jsii.get(self, "nodeType"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INodeProps).__jsii_proxy_class__ = lambda : _INodePropsProxy


@jsii.interface(jsii_type="aws-pdk.cdk_graph.IOutputNodeProps")
class IOutputNodeProps(ITypedNodeProps, typing_extensions.Protocol):
    '''OutputNode props.'''

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        '''Resolved output value.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''Description.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="exportName")
    def export_name(self) -> typing.Optional[builtins.str]:
        '''Export name.'''
        ...


class _IOutputNodePropsProxy(
    jsii.proxy_for(ITypedNodeProps), # type: ignore[misc]
):
    '''OutputNode props.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.IOutputNodeProps"

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        '''Resolved output value.'''
        return typing.cast(typing.Any, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''Description.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="exportName")
    def export_name(self) -> typing.Optional[builtins.str]:
        '''Export name.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exportName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IOutputNodeProps).__jsii_proxy_class__ = lambda : _IOutputNodePropsProxy


@jsii.interface(jsii_type="aws-pdk.cdk_graph.IParameterNodeProps")
class IParameterNodeProps(ITypedNodeProps, typing_extensions.Protocol):
    '''{@link ParameterNode} props.'''

    @builtins.property
    @jsii.member(jsii_name="parameterType")
    def parameter_type(self) -> builtins.str:
        '''Parameter type.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        '''Resolved value.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''Description.'''
        ...


class _IParameterNodePropsProxy(
    jsii.proxy_for(ITypedNodeProps), # type: ignore[misc]
):
    '''{@link ParameterNode} props.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.IParameterNodeProps"

    @builtins.property
    @jsii.member(jsii_name="parameterType")
    def parameter_type(self) -> builtins.str:
        '''Parameter type.'''
        return typing.cast(builtins.str, jsii.get(self, "parameterType"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        '''Resolved value.'''
        return typing.cast(typing.Any, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''Description.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IParameterNodeProps).__jsii_proxy_class__ = lambda : _IParameterNodePropsProxy


@jsii.interface(jsii_type="aws-pdk.cdk_graph.IReferenceProps")
class IReferenceProps(ITypedEdgeProps, typing_extensions.Protocol):
    '''Reference edge props.'''

    @builtins.property
    @jsii.member(jsii_name="referenceType")
    def reference_type(self) -> typing.Optional[ReferenceTypeEnum]:
        '''Type of reference.'''
        ...

    @reference_type.setter
    def reference_type(self, value: typing.Optional[ReferenceTypeEnum]) -> None:
        ...


class _IReferencePropsProxy(
    jsii.proxy_for(ITypedEdgeProps), # type: ignore[misc]
):
    '''Reference edge props.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.IReferenceProps"

    @builtins.property
    @jsii.member(jsii_name="referenceType")
    def reference_type(self) -> typing.Optional[ReferenceTypeEnum]:
        '''Type of reference.'''
        return typing.cast(typing.Optional[ReferenceTypeEnum], jsii.get(self, "referenceType"))

    @reference_type.setter
    def reference_type(self, value: typing.Optional[ReferenceTypeEnum]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b20346f45e8bac075c89073c4606cb664ea583a1c99e2b774a4e4a9e26abec4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "referenceType", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IReferenceProps).__jsii_proxy_class__ = lambda : _IReferencePropsProxy


@jsii.interface(jsii_type="aws-pdk.cdk_graph.IResourceNodeProps")
class IResourceNodeProps(ITypedNodeProps, typing_extensions.Protocol):
    '''ResourceNode props.'''

    @builtins.property
    @jsii.member(jsii_name="cdkOwned")
    def cdk_owned(self) -> builtins.bool:
        '''Indicates if this resource is owned by cdk (defined in cdk library).'''
        ...

    @cdk_owned.setter
    def cdk_owned(self, value: builtins.bool) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> typing.Optional[NodeTypeEnum]:
        '''Type of node.'''
        ...

    @node_type.setter
    def node_type(self, value: typing.Optional[NodeTypeEnum]) -> None:
        ...


class _IResourceNodePropsProxy(
    jsii.proxy_for(ITypedNodeProps), # type: ignore[misc]
):
    '''ResourceNode props.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.IResourceNodeProps"

    @builtins.property
    @jsii.member(jsii_name="cdkOwned")
    def cdk_owned(self) -> builtins.bool:
        '''Indicates if this resource is owned by cdk (defined in cdk library).'''
        return typing.cast(builtins.bool, jsii.get(self, "cdkOwned"))

    @cdk_owned.setter
    def cdk_owned(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf761bb7345ddde31b7cf06cecfa7654aebe72dec96d1b36ea8a395e665dc081)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cdkOwned", value)

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> typing.Optional[NodeTypeEnum]:
        '''Type of node.'''
        return typing.cast(typing.Optional[NodeTypeEnum], jsii.get(self, "nodeType"))

    @node_type.setter
    def node_type(self, value: typing.Optional[NodeTypeEnum]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8b37654d569fb5b8f855a3c9d00105a89e908b61d75450afffc30dd6355bd3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeType", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IResourceNodeProps).__jsii_proxy_class__ = lambda : _IResourceNodePropsProxy


@jsii.interface(jsii_type="aws-pdk.cdk_graph.IStackNodeProps")
class IStackNodeProps(ITypedNodeProps, typing_extensions.Protocol):
    '''{@link StackNode} props.'''

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> typing.Optional[NodeTypeEnum]:
        '''Type of node.'''
        ...

    @node_type.setter
    def node_type(self, value: typing.Optional[NodeTypeEnum]) -> None:
        ...


class _IStackNodePropsProxy(
    jsii.proxy_for(ITypedNodeProps), # type: ignore[misc]
):
    '''{@link StackNode} props.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.IStackNodeProps"

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> typing.Optional[NodeTypeEnum]:
        '''Type of node.'''
        return typing.cast(typing.Optional[NodeTypeEnum], jsii.get(self, "nodeType"))

    @node_type.setter
    def node_type(self, value: typing.Optional[NodeTypeEnum]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ecd1f4d261ce04fdf1452fd6236792aab4dbd879fcb8e34e4fa9c0cbf5b1a53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeType", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IStackNodeProps).__jsii_proxy_class__ = lambda : _IStackNodePropsProxy


@jsii.data_type(
    jsii_type="aws-pdk.cdk_graph.InferredNodeProps",
    jsii_struct_bases=[SGEntity],
    name_mapping={
        "uuid": "uuid",
        "attributes": "attributes",
        "flags": "flags",
        "metadata": "metadata",
        "tags": "tags",
        "dependencies": "dependencies",
        "unresolved_references": "unresolvedReferences",
        "cfn_type": "cfnType",
        "construct_info": "constructInfo",
        "logical_id": "logicalId",
    },
)
class InferredNodeProps(SGEntity):
    def __init__(
        self,
        *,
        uuid: builtins.str,
        attributes: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]]] = None,
        flags: typing.Optional[typing.Sequence[FlagEnum]] = None,
        metadata: typing.Optional[typing.Sequence[typing.Union[_constructs_77d1e7e8.MetadataEntry, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        dependencies: typing.Sequence[builtins.str],
        unresolved_references: typing.Sequence[typing.Union[SGUnresolvedReference, typing.Dict[builtins.str, typing.Any]]],
        cfn_type: typing.Optional[builtins.str] = None,
        construct_info: typing.Optional[typing.Union[ConstructInfo, typing.Dict[builtins.str, typing.Any]]] = None,
        logical_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Inferred node props.

        :param uuid: Universally unique identity.
        :param attributes: Serializable entity attributes.
        :param flags: Serializable entity flags.
        :param metadata: Serializable entity metadata.
        :param tags: Serializable entity tags.
        :param dependencies: 
        :param unresolved_references: 
        :param cfn_type: 
        :param construct_info: 
        :param logical_id: 
        '''
        if isinstance(construct_info, dict):
            construct_info = ConstructInfo(**construct_info)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2acae948798ac3e9e02923a9fc8f2b3bc10974e35a8b296e0ce46b6b324973e)
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument flags", value=flags, expected_type=type_hints["flags"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
            check_type(argname="argument unresolved_references", value=unresolved_references, expected_type=type_hints["unresolved_references"])
            check_type(argname="argument cfn_type", value=cfn_type, expected_type=type_hints["cfn_type"])
            check_type(argname="argument construct_info", value=construct_info, expected_type=type_hints["construct_info"])
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uuid": uuid,
            "dependencies": dependencies,
            "unresolved_references": unresolved_references,
        }
        if attributes is not None:
            self._values["attributes"] = attributes
        if flags is not None:
            self._values["flags"] = flags
        if metadata is not None:
            self._values["metadata"] = metadata
        if tags is not None:
            self._values["tags"] = tags
        if cfn_type is not None:
            self._values["cfn_type"] = cfn_type
        if construct_info is not None:
            self._values["construct_info"] = construct_info
        if logical_id is not None:
            self._values["logical_id"] = logical_id

    @builtins.property
    def uuid(self) -> builtins.str:
        '''Universally unique identity.'''
        result = self._values.get("uuid")
        assert result is not None, "Required property 'uuid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]]:
        '''Serializable entity attributes.

        :see: {@link Attributes }
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]], result)

    @builtins.property
    def flags(self) -> typing.Optional[typing.List[FlagEnum]]:
        '''Serializable entity flags.

        :see: {@link FlagEnum }
        '''
        result = self._values.get("flags")
        return typing.cast(typing.Optional[typing.List[FlagEnum]], result)

    @builtins.property
    def metadata(
        self,
    ) -> typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]]:
        '''Serializable entity metadata.

        :see: {@link Metadata }
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Serializable entity tags.

        :see: {@link Tags }
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def dependencies(self) -> typing.List[builtins.str]:
        result = self._values.get("dependencies")
        assert result is not None, "Required property 'dependencies' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def unresolved_references(self) -> typing.List[SGUnresolvedReference]:
        result = self._values.get("unresolved_references")
        assert result is not None, "Required property 'unresolved_references' is missing"
        return typing.cast(typing.List[SGUnresolvedReference], result)

    @builtins.property
    def cfn_type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("cfn_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def construct_info(self) -> typing.Optional[ConstructInfo]:
        result = self._values.get("construct_info")
        return typing.cast(typing.Optional[ConstructInfo], result)

    @builtins.property
    def logical_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("logical_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InferredNodeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ISerializableNode)
class Node(BaseEntity, metaclass=jsii.JSIIMeta, jsii_type="aws-pdk.cdk_graph.Node"):
    '''Node class is the base definition of **node** entities in the graph, as in standard `graph theory <https://en.wikipedia.org/wiki/Graph_theory>`_.'''

    def __init__(self, props: INodeProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4de5b09f927d57df12f03be58ace29ba4c140ec92e2fa59d823bc4d75c65ca1c)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="addChild")
    def add_child(self, node: "Node") -> None:
        '''Add *child* node.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__822deab54197c7dba7e8d8cb7e80f33afdbba819d26325847b05914e1ab6b977)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "addChild", [node]))

    @jsii.member(jsii_name="addLink")
    def add_link(self, edge: Edge) -> None:
        '''Add *link* to another node.

        :param edge: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92c69958865778a5cd6c7a44298d37111bd3877e80fb8e8fe2e99a907a3f4be9)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(None, jsii.invoke(self, "addLink", [edge]))

    @jsii.member(jsii_name="addReverseLink")
    def add_reverse_link(self, edge: Edge) -> None:
        '''Add *link* from another node.

        :param edge: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9287497ed897a1b295091b45a78b0138ee423db55dd248100f2d2eca69539b7a)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(None, jsii.invoke(self, "addReverseLink", [edge]))

    @jsii.member(jsii_name="doesDependOn")
    def does_depend_on(self, node: "Node") -> builtins.bool:
        '''Indicates if *this node* depends on *another node*.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0e60875e94de5c2a9e32e8fdfe6a2fb629225df645b603ad29554a65521f7cf)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.invoke(self, "doesDependOn", [node]))

    @jsii.member(jsii_name="doesReference")
    def does_reference(self, node: "Node") -> builtins.bool:
        '''Indicates if *this node* references *another node*.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e98a3325514ea8432e2e8904f0259b4c3bc27af36ec1e0a0dabe641c5938d582)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.invoke(self, "doesReference", [node]))

    @jsii.member(jsii_name="find")
    def find(self, predicate: INodePredicate) -> typing.Optional["Node"]:
        '''Recursively find the nearest sub-node matching predicate.

        :param predicate: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bbf6cf8a35ed3e35067d0679cc7f9b2aee3f745a16bbaff31f21f752664f5b0)
            check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
        return typing.cast(typing.Optional["Node"], jsii.invoke(self, "find", [predicate]))

    @jsii.member(jsii_name="findAll")
    def find_all(
        self,
        options: typing.Optional[IFindNodeOptions] = None,
    ) -> typing.List["Node"]:
        '''Return this construct and all of its sub-nodes in the given order.

        Optionally filter nodes based on predicate.

        :param options: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6fc2a3a6249ddd91300d2abc294c7192eff6bead218f435962c6007c14e0bba)
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
        return typing.cast(typing.List["Node"], jsii.invoke(self, "findAll", [options]))

    @jsii.member(jsii_name="findAllLinks")
    def find_all_links(
        self,
        options: typing.Optional[IFindEdgeOptions] = None,
    ) -> typing.List[Edge]:
        '''Return all direct links of this node and that of all sub-nodes.

        Optionally filter links based on predicate.

        :param options: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eece34c91b06c0696c58f0b3937c6b8b3fe81418cf88b58c9dc13a3b1340eee)
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
        return typing.cast(typing.List[Edge], jsii.invoke(self, "findAllLinks", [options]))

    @jsii.member(jsii_name="findAncestor")
    def find_ancestor(
        self,
        predicate: INodePredicate,
        max: typing.Optional[jsii.Number] = None,
    ) -> typing.Optional["Node"]:
        '''Find nearest *ancestor* of *this node* matching given predicate.

        :param predicate: - Predicate to match ancestor.
        :param max: -

        :max: {number} [max] - Optional maximum levels to ascend
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__726632e2a9d796041bf110c2b084edeca68991dec231f118848aa8e8b21a1981)
            check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
            check_type(argname="argument max", value=max, expected_type=type_hints["max"])
        return typing.cast(typing.Optional["Node"], jsii.invoke(self, "findAncestor", [predicate, max]))

    @jsii.member(jsii_name="findChild")
    def find_child(self, id: builtins.str) -> typing.Optional["Node"]:
        '''Find child with given *id*.

        Similar to ``find`` but does not throw error if no child found.

        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20d053b5fec926c5b50fb68503293367d164bfb4564c1b916b306a99ba68cbf3)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(typing.Optional["Node"], jsii.invoke(self, "findChild", [id]))

    @jsii.member(jsii_name="findLink")
    def find_link(
        self,
        predicate: IEdgePredicate,
        reverse: typing.Optional[builtins.bool] = None,
        follow: typing.Optional[builtins.bool] = None,
        direct: typing.Optional[builtins.bool] = None,
    ) -> typing.Optional[Edge]:
        '''Find link of this node based on predicate.

        By default this will follow link
        chains to evaluate the predicate against and return the matching direct link
        of this node.

        :param predicate: Edge predicate function to match edge.
        :param reverse: Indicates if links are search in reverse order.
        :param follow: Indicates if link chain is followed.
        :param direct: Indicates that only *direct* links should be searched.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8b0fbb510b384c1fa0b6acde8f86d1d0ce87073628b74fc37d4425c97a9b6d1)
            check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
            check_type(argname="argument reverse", value=reverse, expected_type=type_hints["reverse"])
            check_type(argname="argument follow", value=follow, expected_type=type_hints["follow"])
            check_type(argname="argument direct", value=direct, expected_type=type_hints["direct"])
        return typing.cast(typing.Optional[Edge], jsii.invoke(self, "findLink", [predicate, reverse, follow, direct]))

    @jsii.member(jsii_name="findLinks")
    def find_links(
        self,
        predicate: IEdgePredicate,
        reverse: typing.Optional[builtins.bool] = None,
        follow: typing.Optional[builtins.bool] = None,
        direct: typing.Optional[builtins.bool] = None,
    ) -> typing.List[Edge]:
        '''Find all links of this node based on predicate.

        By default this will follow link
        chains to evaluate the predicate against and return the matching direct links
        of this node.

        :param predicate: Edge predicate function to match edge.
        :param reverse: Indicates if links are search in reverse order.
        :param follow: Indicates if link chain is followed.
        :param direct: Indicates that only *direct* links should be searched.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ebd234a21944255ce7a3bf46c98de05f9b060c0975f591be9e42ccc10fbe1e)
            check_type(argname="argument predicate", value=predicate, expected_type=type_hints["predicate"])
            check_type(argname="argument reverse", value=reverse, expected_type=type_hints["reverse"])
            check_type(argname="argument follow", value=follow, expected_type=type_hints["follow"])
            check_type(argname="argument direct", value=direct, expected_type=type_hints["direct"])
        return typing.cast(typing.List[Edge], jsii.invoke(self, "findLinks", [predicate, reverse, follow, direct]))

    @jsii.member(jsii_name="getCfnProp")
    def get_cfn_prop(
        self,
        key: builtins.str,
    ) -> typing.Optional[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]:
        '''Get specific CloudFormation property.

        :param key: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc4489bb29c0dc7a340d7b85fffe41c572b9326c7053686630729dadf5e78df0)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(typing.Optional[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]], jsii.invoke(self, "getCfnProp", [key]))

    @jsii.member(jsii_name="getChild")
    def get_child(self, id: builtins.str) -> "Node":
        '''Get *child* node with given *id*.

        :param id: -

        :throws: Error if no child with given id
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95ecc4c3f12cecd2503192a369c960bd31175714b90e2013b3ffaa54ea7be73f)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast("Node", jsii.invoke(self, "getChild", [id]))

    @jsii.member(jsii_name="getLinkChains")
    def get_link_chains(
        self,
        reverse: typing.Optional[builtins.bool] = None,
    ) -> typing.List[typing.List[typing.Any]]:
        '''Resolve all link chains.

        :param reverse: -

        :see: {@link EdgeChain }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__080aecd0422d40fd61753e5b7b7579c8f5acf9826b5bf5a4f84b8e1e88f76a65)
            check_type(argname="argument reverse", value=reverse, expected_type=type_hints["reverse"])
        return typing.cast(typing.List[typing.List[typing.Any]], jsii.invoke(self, "getLinkChains", [reverse]))

    @jsii.member(jsii_name="getNearestAncestor")
    def get_nearest_ancestor(self, node: "Node") -> "Node":
        '''Gets the nearest **common** *ancestor* shared between *this node* and another *node*.

        :param node: -

        :throws: Error if *node* does not share a **common** *ancestor*
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24390e5e28533a0151b46f1d6d1bc717c4045cfba51f28688db9b249718dcb0d)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast("Node", jsii.invoke(self, "getNearestAncestor", [node]))

    @jsii.member(jsii_name="isAncestor")
    def is_ancestor(self, ancestor: "Node") -> builtins.bool:
        '''Indicates if a specific *node* is an *ancestor* of *this node*.

        :param ancestor: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a6376857f895fa88fa486841fc445ae09d54f2e973f92359dd41a6869d1b08f)
            check_type(argname="argument ancestor", value=ancestor, expected_type=type_hints["ancestor"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isAncestor", [ancestor]))

    @jsii.member(jsii_name="isChild")
    def is_child(self, node: "Node") -> builtins.bool:
        '''Indicates if specific *node* is a *child* of *this node*.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72c281234d936d64eab0583e21a5cead88187f32f5d4ed0062f8e63e5f44db99)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isChild", [node]))

    @jsii.member(jsii_name="mutateCollapse")
    def mutate_collapse(self) -> None:
        '''Collapses all sub-nodes of *this node* into *this node*.

        :destructive: true
        '''
        return typing.cast(None, jsii.invoke(self, "mutateCollapse", []))

    @jsii.member(jsii_name="mutateCollapseTo")
    def mutate_collapse_to(self, ancestor: "Node") -> "Node":
        '''Collapses *this node* into *an ancestor*.

        :param ancestor: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30a49bf003e095e6e8742bb86271798506e8e46a6fc34ebb223904c1ad140d61)
            check_type(argname="argument ancestor", value=ancestor, expected_type=type_hints["ancestor"])
        return typing.cast("Node", jsii.invoke(self, "mutateCollapseTo", [ancestor]))

    @jsii.member(jsii_name="mutateCollapseToParent")
    def mutate_collapse_to_parent(self) -> "Node":
        '''Collapses *this node* into *it's parent node*.

        :destructive: true
        '''
        return typing.cast("Node", jsii.invoke(self, "mutateCollapseToParent", []))

    @jsii.member(jsii_name="mutateDestroy")
    def mutate_destroy(self, strict: typing.Optional[builtins.bool] = None) -> None:
        '''Destroys this node by removing all references and removing this node from the store.

        :param strict: - Indicates that this node must not have references.

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3d379a902ce679e3cebc333e6e6f2cc75ef5ab9bb08d6ff9f61180e6683e781)
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
        return typing.cast(None, jsii.invoke(self, "mutateDestroy", [strict]))

    @jsii.member(jsii_name="mutateHoist")
    def mutate_hoist(self, new_parent: "Node") -> None:
        '''Hoist *this node* to an *ancestor* by removing it from its current parent node and in turn moving it to the ancestor.

        :param new_parent: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ed3665b9a2a6c5a93a3d4999028e70630a5cd738c82689f4e290118ad177873)
            check_type(argname="argument new_parent", value=new_parent, expected_type=type_hints["new_parent"])
        return typing.cast(None, jsii.invoke(self, "mutateHoist", [new_parent]))

    @jsii.member(jsii_name="mutateMove")
    def mutate_move(self, new_parent: "Node") -> None:
        '''Move this node into a new parent node.

        :param new_parent: - The parent to move this node to.

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a674cdc8e325d84bdbfe1dbd39a2d8b78daf6848f004711b308462aae3897d4e)
            check_type(argname="argument new_parent", value=new_parent, expected_type=type_hints["new_parent"])
        return typing.cast(None, jsii.invoke(self, "mutateMove", [new_parent]))

    @jsii.member(jsii_name="mutateRemoveChild")
    def mutate_remove_child(self, node: "Node") -> builtins.bool:
        '''Remove a *child* node from *this node*.

        :param node: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17f7df7fbbe01468d577cc8d08e9c83043808cc84720675a256302c06b838f1f)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveChild", [node]))

    @jsii.member(jsii_name="mutateRemoveLink")
    def mutate_remove_link(self, link: Edge) -> builtins.bool:
        '''Remove a *link* from *this node*.

        :param link: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3cd9997bbf7b1107341c7746a015a44f76cf17a58af3da4c25497fdb9aea274)
            check_type(argname="argument link", value=link, expected_type=type_hints["link"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveLink", [link]))

    @jsii.member(jsii_name="mutateRemoveReverseLink")
    def mutate_remove_reverse_link(self, link: Edge) -> builtins.bool:
        '''Remove a *link* to *this node*.

        :param link: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94701de03510debf27fa071300acf639253ed529c495ae61ed4350beda741691)
            check_type(argname="argument link", value=link, expected_type=type_hints["link"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveReverseLink", [link]))

    @jsii.member(jsii_name="mutateUncluster")
    def mutate_uncluster(self) -> None:
        '''Hoist all children to parent and collapse node to parent.

        :destructive: true
        '''
        return typing.cast(None, jsii.invoke(self, "mutateUncluster", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''Get string representation of this node.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="allowDestructiveMutations")
    def allow_destructive_mutations(self) -> builtins.bool:
        '''Indicates if this node allows destructive mutations.

        :see: {@link Store.allowDestructiveMutations }
        '''
        return typing.cast(builtins.bool, jsii.get(self, "allowDestructiveMutations"))

    @builtins.property
    @jsii.member(jsii_name="children")
    def children(self) -> typing.List["Node"]:
        '''Get all direct child nodes.'''
        return typing.cast(typing.List["Node"], jsii.get(self, "children"))

    @builtins.property
    @jsii.member(jsii_name="dependedOnBy")
    def depended_on_by(self) -> typing.List["Node"]:
        '''Get list of **Nodes** that *depend on this node*.

        :see: {@link Node.reverseDependencyLinks }
        '''
        return typing.cast(typing.List["Node"], jsii.get(self, "dependedOnBy"))

    @builtins.property
    @jsii.member(jsii_name="dependencies")
    def dependencies(self) -> typing.List["Node"]:
        '''Get list of **Nodes** that *this node depends on*.

        :see: {@link Node.dependencyLinks }
        '''
        return typing.cast(typing.List["Node"], jsii.get(self, "dependencies"))

    @builtins.property
    @jsii.member(jsii_name="dependencyLinks")
    def dependency_links(self) -> typing.List["Dependency"]:
        '''Gets list of {@link Dependency} links (edges) where this node is the **source**.'''
        return typing.cast(typing.List["Dependency"], jsii.get(self, "dependencyLinks"))

    @builtins.property
    @jsii.member(jsii_name="depth")
    def depth(self) -> jsii.Number:
        '''Indicates the depth of the node relative to root (0).'''
        return typing.cast(jsii.Number, jsii.get(self, "depth"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''Node id, which is only unique within parent scope.'''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="isAsset")
    def is_asset(self) -> builtins.bool:
        '''Indicates if this node is considered a {@link FlagEnum.ASSET}.'''
        return typing.cast(builtins.bool, jsii.get(self, "isAsset"))

    @builtins.property
    @jsii.member(jsii_name="isCfnFqn")
    def is_cfn_fqn(self) -> builtins.bool:
        '''Indicates if node ConstructInfoFqn denotes a ``aws-cdk-lib.*.Cfn*`` construct.

        :see: {@link FlagEnum.CFN_FQN }
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isCfnFqn"))

    @builtins.property
    @jsii.member(jsii_name="isCluster")
    def is_cluster(self) -> builtins.bool:
        '''Indicates if this node is considered a {@link FlagEnum.CLUSTER}.'''
        return typing.cast(builtins.bool, jsii.get(self, "isCluster"))

    @builtins.property
    @jsii.member(jsii_name="isCustomResource")
    def is_custom_resource(self) -> builtins.bool:
        '''Indicates if node is a *Custom Resource*.'''
        return typing.cast(builtins.bool, jsii.get(self, "isCustomResource"))

    @builtins.property
    @jsii.member(jsii_name="isExtraneous")
    def is_extraneous(self) -> builtins.bool:
        '''Indicates if this node is considered a {@link FlagEnum.EXTRANEOUS} node or determined to be extraneous: - Clusters that contain no children.'''
        return typing.cast(builtins.bool, jsii.get(self, "isExtraneous"))

    @builtins.property
    @jsii.member(jsii_name="isGraphContainer")
    def is_graph_container(self) -> builtins.bool:
        '''Indicates if this node is considered a {@link FlagEnum.GRAPH_CONTAINER}.'''
        return typing.cast(builtins.bool, jsii.get(self, "isGraphContainer"))

    @builtins.property
    @jsii.member(jsii_name="isLeaf")
    def is_leaf(self) -> builtins.bool:
        '''Indicates if this node is a *leaf* node, which means it does not have children.'''
        return typing.cast(builtins.bool, jsii.get(self, "isLeaf"))

    @builtins.property
    @jsii.member(jsii_name="isTopLevel")
    def is_top_level(self) -> builtins.bool:
        '''Indicates if node is direct child of the graph root node.'''
        return typing.cast(builtins.bool, jsii.get(self, "isTopLevel"))

    @builtins.property
    @jsii.member(jsii_name="links")
    def links(self) -> typing.List[Edge]:
        '''Gets all links (edges) in which this node is the **source**.'''
        return typing.cast(typing.List[Edge], jsii.get(self, "links"))

    @builtins.property
    @jsii.member(jsii_name="nodeType")
    def node_type(self) -> NodeTypeEnum:
        '''Type of node.'''
        return typing.cast(NodeTypeEnum, jsii.get(self, "nodeType"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        '''Path of the node.'''
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="referencedBy")
    def referenced_by(self) -> typing.List["Node"]:
        '''Get list of **Nodes** that *reference this node*.

        :see: {@link Node.reverseReferenceLinks }
        '''
        return typing.cast(typing.List["Node"], jsii.get(self, "referencedBy"))

    @builtins.property
    @jsii.member(jsii_name="referenceLinks")
    def reference_links(self) -> typing.List["Reference"]:
        '''Gets list of {@link Reference} links (edges) where this node is the **source**.'''
        return typing.cast(typing.List["Reference"], jsii.get(self, "referenceLinks"))

    @builtins.property
    @jsii.member(jsii_name="references")
    def references(self) -> typing.List["Node"]:
        '''Get list of **Nodes** that *this node references*.

        :see: {@link Node.referenceLinks }
        '''
        return typing.cast(typing.List["Node"], jsii.get(self, "references"))

    @builtins.property
    @jsii.member(jsii_name="reverseDependencyLinks")
    def reverse_dependency_links(self) -> typing.List["Dependency"]:
        '''Gets list of {@link Dependency} links (edges) where this node is the **target**.'''
        return typing.cast(typing.List["Dependency"], jsii.get(self, "reverseDependencyLinks"))

    @builtins.property
    @jsii.member(jsii_name="reverseLinks")
    def reverse_links(self) -> typing.List[Edge]:
        '''Gets all links (edges) in which this node is the **target**.'''
        return typing.cast(typing.List[Edge], jsii.get(self, "reverseLinks"))

    @builtins.property
    @jsii.member(jsii_name="reverseReferenceLinks")
    def reverse_reference_links(self) -> typing.List["Reference"]:
        '''Gets list of {@link Reference} links (edges) where this node is the **target**.'''
        return typing.cast(typing.List["Reference"], jsii.get(self, "reverseReferenceLinks"))

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List["Node"]:
        '''Gets descending ordered list of ancestors from the root.'''
        return typing.cast(typing.List["Node"], jsii.get(self, "scopes"))

    @builtins.property
    @jsii.member(jsii_name="siblings")
    def siblings(self) -> typing.List["Node"]:
        '''Get list of *siblings* of this node.'''
        return typing.cast(typing.List["Node"], jsii.get(self, "siblings"))

    @builtins.property
    @jsii.member(jsii_name="cfnProps")
    def cfn_props(self) -> typing.Optional[PlainObject]:
        '''Gets CloudFormation properties for this node.'''
        return typing.cast(typing.Optional[PlainObject], jsii.get(self, "cfnProps"))

    @builtins.property
    @jsii.member(jsii_name="cfnType")
    def cfn_type(self) -> typing.Optional[builtins.str]:
        '''Get the CloudFormation resource type for this node.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cfnType"))

    @builtins.property
    @jsii.member(jsii_name="constructInfo")
    def construct_info(self) -> typing.Optional[ConstructInfo]:
        '''Synthesized construct information defining jii resolution data.'''
        return typing.cast(typing.Optional[ConstructInfo], jsii.get(self, "constructInfo"))

    @builtins.property
    @jsii.member(jsii_name="constructInfoFqn")
    def construct_info_fqn(self) -> typing.Optional[builtins.str]:
        '''Synthesized construct information defining jii resolution data.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "constructInfoFqn"))

    @builtins.property
    @jsii.member(jsii_name="logicalId")
    def logical_id(self) -> typing.Optional[builtins.str]:
        '''Logical id of the node, which is only unique within containing stack.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logicalId"))

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> typing.Optional["Node"]:
        '''Parent node.

        Only the root node should not have parent.
        '''
        return typing.cast(typing.Optional["Node"], jsii.get(self, "parent"))

    @builtins.property
    @jsii.member(jsii_name="rootStack")
    def root_stack(self) -> typing.Optional["StackNode"]:
        '''Get **root** stack.'''
        return typing.cast(typing.Optional["StackNode"], jsii.get(self, "rootStack"))

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> typing.Optional["StackNode"]:
        '''Stack the node is contained in.'''
        return typing.cast(typing.Optional["StackNode"], jsii.get(self, "stack"))


class OutputNode(
    Node,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-pdk.cdk_graph.OutputNode",
):
    '''OutputNode defines a cdk CfnOutput resources.'''

    def __init__(self, props: IOutputNodeProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1fd6fb2bd31ca0a711fbe639b40353deb37a3a2ba5c57893f31f5fd610c6725)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isOutputNode")
    @builtins.classmethod
    def is_output_node(cls, node: Node) -> builtins.bool:
        '''Indicates if node is an {@link OutputNode}.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e2c3cc672265efde96974d40877e2a5be5217155a14a90f9d56cd0bafed9c14)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isOutputNode", [node]))

    @jsii.member(jsii_name="mutateDestroy")
    def mutate_destroy(self, strict: typing.Optional[builtins.bool] = None) -> None:
        '''Destroys this node by removing all references and removing this node from the store.

        :param strict: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8b091eb51e6eb2bd1d856fe4020eeb8dca3fb5c7af39d0100de3623b0fd1ecd)
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
        return typing.cast(None, jsii.invoke(self, "mutateDestroy", [strict]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATTR_EXPORT_NAME")
    def ATTR_EXPORT_NAME(cls) -> builtins.str:
        '''Attribute key where output export name is stored.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ATTR_EXPORT_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATTR_VALUE")
    def ATTR_VALUE(cls) -> builtins.str:
        '''Attribute key where output value is stored.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ATTR_VALUE"))

    @builtins.property
    @jsii.member(jsii_name="isExport")
    def is_export(self) -> builtins.bool:
        '''Indicates if {@link OutputNode} is **exported**.'''
        return typing.cast(builtins.bool, jsii.get(self, "isExport"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        '''Get the *value** attribute.'''
        return typing.cast(typing.Any, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="exportName")
    def export_name(self) -> typing.Optional[builtins.str]:
        '''Get the export name attribute.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "exportName"))


class ParameterNode(
    Node,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-pdk.cdk_graph.ParameterNode",
):
    '''ParameterNode defines a CfnParameter node.'''

    def __init__(self, props: IParameterNodeProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51225a1d733befcee7640052187873b7edb06412a37d44126772532d11386cec)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isParameterNode")
    @builtins.classmethod
    def is_parameter_node(cls, node: Node) -> builtins.bool:
        '''Indicates if node is a {@link ParameterNode}.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b77fe15850f537de7f8f30c0d2e0be8092ed0a3be8aa9d12b29f1c8133086e1)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isParameterNode", [node]))

    @jsii.member(jsii_name="mutateDestroy")
    def mutate_destroy(self, strict: typing.Optional[builtins.bool] = None) -> None:
        '''Destroys this node by removing all references and removing this node from the store.

        :param strict: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2978043840e2d17ee52ec9a18825cab34ab1e02e0e25509e8358a5c778c105f7)
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
        return typing.cast(None, jsii.invoke(self, "mutateDestroy", [strict]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATTR_TYPE")
    def ATTR_TYPE(cls) -> builtins.str:
        '''Attribute key where parameter type is stored.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ATTR_TYPE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATTR_VALUE")
    def ATTR_VALUE(cls) -> builtins.str:
        '''Attribute key where parameter value is store.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ATTR_VALUE"))

    @builtins.property
    @jsii.member(jsii_name="isStackReference")
    def is_stack_reference(self) -> builtins.bool:
        '''Indicates if parameter is a reference to a stack.'''
        return typing.cast(builtins.bool, jsii.get(self, "isStackReference"))

    @builtins.property
    @jsii.member(jsii_name="parameterType")
    def parameter_type(self) -> typing.Any:
        '''Get the parameter type attribute.'''
        return typing.cast(typing.Any, jsii.get(self, "parameterType"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Any:
        '''Get the value attribute.'''
        return typing.cast(typing.Any, jsii.get(self, "value"))


class Reference(Edge, metaclass=jsii.JSIIMeta, jsii_type="aws-pdk.cdk_graph.Reference"):
    '''Reference edge class defines a directed relationship between nodes.'''

    def __init__(self, props: IReferenceProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e70ff4d6f7671822a057ae6a06256f4a86380c90fcbbc00fd06bfcd238e14ab)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isRef")
    @builtins.classmethod
    def is_ref(cls, edge: Edge) -> builtins.bool:
        '''Indicates if edge is a **Ref** based {@link Reference} edge.

        :param edge: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa48dcc02db2c6f903ba1d45fed9966f4e1b48ca2ef148f70c34c41f471b4200)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isRef", [edge]))

    @jsii.member(jsii_name="isReference")
    @builtins.classmethod
    def is_reference(cls, edge: Edge) -> builtins.bool:
        '''Indicates if edge is a {@link Reference}.

        :param edge: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__775825c91a05498f95a2a4ad0eaceeb37d055357936d920eca3ea922f8f67e76)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isReference", [edge]))

    @jsii.member(jsii_name="resolveChain")
    def resolve_chain(self) -> typing.List[typing.Any]:
        '''Resolve reference chain.'''
        return typing.cast(typing.List[typing.Any], jsii.invoke(self, "resolveChain", []))

    @jsii.member(jsii_name="resolveTargets")
    def resolve_targets(self) -> typing.List[Node]:
        '''Resolve targets by following potential edge chain.

        :see: {@link EdgeChain }
        '''
        return typing.cast(typing.List[Node], jsii.invoke(self, "resolveTargets", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATT_TYPE")
    def ATT_TYPE(cls) -> builtins.str:
        '''Attribute defining the type of reference.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ATT_TYPE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PREFIX")
    def PREFIX(cls) -> builtins.str:
        '''Edge prefix to denote **Ref** type reference edge.'''
        return typing.cast(builtins.str, jsii.sget(cls, "PREFIX"))

    @builtins.property
    @jsii.member(jsii_name="referenceType")
    def reference_type(self) -> ReferenceTypeEnum:
        '''Get type of reference.'''
        return typing.cast(ReferenceTypeEnum, jsii.get(self, "referenceType"))


class ResourceNode(
    Node,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-pdk.cdk_graph.ResourceNode",
):
    '''ResourceNode class defines a L2 cdk resource construct.'''

    def __init__(self, props: IResourceNodeProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b8a5191e9d681773ced3070c7c959320beb61067aa93abadcab503ddd27eaef)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isResourceNode")
    @builtins.classmethod
    def is_resource_node(cls, node: Node) -> builtins.bool:
        '''Indicates if node is a {@link ResourceNode}.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__621a3bf7faf19f2a14e8669f5c56819be04579b841ea8fab0e085de855a84375)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isResourceNode", [node]))

    @jsii.member(jsii_name="mutateCfnResource")
    def mutate_cfn_resource(
        self,
        cfn_resource: typing.Optional["CfnResourceNode"] = None,
    ) -> None:
        '''Modifies the L1 resource wrapped by this L2 resource.

        :param cfn_resource: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8132a28cf569d50c469b3a4d805a0ee10ee428005027bf0decb5c9148b549c69)
            check_type(argname="argument cfn_resource", value=cfn_resource, expected_type=type_hints["cfn_resource"])
        return typing.cast(None, jsii.invoke(self, "mutateCfnResource", [cfn_resource]))

    @jsii.member(jsii_name="mutateRemoveChild")
    def mutate_remove_child(self, node: Node) -> builtins.bool:
        '''Remove a *child* node from *this node*.

        :param node: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df7273148d4e4651115533e8713c91dcf62db903d2ceccea9c4550784c999dd0)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveChild", [node]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATT_WRAPPED_CFN_PROPS")
    def ATT_WRAPPED_CFN_PROPS(cls) -> builtins.str:
        '''Attribute key for cfn properties.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ATT_WRAPPED_CFN_PROPS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATT_WRAPPED_CFN_TYPE")
    def ATT_WRAPPED_CFN_TYPE(cls) -> builtins.str:
        '''Attribute key for cfn resource type.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ATT_WRAPPED_CFN_TYPE"))

    @builtins.property
    @jsii.member(jsii_name="isCdkOwned")
    def is_cdk_owned(self) -> builtins.bool:
        '''Indicates if this resource is owned by cdk (defined in cdk library).'''
        return typing.cast(builtins.bool, jsii.get(self, "isCdkOwned"))

    @builtins.property
    @jsii.member(jsii_name="isWrapper")
    def is_wrapper(self) -> builtins.bool:
        '''Indicates if Resource wraps a single CfnResource.'''
        return typing.cast(builtins.bool, jsii.get(self, "isWrapper"))

    @builtins.property
    @jsii.member(jsii_name="cfnProps")
    def cfn_props(self) -> typing.Optional[PlainObject]:
        '''Get the cfn properties from the L1 resource that this L2 resource wraps.'''
        return typing.cast(typing.Optional[PlainObject], jsii.get(self, "cfnProps"))

    @builtins.property
    @jsii.member(jsii_name="cfnResource")
    def cfn_resource(self) -> typing.Optional["CfnResourceNode"]:
        '''Get the default/primary CfnResource that this Resource wraps.'''
        return typing.cast(typing.Optional["CfnResourceNode"], jsii.get(self, "cfnResource"))

    @builtins.property
    @jsii.member(jsii_name="cfnType")
    def cfn_type(self) -> typing.Optional[builtins.str]:
        '''Get the CloudFormation resource type for this L2 resource or for the L1 resource is wraps.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cfnType"))


class RootNode(Node, metaclass=jsii.JSIIMeta, jsii_type="aws-pdk.cdk_graph.RootNode"):
    '''RootNode represents the root of the store tree.'''

    def __init__(self, store: Store) -> None:
        '''
        :param store: Reference to the store.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed0a649be00d48d3240cd359fc9a3209f3800891b33b9b3a1695d2935c3366b7)
            check_type(argname="argument store", value=store, expected_type=type_hints["store"])
        jsii.create(self.__class__, self, [store])

    @jsii.member(jsii_name="isRootNode")
    @builtins.classmethod
    def is_root_node(cls, node: Node) -> builtins.bool:
        '''Indicates if node is a {@link RootNode}.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4da2a06f28639ec500a9e0d6f2c994ab4d6c86939356117317ac2a0a8a554131)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isRootNode", [node]))

    @jsii.member(jsii_name="findAll")
    def find_all(
        self,
        options: typing.Optional[IFindNodeOptions] = None,
    ) -> typing.List[Node]:
        '''Return this construct and all of its sub-nodes in the given order.

        Optionally filter nodes based on predicate.
        **The root not is excluded from list**

        :param options: -

        :inheritdoc: **The root not is excluded from list**
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4605265ca1a29a320ed54ce5c386cd4b3eaaf469030150f182e85cc9fb4f7fd4)
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
        return typing.cast(typing.List[Node], jsii.invoke(self, "findAll", [options]))

    @jsii.member(jsii_name="mutateCollapse")
    def mutate_collapse(self) -> None:
        '''Collapses all sub-nodes of *this node* into *this node*.

        .. epigraph::

           {@link RootNode} does not support this mutation

        :inheritdoc: true
        :throws: Error does not support
        '''
        return typing.cast(None, jsii.invoke(self, "mutateCollapse", []))

    @jsii.member(jsii_name="mutateCollapseTo")
    def mutate_collapse_to(self, _ancestor: Node) -> Node:
        '''Collapses *this node* into *an ancestor* > {@link RootNode} does not support this mutation.

        :param _ancestor: -

        :inheritdoc: true
        :throws: Error does not support
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f09f0ee53c4d93c2d042b780b8b154fe70ddde62aad07e5583a7bec87703fff7)
            check_type(argname="argument _ancestor", value=_ancestor, expected_type=type_hints["_ancestor"])
        return typing.cast(Node, jsii.invoke(self, "mutateCollapseTo", [_ancestor]))

    @jsii.member(jsii_name="mutateCollapseToParent")
    def mutate_collapse_to_parent(self) -> Node:
        '''Collapses *this node* into *it's parent node* > {@link RootNode} does not support this mutation.

        :inheritdoc: true
        :throws: Error does not support
        '''
        return typing.cast(Node, jsii.invoke(self, "mutateCollapseToParent", []))

    @jsii.member(jsii_name="mutateDestroy")
    def mutate_destroy(self, _strict: typing.Optional[builtins.bool] = None) -> None:
        '''Destroys this node by removing all references and removing this node from the store.

        .. epigraph::

           {@link RootNode} does not support this mutation

        :param _strict: -

        :inheritdoc: true
        :throws: Error does not support
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab8acf700c048bcde2989edf7b007d36b2c7f69c6ce6d6fd6ce288db08717f04)
            check_type(argname="argument _strict", value=_strict, expected_type=type_hints["_strict"])
        return typing.cast(None, jsii.invoke(self, "mutateDestroy", [_strict]))

    @jsii.member(jsii_name="mutateHoist")
    def mutate_hoist(self, _new_parent: Node) -> None:
        '''Hoist *this node* to an *ancestor* by removing it from its current parent node and in turn moving it to the ancestor.

        .. epigraph::

           {@link RootNode} does not support this mutation

        :param _new_parent: -

        :inheritdoc: true
        :throws: Error does not support
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18dba6f843f37b8527da73f88894707657ee31ea2b55d42af96c8708c045ae31)
            check_type(argname="argument _new_parent", value=_new_parent, expected_type=type_hints["_new_parent"])
        return typing.cast(None, jsii.invoke(self, "mutateHoist", [_new_parent]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PATH")
    def PATH(cls) -> builtins.str:
        '''Fixed path of root.'''
        return typing.cast(builtins.str, jsii.sget(cls, "PATH"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="UUID")
    def UUID(cls) -> builtins.str:
        '''Fixed UUID of root.'''
        return typing.cast(builtins.str, jsii.sget(cls, "UUID"))


@jsii.data_type(
    jsii_type="aws-pdk.cdk_graph.SGEdge",
    jsii_struct_bases=[SGEntity],
    name_mapping={
        "uuid": "uuid",
        "attributes": "attributes",
        "flags": "flags",
        "metadata": "metadata",
        "tags": "tags",
        "direction": "direction",
        "edge_type": "edgeType",
        "source": "source",
        "target": "target",
    },
)
class SGEdge(SGEntity):
    def __init__(
        self,
        *,
        uuid: builtins.str,
        attributes: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]]] = None,
        flags: typing.Optional[typing.Sequence[FlagEnum]] = None,
        metadata: typing.Optional[typing.Sequence[typing.Union[_constructs_77d1e7e8.MetadataEntry, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        direction: EdgeDirectionEnum,
        edge_type: EdgeTypeEnum,
        source: builtins.str,
        target: builtins.str,
    ) -> None:
        '''Serializable graph edge entity.

        :param uuid: Universally unique identity.
        :param attributes: Serializable entity attributes.
        :param flags: Serializable entity flags.
        :param metadata: Serializable entity metadata.
        :param tags: Serializable entity tags.
        :param direction: Indicates the direction in which the edge is directed.
        :param edge_type: Type of edge.
        :param source: UUID of edge **source** node (tail).
        :param target: UUID of edge **target** node (head).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fabddd2d6e7dbb1948d1fe7198dd1d701a842fa5891d20acd1b2a2319c634390)
            check_type(argname="argument uuid", value=uuid, expected_type=type_hints["uuid"])
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument flags", value=flags, expected_type=type_hints["flags"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
            check_type(argname="argument edge_type", value=edge_type, expected_type=type_hints["edge_type"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uuid": uuid,
            "direction": direction,
            "edge_type": edge_type,
            "source": source,
            "target": target,
        }
        if attributes is not None:
            self._values["attributes"] = attributes
        if flags is not None:
            self._values["flags"] = flags
        if metadata is not None:
            self._values["metadata"] = metadata
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def uuid(self) -> builtins.str:
        '''Universally unique identity.'''
        result = self._values.get("uuid")
        assert result is not None, "Required property 'uuid' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]]:
        '''Serializable entity attributes.

        :see: {@link Attributes }
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]]]], result)

    @builtins.property
    def flags(self) -> typing.Optional[typing.List[FlagEnum]]:
        '''Serializable entity flags.

        :see: {@link FlagEnum }
        '''
        result = self._values.get("flags")
        return typing.cast(typing.Optional[typing.List[FlagEnum]], result)

    @builtins.property
    def metadata(
        self,
    ) -> typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]]:
        '''Serializable entity metadata.

        :see: {@link Metadata }
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.List[_constructs_77d1e7e8.MetadataEntry]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Serializable entity tags.

        :see: {@link Tags }
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def direction(self) -> EdgeDirectionEnum:
        '''Indicates the direction in which the edge is directed.'''
        result = self._values.get("direction")
        assert result is not None, "Required property 'direction' is missing"
        return typing.cast(EdgeDirectionEnum, result)

    @builtins.property
    def edge_type(self) -> EdgeTypeEnum:
        '''Type of edge.'''
        result = self._values.get("edge_type")
        assert result is not None, "Required property 'edge_type' is missing"
        return typing.cast(EdgeTypeEnum, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''UUID of edge **source**  node (tail).'''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''UUID of edge **target**  node (head).'''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SGEdge(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StackNode(Node, metaclass=jsii.JSIIMeta, jsii_type="aws-pdk.cdk_graph.StackNode"):
    '''StackNode defines a cdk Stack.'''

    def __init__(self, props: IStackNodeProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__590aac6253a068cedebe162ee1aa92c4d1612c141dcb62376fb179332bfbf641)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isStackNode")
    @builtins.classmethod
    def is_stack_node(cls, node: Node) -> builtins.bool:
        '''Indicates if node is a {@link StackNode}.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0651e31384c6ac306157af7492f25129c1a687365abbf66a3398f0d021af6c32)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isStackNode", [node]))

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, node: Node) -> "StackNode":
        '''Gets the {@link StackNode} containing a given resource.

        :param node: -

        :throws: Error is node is not contained in a stack
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39608636d30a2bd59b0997c504e494b1545cb2042542995ea21ae5aa1d86b4eb)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast("StackNode", jsii.sinvoke(cls, "of", [node]))

    @jsii.member(jsii_name="addOutput")
    def add_output(self, node: OutputNode) -> None:
        '''Associate {@link OutputNode} with this stack.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2ad8b400cbb438831a15ca9a16942bb72628f576a40bcc65bcb8af4f7f28c3f)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "addOutput", [node]))

    @jsii.member(jsii_name="addParameter")
    def add_parameter(self, node: ParameterNode) -> None:
        '''Associate {@link ParameterNode} with this stack.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd793ebd99692a7e0ef130cc82fd9ac6a0ecf81a788c782d07e3e3cc395e28ed)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(None, jsii.invoke(self, "addParameter", [node]))

    @jsii.member(jsii_name="findOutput")
    def find_output(self, logical_id: builtins.str) -> OutputNode:
        '''Find {@link OutputNode} with *logicalId* defined by this stack.

        :param logical_id: -

        :throws: Error is no output found matching *logicalId*
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f30f1f177d63cd18b7584d98af04ab62b32c4176f595447cbd1cac04983c4a3)
            check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
        return typing.cast(OutputNode, jsii.invoke(self, "findOutput", [logical_id]))

    @jsii.member(jsii_name="findParameter")
    def find_parameter(self, parameter_id: builtins.str) -> ParameterNode:
        '''Find {@link ParameterNode} with *parameterId* defined by this stack.

        :param parameter_id: -

        :throws: Error is no parameter found matching *parameterId*
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8926b2187e3e5994254174752b35d287c1056901ed5e035bc00edb26562435eb)
            check_type(argname="argument parameter_id", value=parameter_id, expected_type=type_hints["parameter_id"])
        return typing.cast(ParameterNode, jsii.invoke(self, "findParameter", [parameter_id]))

    @jsii.member(jsii_name="mutateDestroy")
    def mutate_destroy(self, strict: typing.Optional[builtins.bool] = None) -> None:
        '''Destroys this node by removing all references and removing this node from the store.

        :param strict: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d9c8526d44b3801e35ea5b177050b07496dc498193bdde2cdd4ea667283c4de)
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
        return typing.cast(None, jsii.invoke(self, "mutateDestroy", [strict]))

    @jsii.member(jsii_name="mutateHoist")
    def mutate_hoist(self, new_parent: Node) -> None:
        '''Hoist *this node* to an *ancestor* by removing it from its current parent node and in turn moving it to the ancestor.

        :param new_parent: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cee4c94ce143978312df90300bd8873d88efc6c3a3077aabf1afd3c9aa87f0ee)
            check_type(argname="argument new_parent", value=new_parent, expected_type=type_hints["new_parent"])
        return typing.cast(None, jsii.invoke(self, "mutateHoist", [new_parent]))

    @jsii.member(jsii_name="mutateRemoveOutput")
    def mutate_remove_output(self, node: OutputNode) -> builtins.bool:
        '''Disassociate {@link OutputNode} from this stack.

        :param node: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3684cc592b26484e0d3ee6c6542bcff88f9b6c5db044974bad0a977c07de183e)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveOutput", [node]))

    @jsii.member(jsii_name="mutateRemoveParameter")
    def mutate_remove_parameter(self, node: ParameterNode) -> builtins.bool:
        '''Disassociate {@link ParameterNode} from this stack.

        :param node: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76d82dc962b1aba04296fa3a35a18a6bfe92780106dc9bef8ad62637a97378cd)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveParameter", [node]))

    @builtins.property
    @jsii.member(jsii_name="exports")
    def exports(self) -> typing.List[OutputNode]:
        '''Get all **exported** {@link OutputNode}s defined by this stack.'''
        return typing.cast(typing.List[OutputNode], jsii.get(self, "exports"))

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> typing.List[OutputNode]:
        '''Get all {@link OutputNode}s defined by this stack.'''
        return typing.cast(typing.List[OutputNode], jsii.get(self, "outputs"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.List[ParameterNode]:
        '''Get all {@link ParameterNode}s defined by this stack.'''
        return typing.cast(typing.List[ParameterNode], jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="stage")
    def stage(self) -> typing.Optional["StageNode"]:
        '''Get {@link StageNode} containing this stack.'''
        return typing.cast(typing.Optional["StageNode"], jsii.get(self, "stage"))


class StageNode(Node, metaclass=jsii.JSIIMeta, jsii_type="aws-pdk.cdk_graph.StageNode"):
    '''StageNode defines a cdk Stage.'''

    def __init__(self, props: ITypedNodeProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88c8b723d772619296d7a8df1e430aa057ec9d45cd827594f64f48be601015be)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isStageNode")
    @builtins.classmethod
    def is_stage_node(cls, node: Node) -> builtins.bool:
        '''Indicates if node is a {@link StageNode}.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a11622999bcfa39c0954982bf1b39365eab1e6e5626d1ce2b30401825997cd2)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isStageNode", [node]))

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, node: Node) -> "StageNode":
        '''Gets the {@link StageNode} containing a given resource.

        :param node: -

        :throws: Error is node is not contained in a stage
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7641c23e43b938d49c56083cc15ffb2f9f4856554b62d034d5efa377f20ff431)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast("StageNode", jsii.sinvoke(cls, "of", [node]))

    @jsii.member(jsii_name="addStack")
    def add_stack(self, stack: StackNode) -> None:
        '''Associate a {@link StackNode} with this stage.

        :param stack: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a0d249c66dc48bd6fe9d0b8828fab5e3cea75297c9d3b38b73a7040758a859b)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(None, jsii.invoke(self, "addStack", [stack]))

    @jsii.member(jsii_name="mutateRemoveStack")
    def mutate_remove_stack(self, stack: StackNode) -> builtins.bool:
        '''Disassociate {@link StackNode} from this stage.

        :param stack: -

        :destructive: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4be116585e82102b2f7a5d2406ba52090681049352c6260ffe6671d9f7d784a)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(builtins.bool, jsii.invoke(self, "mutateRemoveStack", [stack]))

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List[StackNode]:
        '''Gets all stacks contained by this stage.'''
        return typing.cast(typing.List[StackNode], jsii.get(self, "stacks"))


class AppNode(Node, metaclass=jsii.JSIIMeta, jsii_type="aws-pdk.cdk_graph.AppNode"):
    '''AppNode defines a cdk App.'''

    def __init__(self, props: IAppNodeProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3068a04437e2d3b339815e75ef0373566b9870ef8d4dab082f5f48553eada1c4)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isAppNode")
    @builtins.classmethod
    def is_app_node(cls, node: Node) -> builtins.bool:
        '''Indicates if node is a {@link AppNode}.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd843be7c005958850b81b954b35815384bdcd33e27969c3aed4b95c12ac1567)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isAppNode", [node]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PATH")
    def PATH(cls) -> builtins.str:
        '''Fixed path of the App.'''
        return typing.cast(builtins.str, jsii.sget(cls, "PATH"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="UUID")
    def UUID(cls) -> builtins.str:
        '''Fixed UUID for App node.'''
        return typing.cast(builtins.str, jsii.sget(cls, "UUID"))


class AttributeReference(
    Reference,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-pdk.cdk_graph.AttributeReference",
):
    '''Attribute type reference edge.'''

    def __init__(self, props: IAttributeReferenceProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e79388de81e35f7c5c04c75c0d9cec5dce256de534160060ba06ee7e6249c59e)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isAtt")
    @builtins.classmethod
    def is_att(cls, edge: Edge) -> builtins.bool:
        '''Indicates if edge in an **Fn::GetAtt** {@link Reference}.

        :param edge: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce89160b3d2b16e21117b3d1e23ea6d27a789430c39f80fb5a1061dce7f9fd3a)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isAtt", [edge]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATT_VALUE")
    def ATT_VALUE(cls) -> builtins.str:
        '''Attribute key for resolved value of attribute reference.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ATT_VALUE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PREFIX")
    def PREFIX(cls) -> builtins.str:
        '''Edge prefix to denote **Fn::GetAtt** type reference edge.'''
        return typing.cast(builtins.str, jsii.sget(cls, "PREFIX"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        '''Get the resolved attribute value.'''
        return typing.cast(builtins.str, jsii.get(self, "value"))


class CfnResourceNode(
    Node,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-pdk.cdk_graph.CfnResourceNode",
):
    '''CfnResourceNode defines an L1 cdk resource.'''

    def __init__(self, props: ICfnResourceNodeProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3bea70085eef8081d8a47b4d4649a7a4f3ff84deb87f8db128889dfbfd90f06)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isCfnResourceNode")
    @builtins.classmethod
    def is_cfn_resource_node(cls, node: Node) -> builtins.bool:
        '''Indicates if a node is a {@link CfnResourceNode}.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d38cd42a9f1fc22e5ba3d4d9ea8d8f20bd5a02005e96a10f975040c50a0a3ae9)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnResourceNode", [node]))

    @jsii.member(jsii_name="isEquivalentFqn")
    def is_equivalent_fqn(self, resource: ResourceNode) -> builtins.bool:
        '''Evaluates if CfnResourceNode fqn is equivalent to ResourceNode fqn.

        :param resource: - {@link Graph.ResourceNode } to compare.

        :return: Returns ``true`` if equivalent, otherwise ``false``

        Example::

            `aws-cdk-lib.aws_lambda.Function` => `aws-cdk-lib.aws_lambda.CfnFunction`
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f81b4819cda3659cfd256e9111bdb3c1c76b2cef67e9373972be55f5a5d83910)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isEquivalentFqn", [resource]))

    @jsii.member(jsii_name="mutateDestroy")
    def mutate_destroy(self, strict: typing.Optional[builtins.bool] = None) -> None:
        '''Destroys this node by removing all references and removing this node from the store.

        :param strict: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d9fee1f5b74884d1a34d96b540a10a01ed252830e6aa1f12edf419a761562cf)
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
        return typing.cast(None, jsii.invoke(self, "mutateDestroy", [strict]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ATT_IMPORT_ARN_TOKEN")
    def ATT_IMPORT_ARN_TOKEN(cls) -> builtins.str:
        '''Normalized CfnReference attribute.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ATT_IMPORT_ARN_TOKEN"))

    @builtins.property
    @jsii.member(jsii_name="isExtraneous")
    def is_extraneous(self) -> builtins.bool:
        '''Indicates if this node is considered a {@link FlagEnum.EXTRANEOUS} node or determined to be extraneous: - Clusters that contain no children.

        :inheritdoc: true
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isExtraneous"))

    @builtins.property
    @jsii.member(jsii_name="isImport")
    def is_import(self) -> builtins.bool:
        '''Indicates if this CfnResource is imported (eg: ``s3.Bucket.fromBucketArn``).'''
        return typing.cast(builtins.bool, jsii.get(self, "isImport"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> typing.Optional[ResourceNode]:
        '''Reference to the L2 Resource that wraps this L1 CfnResource if it is wrapped.'''
        return typing.cast(typing.Optional[ResourceNode], jsii.get(self, "resource"))


class Dependency(
    Edge,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-pdk.cdk_graph.Dependency",
):
    '''Dependency edge class defines CloudFormation dependency between resources.'''

    def __init__(self, props: ITypedEdgeProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36628c6a204802b0681869f5b9f9acd9eaebde564e5001cfba2430aacb6aa8a2)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isDependency")
    @builtins.classmethod
    def is_dependency(cls, edge: Edge) -> builtins.bool:
        '''Indicates if given edge is a {@link Dependency} edge.

        :param edge: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afe92838421ca1539a31bb4c15527134a3f66a6f7bf0a746c923ddeebb820000)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isDependency", [edge]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PREFIX")
    def PREFIX(cls) -> builtins.str:
        '''Edge prefix to denote dependency edge.'''
        return typing.cast(builtins.str, jsii.sget(cls, "PREFIX"))


@jsii.interface(jsii_type="aws-pdk.cdk_graph.INestedStackNodeProps")
class INestedStackNodeProps(IStackNodeProps, typing_extensions.Protocol):
    '''{@link NestedStackNode} props.'''

    @builtins.property
    @jsii.member(jsii_name="parentStack")
    def parent_stack(self) -> StackNode:
        '''Parent stack.'''
        ...


class _INestedStackNodePropsProxy(
    jsii.proxy_for(IStackNodeProps), # type: ignore[misc]
):
    '''{@link NestedStackNode} props.'''

    __jsii_type__: typing.ClassVar[str] = "aws-pdk.cdk_graph.INestedStackNodeProps"

    @builtins.property
    @jsii.member(jsii_name="parentStack")
    def parent_stack(self) -> StackNode:
        '''Parent stack.'''
        return typing.cast(StackNode, jsii.get(self, "parentStack"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INestedStackNodeProps).__jsii_proxy_class__ = lambda : _INestedStackNodePropsProxy


class ImportReference(
    Reference,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-pdk.cdk_graph.ImportReference",
):
    '''Import reference defines **Fn::ImportValue** type reference edge.'''

    def __init__(self, props: ITypedEdgeProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ddd1dd9d3d450888e5bffea084513aa17869b5a14c55f93f0aa8caf8e5c9b13)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isImport")
    @builtins.classmethod
    def is_import(cls, edge: Edge) -> builtins.bool:
        '''Indicates if edge is **Fn::ImportValue** based {@link Reference}.

        :param edge: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16fac6c6d5a2136120c493cc742c1f33908f37c1129f0d45992fcaf338874f52)
            check_type(argname="argument edge", value=edge, expected_type=type_hints["edge"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isImport", [edge]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PREFIX")
    def PREFIX(cls) -> builtins.str:
        '''Edge prefix to denote **Fn::ImportValue** type reference edge.'''
        return typing.cast(builtins.str, jsii.sget(cls, "PREFIX"))


class NestedStackNode(
    StackNode,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-pdk.cdk_graph.NestedStackNode",
):
    '''NestedStackNode defines a cdk NestedStack.'''

    def __init__(self, props: INestedStackNodeProps) -> None:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04cf8848087be042c07dfd80c6704feb8b78ff21c84c4808b90a4ffb8fe51e41)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="isNestedStackNode")
    @builtins.classmethod
    def is_nested_stack_node(cls, node: Node) -> builtins.bool:
        '''Indicates if node is a {@link NestedStackNode}.

        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a7984652f1ebc1034f9483760bc360e48124cac88d25f9e1ed8b8056227509f)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isNestedStackNode", [node]))

    @jsii.member(jsii_name="mutateHoist")
    def mutate_hoist(self, new_parent: Node) -> None:
        '''Hoist *this node* to an *ancestor* by removing it from its current parent node and in turn moving it to the ancestor.

        :param new_parent: -

        :inheritdoc: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb2253eb6d34afa6a9adf348ad3a89054243b0c5c5b446fa98e43315fb5a80dc)
            check_type(argname="argument new_parent", value=new_parent, expected_type=type_hints["new_parent"])
        return typing.cast(None, jsii.invoke(self, "mutateHoist", [new_parent]))

    @builtins.property
    @jsii.member(jsii_name="parentStack")
    def parent_stack(self) -> typing.Optional[StackNode]:
        '''Get parent stack of this nested stack.'''
        return typing.cast(typing.Optional[StackNode], jsii.get(self, "parentStack"))


__all__ = [
    "AppNode",
    "AttributeReference",
    "BaseEntity",
    "CdkConstructIds",
    "CdkGraph",
    "CdkGraphArtifact",
    "CdkGraphArtifacts",
    "CdkGraphContext",
    "CfnAttributesEnum",
    "CfnResourceNode",
    "ConstructInfo",
    "ConstructInfoFqnEnum",
    "Dependency",
    "Edge",
    "EdgeDirectionEnum",
    "EdgeTypeEnum",
    "FilterPreset",
    "FilterStrategy",
    "FilterValue",
    "Filters",
    "FlagEnum",
    "IAppNodeProps",
    "IAttributeReferenceProps",
    "IBaseEntityDataProps",
    "IBaseEntityProps",
    "ICdkGraphPlugin",
    "ICdkGraphProps",
    "ICfnResourceNodeProps",
    "IEdgePredicate",
    "IEdgeProps",
    "IFilter",
    "IFilterFocusCallback",
    "IFindEdgeOptions",
    "IFindNodeOptions",
    "IGraphFilter",
    "IGraphFilterPlan",
    "IGraphFilterPlanFocusConfig",
    "IGraphPluginBindCallback",
    "IGraphReportCallback",
    "IGraphStoreFilter",
    "IGraphSynthesizeCallback",
    "IGraphVisitorCallback",
    "INestedStackNodeProps",
    "INodePredicate",
    "INodeProps",
    "IOutputNodeProps",
    "IParameterNodeProps",
    "IReferenceProps",
    "IResourceNodeProps",
    "ISerializableEdge",
    "ISerializableEntity",
    "ISerializableGraphStore",
    "ISerializableNode",
    "IStackNodeProps",
    "IStoreCounts",
    "ITypedEdgeProps",
    "ITypedNodeProps",
    "ImportReference",
    "InferredNodeProps",
    "MetadataTypeEnum",
    "NestedStackNode",
    "Node",
    "NodeTypeEnum",
    "OutputNode",
    "ParameterNode",
    "PlainObject",
    "Reference",
    "ReferenceTypeEnum",
    "ResourceNode",
    "RootNode",
    "SGEdge",
    "SGEntity",
    "SGGraphStore",
    "SGNode",
    "SGUnresolvedReference",
    "StackNode",
    "StageNode",
    "Store",
]

publication.publish()

def _typecheckingstub__27c0cd401dadd0588452f1c1fae52718266f81e977ff9050ff78dcccfc0061d2(
    root: _constructs_77d1e7e8.Construct,
    *,
    plugins: typing.Optional[typing.Sequence[ICdkGraphPlugin]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5d82cab11551fcff2f6299519c75d5a93c746fbe6dfe8fbde7907683afd2b05(
    *,
    filename: builtins.str,
    filepath: builtins.str,
    id: builtins.str,
    source: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81d647d056df85d7e9a08428ddffd79e799c8b938e7fc1bef8c7d407f82c6a04(
    store: Store,
    outdir: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e16b57de7ebe5b23f364abe4879e95b0dd49cd7e83223e6b491ce5e40118f00(
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf66d947af8fa192724e3f4300774ff37a03388b3e4aea4074df2e2f4090770d(
    filename: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cf12c69a297801d655846dae260d45c9d599a7622f2a7f45c4d3c8a23b4ece6(
    source: typing.Union[CdkGraph, ICdkGraphPlugin],
    id: builtins.str,
    filepath: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5b3da94247e169bc2d88970ff455d7a307e1e3b605f1fdff0b9a65746e6f714(
    source: typing.Union[CdkGraph, ICdkGraphPlugin],
    id: builtins.str,
    filename: builtins.str,
    data: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195e54720f463a462c44f63ad105f7349df2eee3da6f49d9ba35c8c0319ac6bb(
    *,
    fqn: builtins.str,
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0695bb07e020bdbc6bac5a911e6ab1f1502e5347a5cb9e050d281bf05be5941b(
    *,
    regex: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8629401beba8ab9f067d55546a5ee55a1c37335f829a6c553e3b96d8cf88e2bc(
    cfn_types: typing.Sequence[typing.Union[FilterValue, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a81614a43e7cf62541648ca269c11c3a23f8573738aa72ba6f7bed7ba9a641e9(
    node_types: typing.Sequence[typing.Union[FilterValue, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcceca9ffcce9781c83f4f4fea91d82aeb5a4ac97cc7cfed47b1f20180e05b3a(
    cfn_types: typing.Sequence[typing.Union[FilterValue, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08a61543609b4769faeba386592504091bbd2467ea05f2b8b438803edf2c72e6(
    node_types: typing.Sequence[typing.Union[FilterValue, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3265a83360e0a421b9bff4299ba5e2032b313b98a8b232cb2f39c2fd87deee7(
    cluster_types: typing.Optional[typing.Sequence[NodeTypeEnum]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e7145a4cf4d60e5ecd33563cbc93b575d2b0cb54a29ed65bd480f3cfced5b06(
    store: Store,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec3ef32f6ccb0052708916e41815fb90eef21f2a6a4166f10f81355024fc3ae(
    value: IGraphPluginBindCallback,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10f09faa94a1e661dc734f7fe17dd01bc53a6d99cdd7cb89c29b22872f935c3d(
    value: typing.Optional[IGraphVisitorCallback],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fce80a55da3622644d29ec84456917eb0beec770e0518163aa866c07a74e63c2(
    value: typing.Optional[IGraphReportCallback],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__327e61b18f62c219319411532c743a133ca4ccf49b67778fe14192f2d7d48295(
    value: typing.Optional[IGraphSynthesizeCallback],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f41f7d3ea20834a84a5383430600b13d06568854f927c95f668f009d4b6b3eec(
    *,
    plugins: typing.Optional[typing.Sequence[ICdkGraphPlugin]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5104b846228daa4b8c1327d05b0f107eccc2bc188eadb4c78f3bf8d9f1966b09(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e372c28af11eeb9c028663f92cca63cb2113a713369c52ab35590d6c7aac4a94(
    *,
    graph: typing.Optional[typing.Union[IGraphFilter, typing.Dict[builtins.str, typing.Any]]] = None,
    store: typing.Optional[IGraphStoreFilter] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7461ffa3e5819d67add5a1801ca2dc33b32fe7c91ac20ab346e8f1a4583dd300(
    store: Store,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be88ede9716eae25ace453020f7c5b190ff0cdc34d57f31ced2e412d4b3c8da8(
    value: typing.Optional[_constructs_77d1e7e8.ConstructOrder],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dffad915d3f4eece0462979b246e33b227765e2e3c13712ab80a2caad005998a(
    value: typing.Optional[IEdgePredicate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__111fb97b7ffc01e9032f0bfd6f545b8285bb3d991e206bf3d9ce52b6e13cca09(
    value: typing.Optional[builtins.bool],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81452004140db3cdc6d913f09e8a0cad6783c636889e27996cd92075d886026d(
    value: typing.Optional[_constructs_77d1e7e8.ConstructOrder],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ab65295afddf6807d1aaa7a7feefb126d17fb6c48a4ff4876355df9276f1104(
    value: typing.Optional[INodePredicate],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__840da42ae2fc1e59d55f4dfbb9303d1aa93fee75f0d64b0effb1b828bb2e79bf(
    *,
    all_nodes: typing.Optional[builtins.bool] = None,
    edge: typing.Optional[IEdgePredicate] = None,
    inverse: typing.Optional[builtins.bool] = None,
    node: typing.Optional[INodePredicate] = None,
    strategy: typing.Optional[FilterStrategy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ccb6194666839ca5d5cb519d9346bdf8d90cb2b378883da4fe080c7887dc09c(
    *,
    all_nodes: typing.Optional[builtins.bool] = None,
    filters: typing.Optional[typing.Sequence[typing.Union[IFilter, typing.Dict[builtins.str, typing.Any]]]] = None,
    focus: typing.Optional[typing.Union[IGraphFilterPlanFocusConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    order: typing.Optional[_constructs_77d1e7e8.ConstructOrder] = None,
    preset: typing.Optional[FilterPreset] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e394bd3f78468d03deb74b83a2ce7cf9270776ac045d8a8e9f3ed619d1070559(
    *,
    filter: IFilterFocusCallback,
    no_hoist: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9410ad2f608ab5a52bfc6304fa30426823a4b1855524b07676969f9da1dc191e(
    store: Store,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad4271c60ee6c959db9db1ea974a08da8f6ec89f3fc7ddf8a7d8d52f99d5ed98(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c4298dbc4d14316130bfb52fe6d8e564a020dfe8b99ce11a210e9bb9c552173(
    *,
    uuid: builtins.str,
    attributes: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]]] = None,
    flags: typing.Optional[typing.Sequence[FlagEnum]] = None,
    metadata: typing.Optional[typing.Sequence[typing.Union[_constructs_77d1e7e8.MetadataEntry, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34a52c739dad71eb3b97fd79836a41dbfb17d6e665d15dc52ab667582094ffae(
    *,
    edges: typing.Sequence[typing.Union[SGEdge, typing.Dict[builtins.str, typing.Any]]],
    tree: typing.Union[SGNode, typing.Dict[builtins.str, typing.Any]],
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d435ebf5b1908bfd33e7828e8120584949ceff2333073d1ffcfc51a86ef85dd4(
    *,
    uuid: builtins.str,
    attributes: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]]] = None,
    flags: typing.Optional[typing.Sequence[FlagEnum]] = None,
    metadata: typing.Optional[typing.Sequence[typing.Union[_constructs_77d1e7e8.MetadataEntry, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    id: builtins.str,
    node_type: NodeTypeEnum,
    path: builtins.str,
    cfn_type: typing.Optional[builtins.str] = None,
    children: typing.Optional[typing.Mapping[builtins.str, typing.Union[SGNode, typing.Dict[builtins.str, typing.Any]]]] = None,
    construct_info: typing.Optional[typing.Union[ConstructInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    edges: typing.Optional[typing.Sequence[builtins.str]] = None,
    logical_id: typing.Optional[builtins.str] = None,
    parent: typing.Optional[builtins.str] = None,
    stack: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aa3d2ca6809903d0c1c1007c08a3af3aa7c7b0d99bfe4ddd6b7fecde5920a22(
    *,
    reference_type: ReferenceTypeEnum,
    source: builtins.str,
    target: builtins.str,
    value: typing.Optional[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c45d72e0054b126e56496c4ce2a10ee06961c134ccbf0faecfb2f64d5d156523(
    allow_destructive_mutations: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__335c616a8314affc9fe4b7086b907b674a8da8b27da8d2f63a766b87dcffde22(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1a099a580cbeb023b54267c1b9878d7f478c99bb20555bf165780237d8a619(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__588ba0c5a3a0dac34251b68e97e9c44c67932aac318a97061378db2f1d23c965(
    stack: StackNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb7569264399acfbfb90d5aa050eeff17baed229adae68b4dcf2ac2d71e522a6(
    stage: StageNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed18acd48a1a5beb1bb89d3eee9d8f0a0285253129176d9fcbc2b25516eddbe3(
    allow_destructive_mutations: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ea44fc5d181e0cf068fa4129788a74ff74367b6d4f463978405b6d267b7d87(
    stack: StackNode,
    logical_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__582eed54711f17977a95af99dbe2108fbf969bcf9385fffc44f1677b386ace2b(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec309c80416841f360acb7624800ed5cdddedec2dd6c57f30a8317d67d0b4cd2(
    stack: StackNode,
    logical_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37ae0302916f9100547ab1f26b6ceedf23ba65bc23b3f2b7653559479191544(
    uid: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98bb3d9a7f041be77d073f12f70b7408b4b8fa058939343f6b01b1b2c5074316(
    uuid: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9df12223d11a345cbcb9cb57a082c1ef151d6f3f2fd59b572f58b3b5612a32(
    uuid: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31fb4e2eff7befd95a27ebc6715d47be47b3550641a63c2a3d60d5ced1760df8(
    uuid: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcf168d106c59be24c47311b2428c41642e7c2c969148c39596ac1ab07b945f4(
    uuid: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f520ec94ffdd0afa2ce964d73a479ea7130635d3bc90e7d70366b068b725afb(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ec35cd5062bb3b84eba76df1785554984bfef15367cf3af5a9f9765f9b9c80d(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4555fcf416c414465d91a9a0b679ed2f5cca937866e3b6cbe6c2067a93d2b682(
    arn_token: builtins.str,
    resource: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8580bf6d78ed80f02af00ee71fda2b1988ed2847a318f3320d727cd7de2e54a(
    stack: StackNode,
    logical_id: builtins.str,
    resource: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b940bd9a4a4c2d38a71391c1d42165194cc345bb0824366700599aae6db3e1(
    props: IBaseEntityProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b1c4c627b858975af0e5487ad5e1acc512ce053447f149f2a167c14443a359c(
    key: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49650010b6731e36ec20882aec595ef28b66f6840da8cfcb86ea68423c55fb0e(
    flag: FlagEnum,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18c27ec4f07f61e9a6c86f2f37905e3c29b62e16547c0c9626e9cfa1e1edd8aa(
    metadata_type: builtins.str,
    data: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02a58d59b46c96be9085ed903fa96d25a78036d69b02b701bebc8e424970dc36(
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f76c419e91f82c7f73ec1de78a72e72fca4fe5de6ab303fdec9954eaa54a29b(
    data: IBaseEntityDataProps,
    overwrite: typing.Optional[builtins.bool] = None,
    apply_flags: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__778d54204d04976cbf2decdd42cdc6b13714d26edd6fd4b74fc70164d0158bdf(
    metadata_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b9e505ed524dbf121193f8044949f9e28ee8641817667e03e7084dfe003ad13(
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64987e8e7e28f42c60371e62806aa0197ee7cd9a02af8c3327d1a3cb1c8f20d3(
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4af255296cac152f625d15dd62ab4c241ce5fc919bd994a038e78cb5947c9bae(
    key: builtins.str,
    value: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6be01caa1b4b8b4e3d74fc44cbe6cc4c197a9e89b837b14fec578250b0ab0519(
    flag: FlagEnum,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77b017330c657e60671de0a279b75114d7fe3ab2420a36da7d33bcc8b7829c6d(
    metadata_type: builtins.str,
    data: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a66cabe9a9fdf3171e68dfe81dfe7ec7f026ad9a63f45ff970771501fa193fbb(
    key: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__247b9f93aba2c1ac53d20f2c7a52841da482b5ddcbb73e6a22b5f6ef671e3a2d(
    key: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__debfcb941751c761cb39b0745cb3cff09acdf97df6b8257c6edd9ce3515254dc(
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99ee3f72791f8a9a48462c55518e9749803916a029b9443c7170ddceb15b9d5c(
    strict: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c923c62f7fba1f4e39d79d6fc22d32315d3a1533a31dfe82ea42349955f26253(
    props: IEdgeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41aa4c7fc4c2053cfa79e7e4048a16c8445adda20e2f1674f69dbaaca4c85a60(
    chain: typing.Sequence[typing.Any],
    predicate: IEdgePredicate,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8df4c980e3b05dd72ec3bdfd846ccc9f5ce648bdf083abf26da71bb79d157a73(
    chain: typing.Sequence[typing.Any],
    predicate: IEdgePredicate,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae9ce2c39f795eb5043aa7e58c1c19469412ce091e346f78d50de410987f935d(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2c577a6bd65d6a64d26ce8586979f63c6bd2853876f21b37ac7e128296bdfd7(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6617bb51d2ca010bd03c333ffb5ce299f8d9139e9584ffd57d62d604a1f808f(
    _strict: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__153a587294604c6162e3494be66889c2f74337a568c0c304a0e9bbdf1278326a(
    direction: EdgeDirectionEnum,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae65196193cf0a9355730fd93ac666a87554187ec519ded9d28790f2b7bdc0b(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e71af489fe71f57f9d69977b2d17497bd61be3099e05ad7b4fa2dfcac709ca3(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cb4455c6155f299476a670d0e997b71808f20671144d43b0bee567bac569469(
    value: typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject, typing.List[typing.Union[builtins.str, jsii.Number, builtins.bool, PlainObject]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be6be7326a849c07dcb81fa86dc40a866bea3e67d81c9cb2af912bc8abf833aa(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e96a1c36c84cd0c68af3453ab9f4614eda7c4ff0396c1167687cf813b028f08(
    value: typing.Optional[NodeTypeEnum],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b20346f45e8bac075c89073c4606cb664ea583a1c99e2b774a4e4a9e26abec4b(
    value: typing.Optional[ReferenceTypeEnum],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf761bb7345ddde31b7cf06cecfa7654aebe72dec96d1b36ea8a395e665dc081(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8b37654d569fb5b8f855a3c9d00105a89e908b61d75450afffc30dd6355bd3c(
    value: typing.Optional[NodeTypeEnum],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ecd1f4d261ce04fdf1452fd6236792aab4dbd879fcb8e34e4fa9c0cbf5b1a53(
    value: typing.Optional[NodeTypeEnum],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2acae948798ac3e9e02923a9fc8f2b3bc10974e35a8b296e0ce46b6b324973e(
    *,
    uuid: builtins.str,
    attributes: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]]] = None,
    flags: typing.Optional[typing.Sequence[FlagEnum]] = None,
    metadata: typing.Optional[typing.Sequence[typing.Union[_constructs_77d1e7e8.MetadataEntry, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    dependencies: typing.Sequence[builtins.str],
    unresolved_references: typing.Sequence[typing.Union[SGUnresolvedReference, typing.Dict[builtins.str, typing.Any]]],
    cfn_type: typing.Optional[builtins.str] = None,
    construct_info: typing.Optional[typing.Union[ConstructInfo, typing.Dict[builtins.str, typing.Any]]] = None,
    logical_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4de5b09f927d57df12f03be58ace29ba4c140ec92e2fa59d823bc4d75c65ca1c(
    props: INodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__822deab54197c7dba7e8d8cb7e80f33afdbba819d26325847b05914e1ab6b977(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92c69958865778a5cd6c7a44298d37111bd3877e80fb8e8fe2e99a907a3f4be9(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9287497ed897a1b295091b45a78b0138ee423db55dd248100f2d2eca69539b7a(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0e60875e94de5c2a9e32e8fdfe6a2fb629225df645b603ad29554a65521f7cf(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e98a3325514ea8432e2e8904f0259b4c3bc27af36ec1e0a0dabe641c5938d582(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bbf6cf8a35ed3e35067d0679cc7f9b2aee3f745a16bbaff31f21f752664f5b0(
    predicate: INodePredicate,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6fc2a3a6249ddd91300d2abc294c7192eff6bead218f435962c6007c14e0bba(
    options: typing.Optional[IFindNodeOptions] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eece34c91b06c0696c58f0b3937c6b8b3fe81418cf88b58c9dc13a3b1340eee(
    options: typing.Optional[IFindEdgeOptions] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__726632e2a9d796041bf110c2b084edeca68991dec231f118848aa8e8b21a1981(
    predicate: INodePredicate,
    max: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20d053b5fec926c5b50fb68503293367d164bfb4564c1b916b306a99ba68cbf3(
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8b0fbb510b384c1fa0b6acde8f86d1d0ce87073628b74fc37d4425c97a9b6d1(
    predicate: IEdgePredicate,
    reverse: typing.Optional[builtins.bool] = None,
    follow: typing.Optional[builtins.bool] = None,
    direct: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ebd234a21944255ce7a3bf46c98de05f9b060c0975f591be9e42ccc10fbe1e(
    predicate: IEdgePredicate,
    reverse: typing.Optional[builtins.bool] = None,
    follow: typing.Optional[builtins.bool] = None,
    direct: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc4489bb29c0dc7a340d7b85fffe41c572b9326c7053686630729dadf5e78df0(
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95ecc4c3f12cecd2503192a369c960bd31175714b90e2013b3ffaa54ea7be73f(
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__080aecd0422d40fd61753e5b7b7579c8f5acf9826b5bf5a4f84b8e1e88f76a65(
    reverse: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24390e5e28533a0151b46f1d6d1bc717c4045cfba51f28688db9b249718dcb0d(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a6376857f895fa88fa486841fc445ae09d54f2e973f92359dd41a6869d1b08f(
    ancestor: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72c281234d936d64eab0583e21a5cead88187f32f5d4ed0062f8e63e5f44db99(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30a49bf003e095e6e8742bb86271798506e8e46a6fc34ebb223904c1ad140d61(
    ancestor: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3d379a902ce679e3cebc333e6e6f2cc75ef5ab9bb08d6ff9f61180e6683e781(
    strict: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed3665b9a2a6c5a93a3d4999028e70630a5cd738c82689f4e290118ad177873(
    new_parent: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a674cdc8e325d84bdbfe1dbd39a2d8b78daf6848f004711b308462aae3897d4e(
    new_parent: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17f7df7fbbe01468d577cc8d08e9c83043808cc84720675a256302c06b838f1f(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3cd9997bbf7b1107341c7746a015a44f76cf17a58af3da4c25497fdb9aea274(
    link: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94701de03510debf27fa071300acf639253ed529c495ae61ed4350beda741691(
    link: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1fd6fb2bd31ca0a711fbe639b40353deb37a3a2ba5c57893f31f5fd610c6725(
    props: IOutputNodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e2c3cc672265efde96974d40877e2a5be5217155a14a90f9d56cd0bafed9c14(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8b091eb51e6eb2bd1d856fe4020eeb8dca3fb5c7af39d0100de3623b0fd1ecd(
    strict: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51225a1d733befcee7640052187873b7edb06412a37d44126772532d11386cec(
    props: IParameterNodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b77fe15850f537de7f8f30c0d2e0be8092ed0a3be8aa9d12b29f1c8133086e1(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2978043840e2d17ee52ec9a18825cab34ab1e02e0e25509e8358a5c778c105f7(
    strict: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e70ff4d6f7671822a057ae6a06256f4a86380c90fcbbc00fd06bfcd238e14ab(
    props: IReferenceProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa48dcc02db2c6f903ba1d45fed9966f4e1b48ca2ef148f70c34c41f471b4200(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__775825c91a05498f95a2a4ad0eaceeb37d055357936d920eca3ea922f8f67e76(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b8a5191e9d681773ced3070c7c959320beb61067aa93abadcab503ddd27eaef(
    props: IResourceNodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__621a3bf7faf19f2a14e8669f5c56819be04579b841ea8fab0e085de855a84375(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8132a28cf569d50c469b3a4d805a0ee10ee428005027bf0decb5c9148b549c69(
    cfn_resource: typing.Optional[CfnResourceNode] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df7273148d4e4651115533e8713c91dcf62db903d2ceccea9c4550784c999dd0(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed0a649be00d48d3240cd359fc9a3209f3800891b33b9b3a1695d2935c3366b7(
    store: Store,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4da2a06f28639ec500a9e0d6f2c994ab4d6c86939356117317ac2a0a8a554131(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4605265ca1a29a320ed54ce5c386cd4b3eaaf469030150f182e85cc9fb4f7fd4(
    options: typing.Optional[IFindNodeOptions] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f09f0ee53c4d93c2d042b780b8b154fe70ddde62aad07e5583a7bec87703fff7(
    _ancestor: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab8acf700c048bcde2989edf7b007d36b2c7f69c6ce6d6fd6ce288db08717f04(
    _strict: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18dba6f843f37b8527da73f88894707657ee31ea2b55d42af96c8708c045ae31(
    _new_parent: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fabddd2d6e7dbb1948d1fe7198dd1d701a842fa5891d20acd1b2a2319c634390(
    *,
    uuid: builtins.str,
    attributes: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[builtins.str, jsii.Number, builtins.bool, typing.Union[PlainObject, typing.Dict[builtins.str, typing.Any]]]]]]] = None,
    flags: typing.Optional[typing.Sequence[FlagEnum]] = None,
    metadata: typing.Optional[typing.Sequence[typing.Union[_constructs_77d1e7e8.MetadataEntry, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    direction: EdgeDirectionEnum,
    edge_type: EdgeTypeEnum,
    source: builtins.str,
    target: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__590aac6253a068cedebe162ee1aa92c4d1612c141dcb62376fb179332bfbf641(
    props: IStackNodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0651e31384c6ac306157af7492f25129c1a687365abbf66a3398f0d021af6c32(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39608636d30a2bd59b0997c504e494b1545cb2042542995ea21ae5aa1d86b4eb(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2ad8b400cbb438831a15ca9a16942bb72628f576a40bcc65bcb8af4f7f28c3f(
    node: OutputNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd793ebd99692a7e0ef130cc82fd9ac6a0ecf81a788c782d07e3e3cc395e28ed(
    node: ParameterNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f30f1f177d63cd18b7584d98af04ab62b32c4176f595447cbd1cac04983c4a3(
    logical_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8926b2187e3e5994254174752b35d287c1056901ed5e035bc00edb26562435eb(
    parameter_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d9c8526d44b3801e35ea5b177050b07496dc498193bdde2cdd4ea667283c4de(
    strict: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cee4c94ce143978312df90300bd8873d88efc6c3a3077aabf1afd3c9aa87f0ee(
    new_parent: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3684cc592b26484e0d3ee6c6542bcff88f9b6c5db044974bad0a977c07de183e(
    node: OutputNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d82dc962b1aba04296fa3a35a18a6bfe92780106dc9bef8ad62637a97378cd(
    node: ParameterNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88c8b723d772619296d7a8df1e430aa057ec9d45cd827594f64f48be601015be(
    props: ITypedNodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a11622999bcfa39c0954982bf1b39365eab1e6e5626d1ce2b30401825997cd2(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7641c23e43b938d49c56083cc15ffb2f9f4856554b62d034d5efa377f20ff431(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a0d249c66dc48bd6fe9d0b8828fab5e3cea75297c9d3b38b73a7040758a859b(
    stack: StackNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4be116585e82102b2f7a5d2406ba52090681049352c6260ffe6671d9f7d784a(
    stack: StackNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3068a04437e2d3b339815e75ef0373566b9870ef8d4dab082f5f48553eada1c4(
    props: IAppNodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd843be7c005958850b81b954b35815384bdcd33e27969c3aed4b95c12ac1567(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e79388de81e35f7c5c04c75c0d9cec5dce256de534160060ba06ee7e6249c59e(
    props: IAttributeReferenceProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce89160b3d2b16e21117b3d1e23ea6d27a789430c39f80fb5a1061dce7f9fd3a(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3bea70085eef8081d8a47b4d4649a7a4f3ff84deb87f8db128889dfbfd90f06(
    props: ICfnResourceNodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d38cd42a9f1fc22e5ba3d4d9ea8d8f20bd5a02005e96a10f975040c50a0a3ae9(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f81b4819cda3659cfd256e9111bdb3c1c76b2cef67e9373972be55f5a5d83910(
    resource: ResourceNode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d9fee1f5b74884d1a34d96b540a10a01ed252830e6aa1f12edf419a761562cf(
    strict: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36628c6a204802b0681869f5b9f9acd9eaebde564e5001cfba2430aacb6aa8a2(
    props: ITypedEdgeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afe92838421ca1539a31bb4c15527134a3f66a6f7bf0a746c923ddeebb820000(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ddd1dd9d3d450888e5bffea084513aa17869b5a14c55f93f0aa8caf8e5c9b13(
    props: ITypedEdgeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16fac6c6d5a2136120c493cc742c1f33908f37c1129f0d45992fcaf338874f52(
    edge: Edge,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04cf8848087be042c07dfd80c6704feb8b78ff21c84c4808b90a4ffb8fe51e41(
    props: INestedStackNodeProps,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7984652f1ebc1034f9483760bc360e48124cac88d25f9e1ed8b8056227509f(
    node: Node,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb2253eb6d34afa6a9adf348ad3a89054243b0c5c5b446fa98e43315fb5a80dc(
    new_parent: Node,
) -> None:
    """Type checking stubs"""
    pass
