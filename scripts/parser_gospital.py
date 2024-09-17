from hse3_files.parser_fucn import find_section_by_optimized_path, parse_table


def get_gosp_info(data):
    short_path_to_section = ['component', 
                             'structuredBody', 
                             'component', 
                             'section', 
                             'text']
    
    section_fields = find_section_by_optimized_path(data, short_path_to_section)

    table = parse_table(section_fields)

    short_path_to_section = ['component', 
                             'structuredBody', 
                             'component', 
                             'section', 
                             'entry', 2, 
                             'observation', 
                             'value']
    
    section_fields = find_section_by_optimized_path(data, short_path_to_section)
    type_gosp = section_fields['displayName']

    short_path_to_section = ['component', 
                             'structuredBody', 
                             'component', 
                             'section', 
                             'entry', 3, 
                             'observation', 
                             'value']
    
    section_fields = find_section_by_optimized_path(data, short_path_to_section)
    way_gosp = section_fields['displayName']

    return table, type_gosp, way_gosp
