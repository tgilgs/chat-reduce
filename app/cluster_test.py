import json
from extract_topics import cluster_topics
# print(data)
# print(data["items"][1]["text"])

processed_data = cluster_topics('static/files/example_revision.json')

with open('static/files/topic_clusters.json', 'w') as outfile:
    json.dump(processed_data, outfile)
