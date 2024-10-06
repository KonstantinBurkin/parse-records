"""mixin class with shared methods"""

from typing import Union


class ParserFunctions:
    "class with shared parsing functions"

    def find_section_by_optimized_path(
        self,
        data: dict,
        short_path: list[str],
        fields=None,
        prefix="{urn:hl7-org:v3}",
    ) -> Union[dict, str]:
        """
        Navigate a nested JSON structure along the specified path,
            automatically adding a prefix to string path elements.
        Optionally return only specific fields from the final block.

        :param data: The JSON data as a nested Python dictionary.
        :param short_path: The simplified path to the desired section as a list of keys and indices.
        :param fields: Optional. A tuple or list of field names to return from the final block.
            If None, returns the entire block.
        :param prefix: The prefix to add to string elements in the path.
        :return: The section at the specified path, or specific fields from the section,
            or None if the path is invalid.
        """
        current = data
        full_path = [
            (prefix + element) if isinstance(element, str) else element
            for element in short_path
        ]

        try:
            for key in full_path:
                if isinstance(current, list):  # Handle list indices
                    current = current[int(key)]
                else:  # Handle dictionary keys
                    current = current[key]

            if (
                fields
                and isinstance(fields, (list, tuple))
                and isinstance(current, dict)
            ):
                return {field: current.get(field, None) for field in fields}

            return current
        except (KeyError, IndexError, ValueError, TypeError):
            return None  # Path was invalid

    def get_sex(
        self,
        data: dict,
    ) -> Union["Мужской", "Женский"]:
        """get gender from record

        Returns:
            _type_: _description_
        """
        short_path_to_section = [
            "recordTarget",
            "patientRole",
            "patient",
            "administrativeGenderCode",
        ]

        section_fields = self.find_section_by_optimized_path(
            data,
            short_path_to_section,
        )

        return section_fields["displayName"]

    def get_age(
        self,
        data: dict,
    ) -> str:
        """get birth date from record

        Args:
            data (dict): _description_

        Returns:
            str: _description_
        """
        short_path_to_section = [
            "recordTarget",
            "patientRole",
            "patient",
            "birthTime",
        ]

        section_fields = self.find_section_by_optimized_path(
            data,
            short_path_to_section,
        )

        return section_fields["value"]
