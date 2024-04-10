import dataclasses
from dataclasses import dataclass


@dataclass
class x:
    a:int = 0


class y(x):

    @property
    def a(self):
        return 1
    
    @a.setter
    def a(self, __a):
        pass


print(y().a)