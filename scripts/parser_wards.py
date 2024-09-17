from hse3_files.parser_fucn import find_section_by_optimized_path, parse_table


def get_ward_table(data):
    short_path_to_section = ['component', 
                             'structuredBody', 
                             'component', 
                             'section', 
                             'component', 3, 
                             'section', 
                             'text']


    section_fields = find_section_by_optimized_path(data, short_path_to_section)

    table = parse_table(section_fields)
    return table
