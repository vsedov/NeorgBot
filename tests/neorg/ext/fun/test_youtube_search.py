import unittest

from neorg.ext.fun._youtube import Youtube


class TestYoutube(unittest.TestCase):
    """Test youtube module for fetching and getting youtube videos."""

    def test_get_video(self):
        """Test the get videos, where it should return over 5 videos. """
        valid = Youtube().get_video()
        self.assertTrue(len(valid["result"]) >= 1)
        valid_list = list(valid.values())[0][0]  # get first element to check values

        get_title = valid_list["accessibility"]["title"]
        if "neovim" in get_title.lower():
            self.assertTrue(True)
        else:
            self.fail()

    def test_search_playlist(self):
        """ Check if playlist search is valid or corrolated to what we want."""
        valid = Youtube().search_playlist("Star wars Musics")
        title = list(valid.values())[0][0]["title"]
        self.assertTrue("star wars" in title.lower())

    def test_search_suggestion(self):
        """List of valid suggestions that one can use, in this case, checking for neovim vs vim."""
        valid = Youtube().get_search_suggestion("neovim")
        self.assertIn("neovim vs vim", [i.lower() for i in list(valid.values())[0]])

    def test_auto_suggested_video(self):
        """
        Test auto suggested videos names, for example neovim -> list of valid names you can search.
        """
        valid = Youtube().auto_suggester_search("neovim")
        self.assertTrue(len(list(valid.values())[0]) == 1)

    def test_video_limit(self):
        """
        test video limit from 1 , 10 on getting valid videos
        """
        for i in range(1, 10):
            valid = Youtube().get_video("Star Wars", i)
            self.assertTrue(len(list(valid.values())[0]) == i)

    def test_playlist_limit(self):
        """
        test playlist limit from 1 , 10 on getting playlists.
        """
        for i in range(1, 10):
            valid = Youtube().search_playlist("star wars", i)
            self.assertTrue(len(list(valid.values())[0]) == i)
