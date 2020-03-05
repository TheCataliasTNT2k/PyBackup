class Config:
    backup_dir: str = ""
    database_container_name: str = None
    database_list: list = None
    database_username: str = None
    database_password: str = None
    gitlab_container_name: str = None
    file_path_list: list = None
    checksums: list = None

    def __init__(self, json: dict):
        self.backup_dir = json.get("backup_dir")
        if self.backup_dir is None:
            print("Error: Backup location is not properly initialized! Exiting.")
            exit(1)
        database_values: dict = json.get("database")
        if not (isinstance(database_values, dict) or database_values is None):
            print("Error: Database values are not properly initialized! Exiting.")
            exit(1)
        if database_values is not None:
            self.database_container_name = database_values.get("container_name")
            self.database_password = database_values.get("password")
            self.database_username = database_values.get("username")
            self.database_list = database_values.get("list")
        self.gitlab_container_name: dict = json.get("gitlab_container_name")
        if not (isinstance(self.gitlab_container_name, str) or self.gitlab_container_name is None):
            print("Error: Gitlab container name is not properly initialized! Exiting.")
            exit(1)
        file_values: dict = json.get("files")
        if not (isinstance(file_values, dict) or file_values is None):
            print("Error: File values are not properly initialized! Exiting.")
            exit(1)
        if file_values is not None:
            self.file_path_list = file_values.get("paths")
        self.checksums = file_values.get("checksums")

    def verify_settings(self):
        if self.backup_dir in [None, ""]:
            print(
                f"Warning: Path to local backup folder is not properly initialized! Using default value: "
                f'"/var/backups/system/"'
            )
            self.backup_dir = "/var/backups/system/"
        if self.checksums is None:
            self.checksums = []
        if self.file_path_list is None:
            self.file_path_list = []


def create_from_json(json: dict) -> Config:
    return Config(json)
