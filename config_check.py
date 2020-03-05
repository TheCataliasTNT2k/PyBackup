class Config:
    backup_dir: str = ""
    time_hour: int = 0
    time_minute: int = 0
    database_list: list = None
    file_path_list: list = None
    checksums: list = None

    def __init__(self, json: dict):
        self.backup_dir = json.get("backup_dir")
        database_values: dict = json.get("database")
        if not (isinstance(database_values, dict) or database_values is None):
            print("Error: Database values are not properly initialized! Exiting.")
            exit(1)
        if database_values is not None:
            self.database_list = database_values.get("list")
        file_values: dict = json.get("files")
        if not (isinstance(file_values, dict) or file_values is None):
            print("Error: File values are not properly initialized! Exiting.")
            exit(1)
        if file_values is not None:
            self.file_path_list = file_values.get("paths")
        if self.backup_dir is None:
            print("Error: Backup location is not properly initialized! Exiting.")
            exit(1)
        time_values: dict = json.get("time")
        if not isinstance(time_values, dict):
            print("Warning: Time values are not properly initialized! Using default value: 03:00")
            self.time_hour = 3
            self.time_minute = 0
        else:
            self.time_hour = time_values.get("hour")
            self.time_minute = time_values.get("minute")
        self.checksums = file_values.get("checksums")

    def verify_settings(self):
        try:
            self.time_hour = int(self.time_hour)
        except ValueError:
            print("Error: Unable to convert minute part of time to int! Exiting.")
            exit(1)
        try:
            self.time_minute = int(self.time_minute)
        except ValueError:
            print("Error: Unable to convert hour part of time to int! Exiting.")
            exit(1)
        if self.file_path_list is None:
            self.file_path_list = []
        if self.database_list is None:
            self.database_list = []
        if self.checksums is None:
            self.checksums = []


def create_from_json(json: dict) -> Config:
    return Config(json)
