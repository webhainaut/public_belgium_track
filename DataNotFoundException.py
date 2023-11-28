class DataNotFoundException(Exception):
    """data from arrest pdf not found"""

    def __init__(self, msg="", data="", ref="", *args, **kwargs):
        """Init le message."""
        msg = msg or "{data} non trouvée dans le pdf {ref}".format(data=data, ref=ref)
        super().__init__(msg, *args, **kwargs)