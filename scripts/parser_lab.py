"""parse lab records with LabParser class"""

import pandas as pd
from .mixin.parcer_functions import ParserFunctions

# from .parser_fucn import (
#     find_section_by_optimized_path,
#     convert_table_to_dataframe,
# )


class LabParser(ParserFunctions):
    """class for parsing lab records"""

    def clean_keys(
        self,
        obj: dict,
    ):
        """Recursively remove namespace prefixes from dictionary keys."""
        if isinstance(obj, dict):
            new_dict = {}
            for key, value in obj.items():
                new_key = key
                if key.startswith("{"):
                    new_key = key[key.find("}") + 1 :]
                new_dict[new_key] = self.clean_keys(value)
            return new_dict
        elif isinstance(obj, list):
            return [self.clean_keys(item) for item in obj]
        else:
            return obj

    def convert_table_to_dataframe(
        self,
        table_data: dict,
    ) -> pd.DataFrame:
        """Convert the given table data into a Pandas DataFrame."""
        # Clean the keys to remove namespace prefixes
        cleaned_data = self.clean_keys(table_data)

        # Extract column names from the table headers
        headers = cleaned_data["table"]["thead"]["tr"]["th"]
        col_names = [th.get("text", None) for th in headers]

        data_rows = []
        for row in cleaned_data["table"]["tbody"]["tr"]:
            td = row["td"]
            if isinstance(td, list):
                row_data = []
                for cell in td:
                    if "text" in cell:
                        row_data.append(cell["text"])
                    elif "content" in cell and "text" in cell["content"]:
                        row_data.append(cell["content"]["text"])
                    else:
                        row_data.append(None)
                # Ensure each row has the same number of columns
                if len(row_data) < len(col_names):
                    row_data.extend([None] * (len(col_names) - len(row_data)))
                data_rows.append(row_data)
            elif isinstance(td, dict):
                # Handle rows with colspan (e.g., section headers)
                if "content" in td and "text" in td["content"]:
                    text = td["content"]["text"]
                    row_data = [text] + [None] * (len(col_names) - 1)
                    data_rows.append(row_data)

        # Create the DataFrame

        df = pd.DataFrame(data_rows, columns=col_names)
        return df

    def get_table_1(
        self,
        data: dict,
    ) -> pd.DataFrame:
        """get table from lab records"""
        short_path_to_section = [
            "component",
            "structuredBody",
            "component",
            2,
            "section",
            "text",
        ]

        section_fields = self.find_section_by_optimized_path(
            data,
            short_path_to_section,
        )
        table = self.convert_table_to_dataframe(section_fields)

        return table

    def table_to_features(
        self,
        table: pd.DataFrame,
    ) -> dict:
        """convert table from lab record to features of new dataframe"""
        lab_features = (
            table.pivot_table(
                columns=["Показатель"],
                values=["Значение / чувствительность (для бак.исследований)"],
                aggfunc=lambda x: x,
            )
            .rename(
                columns={
                    # TODO: rename columns for final dataframe
                    "refds": "efrdwsa",
                }
            )
            .to_dict("records")[0]
        )
        lab_features.update(
            {
                "lab_date": table["Дата"].dropna().values[0],
            }
        )

        return lab_features
