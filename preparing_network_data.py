import pandas as pd
from collections import Counter
import csv

def read_csv(file_path):
    return pd.read_csv(file_path)

def process_data(df, language_list):
    """
    Process data from DataFrame, filter by language, and create a list of key content.
    """
    key_content_list = []
    for j in range(df.shape[0]):
        concept = str(df.at[j, 'Concept'])
        language = str(df.at[j, 'Language_name'])
        synonyms = str(df.at[j, 'Synonyms_number'])
        if language in language_list:
            content_list = [str(df.at[j, column_name]) for column_name in df.columns[6:]]
            for _, content in enumerate(content_list):
                if content != 'nan':
                    key_content = '%'.join([concept, content, synonyms])
                    key_content_list.append(key_content)
    return key_content_list

def calculate_weights(result):
    """
    Calculate weights based on the result dictionary.
    """
    result_new = {}
    for key in result:
        str_list = key.split(sep='%')
        str_new = str_list[0] + "%" + str_list[1]
        count_new = float(result.get(key, 'Null')) / (float(str_list[2]) if str_list[2] in ['2.0', '3.0', '4.0', '5.0'] else 1)
        result_new[str_new] = result_new.get(str_new, 0) + count_new
    return result_new

def write_csv(data_path, result_new, concept_list):
    """
    Write network data to CSV file.
    """
    with open(data_path, 'w', newline='') as csvfile:
        fieldnames = ['source', 'target', 'weight']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for key, value in result_new.items():
            source, target = key.split('%')
            if source != target.upper():
                if target.upper() in concept_list:
                    writer.writerow({'source': source.upper(), 'target': target.upper(), 'weight': value})
                else:
                    writer.writerow({'source': source.upper(), 'target': target, 'weight': value})

# Define paths and lists
database_csv_path = r'/Cross-Linguistic Database of Polysemous Basic Vocabulary.csv'
network_data_path = '/file.csv'
language_list = ['Arabic', 'Armenian', 'Basque', 'Bengali', 'Bouyei', 'Burmese', 'Croatian', 'Czech', 'Danish', 'Dutch', 'Finnish', 'French', 'German', 'Greek', 'Hausa', 'Hawaiian', 'Hebrew', 'Hindi', 'Hungarian', 'Icelandic', 'Indonesia', 'Irish', 'Italian', 'Japanese', 'Khmer', 'Korean', 'Kyrgyz', 'Lao', 'Latin', 'Li', 'Lingao', 'Lithuanian', 'Malagasy', 'Malay', 'Manchu', 'Maori', 'Marshallese', 'Mongolian', 'Norsk', 'Pali', 'Pashto', 'Persian', 'Polish', 'Portuguese', 'Russian', 'Scottishgaelic', 'Shan', 'Slovak', 'Spanish', 'Swahili', 'Swedish', 'Tamil', 'Telugu', 'Thai', 'Turkish', 'Urdu', 'Uyghur', 'Vietnam', 'Zhuang']
concept_list = ['I', 'YOU', 'THIS', 'THAT', 'WHO', 'WHAT', 'NOT', 'ONE', 'TWO', 'THREE', 'MANY', 'BIG', 'LONG', 'SMALL', 'BLACK', 'WHITE', 'COLD', 'BAD', 'HOT', 'GOOD', 'NEW', 'OLD', 'SQUARE', 'ROUND', 'WOMAN', 'MAN', 'HUMAN', 'PERSON', 'DOG', 'BIRD', 'HEAD', 'EYE', 'EAR', 'MOUTH', 'HAND', 'HEART', 'FOOT', 'BLOOD', 'BONE', 'SEE_LOOK', 'EAT', 'DRINK', 'HEAR_LISTEN', 'SLEEP', 'DIE', 'COME', 'GO', 'STAND', 'SAY', 'GIVE', 'SUN', 'MOON', 'WATER', 'STONE', 'RAIN', 'TREE', 'EARTH_SOIL', 'FIRE', 'SKY', 'NIGHT']
#28language_list=['Hausa', 'Finnish', 'Lao', 'Hebrew', 'Malagasy', 'Bouyei', 'Burmese', 'Mongolian', 'Indonesia', 'Zhuang', 'Chinese', 'Telugu', 'Kyrgyz', 'Basque', 'Maori', 'Malay', 'Arabic', 'Turkish', 'Korean', 'Uyghur', 'Manchu', 'Li', 'Thai', 'Lingao', 'Shan', 'Vietnam', 'Hawaiian', 'Tamil']

# Main execution
df = read_csv(database_csv_path)
key_content_list = process_data(df, language_list)
result = Counter(key_content_list)
result_new = calculate_weights(result)
write_csv(network_data_path, result_new, concept_list)
