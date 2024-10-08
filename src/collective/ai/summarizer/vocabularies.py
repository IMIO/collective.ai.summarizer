from Acquisition import aq_get
from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.i18n import translate


@implementer(IVocabularyFactory)
class SummarizablePortalTypesVocabulary:
    """
    """

    def __call__(self, context):
        site = getSite()
        ttool = getToolByName(site, "portal_types", None)
        if ttool is None:
            return SimpleVocabulary([])

        request = aq_get(ttool, "REQUEST", None)
        items = []
        for ctype in ttool.listContentTypes():
            ty_info = ttool.getTypeInfo(ctype)
            if not hasattr(ty_info, "behaviors") or 'collective.ai.summarizer.ai_summarizable' not in ty_info.behaviors:
                continue
            items.append((translate(ttool[ctype].Title(), context=request), ctype))

        return SimpleVocabulary([SimpleTerm(i[1], i[1], i[0]) for i in sorted(items)])
