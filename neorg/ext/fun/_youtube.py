import random

from youtubesearchpython.__future__ import PlaylistsSearch  # Search PlayList
from youtubesearchpython.__future__ import Suggestions  # Async Searc
from youtubesearchpython.__future__ import VideosSearch  # Async Searc


class Youtube:
    """
    Wrapper Class To Search youtube, using youtubesearchpython api .
    """

    def __init__(self):

        self.video_search = VideosSearch
        self.playlist_search = PlaylistsSearch
        self.suggestion = Suggestions

    async def get_video(self, video_name: str = "Neovim", limit: int = 5) -> dict:
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
        video_result = await self.video_search(video_name, limit).next()
        return video_result

    async def search_playlist(self, playlist_name: str = "Neovim", limit: int = 1) -> dict:
        """
        Search Playlist, with respect to name and limit.
        """
        playlist_search = self.playlist_search(playlist_name, limit, language="en", region="US")
        return await playlist_search.next()

    async def get_search_suggestion(self, suggestion: str = "Neovim", language: str = "en", reigon: str = "US") -> dict:
        """
        Get search suggestions, that you can use when calling self.get_video
        """
        suggestions = await self.suggestion.get(suggestion, language="en", region="US")
        return suggestions

    async def auto_suggester_search(self, suggestion: str = "Neovim") -> dict:
        """
        Auto suggestion search
        Give a name, calles get search suggestions, and picks a random value with the default parameters,
        with that you call self.get_video to fetch only 1 video based on random search parameter.
        """
        valid_names = await self.get_search_suggestion(suggestion=suggestion)
        return await self.get_video(video_name=random.choice(list(valid_names.values())[0]), limit=1)
