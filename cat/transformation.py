class Transformation:
    def __init__(self, tid, left_map, right_map):
        self.id = tid
        self.left_map = tuple(left_map)
        self.right_map = tuple(right_map)
        self._map = {l: r for l, r in zip(left_map, right_map)}

    def __getitem__(self, i):
        if i not in self._map: return i
        return self._map[i]

    def __hash__(self):
        return hash((self.left_map, self.right_map))

    def __eq__(self, other):
        return (self.left_map, self.right_map) == (other.left_map, other.right_map)

    def __str__(self):
        return "Transformation(" + str(self.left_map) + ", " + str(self.right_map) + ")"

    def to_json(self):
        return {
            "id": self.id,
            "left": self.left_map,
            "right": self.right_map
        }

    @staticmethod
    def from_json(j):
        return Transformation(j["id"], j["left"], j["right"])
