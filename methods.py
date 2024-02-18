from whoosh import index
from whoosh.fields import TEXT, Schema
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from openai import OpenAI
import re
import os

wiki_directory = 'wiki_files'
wiki_index = "wiki_index"
nltk.download("stopwords")
ps = PorterStemmer()
stop_words = set(stopwords.words("english"))


def tokenize_and_prepare(contents):
    words = []
    for content in contents:
        token = nltk.word_tokenize(content)
        token = [ps.stem(word) for word in token if (word.lower() not in stop_words)]
        words.append(token)
    return words


def tokenize(content):
    token = nltk.word_tokenize(content)
    token = [ps.stem(word) for word in token if (word.lower() not in stop_words)]
    return token


def parse_file(file_name):
    path = f'wiki_files/{file_name}'
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # get text based on what is between '[[' and ']]'
    # separate between what is between '[[' and ']]' and what is not
    # and what is outside, first matching what is inside then mathing what is outside
    text = re.split(r'\n*\[\[(.*?)\]\]\n', content)
    text = list(filter(lambda x: x.strip(), text))

    # get the title from every even element
    # get the contents from every odd element
    titles = text[0::2]
    contents = text[1::2]

    # tokeninze the contents and stem each word
    # check if the word is a stop word
    # if a word is a stop word remove it from the list
    tokenized_content = tokenize_and_prepare(contents)

    # return titles and contents
    return titles, tokenized_content


def get_questions():
    # read the questions.txt file
    with open("questions.txt", "r", encoding="utf-8") as file:
        content = file.read()

    # separate the text in 4 lines: category, clue, answer, newline
    # get the category from every first of four lines
    # get the clues from every seocnd of four lines
    # get the answer from every third of four lines
    # ignore the fourth line as it is a newline
    text = content.splitlines()
    categories = text[0::4]
    clues = text[1::4]
    answers = text[2::4]

    # return the categories, clues and answers
    return categories, clues, answers


def create_index():
    print("Creating index...")

    # Set up index schema
    schema = Schema(
        title=TEXT(stored=True),
        content=TEXT(stored=True),
    )

    # Create index file
    ix = index.create_in(wiki_index, schema)
    with ix.writer() as writer:
        for file_name in os.listdir(wiki_directory):
            title, content = parse_file(file_name)

            print(file_name + ' index added to index file')

            # from the list of titles and contents, add to the index file one by one
            if title and content:
                for i in range(len(content)):
                    content_string = ' '.join(content[i])
                    writer.add_document(title=title[i], content=content_string)

    print("Index creation finished")
    ix.close()


def call_chatGPT(gpt_string):
    # If the api_key does not work, try your own
    client = OpenAI(api_key="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")
    response = client.chat.completions.create(
        messages=
        [
            {
                "role": "user",
                "content": gpt_string,
            }
        ],
        model="gpt-3.5-turbo",
    )
    return response['choices'][0]['message']['content']