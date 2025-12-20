import dataclasses


@dataclasses.dataclass
class Mountain:
    mount_name: str
    mount_peak_name: str
    route_list: list
