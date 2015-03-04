#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from tuskarclient.common import auth
from tuskarclient.openstack.common.apiclient import client as apiclient
import tuskarclient.openstack.common.cliutils as utils

API_NAME = 'tuskar'
API_VERSION_OPTION = 'os_tuskar_api_version'
DEFAULT_TUSKAR_API_VERSION = '2'

# Required by the OSC plugin interface

API_VERSIONS = {
    '2': 'tuskarclient.v2.client.Client'
}

VERSION_MAP = {
    '2': 'tuskarclient.v2.client.Client'
}


def get_client(api_version, **kwargs):
    """Get an authtenticated client, based on the credentials
       in the keyword args.

    :param api_version: the API version to use (only '2' is valid)
    :param kwargs: keyword args containing credentials, either:
            * os_auth_token: pre-existing token to re-use
            * tuskar_url: tuskar API endpoint
            or:
            * os_username: name of user
            * os_password: user's password
            * os_auth_url: endpoint to authenticate against
            * os_tenant_{name|id}: name or ID of tenant
    """
    # Try call for client with token and endpoint.
    # If it returns None, call for client with credentials
    cli_kwargs = {
        'username': kwargs.get('os_username'),
        'password': kwargs.get('os_password'),
        'tenant_name': kwargs.get('os_tenant_name'),
        'token': kwargs.get('os_auth_token'),
        'auth_url': kwargs.get('os_auth_url'),
        'endpoint': kwargs.get('tuskar_url'),
    }
    client = Client(api_version, **cli_kwargs)
    # If we have a client, return it
    if client:
        return client
    # otherwise raise error
    else:
        raise ValueError("Need correct set of parameters")


def Client(version, **kwargs):
    client_class = apiclient.BaseClient.get_class('tuskarclient',
                                                  version,
                                                  VERSION_MAP)
    keystone_auth = auth.KeystoneAuthPlugin(
        username=kwargs.get('username'),
        password=kwargs.get('password'),
        tenant_name=kwargs.get('tenant_name'),
        token=kwargs.get('token'),
        auth_url=kwargs.get('auth_url'),
        endpoint=kwargs.get('endpoint'))
    http_client = apiclient.HTTPClient(keystone_auth)
    return client_class(http_client)

# Required by the OSC plugin interface
def make_client(instance):
    """Returns a client to the ClientManager

    Called to instantiate the requested client version.  instance has
    any available auth info that may be required to prepare the client.

    :param ClientManager instance: The ClientManager that owns the new client
    """
    client_class = apiclient.BaseClient.get_class(
        "%sclient" % API_NAME ,
        instance._api_version[API_NAME],
        VERSION_MAP)
    keystone_auth = auth.KeystoneAuthPlugin(
        token=instance.auth_ref.token,
        auth_url=instance.auth_ref.auth_url,
        endpoint=instance.get_endpoint_for_service_type('management')
    )
    http_client = apiclient.HTTPClient(keystone_auth)

    return client_class(http_client)

# Required by the OSC plugin interface
def build_option_parser(parser):
    """Hook to add global options

    Called from openstackclient.shell.OpenStackShell.__init__()
    after the builtin parser has been initialized.  This is
    where a plugin can add global options such as an API version setting.

    :param argparse.ArgumentParser parser: The parser object that has been
        initialized by OpenStackShell.
    """
    parser.add_argument(
        '--os-tuskar-api-version',
        metavar='<tuskar-api-version>',
        default=utils.env(
            'OS_TUSKAR_API_VERSION',
            default=DEFAULT_TUSKAR_API_VERSION),
        help='OSC Plugin API version, default=' +
             DEFAULT_TUSKAR_API_VERSION +
             ' (Env: OS_TUSKAR_API_VERSION)')
    parser.add_argument(
        '--tuskar-url',
        metavar='<tuskar-endpoint-url>',
        default=utils.env('TUSKAR_URL'),
        help='Defaults to env[TUSKAR_URL]')
    return parser