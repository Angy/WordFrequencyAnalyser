import re
from collections import Counter

from django.shortcuts import render
from .forms import FrequencyAnalyserForm


def home(request):
    if request.method == 'POST':
        form = FrequencyAnalyserForm(request.POST, request.FILES)

        if form.is_valid():
            # list of normalised words
            words_from_file = _get_file(fileinput=form.cleaned_data['file'])

            if form.cleaned_data['word']:
                #  alphabetically list of all the input words
                split_words = sorted(form.cleaned_data['word'].split(','))

                # all words and their frequencyies
                word_list = calculate_frequency_for_word(
                    word_list=words_from_file,
                    words=[words.strip() for words in split_words]
                )

                if form.cleaned_data['frequency']:
                    desired_frequency = form.cleaned_data['frequency']
                    # get a list of n frequent words
                    frequency = most_frequent_n_words(n=desired_frequency,
                                                      words=words_from_file)
                    text = '%d frequent words' % desired_frequency
                else:
                    # list of word(s) with highest frequency
                    frequency = calculate_highest_frequency(
                        word_list=word_list
                    )
                    text = 'Most frequent word'

            else:
                # get all the words from input file if no word is specified
                word_list = _all_words_count(
                    word_list=words_from_file
                )
                if form.cleaned_data['frequency']:
                    desired_frequency = form.cleaned_data['frequency']
                    # get a list of n frequent words in the value of n is
                    # provided
                    frequency = most_frequent_n_words(n=desired_frequency,
                                                      words=words_from_file)
                    text = '%d frequent words' % desired_frequency
                else:
                    # list words with highest frequency (ooccurance)
                    frequency = calculate_highest_frequency(
                        word_list=word_list)
                    text = 'Most frequent word'

            return render(request, 'home.html', {'form': form,
                                                 'counts': word_list,
                                                 'frequency': frequency,
                                                 'text': text})
    else:
        form = FrequencyAnalyserForm(data=None)
    return render(request, 'home.html', {'form': form})


def _get_file(fileinput):
    # read each line of the input file and stringify
    file = str(fileinput.read(), 'utf-8')

    # find all the words (a-z and/or A-Z)
    line = re.sub(r"[^A-Za-z\s]", "", file.strip())

    # split the line into normalised words, i.e. all with identical case
    word_list = [word.casefold() for word in line.split()]

    # return the alphabetically ordered list of normalised words
    return sorted(word_list)


def _all_words_count(*, word_list):
    word_count = dict()

    for word in word_list:
        word_count[word] = word_list.count(word)
    return word_count


def calculate_frequency_for_word(*, word_list, words):
    word_count = dict()

    # count the occurance of all input words in the list
    for word in words:
        word_count[word] = word_list.count(word)
    return word_count


def calculate_highest_frequency(*, word_list):
    most_common_words = []

    # check for the max frequency value in the list and append that word to
    # a new list
    highest_frequency = max(word_list.values())
    for word, ct in word_list.items():
        if ct == highest_frequency:
            most_common_words.append(word)
    return most_common_words


def most_frequent_n_words(*, n, words):
    counts = dict()
    # count the occurance of each word in the list and add both the values as
    # a key, pair to a dict
    for word in words:
        counts[word] = words.count(word)

    # optimise finding the most common n words from the dict
    word_frequency = Counter(counts)

    # alphabetically ordered list of keys that has n frequent occurance
    desired_frequency = sorted(
        [key for key, _ in word_frequency.most_common(n)]
    )

    return desired_frequency
