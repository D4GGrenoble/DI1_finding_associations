import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

replacements = {'éèêë':'e', 'àâä':'a', 'ùûü':'u', 'ôö':'o', 'îï':'i'}
sep = {',', ';', '(', "'", ')', ';', '\\', ' ', '’'}
unwanted = {'y', 'c', 'de', 'le', 'd', 'l', 'du', 'la', 'un', 'une', 'des', 'les', 'et', 'a', 'à', 'au', 'association', 'activités', 'associations'}
folder = 'C:\\Users\\evill\\Documents\\D4GG_charities\\small_data_shipped\\'
filename = 'clean_data_small.csv'
test_mode = False
verbose_mode = False


def clean_word(word):
    cleaned_word = word.lower()
    for accents in replacements:
        for a in accents:
            cleaned_word = cleaned_word.replace(a, replacements[accents])

    return cleaned_word


def extract_cat_words(cat_w, count_words):
    mod_count_words = count_words.copy()
    cat_df = pd.DataFrame(cat_w)
    cat_df['count'] = np.nan
    length = len(cat_w)
    for i in range(length):
        w = cat_w[i]
        if w in count_words.keys():
            cat_df.iloc[i, 1] = mod_count_words.get(w)
            del mod_count_words[w]
    return cat_df, mod_count_words


def create_wordcloud_list(word_list, in_count_words, verbose=True):
    # Create and generate a word cloud image:
    cat_df, count_words = extract_cat_words(word_list, in_count_words)
    cat_freq_dict = dict()
    for w, c in cat_df.values:
        cat_freq_dict[w] = c / len(cat_df)  # to get the frequencies

    if verbose:
        print(cat_df)
    out_wordcloud = WordCloud(width=1360, height=1200).generate_from_frequencies(cat_freq_dict)

    return out_wordcloud


def plot_wordcloud(in_wordcloud):
    # Display the generated image
    plt.imshow(in_wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    return


if test_mode:
    data = pd.read_csv(folder + filename, sep=',', nrows=100)
else:
    data = pd.read_csv(folder + filename, sep=',')

print(data.columns)

# social desc = free text description
print('objet social description -------------------')
print(data['objet_social1_desc'])

# What are their main objectives?
desc = data['objet_social1_desc'].dropna()

words = desc.str.split(pat=',', n=-1, expand=True)
words = words.stack().reset_index(drop=True)

desc_str = str(desc)
print(words.head())

# separate meaningful words and count them
count_words = dict()
for obj in desc:
    w = ''
    for c in obj:
        if c in sep:
            if w != '' and w not in unwanted:
                detected_word = clean_word(w)
                if detected_word not in count_words.keys():
                    count_words[detected_word] = 0
                count_words[detected_word] += 1
            w = ''
        else:
            w += c

print(count_words)

# make categories
cat_sport_w = ['sports', 'football', 'futsal', 'athletisme', 'pentathlon', 'footing', 'triathlon', 'jogging', 'petanque',
               'velo', 'vtt', 'course', 'cyclisme', 'danse']
cat_help_w = ['humanitaires', 'caritatives', 'aide', 'benevolat', 'developpement', 'urgence', 'solidarites']
#cat_culture_w = ['theatre', 'spectacles', 'variete']

stopwords_1 = set(STOPWORDS)
stopwords_1.update(unwanted)
#
# wordcloud_sport = WordCloud(stopwords=stopwords_1, background_color="black").generate(cat_sport_df[0])
# # Save picture
# wordcloud.to_file('wordcloud.png')




wordcloud_sport = create_wordcloud_list(cat_sport_w, count_words, verbose_mode)
plot_wordcloud(wordcloud_sport)
wordcloud_sport.to_file('wordcloud_sport.png')

wordcloud_help = create_wordcloud_list(cat_help_w, count_words, verbose_mode)
plot_wordcloud(wordcloud_help)
wordcloud_help.to_file('wordcloud_help.png')

# wordcloud_culture = create_wordcloud_list(cat_culture_w, count_words, verbose_mode)
# plot_wordcloud(wordcloud_culture)
