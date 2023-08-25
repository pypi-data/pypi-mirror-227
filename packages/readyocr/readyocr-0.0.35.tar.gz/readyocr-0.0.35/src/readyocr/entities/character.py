from readyocr.entities.bbox import BoundingBox
from readyocr.entities.textbox import TextBox


class Character(TextBox):
    """
    To create a new :class:`Character` object we need the following

    :param id: Unique identifier of the Character entity.
    :type id: str
    :param bbox: Bounding box of the Character entity.
    :type bbox: BoundingBox
    :param text: Transcription of the Character object.
    :type text: str
    :param confidence: value storing the confidence of detection out of 100.
    :type confidence: float
    """

    def __init__(
        self,
        id: str,
        bbox: BoundingBox,
        text: str="",
        confidence: float=0,
        metadata: dict=None,
    ):
        super().__init__(id, bbox, text, confidence, metadata)

    def __repr__(self):
        return f"Character(id: '{self.id}', x: {self.bbox.x}, y: {self.bbox.y}, width: {self.bbox.width}, height: {self.bbox.height}, text: {self.text},confidence: {self.confidence}, tags: [{self._tags}])"