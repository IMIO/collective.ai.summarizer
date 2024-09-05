# -*- coding: utf-8 -*-
from collective.ai.summarizer.behaviors.ai_summarizable import IAiSummarizable
from collective.ai.summarizer.testing import COLLECTIVE_AI_SUMMARIZER_INTEGRATION_TESTING  # noqa
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class AiSummarizableIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_AI_SUMMARIZER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_behavior_ai_summarizable(self):
        behavior = getUtility(IBehavior, 'collective.ai.summarizer.ai_summarizable')
        self.assertEqual(
            behavior.marker,
            IAiSummarizable,
        )
