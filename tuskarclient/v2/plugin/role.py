#   Copyright 2012-2013 OpenStack Foundation
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

"""Tuskar v2 Role action implementations"""

import logging
import six

from cliff import command
from cliff import lister
from cliff import show
from keystoneclient import exceptions as ksc_exc

from openstackclient.common import exceptions
from openstackclient.common import utils
from openstackclient.i18n import _  # noqa


class ListRole(lister.Lister):
    """List roles"""

    log = logging.getLogger(__name__ + '.ListRole')

    def get_parser(self, prog_name):
        parser = super(ListRole, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        tuskar_client = self.app.client_manager.tuskar
        import pdb; pdb.set_trace()
        data = tuskar_client.roles.list()

        return (columns,
                (utils.get_item_properties(
                    s, columns,
                    formatters={},
                ) for s in data))


