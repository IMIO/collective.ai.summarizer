# -*- coding: utf-8 -*-
from collective.ai.summarizer import _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.autoform import directives
from plone.z3cform import layout
from z3c.form.browser.password import PasswordFieldWidget
from zope import schema
from zope.interface import Interface

class IAiSummarizerSettings(Interface):

    ai_api_service_url = schema.URI(
        title=_("ai_api_service_url"),
        default="https://changeme.org",
        required=False,
    )
    directives.widget("ai_api_key", PasswordFieldWidget)
    ai_api_key = schema.TextLine(
        title=_("ai_api_key"),
        default="",
        required=False,
    )

    ai_summarizer_prompt = schema.Text(
        title=_("ai_summarizer_prompt"),
        default="""Voici un texte :
'''
{}
'''
Résume ce texte en 2 paragraphes. Sois clair et concis.
        """,
        required=False,
    )

class AiSummarizerControlPanelForm(RegistryEditForm):
    label = _("AI Summarizer settings")
    schema = IAiSummarizerSettings


AiSummarizerControlPanelView = layout.wrap_form(
    AiSummarizerControlPanelForm, ControlPanelFormWrapper
)
