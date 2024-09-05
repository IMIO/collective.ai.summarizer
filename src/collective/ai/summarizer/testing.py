# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PLONE_FIXTURE,
    PloneSandboxLayer,
)
from plone.testing import z2

import collective.ai.summarizer


class CollectiveAiSummarizerLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.ai.summarizer)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.ai.summarizer:default')


COLLECTIVE_AI_SUMMARIZER_FIXTURE = CollectiveAiSummarizerLayer()


COLLECTIVE_AI_SUMMARIZER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_AI_SUMMARIZER_FIXTURE,),
    name='CollectiveAiSummarizerLayer:IntegrationTesting',
)


COLLECTIVE_AI_SUMMARIZER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_AI_SUMMARIZER_FIXTURE,),
    name='CollectiveAiSummarizerLayer:FunctionalTesting',
)


COLLECTIVE_AI_SUMMARIZER_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_AI_SUMMARIZER_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveAiSummarizerLayer:AcceptanceTesting',
)
