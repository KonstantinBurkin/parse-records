from hse3_files.parser_fucn import find_section_by_optimized_path


def get_amnez_life(data):
    short_path_to_section = ['component', 
                             'structuredBody', 
                             'component', 
                             'section', 
                             'component', 2,
                             'section', 
                             'text']


    section_fields = find_section_by_optimized_path(data, short_path_to_section)

    return section_fields['text']
