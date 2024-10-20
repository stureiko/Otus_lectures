class Model:
    def __init__(self) -> None:
        self.name = 'my dummy model'
        

    def predict(self, val: list) -> tuple[bool, tuple[int]]:
        # check all elements in list are great than zero
        res = all(v > 0 for v in val)
        if res:
            idx = []
        else:
            idx = [index for index, value in enumerate(val) if value < 0]
        return (res, idx)