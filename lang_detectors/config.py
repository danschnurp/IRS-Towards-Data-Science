data_path = './data'
languages = ['cs', 'de', 'en', 'es', 'fr', 'it', 'pl', 'pt', 'ru', 'sk']
col_names = ['label', 'text']
model_path = './models'

# mappings of labels to numbers
lang2label = {}
label2lang = {}

# create mapping
for i, lang in enumerate(languages):
    lang2label[lang] = i
    label2lang[i] = lang
