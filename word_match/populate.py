from pymongo import MongoClient

# with open("input.txt", "r") as f:
#     lines = []
#     for l in f.readlines():
#         if l != "\n" and l.find("Harvard") == -1:
#             l = l.split(". ")[1]
#             lines.append(l[:-2])
# with open("processed.txt", "w") as f:
#     for line in lines:
#         f.write(line + "\n")

with open("processed.txt", "r") as f:
    lines = []
    for l in f.readlines():
        lines.append(l)

port = 27017
host = 'localhost'
client = MongoClient(host, port)
db = client.passphrase

id = 30
for l in lines:
    mydict = {"pass": l[:-1], "id": id}
    id += 1
    db.phrases.insert_one(mydict)
