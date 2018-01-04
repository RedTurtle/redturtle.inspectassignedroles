# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import redturtle.inspectassignedroles


class RedturtleInspectassignedrolesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=redturtle.inspectassignedroles)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'redturtle.inspectassignedroles:default')


REDTURTLE_INSPECTASSIGNEDROLES_FIXTURE = RedturtleInspectassignedrolesLayer()


REDTURTLE_INSPECTASSIGNEDROLES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(REDTURTLE_INSPECTASSIGNEDROLES_FIXTURE,),
    name='RedturtleInspectassignedrolesLayer:IntegrationTesting'
)


REDTURTLE_INSPECTASSIGNEDROLES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(REDTURTLE_INSPECTASSIGNEDROLES_FIXTURE,),
    name='RedturtleInspectassignedrolesLayer:FunctionalTesting'
)


REDTURTLE_INSPECTASSIGNEDROLES_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        REDTURTLE_INSPECTASSIGNEDROLES_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='RedturtleInspectassignedrolesLayer:AcceptanceTesting'
)
