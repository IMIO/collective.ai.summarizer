# -*- coding: utf-8 -*-
from collective.ai.core.browser.controlpanel import IAiCoreSettings, AiControlPanelFormWrapper
from collective.ai.core.interfaces import ICollectiveAiControlPanelFieldProvider
from collective.ai.summarizer import _
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.registry.interfaces import IRegistry
from plone.z3cform import layout
from plone.z3cform.fieldsets.interfaces import IFormExtender
from z3c.form import field
from z3c.form.browser.password import PasswordFieldWidget
from z3c.form.interfaces import IFormLayer
from zope import schema
from plone.supermodel import model
from zope.component import adapter
from zope.interface import alsoProvides, provider, implementer, Interface


class IAiSummarizerSettings(Interface):

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
    AiSummarizerControlPanelForm, AiControlPanelFormWrapper
)
