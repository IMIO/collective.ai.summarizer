from collective.ai.core.interfaces import IAiActionsProvider
from collective.ai.summarizer.behaviors.ai_summarizable import IAiSummarizable
from collective.ai.summarizer.browser.controlpanel import IAiSummarizerSettings
from plone.protect.utils import addTokenToUrl
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import implementer


@implementer(IAiActionsProvider)
class SummarizerActions:
    def __call__(self, context, request):
        if not IAiSummarizable.providedBy(context):
            return []
        registry = getUtility(IRegistry)
        summarizer_settings = registry.forInterface(IAiSummarizerSettings, check=False)
        results = []
        if not hasattr(summarizer_settings, "summarizers") or not summarizer_settings.summarizers:
            return []
        for i, summarizer in enumerate(summarizer_settings.summarizers):
            if context.portal_type != summarizer['portal_type'] or summarizer['active'] is False:
                continue
            results.append(
                {
                    "title": summarizer["label"],
                    "description": "",
                    "action": addTokenToUrl(f"{context.absolute_url()}/@@ai-summarizer-action?summarizer={i}", request),
                    "selected": False,
                    "icon": "text-paragraph",
                    "extra": {
                        "id": "plone-contentmenu-actions-" + "id",
                        "separator": None,
                        "class": 'cssClass',
                        "modal": '',
                    },
                    "submenu": None,
                }
            )
        return results
