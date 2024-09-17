from hse3_files.parser_fucn import find_section_by_optimized_path

def get_condition(data):
    short_path_to_section = ['component', 
                             'structuredBody', 
                             'component', 
                             'section', 
                             'component', 1, 
                             'section', 
                             'text', 
                             'content']
    
    section_fields = find_section_by_optimized_path(data, short_path_to_section)

    result = []
    for el in section_fields:
        result.append(el['text'])

    return result
