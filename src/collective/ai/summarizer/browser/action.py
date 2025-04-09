# -*- coding: utf-8 -*-
from collective.ai.summarizer.adapters import IAISummarizeAdapter
from collective.ai.summarizer.behaviors.summarizable import IAISummarizable
from Products.Five.browser import BrowserView

import logging

from zope.component import getAdapter

logger = logging.getLogger("collective.ai.summarizer")


class AISummarizerAction(BrowserView):

    def available(self):
        """
        Show action only if content is has the AISummarizable behavior.
        """
        if not IAISummarizable.providedBy(self.context):
            return False
        return True

    def __call__(self):
        handler = IAISummarizeAdapter(self.context)
        handler.summarize()
        self.request.response.redirect(self.context.absolute_url())
