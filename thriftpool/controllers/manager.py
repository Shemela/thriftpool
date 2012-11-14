from __future__ import absolute_import

from logging import getLogger

from gaffer.manager import Manager

from thriftworker.utils.decorators import cached_property
from thriftpool.components.base import Namespace
from thriftpool.controllers.base import Controller

logger = getLogger(__name__)


class ManagerNamespace(Namespace):

    name = 'manager'

    def modules(self):
        return ['thriftpool.components.loop',
                'thriftpool.components.listeners',
                'thriftpool.components.workers',
                'thriftpool.components.watchdog']


class ManagerController(Controller):

    Namespace = ManagerNamespace

    listeners = None
    workers = None

    def on_before_init(self):
        self.app.finalize()
        super(ManagerController, self).on_before_init()

    @cached_property
    def manager(self):
        return Manager(loop=self.app.loop)