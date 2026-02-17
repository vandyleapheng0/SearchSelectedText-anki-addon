from aqt.utils import openLink
from anki.hooks import addHook
from urllib.parse import urlencode


class SearchProvider:
    def __init__(self, name, url, searchParameter):
        self.name = name
        self.url = url
        self.searchParameter = searchParameter

    def search(self, searchQuery):
        openLink(self.url + urlencode({self.searchParameter: searchQuery}))


searchProviders = (
    SearchProvider("Google", "https://www.google.com/search?", "q"),
    SearchProvider(
        "Reverso",
        "https://www.reverso.net/traduction-texte#sl=fra&tl=eng&",
        "text",
    ),
)


def addToContextMenu(view, menu):
    selectedText: str = view.page().selectedText()
    if not selectedText:
        return

    searchQuery = " ".join(selectedText.split())
    label = 'Search for "%s" on ' % (
        searchQuery if len(searchQuery) < 25 else searchQuery[:25] + "..."
    )

    for searchProvider in searchProviders:
        actionMenu = menu.addAction(label + searchProvider.name)
        actionMenu.triggered.connect(
            lambda _, provider=searchProvider: provider.search(searchQuery)
        )


addHook("AnkiWebView.contextMenuEvent", addToContextMenu)
