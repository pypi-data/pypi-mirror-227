# NOTE: This is an auto-generated file. All modifications will be overwritten.
# type: ignore
from __future__ import annotations

from typing import Any, TypedDict, Optional
from enum import IntEnum

from polywrap import (
    Uri,
    Client,
    GenericMap,
    PolywrapClient,
    PolywrapClientConfigBuilder,
    sys_bundle,
    web3_bundle
)


### Env START ###

### Env END ###

### Objects START ###

### Objects END ###

### Enums START ###
### Enums END ###

### Imported Objects START ###

# URI: "wrapscan.io/polywrap/ipfs-http-client@1.0" #
IpfsCatOptions = TypedDict("IpfsCatOptions", {
    "offset": Optional[int],
    "length": Optional[int],
}, total=False)

# URI: "wrapscan.io/polywrap/ipfs-http-client@1.0" #
IpfsAddOptions = TypedDict("IpfsAddOptions", {
    "pin": Optional[bool],
    "onlyHash": Optional[bool],
    "wrapWithDirectory": Optional[bool],
}, total=False)

# URI: "wrapscan.io/polywrap/ipfs-http-client@1.0" #
IpfsResolveOptions = TypedDict("IpfsResolveOptions", {
    "recursive": Optional[bool],
    "dhtRecordCount": Optional[int],
    "dhtTimeout": Optional[str],
}, total=False)

# URI: "wrapscan.io/polywrap/ipfs-http-client@1.0" #
IpfsResolveResult = TypedDict("IpfsResolveResult", {
    "cid": str,
    "provider": str,
}, total=False)

# URI: "wrapscan.io/polywrap/ipfs-http-client@1.0" #
IpfsAddResult = TypedDict("IpfsAddResult", {
    "name": str,
    "hash": str,
    "size": str,
}, total=False)

# URI: "wrapscan.io/polywrap/ipfs-http-client@1.0" #
IpfsFileEntry = TypedDict("IpfsFileEntry", {
    "name": str,
    "data": bytes,
}, total=False)

# URI: "wrapscan.io/polywrap/ipfs-http-client@1.0" #
IpfsDirectoryEntry = TypedDict("IpfsDirectoryEntry", {
    "name": str,
    "directories": Optional[list["IpfsDirectoryEntry"]],
    "files": Optional[list["IpfsFileEntry"]],
}, total=False)

# URI: "wrapscan.io/polywrap/ipfs-http-client@1.0" #
IpfsBlob = TypedDict("IpfsBlob", {
    "directories": Optional[list["IpfsDirectoryEntry"]],
    "files": Optional[list["IpfsFileEntry"]],
}, total=False)

### Imported Objects END ###

### Imported Enums START ###


### Imported Enums END ###

### Imported Modules START ###

# URI: "wrapscan.io/polywrap/ipfs-http-client@1.0" #
IpfsModuleArgsCat = TypedDict("IpfsModuleArgsCat", {
    "cid": str,
    "ipfsProvider": str,
    "timeout": Optional[int],
    "catOptions": Optional["IpfsCatOptions"],
}, total=False)

# URI: "wrapscan.io/polywrap/ipfs-http-client@1.0" #
IpfsModuleArgsResolve = TypedDict("IpfsModuleArgsResolve", {
    "cid": str,
    "ipfsProvider": str,
    "timeout": Optional[int],
    "resolveOptions": Optional["IpfsResolveOptions"],
}, total=False)

# URI: "wrapscan.io/polywrap/ipfs-http-client@1.0" #
IpfsModuleArgsAddFile = TypedDict("IpfsModuleArgsAddFile", {
    "data": "IpfsFileEntry",
    "ipfsProvider": str,
    "timeout": Optional[int],
    "addOptions": Optional["IpfsAddOptions"],
}, total=False)

# URI: "wrapscan.io/polywrap/ipfs-http-client@1.0" #
IpfsModuleArgsAddDir = TypedDict("IpfsModuleArgsAddDir", {
    "data": "IpfsDirectoryEntry",
    "ipfsProvider": str,
    "timeout": Optional[int],
    "addOptions": Optional["IpfsAddOptions"],
}, total=False)

