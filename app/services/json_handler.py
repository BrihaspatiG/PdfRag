import os
import json


class JSONHandler:

    def save(self, data, output_path):

        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True
        )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

    def load(self, input_path):

        with open(
            input_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)