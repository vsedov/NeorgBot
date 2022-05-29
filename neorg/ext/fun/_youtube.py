import random

from youtubesearchpython import PlaylistsSearch  # Search PlayList
from youtubesearchpython import Suggestions  # Async Searc
from youtubesearchpython import VideosSearch  # Async Searc
from youtubesearchpython import ResultMode


class Youtube:
    """
    Wrapper Class To Search youtube, using youtubesearchpython api .
    """

    def __init__(self):

        self.video_search = VideosSearch
        self.playlist_search = PlaylistsSearch
        self.suggestion = Suggestions

    def get_video(self, video_name: str = "Neovim", limit: int = 1) -> dict:
        """Get video : fetches most common videos that are strongly linked to what you want.

        Parameters
        ----------
        video_name : str
            Video Name : "Star wars episode 3 epic remix" would return a list of 5 valid videos from Search
        limit : int
            Limit, how many videos do you want

        Returns
        -------
        dict
            Dictionary returningin information about those videos dict[dict] format similar to json
        """
        video_result = self.video_search(video_name, limit).result()
        return video_result

    def search_playlist(self, playlist_name: str = "Neovim", limit: int = 1) -> dict:
        """
        Search Playlist, with respect to name and limit.
        """
        playlist_search = self.playlist_search(playlist_name, limit, language="en", region="US")
        return playlist_search.result()

    def get_search_suggestion(self, query: str = "Neovim") -> dict:
        """
        Get search suggestions, that you can use when calling self.get_video
        neovim -> {'result': ['neovim', 'neovim setup', 'neovim tutorial', 'neovim vs vim',
        'neovim from scratch', 'neovim lsp', 'neovim plugins', 'neovim lua', 'neovim vs vscode',
        'neovim configuration', 'neovim config', 'neovim windows', 'neovim vscode', 'neovim python']}
        """
        suggestions = self.suggestion(language="en", region="US")
        valid = suggestions.get(query, mode=ResultMode.dict)
        return valid

    def auto_suggester_search(self, suggestion: str = "Neovim") -> dict:
        """
        Auto suggestion search
        Give a name, calles get search suggestions, and picks a random value with the default parameters,
        with that you call self.get_video to fetch only 1 video based on random search parameter.
        """
        valid_names = self.get_search_suggestion(query=suggestion)

        return self.get_video(video_name=random.choice(list(valid_names.values())[0]), limit=1)


if __name__ == "__main__":
    limit = 1
    query = "text"

    search = Youtube().get_search_suggestion()
    print(search)

else:
    pass
