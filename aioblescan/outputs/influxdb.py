import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from aioblescan.outputs import config

class InfluxDB:
    def __init__(self, config: config.InfluxDBConfig):
        self.client = influxdb_client.InfluxDBClient(
           url=config.url,
           token=config.token,
           org=config.org
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.config = config

    def write(self, record):
        point = influxdb_client.Point(self.config.measurement)

        for recordName, fieldName in self.config.fieldsMap.items():
            recordValue = record.get(recordName)
            if recordValue is not None:
                point = point.field(fieldName, recordValue)

        for recordName, tagName in self.config.tagsMap.items():
            tagValue = record.get(recordName)
            remappedTagValue = self.config.tagsValueMap.get(tagValue, None)
            if tagValue is not None:
                point = point.tag(tagName, tagValue if remappedTagValue is None else remappedTagValue)

        print(f"Writing point: {point.to_line_protocol()}")

        self.write_api.write(bucket=self.config.bucket, record=point)
