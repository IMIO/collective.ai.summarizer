# -*- coding: utf-8 -*-
from collective.ai.core.browser.controlpanel import IAiCoreSettings
from collective.ai.summarizer.behaviors.ai_summarizable import IAiSummarizable
from plone import api
from plone import registry
from plone.registry.interfaces import IRegistry
from zope.component import getUtility, adapter
from zope.interface import implementer, Interface
from collective.ai.summarizer.browser.controlpanel import IAiSummarizerSettings

import logging

logger = logging.getLogger("collective.ai.summarizer")

class IAiSummarizeAdapter(Interface):
    """"""

@implementer(IAiSummarizeAdapter)
@adapter(IAiSummarizable)
class AiSummarizeAdapter(object):
    """Handle summarization operations on an object"""

    def __init__(self, context):
        self.context = context

    def summarize(self):
        from openai import OpenAI
        registry = getUtility(IRegistry)
        ai_settings = registry.forInterface(IAiCoreSettings, check=False)
        summarizer_settings = registry.forInterface(IAiSummarizerSettings, check=False)
        prompt = summarizer_settings.ai_summarizer_prompt.format(self.context.text.output)
        service_settings = ai_settings.ai_text_completion_services[0]
        client = OpenAI(
            base_url=service_settings["api_service_url"],
            api_key=service_settings["api_key"],
            **service_settings["extra_config"]
        )

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        self.context.summary = completion.choices[0].message.content




class ISummarizer(Interface):
    def summarize(self, text):
        pass

@implementer(ISummarizer)
class OpenAISummarizer:
    def summarize(self, text):
        return text[:200]

@implementer(ISummarizer)
class OpenRouterSummarizer:
    def summarize(self, text):
        return text[:200]
