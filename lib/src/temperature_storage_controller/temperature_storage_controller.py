import os


class TemperatureStorageController:
    def __init__(self, temperature_file_path, fs_test_file_path, logger):
        self.logger = logger
        self.temperature_file_path = temperature_file_path
        self.fs_test_file_path = fs_test_file_path

        self.logger.info("Temperature storage controller initialised")

        self.enabled = True
        if not self._storage_available():
            self.logger.info("Temperature storage is not available")
            self.enabled = False

    def _storage_available(self):
        try:
            with open(self.fs_test_file_path, "w") as f:
                f.write("0")
            os.remove(self.fs_test_file_path)
            return True
        except:
            return False

    def persisted_temperature(self):
        if not self.enabled:
            return None
        try:
            with open(self.temperature_file_path, "r") as f:
                temp_str = f.read()
                self.logger.info(f"Found persisted temperature: {temp_str}")
                return float(temp_str)
        except:
            self.logger.info("No persisted temperature found")
            self.delete_persisted_temperature()
            return None

    def persist_temperature(self, temperature):
        if not self.enabled:
            return
        with open(self.temperature_file_path, "w") as f:
            f.write("%.1f" % temperature)
            self.logger.info(f"Persisted new temperature: {temperature}")

    def delete_persisted_temperature(self):
        if not self.enabled:
            return
        try:
            os.remove(self.temperature_file_path)
            self.logger.info("Deleted persisted temperature")
        except:
            self.logger.info("Unable to delete persisted temperature: it may not exist")
