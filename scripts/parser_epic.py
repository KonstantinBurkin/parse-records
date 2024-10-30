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
                current_row.append("None")
                # Assuming 'Not specified' for missing doctor data
            adjusted_rows.append(current_row)

        # Recreate the DataFrame with adjusted rows
        adjusted_df = pd.DataFrame(adjusted_rows, columns=headers)
        return adjusted_df

    def parse_table_wtheader(
        self,
        json_data: dict,
        prefix: str = "{urn:hl7-org:v3}",
    ):
        adjusted_rows = []
        if json_data[f"{prefix}table"][f"{prefix}tbody"][f"{prefix}tr"]:
            first_row = json_data[f"{prefix}table"][f"{prefix}tbody"][f"{prefix}tr"][0]
            num_columns = len(first_row[f"{prefix}td"])
            headers = [f"Column {i + 1}" for i in range(num_columns)]
        else:
            headers = []

        for row in json_data[f"{prefix}table"][f"{prefix}tbody"][f"{prefix}tr"]:
            current_row = []
            for cell in row[f"{prefix}td"]:
                cell_text = cell[f"{prefix}content"].get(
                    "text", "None"
                )  # Default to 'None' if 'text' is not available
                current_row.append(cell_text)
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

    def get_ward_table(
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
            3,
            "section",
            "text",
        ]

        section_fields = self.find_section_by_optimized_path(
            data,
            short_path_to_section,
        )
        table = self.parse_table(section_fields)

        return table

    def get_ward_list(
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
            3,
            "section",
            "component",
        ]

        section_fields = self.find_section_by_optimized_path(
            data,
            short_path_to_section,
        )
        # table = self.parse_table(section_fields)

        return section_fields

    def get_research_list(
        self,
        data: dict,
        i,
    ):
        """
        Всегда ли лист возвращается?
        """
        short_path_to_section = [i, "section"]

        section_fields = self.find_section_by_optimized_path(
            data, short_path_to_section
        )
        if "{urn:hl7-org:v3}component" in section_fields.keys():
            short_path_to_section = ["component", "section", "component"]
            section_fields = self.find_section_by_optimized_path(
                section_fields, short_path_to_section
            )
            return section_fields
        return None

    def get_ward_name(
        self,
        data: list,
        i,
    ):
        short_path_to_section = [
            i,
            "section",
            "title",
        ]
        section_fields = self.find_section_by_optimized_path(
            data, short_path_to_section
        )
        return section_fields["text"]

    def get_research_table(
        self,
        data,
        i,
        typed="table",
    ):
        short_path_to_section = ["section", "text"]

        if type(data) == list:
            short_path_to_section = [i, "section", "text"]

        section_fields = self.find_section_by_optimized_path(
            data, short_path_to_section
        )
        if typed != "table":
            return section_fields

        table = self.parse_table_wtheader(section_fields)

        return table

    def get_research_name(
        self,
        data,
        i,
    ):
        short_path_to_section = ["section", "title"]
        if type(data) == list:
            short_path_to_section = [i, "section", "title"]

        section_fields = self.find_section_by_optimized_path(
            data, short_path_to_section
        )
        return section_fields["text"]

    def compute_full_wards(
        self,
        data: dict,
    ):
        ward_result = {}

        ward_list = self.get_ward_list(data)

        for i in range(len(ward_list)):
            ward_name = self.get_ward_name(ward_list, i)

            res_list = self.get_research_list(ward_list, i)
            research_result = {}
            if res_list:
                for j in range(len(res_list)):
                    res_name = self.get_research_name(res_list, j)
                    res_table = self.get_research_table(res_list, j, "r")
                    research_result[res_name] = res_table

            ward_result[ward_name] = research_result
        return ward_result

    def get_final_table1(
        self,
        data: dict,
    ):
        short_path_to_section = [
            "component",
            "structuredBody",
            "component",
            "section",
            "component",
            4,
            "section",
            "text",
        ]

        section_fields = self.find_section_by_optimized_path(
            data, short_path_to_section
        )
        table = self.parse_table_2(section_fields)

        return table

    def get_final_table2(
        self,
        data: dict,
    ):
        short_path_to_section = [
            "component",
            "structuredBody",
            "component",
            "section",
            "component",
            4,
            "section",
            "component",
            "section",
            "text",
        ]

        section_fields = self.find_section_by_optimized_path(
            data, short_path_to_section
        )
        table = self.parse_table_2(section_fields)

        return table

    def parse_table_2(
        self,
        json_data,
        prefix="{urn:hl7-org:v3}",
    ):
        """
        For small tables works better.
        """

        adjusted_rows = []
        headers = [
            header["text"]
            for header in json_data[f"{prefix}table"][f"{prefix}thead"][f"{prefix}tr"][
                f"{prefix}th"
            ]
        ]

        # Get the table rows
        rows = json_data[f"{prefix}table"][f"{prefix}tbody"][f"{prefix}tr"]

        # If rows is a dictionary (single row), convert it to a list
        if isinstance(rows, dict):
            rows = [rows]

        # Process each row
        for row in rows:
            current_row = []
            for cell in row[f"{prefix}td"]:
                # Handle cases where content might be missing or empty
                text_content = cell[f"{prefix}content"].get("text", "None")
                current_row.append(text_content)

            # Check if the row has fewer items than headers, and pad with 'None' for missing values
            while len(current_row) < len(headers):
                current_row.append("None")  # Assuming 'None' for missing data

            adjusted_rows.append(current_row)

        # Recreate the DataFrame with adjusted rows
        adjusted_df = pd.DataFrame(adjusted_rows, columns=headers)
        return adjusted_df
