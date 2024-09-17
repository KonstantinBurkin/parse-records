from hse3_files.parser_fucn import find_section_by_optimized_path

def get_sex(data):
    short_path_to_section = ['recordTarget', 
                             'patientRole', 
                             'patient', 
                             'administrativeGenderCode']
    
    section_fields = find_section_by_optimized_path(data, short_path_to_section)

    return section_fields['displayName']


def get_age(data):
    short_path_to_section = ['recordTarget', 
                             'patientRole', 
                             'patient', 
                             'birthTime']
    
    section_fields = find_section_by_optimized_path(data, short_path_to_section)

    return section_fields['value']
