
class NormalFromETI:
    def __getitem__(self, key):
        credence, interval = key
        print(credence, interval)

normal = NormalFromETI()


@dataclass
class ETIParams:
    credence: float
    low: float
    high: float

    def normal_eti(self, name: str):
        print(name, self, "TODO: implement CI") 
        return Normal(name, 0, 1)

    def normal(self):
        return construct(self.normal_eti, None)

