import logging

from rc.exceptions import RcException


logger = logging.getLogger(__name__)

class ConfigError(RcException):
    def __init__(self, msg):
        super().__init__(f"config file error: {msg}")
        
class ConfigManager:
    REQUIRED_KEYS = ['cloud_storage', 'bucket_name', 'cloud_storage_dir', 'minio_url', 'git_initial_commit', 'git_initial_branch', 'git_org', 'repo_name', 's3_storage_secret_key', 's3_storage_access_key', 'minio_secret_key', 'minio_access_key', 'gitignored_extensions']
    def __init__(self, config_data, required_keys=REQUIRED_KEYS):
        self.config_dict = self._store_config_values(config_data)
        self.required_keys = required_keys or []

        missing_keys = [key for key in self.required_keys if key not in self.config_dict]
        if missing_keys:
            raise ValueError(f"Required config keys are missing: {', '.join(missing_keys)}")
    
    def _store_config_values(self, config_data):
        config_dict = {}
        for item in config_data:
            config_dict[item['conf_key']] = item['conf_value']
        return config_dict
    
    def get_config_value(self, key):
        value = self.config_dict.get(key, None)
        if value is None:
            raise ConfigError(f"Key '{key}' not found in configuration")
        return value