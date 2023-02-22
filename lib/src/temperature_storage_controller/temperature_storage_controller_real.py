import supervisor  # type: ignore
from .temperature_storage_controller import TemperatureStorageController


class TemperatureStorageControllerReal(TemperatureStorageController):
    def __init__(self, temperature_file_path, fs_test_file_path, logger):
        super().__init__(temperature_file_path, fs_test_file_path, logger)

    def persisted_temperature(self):
        try:
            return super().persisted_temperature()
        except ValueError:
            self.logger.info(
                f"Persisted temperature is invalid / corrupted, deleting it and restarting"
            )
            self.delete_persisted_temperature()
            supervisor.reload()
            return None
