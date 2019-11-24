# README
To understrand the different files

# group_words.py
Reading the description of each association, and counting every time a word is appearing.
I then keep only words that appeared the most, and associciate every association with those words.

This file is trying to detect categories, but it is not efficient, since then, I discovered other libraries, which
I used for the 2nd attempt ...

# detect_categories.py
This file is basically doing the same thing than group_words.py, except that he use specialized librairies
like nltk and spacy. Those libraries allow me to automatically separate words, cleaning the stopwords, and lemmatizing
the words !

I think the result is great, it may be useful ! :D
