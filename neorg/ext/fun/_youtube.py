# class Youtube:
#     # TODO: Add more search options
#     def __init__(self, query: str, max_results: int = 1):
#         self.max_results: int = max_results
#         self.query: str = query
#
#     @property
#     def _max_results(self) -> int:
#         return self.max_results
#
#     @property
#     def _query(self) -> str:
#         return self.query
#
#     @_query.setter
#     def _query(self, query: str) -> None:
#         self.query = query
#
#     def __str__(self):
#         return f"Youtube Search: {self.query}"
#
#     def search(self) -> dict:
#         search = VideosSearch(self.query, maxResults=self.max_results)
#         return search.to_dict()
#
#     def advanced_fuzzy_search__best_match(self) -> dict:
#         search = VideosSearch(self.query, maxResults=self.max_results)
#         name = search.to_dict()['items'][0]['snippet']['title']
#         best_match = process.extractOne(self.query, name)
#         return best_match
