"""parse epic records with EpicParser class"""

import pandas as pd
from .mixin.parcer_functions import ParserFunctions

# from .parser_fucn import (
#     find_section_by_optimized_path,
#     convert_table_to_dataframe,
# )


class EpicParser(ParserFunctions):
    """class for parsing epic records"""

    def parse_table(
        self,
        json_data: dict,
        prefix: str = "{urn:hl7-org:v3}",
    ):
        """parse table from epic recors"""
        adjusted_rows = []
        headers = [
            header["text"]
            for header in json_data[f"{prefix}table"][f"{prefix}thead"][f"{prefix}tr"][
                f"{prefix}th"
            ]
        ]

        for row in json_data[f"{prefix}table"][f"{prefix}tbody"][f"{prefix}tr"]:
            current_row = []
            for cell in row[f"{prefix}td"]:
                current_row.append(cell[f"{prefix}content"]["text"])
            # Check if the row has fewer items than headers, if so, add a placeholder
            if len(current_row) < len(headers):
                current_row.append(
                    "None"
                )  # Assuming 'Not specified' for missing doctor data
            adjusted_rows.append(current_row)

        # Recreate the DataFrame with adjusted rows
        adjusted_df = pd.DataFrame(adjusted_rows, columns=headers)
        return adjusted_df

    def get_features_from_diagnosis_table(
        self,
        data: dict,
    ) -> dict:
        """get features from diagnosis table"""
        short_path_to_section = [
            "component",
            "structuredBody",
            "component",
            "section",
            "component",
            1,
            "section",
            "component",
            "section",
            "text",
        ]

        section_fields = self.find_section_by_optimized_path(
            data, short_path_to_section
        )

        table = self.parse_table(section_fields)

        features_for_dataframe = {}

        code_disease_features = (
            table.pivot_table(
                columns=["Вид нозологической единицы"],
                values=["Код по МКБ-10"],
                aggfunc=lambda x: list(set(x)),
            )
            .rename(
                columns={
                    "Осложнение основного заболевания": "complication_of_main_disease_code",
                    "Основное заболевание": "main_disease_code",
                    "Сопутствующее заболевание": "secondary_disease_code",
                    "Фоновое заболевание": "background_disease_code",
                }
            )
            .to_dict("records")[0]
        )

        disease_description_features = (
            table.pivot_table(
                columns=["Вид нозологической единицы"],
                values=["Врачебное описание нозологической единицы"],
                aggfunc=lambda x: "".join(set(x)),
            )
            .rename(
                columns={
                    "Осложнение основного заболевания": "complication_of_main_disease_desc",
                    "Основное заболевание": "main_disease_desc",
                    "Сопутствующее заболевание": "secondary_disease_desc",
                    "Фоновое заболевание": "background_disease_desc",
                }
            )
            .to_dict("records")[0]
        )

        features_for_dataframe.update(disease_description_features)
        features_for_dataframe.update(code_disease_features)

        return features_for_dataframe

    def get_amnez_d(
        self,
        data: dict,
    ) -> str:
        """parse data from anamnez"""
        short_path_to_section = [
            "component",
            "structuredBody",
            "component",
            "section",
            "component",
            0,
            "section",
            "text",
        ]

        section_fields = self.find_section_by_optimized_path(
            data,
            short_path_to_section,
        )

        return section_fields["text"]

    def get_condition(
        self,
        data: dict,
    ) -> str:
        """parse data with current condition"""
        short_path_to_section = [
            "component",
            "structuredBody",
            "component",
            "section",
            "component",
            1,
            "section",
            "text",
            "content",
        ]

        section_fields = self.find_section_by_optimized_path(
            data,
            short_path_to_section,
        )

        result = []
        for el in section_fields:
            result.append(el["text"])

        return result

    def get_gosp_info(
        self,
        data: dict,
    ) -> list:  # TODO: add types in list
        """parse gospital info"""
        short_path_to_section = [
            "component",
            "structuredBody",
            "component",
            "section",
            "text",
        ]

        section_fields = self.find_section_by_optimized_path(
            data,
            short_path_to_section,
        )

        table = self.parse_table(section_fields)

        short_path_to_section = [
            "component",
            "structuredBody",
            "component",
            "section",
            "entry",
            2,
            "observation",
            "value",
        ]

        section_fields = self.find_section_by_optimized_path(
            data,
            short_path_to_section,
        )
        type_gosp = section_fields["displayName"]

        short_path_to_section = [
            "component",
            "structuredBody",
            "component",
            "section",
            "entry",
            3,
            "observation",
            "value",
        ]

        section_fields = self.find_section_by_optimized_path(
            data,
            short_path_to_section,
        )
        way_gosp = section_fields["displayName"]

        return table, type_gosp, way_gosp

    def get_amnez_life(
        self,
        data: dict,
    ) -> str:
        """parse anamnez life"""
        short_path_to_section = [
            "component",
            "structuredBody",
            "component",
            "section",
            "component",
            2,
            "section",
            "text",
        ]

        section_fields = self.find_section_by_optimized_path(
            data,
            short_path_to_section,
        )

        return section_fields["text"]