# URI: "wrapscan.io/polywrap/ipfs-http-client@1.0" #
IpfsModuleArgsAddBlob = TypedDict("IpfsModuleArgsAddBlob", {
    "data": "IpfsBlob",
    "ipfsProvider": str,
    "timeout": Optional[int],
    "addOptions": Optional["IpfsAddOptions"],
}, total=False)

# URI: "wrapscan.io/polywrap/ipfs-http-client@1.0" #
class Ipfs:
    _default_client: Client
    _default_uri: Uri
    _default_env: Optional[Any]

    def __init__(
        self,
        client: Optional[Client] = None,
        env: Optional[Any] = None,
        uri: Optional[Uri] = None,
    ):
        self._default_client = self._get_client(client)
        self._default_uri = self._get_uri(uri)
        self._default_env = self._get_env(env)

    def _get_client(self, client: Optional[Client]) -> Client:
        return client or getattr(self, "_default_client", None) or self._get_default_client()

    def _get_uri(self, uri: Optional[Uri]) -> Uri:
        return uri or getattr(self, "_default_uri", None) or self._get_default_uri() 

    def _get_env(self, env: Optional[Any]) -> Any:
        return env or getattr(self, "_default_env", None) or self._get_default_env()

    def _get_default_client(self) -> Client:
        config = (
            PolywrapClientConfigBuilder()
            .add_bundle(sys_bundle)
            .add_bundle(web3_bundle)
            .build()
        )
        return PolywrapClient(config)

    def _get_default_uri(self) -> Optional[Uri]:
        return Uri.from_str("wrapscan.io/polywrap/ipfs-http-client@1.0")

    def _get_default_env(self) -> Any:
        return None

    def cat(
        self,
        args: IpfsModuleArgsCat,
        client: Optional[Client] = None,
        env: Optional[Any] = None,
        uri: Optional[Uri] = None,
    ) -> bytes:
        _client = self._get_client(client)
        _env = self._get_env(env)
        _uri = self._get_uri(uri)

        return _client.invoke(
            uri=_uri,
            method="cat",
            args=args,
            env=_env,
        )

    def resolve(
        self,
        args: IpfsModuleArgsResolve,
        client: Optional[Client] = None,
        env: Optional[Any] = None,
        uri: Optional[Uri] = None,
    ) -> "IpfsResolveResult":
        _client = self._get_client(client)
        _env = self._get_env(env)
        _uri = self._get_uri(uri)

        return _client.invoke(
            uri=_uri,
            method="resolve",
            args=args,
            env=_env,
        )

    def add_file(
        self,
        args: IpfsModuleArgsAddFile,
        client: Optional[Client] = None,
        env: Optional[Any] = None,
        uri: Optional[Uri] = None,
    ) -> "IpfsAddResult":
        _client = self._get_client(client)
        _env = self._get_env(env)
        _uri = self._get_uri(uri)

        return _client.invoke(
            uri=_uri,
            method="addFile",
            args=args,
            env=_env,
        )

    def add_dir(
        self,
        args: IpfsModuleArgsAddDir,
        client: Optional[Client] = None,
        env: Optional[Any] = None,
        uri: Optional[Uri] = None,
    ) -> list["IpfsAddResult"]:
        _client = self._get_client(client)
        _env = self._get_env(env)
        _uri = self._get_uri(uri)

        return _client.invoke(
            uri=_uri,
            method="addDir",
            args=args,
            env=_env,
        )

    def add_blob(
        self,
        args: IpfsModuleArgsAddBlob,
        client: Optional[Client] = None,
        env: Optional[Any] = None,
        uri: Optional[Uri] = None,
    ) -> list["IpfsAddResult"]:
        _client = self._get_client(client)
        _env = self._get_env(env)
        _uri = self._get_uri(uri)

        return _client.invoke(
            uri=_uri,
            method="addBlob",
            args=args,
            env=_env,
        )

### Imported Modules END ###
