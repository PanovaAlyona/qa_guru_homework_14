import dataclasses


@dataclasses.dataclass
class Mountain:
    name: str
    route_list: list
    number_area: str
    number_region: str