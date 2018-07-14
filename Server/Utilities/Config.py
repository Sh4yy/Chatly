import simplejson as json
import os


class Config:

    _file_name = "config.json"
    _instance = None

    def __init__(self, file_name=None):

        if file_name:
            self._file_name = file_name

        data = json.loads(open(Config.get_path()).read())
        for key, value in data.items():
            setattr(self, key, value)

    @classmethod
    def default(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def save(self):
        data = json.dumps(self.__dict__, sort_keys=True, indent=4)
        with open(Config.get_path(), "w") as file:
            file.write(data)
            file.close()

    @classmethod
    def get_path(cls):
        package_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(package_dir, "../" + cls._file_name)

if __name__ == '__main__':
    print(Config.default().__dict__)
