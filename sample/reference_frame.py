class ReferenceFrame:
    def __init__(self, name, position, orientation):
        self.name = name
        self.position = position
        self.orientation = orientation

    def to_dict(self):
        return {
            "name": self.name,
            "position": self.position,
            "orientation": self.orientation
        }