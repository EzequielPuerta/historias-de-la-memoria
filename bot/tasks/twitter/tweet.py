class Tweet:
    def __init__(self, text: str, photos: list[str], _id: str) -> None:
        self.text = text
        self.photos = photos
        self._id = _id
