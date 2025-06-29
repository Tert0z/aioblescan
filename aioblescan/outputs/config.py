import yaml
from dataclasses import dataclass
from typing import List, Optional, Dict


@dataclass
class InfluxDBConfig:
    url: str
    token: str
    org: str
    bucket: str
    fieldsMap: Dict[str, str]
    tagsMap: Dict[str, str]
    tagsValueMap: Dict[str, str]
    measurement: str


@dataclass
class OutputsConfig:
    influxdb: Optional[InfluxDBConfig]
