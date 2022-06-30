import json


class Utils:
    @staticmethod
    def save_to_json(file_path: str, data):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
