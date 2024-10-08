class MissingSectionException(Exception):
    """data from arrest pdf not found"""

    def __init__(self, msg="", title="", url="", *args):
        """Init le message."""
        self.message = msg or 'Section "{title}" not found in {url}'.format(title=title, url=url)
        super().__init__(self.message, *args)
