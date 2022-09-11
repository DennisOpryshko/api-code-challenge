import wikipedia
from datatypes import SearchResponseEntry as Entry
from datatypes import SearchResponse as Response

Page = wikipedia.WikipediaPage

def search_pages(of: str, top: int) -> [Page]:
    try:
        out = [wikipedia.page(of)]
    except wikipedia.DisambiguationError as disambiguation:
        opt = disambiguation.options[0:top]
        out = map(wikipedia.page, opt)
    return out


def run_search(of: str, top: int) -> Response:
    pages   = search_pages(of, top)
    entries = list(map(page_to_entry, pages))
    return Response(results=entries)


def page_to_entry(page: Page) -> Entry:
    return Entry(title=page.title, extract=page.summary)
