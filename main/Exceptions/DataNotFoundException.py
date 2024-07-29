class DataNotFoundException(Exception):
    """data from arrest pdf not found"""

    def __init__(self, msg="", data="", ref="", message="", *args):
        """Init le message."""
        self.message = "{data} non trouvée".format(data=data)
        msg = msg or "{data} non trouvée dans le pdf {ref} {message}".format(data=data, ref=ref, message=message)
        super().__init__(msg, *args)
