from scripts.parser_fucn import find_section_by_optimized_path, parse_table


def get_features_from_diagnosis_table(data) -> dict:
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

    section_fields = find_section_by_optimized_path(data, short_path_to_section)

    table = parse_table(section_fields)

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
