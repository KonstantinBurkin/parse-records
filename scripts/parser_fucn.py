import pandas as pd


def find_section_by_optimized_path(data, short_path, fields=None, prefix='{urn:hl7-org:v3}'):
    """
    Navigate a nested JSON structure along the specified path, automatically adding a prefix to string path elements.
    Optionally return only specific fields from the final block.
    
    :param data: The JSON data as a nested Python dictionary.
    :param short_path: The simplified path to the desired section as a list of keys and indices.
    :param fields: Optional. A tuple or list of field names to return from the final block. If None, returns the entire block.
    :param prefix: The prefix to add to string elements in the path.
    :return: The section at the specified path, or specific fields from the section, or None if the path is invalid.
    """
    current = data
    full_path = [(prefix + element) if isinstance(element, str) else element for element in short_path]
    
    try:
        for key in full_path:
            if isinstance(current, list):  # Handle list indices
                current = current[int(key)]
            else:  # Handle dictionary keys
                current = current[key]
                
        if fields and isinstance(fields, (list, tuple)) and isinstance(current, dict):
            return {field: current.get(field, None) for field in fields}
        
        return current
    except (KeyError, IndexError, ValueError, TypeError):
        return None  # Path was invalid
    

def parse_table(json_data, prefix = '{urn:hl7-org:v3}'):
    adjusted_rows = []
    headers = [header['text'] for header in json_data[f'{prefix}table'][f'{prefix}thead'][f'{prefix}tr'][f'{prefix}th']]

    for row in json_data[f'{prefix}table'][f'{prefix}tbody'][f'{prefix}tr']:
        current_row = []
        for cell in row[f'{prefix}td']:
            current_row.append(cell[f'{prefix}content']['text'])
        # Check if the row has fewer items than headers, if so, add a placeholder
        if len(current_row) < len(headers):
            current_row.append('None')  # Assuming 'Not specified' for missing doctor data
        adjusted_rows.append(current_row)

    # Recreate the DataFrame with adjusted rows
    adjusted_df = pd.DataFrame(adjusted_rows, columns=headers)
    return adjusted_df


def parse_table_wtheader(json_data, prefix = '{urn:hl7-org:v3}'):
    if json_data[f'{prefix}table'][f'{prefix}tbody'][f'{prefix}tr']:
        first_row = json_data[f'{prefix}table'][f'{prefix}tbody'][f'{prefix}tr'][0]
        num_columns = len(first_row[f'{prefix}td'])
        headers = [f'Column {i + 1}' for i in range(num_columns)]
    else:
        headers = []

    for row in json_data[f'{prefix}table'][f'{prefix}tbody'][f'{prefix}tr']:
        current_row = []
        for cell in row[f'{prefix}td']:
            cell_text = cell[f'{prefix}content'].get('text', 'None')  # Default to 'None' if 'text' is not available
            current_row.append(cell_text)
        adjusted_rows.append(current_row)

    # Recreate the DataFrame with adjusted rows
    adjusted_df = pd.DataFrame(adjusted_rows, columns=headers)
    return adjusted_df

