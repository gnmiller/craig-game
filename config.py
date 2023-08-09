from dotenv import dotenv_values

max_characters = 10
data = {
    'data_dir': 'rpg-data',
    'char_dir': 'character',
    'active_dir': 'active',
    'file_ext': 'pickle',
    'envs': dotenv_values(".env"),
    'max_characters': 10
}
