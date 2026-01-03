import os
import json
import re

# Define small words for title case
small_words = {'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}

# Define misspellings and proper nouns corrections
replacements = {
    'pokemons': 'Pokemons',
    'posion': 'Poison',
    'powerfull': 'Powerful',
    'dargon': 'Dragon',
    'ledendary': 'Legendary',
    'defesne': 'Defense',
    'Stroing': 'Strong',
    'stringe': 'Strong',
    'accross': 'Across',
    'outlaire': 'Outlier',
    'ICe': 'Ice',
    'ledenday': 'Legendary',
    'aand': 'and',
    'slowe': 'Slow',
    'pokemon': 'Pokemon',
    'type': 'Type',
    'attack': 'Attack',
    'defense': 'Defense',
    'speed': 'Speed',
    'hp': 'HP',
    'special attack': 'Special Attack',
    'special defense': 'Special Defense',
    # Add more if needed
}

def title_case_header(line):
    # Remove leading # and spaces
    prefix = ''
    while line.startswith('#'):
        prefix += '#'
        line = line[1:]
    line = line.strip()
    if not line:
        return prefix + ' ' + line
    words = line.split()
    result = []
    for i, word in enumerate(words):
        if i == 0 or word.lower() not in small_words:
            result.append(word.capitalize())
        else:
            result.append(word.lower())
    return prefix + ' ' + ' '.join(result)

def beautify_markdown(text):
    lines = text.split('\n')
    new_lines = []
    for line in lines:
        line = line.rstrip()  # Remove trailing spaces
        # Fix misspellings and proper nouns
        for old, new in replacements.items():
            line = re.sub(r'\b' + re.escape(old) + r'\b', new, line, flags=re.IGNORECASE)
        # If it's a header, apply title case
        if line.strip().startswith('#'):
            line = title_case_header(line)
        new_lines.append(line)
    # Join and ensure proper spacing between elements
    # Split into paragraphs (separated by blank lines)
    paragraphs = []
    current = []
    for line in new_lines:
        if line.strip():
            current.append(line)
        else:
            if current:
                paragraphs.append('\n'.join(current))
                current = []
            paragraphs.append('')
    if current:
        paragraphs.append('\n'.join(current))
    # Join paragraphs with double newlines
    return '\n\n'.join(paragraphs)

def process_notebook(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for cell in data['cells']:
        if cell['cell_type'] == 'markdown':
            source_text = ''.join(cell['source'])
            beautified = beautify_markdown(source_text)
            cell['source'] = beautified.split('\n')
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=1)

def main():
    current_dir = os.getcwd()
    for file in os.listdir(current_dir):
        if file.endswith('.ipynb'):
            print(f"Processing {file}")
            process_notebook(os.path.join(current_dir, file))
    print("All notebooks processed.")

if __name__ == "__main__":
    main()