def cluster_topics(json_data):
    import json
    import time
    import nltk
    import re
    import pandas as pd
    import numpy as np
    import scipy as sp
    import math
    from nltk.corpus import stopwords
    from nltk.stem.snowball import SnowballStemmer
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import normalize


    def tokenize_and_stem(text):
        # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
        tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
        for token in tokens:
            if re.search('[a-zA-Z]', token):
                filtered_tokens.append(token)
        stems = [stemmer.stem(t) for t in filtered_tokens]
        return stems


    def tokenize_only(text):
        # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
        tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
        for token in tokens:
            if re.search("[a-zA-Z]", token):
                filtered_tokens.append(token)
        return filtered_tokens

    # data = json.loads(open("example_revision.json").read())
    data = json.loads(json_data.read())
    stopwords = stopwords.words("english")
    stemmer = SnowballStemmer("english")

    # Extract messages
    messages = []
    time_stamps = []
    for i in range(len(data["items"])):
        message = (data["items"][i]["text"])
        time_stamp = data["items"][i]["created"]
        t = float(re.search("[0-9]*:[0-9]*", time_stamp).group(0).replace(":", "."))
        messages.append(message)
        time_stamps.append(t)

    # Extract stemmed and tokenized vocab
    totalvocab_stemmed = []
    totalvocab_tokenized = []
    for i in messages:
        allwords_stemmed = tokenize_and_stem(i)  # for each item in 'synopses', tokenize/stem
        totalvocab_stemmed.extend(allwords_stemmed)  # extend the 'totalvocab_stemmed' list

        allwords_tokenized = tokenize_only(i)
        totalvocab_tokenized.extend(allwords_tokenized)

    vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index=totalvocab_stemmed)
    # print('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')

    # Cluster messages according to topic using K-means
    # define vectorizer parameters
    tfidf_vectorizer = TfidfVectorizer(max_df=0.99, max_features=200000,
                                        min_df=0.01, stop_words='english',
                                        use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1, 3))

    # fit the vectorizer to messages
    # t1 = time.clock()
    tfidf_matrix = tfidf_vectorizer.fit_transform(messages)
    # t2 = time.clock()
    # print("Tf-Idf fit time: ", t2-t1)
    # print(tfidf_matrix.shape)
    terms = tfidf_vectorizer.get_feature_names()

    # insert additional time feature
    new_column = np.asarray(time_stamps).reshape(-1, 1)
    time_norm = normalize(new_column)
    # print(new_column.shape)
    final = sp.sparse.hstack((tfidf_matrix, new_column))
    # print(final.shape)
    terms.append('time')

    # calculate distance between messages using cosine similarity of tf-idf
    dist = 1 - cosine_similarity(final)

    # K-means clustering
    # num_clusters = 5
    num_clusters = math.floor(math.sqrt(len(messages)) / 2)

    km = KMeans(n_clusters=num_clusters)
    t3 = time.clock()
    km.fit(final)
    t4 = time.clock()
    #print("K-means fit time: ", t4 - t3)
    clusters = km.labels_.tolist()

    topics = {}
    for t in range(num_clusters):
        t_name = "topic" + str(t)
        topics[t_name] = {}
        t_messages = []
        for i in range(len(messages)):
            if clusters[i] == t:
                t_messages.append(messages[i])
        topics[t_name]['messages'] = t_messages

        # Export as json
        # with open('topics_time.json', 'w') as outfile:
        # json.dump(topics, outfile)


    # Inspect clusters
    # sorted_messages = {'message': messages, 'cluster': clusters}
    #
    # frame = pd.DataFrame(sorted_messages, index=[clusters], columns=['message', 'cluster'])
    # print(frame['cluster'].value_counts())
    #
    # # top words per cluster
    # print("Top terms per cluster:")
    # print()
    # # sort cluster centers by proximity to centroid
    # order_centroids = km.cluster_centers_.argsort()[:, ::-1]
    #
    # for i in range(num_clusters):
    #     print("Cluster %d words:" % i, end='')
    #
    #     for ind in order_centroids[i, :6]:  # replace 6 with n words per cluster
    #         print(' %s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'), end=',')
    #     print()  # add whitespace
    #     print()  # add whitespace
    #
    #     print("Cluster %d messages:" % i, end='')
    #     for message in frame.ix[i]['message'].values.tolist():
    #         print(' %s,' % message, end='')
    #     print()  # add whitespace
    #     print()  # add whitespace

    return topics