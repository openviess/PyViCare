from PyViCare.PyViCareDevice import Device


class RoomControl(Device):
    """Viessmann RoomControl virtual device.

    Exposes per-room sensor readings. The IoT scope only returns sensor
    data; room metadata, schedules and operating programs are not
    available to public client_ids.
    """

    def getRoomTemperature(self, room_id: str) -> float:
        return float(self.service.getProperty(f"rooms.{room_id}.sensors.temperature")["properties"]["value"]["value"])

    def getRoomHumidity(self, room_id: str) -> float:
        return float(self.service.getProperty(f"rooms.{room_id}.sensors.humidity")["properties"]["value"]["value"])

    def getRoomCO2(self, room_id: str) -> int:
        return int(self.service.getProperty(f"rooms.{room_id}.co2")["properties"]["concentration"]["value"])

    def getRoomCondensationRisk(self, room_id: str) -> bool:
        return bool(self.service.getProperty(f"rooms.{room_id}.condensationRisk")["properties"]["value"]["value"])
