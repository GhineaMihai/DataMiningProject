from whoosh import index
from whoosh.qparser import QueryParser
from whoosh.query import Or
import methods


create_index_value = input('Do you want to create the index? (Y/N) ')
if create_index_value == 'Y':
    methods.create_index()
if create_index_value != 'N' and create_index_value != 'Y':
    print('Use Y or N, capitalized ')
    exit()

category_value = input('Do you want to use the categories when searching the index file? (Y/N) ')
if category_value == 'Y':
    with_category = True
elif category_value == 'N':
    with_category = False
else:
    print('Use Y or N, capitalized ')
    exit()

chatGPT_value = input('Do you want to use ChatGPT? (Y/N)\n'
                      'If api key is no longer available, you have to use one of your own. Change in call_chatgpt method ')
if chatGPT_value == 'Y':
    with_chatGPT = True
elif chatGPT_value == 'N':
    with_chatGPT = False
else:
    print('Use Y or N, capitalized ')
    exit()

# Get the lists of categories, questions and the titles
categories, clues, titles = methods.get_questions()
ix = index.open_dir(methods.wiki_index)
query_parser = QueryParser("content", ix.schema)
matches = 0
matches_first_10 = 0
chatGPT_matches = 0

# There are 100 questions
for i in range(100):
    first_10_results = []
    # Tokenize the clues like we did for the text
    token = methods.tokenize(clues[i])
    word_queries = []
    for word in token:
        word_queries.append(query_parser.parse(word))
    if with_category:
        # Tokenize the categories like we did for the text
        token = methods.tokenize(categories[i])
        category_queries = []
        for word in token:
            category_queries.append(query_parser.parse(word))
        word_queries += category_queries

    combined_query = Or(word_queries)
    with ix.searcher() as searcher:
        results = searcher.search(combined_query)
        # Construct the question fot ChatGPT to answer
        if with_chatGPT:
            gptResult = [results[j]["title"] for j in range(10)]
            gptString = "What is the answer to the following question: " + str(clues[i]) +\
                        "Choose one of the following, only type the answer: \"" + str(gptResult) + "\"."
            print(gptString)
        # Print the result from the question.txt file
        # Print the first 10 results from the query search
        print('----------------------')
        print(titles[i])
        print("First 10 results: ")
        for j in range(10):
            print(results[j]["title"])
        print('-----------------------')
        # If the first result from the query search
        # is the actual result, increase the number of matches
        if len(results) > 0 and results[0]["title"] == titles[i]:
            matches = matches + 1
        # If the one of the top 10 results from the query search
        # is the actual result, increase the number of matches
        for j in range(10):
            first_10_results.append(results[j]["title"])
        if len(results) > 0 and titles[i] in first_10_results:
            matches_first_10 = matches_first_10 + 1
    if with_chatGPT:
        # If the ChatGPT result is the actual result,
        # increase the number of matches
        if len(results) > 0:
            res = methods.call_chatGPT(gptString)
            if res == titles[i]:
                chatGPT_matches = chatGPT_matches + 1

print('P@1=' + str(matches / 100))
print('ResInFirst10=' + str(matches_first_10 / 100))

if with_chatGPT:
    print('ResChatGPT=' + str(chatGPT_matches / 100))
