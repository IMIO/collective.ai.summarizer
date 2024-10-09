# -*- coding: utf-8 -*-
from collective.ai.summarizer.adapters import IAiSummarizeAdapter
from collective.ai.summarizer.behaviors.ai_summarizable import IAiSummarizable
from Products.Five.browser import BrowserView

import logging

from zope.component import getAdapter

logger = logging.getLogger("collective.ai.summarizer")


class AiSummarizerAction(BrowserView):

    def available(self):
        """
        Show action only if content is has the AiSummarizable behavior.
        """
        if not IAiSummarizable.providedBy(self.context):
            return False
        return True

    def __call__(self):
        handler = IAiSummarizeAdapter(self.context)
        handler.summarize()
        self.request.response.redirect(self.context.absolute_url())
