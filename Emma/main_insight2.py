import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

folder = 'C:\\Users\\evill\\Documents\\D4GG_charities\\small_data_shipped\\'
filename = 'clean_data_small.csv'
test_mode = False

if test_mode:
    data = pd.read_csv(folder + filename, sep=',', nrows=100)
else:
    data = pd.read_csv(folder + filename, sep=',')

print(data.columns)

# social desc = free text description
print('objet social description -------------------')
print(data['objet_social1_desc'])

print('objet -------------------')
print(data['objet'])

print('titre court---------------------------------')
print(data['titre_court'])

# What are their main objectives?
desc = data['objet_social1_desc']

words = desc.str.split(pat=',', n=-1, expand=True)
words = words.stack().reset_index(drop=True)

desc_str = str(desc)
print(words.head())

stopwords_1 = set(STOPWORDS)
unwanted = {'de', 'le', 'd', 'l', 'du', 'la', 'un', 'une', 'des', 'les', 'et', 'a', 'à', 'au', 'association', 'activités', 'associations'}
stopwords_1.update(unwanted)

# Create and generate a word cloud image:
wordcloud = WordCloud(stopwords=stopwords_1, background_color="black").generate(desc_str)

# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

# Save picture
wordcloud.to_file('wordcloud.png')
