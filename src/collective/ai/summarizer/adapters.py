# -*- coding: utf-8 -*-
from collective.ai.core.browser.controlpanel import IAICoreSettings
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

from collective.ai.core.services import IAIAPIService
from zope.component._api import getAdapter

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
        self.ai_settings = registry.forInterface(IAICoreSettings, check=False)
        self.summarizer_settings = registry.forInterface(IAiSummarizerSettings, check=False)
        self.summarizer_config = self.summarizer_settings.summarizers[int(self.request.form['summarizer'])]

    def output_field(self):
        return self.summarizer_config['output_field']

    def source_field(self):
        return self.summarizer_config['source_field']

    def get_input_text(self):
        return getattr(self.context, self.source_field()).output

    def set_output_text(self, text):
        setattr(self.context, self.output_field(), text)

    def prompt(self):
        return self.summarizer_config['prompt']

    def summarize(self):
        config_id, model_id = self.summarizer_config["model"].split("__")
        service_type = self.ai_settings.ai_text_completion_services[int(config_id)]["service_type"]
        service = getAdapter(self.context, IAIAPIService, service_type)
        service(int(config_id), model_id)

        # client = OpenAI(
        #     base_url=service_settings["api_service_url"],
        #     api_key=service_settings["api_key"],
        #     **service_settings["extra_config"]
        # )
        # completion = client.chat.completions.create(
        #     model="gpt-4o-mini",
        #     messages=[{"role": "user", "content": )}]
        # )

        # self.set_output_text(completion.choices[0].message.content)
        self.set_output_text(service.complete(self.prompt().format(self.get_input_text())))
