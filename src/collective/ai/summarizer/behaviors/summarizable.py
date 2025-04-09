# -*- coding: utf-8 -*-

from collective.ai.summarizer import _
from plone import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.CMFPlone.utils import safe_hasattr
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zope.interface import provider


@provider(IFormFieldProvider)
class IAISummarizable(model.Schema):
    """
    """


@implementer(IAISummarizable)
@adapter(IAISummarizable)
class AISummarizable(object):

    @property
    def summary(self):
        if safe_hasattr(self.context, 'summary'):
            return self.context.summary
        return None

    @summary.setter
    def summary(self, value):
        self.context.summary = value
