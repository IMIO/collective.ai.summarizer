# -*- coding: utf-8 -*-
from collective.ai.core.browser.controlpanel import IAiCoreSettings
from collective.ai.summarizer.behaviors.ai_summarizable import IAiSummarizable
from plone import api
from plone import registry
from plone.registry.interfaces import IRegistry
from requests.packages import target
from zope.component import getUtility, adapter
from zope.interface import implementer, Interface
from collective.ai.summarizer.browser.controlpanel import IAiSummarizerSettings
from openai import OpenAI
import logging

logger = logging.getLogger("collective.ai.summarizer")


class IAiSummarizeAdapter(Interface):
    """"""
    def __init__(self, context, request):
        pass

@implementer(IAiSummarizeAdapter)
@adapter(IAiSummarizable)
class AiSummarizeAdapter:
    """Handle summarization operations on an object"""

    def __init__(self, context):
        self.context = context
        self.request = context.REQUEST
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(IAiSummarizerSettings, check=False)
        self.summarizer_config = self.settings.summarizers[int(self.request.form['summarizer'])]

    def target_field(self):
        return self.summarizer_config['target_field']

    def source_field(self):
        return self.summarizer_config['source_field']

    def get_input_text(self):
        return getattr(self.context, self.source_field()).output

    def set_output_text(self, text):
        setattr(self.context, self.target_field(), text)

    def prompt(self):
        return self.summarizer_config['prompt']

    def summarize(self):
        import ipdb; ipdb.set_trace()  # TODO: remove me <----------------
        self.set_output_text(summarizer.summarize(self.get_input_text(), self.prompt()))
