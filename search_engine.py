import wikipedia


class SearchEngine:
    def __init__(self):
        wikipedia.set_lang('pt')


    def search(self, term: str) -> str | None:
        try:
            results = wikipedia.search(term)
            page = wikipedia.page(results[0])
            return page.content
        except wikipedia.PageError:
            return None
