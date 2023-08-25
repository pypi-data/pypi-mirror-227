# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetOidcClientCredsResult',
    'AwaitableGetOidcClientCredsResult',
    'get_oidc_client_creds',
    'get_oidc_client_creds_output',
]

@pulumi.output_type
class GetOidcClientCredsResult:
    """
    A collection of values returned by getOidcClientCreds.
    """
    def __init__(__self__, client_id=None, client_secret=None, id=None, name=None, namespace=None):
        if client_id and not isinstance(client_id, str):
            raise TypeError("Expected argument 'client_id' to be a str")
        pulumi.set(__self__, "client_id", client_id)
        if client_secret and not isinstance(client_secret, str):
            raise TypeError("Expected argument 'client_secret' to be a str")
        pulumi.set(__self__, "client_secret", client_secret)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if namespace and not isinstance(namespace, str):
            raise TypeError("Expected argument 'namespace' to be a str")
        pulumi.set(__self__, "namespace", namespace)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> str:
        """
        The Client ID returned by Vault.
        """
        return pulumi.get(self, "client_id")

    @property
    @pulumi.getter(name="clientSecret")
    def client_secret(self) -> str:
        """
        The Client Secret Key returned by Vault.
        """
        return pulumi.get(self, "client_secret")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def namespace(self) -> Optional[str]:
        return pulumi.get(self, "namespace")


class AwaitableGetOidcClientCredsResult(GetOidcClientCredsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetOidcClientCredsResult(
            client_id=self.client_id,
            client_secret=self.client_secret,
            id=self.id,
            name=self.name,
            namespace=self.namespace)


def get_oidc_client_creds(name: Optional[str] = None,
                          namespace: Optional[str] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetOidcClientCredsResult:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_vault as vault

    app = vault.identity.OidcClient("app",
        redirect_uris=[
            "http://127.0.0.1:9200/v1/auth-methods/oidc:authenticate:callback",
            "http://127.0.0.1:8251/callback",
            "http://127.0.0.1:8080/callback",
        ],
        id_token_ttl=2400,
        access_token_ttl=7200)
    creds = vault.identity.get_oidc_client_creds_output(name=app.name)
    ```


    :param str name: The name of the OIDC Client in Vault.
    :param str namespace: The namespace of the target resource.
           The value should not contain leading or trailing forward slashes.
           The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault#namespace).
           *Available only for Vault Enterprise*.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['namespace'] = namespace
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('vault:identity/getOidcClientCreds:getOidcClientCreds', __args__, opts=opts, typ=GetOidcClientCredsResult).value

    return AwaitableGetOidcClientCredsResult(
        client_id=__ret__.client_id,
        client_secret=__ret__.client_secret,
        id=__ret__.id,
        name=__ret__.name,
        namespace=__ret__.namespace)


@_utilities.lift_output_func(get_oidc_client_creds)
def get_oidc_client_creds_output(name: Optional[pulumi.Input[str]] = None,
                                 namespace: Optional[pulumi.Input[Optional[str]]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetOidcClientCredsResult]:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_vault as vault

    app = vault.identity.OidcClient("app",
        redirect_uris=[
            "http://127.0.0.1:9200/v1/auth-methods/oidc:authenticate:callback",
            "http://127.0.0.1:8251/callback",
            "http://127.0.0.1:8080/callback",
        ],
        id_token_ttl=2400,
        access_token_ttl=7200)
    creds = vault.identity.get_oidc_client_creds_output(name=app.name)
    ```


    :param str name: The name of the OIDC Client in Vault.
    :param str namespace: The namespace of the target resource.
           The value should not contain leading or trailing forward slashes.
           The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault#namespace).
           *Available only for Vault Enterprise*.
    """
    ...
