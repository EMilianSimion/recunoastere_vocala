from bson import ObjectId
from pymongo import MongoClient
import Levenshtein as lev


class RandomWord:
    def __init__(self):
        self.port = 27017
        self.host = 'localhost'
        self.client = MongoClient(self.host, self.port)
        self.passphrase = None
        self._id = None
        self.error = None

    def distance_levenshtein(self, str1, str2):
        """distance means number of insertion/deletion/substitution
            ratio means similarity ratio"""
        distance = lev.distance(str1.lower(), str2.lower())
        ratio = lev.ratio(str1.lower(), str2.lower())
        return (distance, ratio)

    def takePhraseForDB(self, user=None):
        user = user.lower()
        passphrase = "Nu s-a putut returna o fraza"
        db = self.client.passphrase
        try:
            var = db.istoricPhrases.find({}, {'_id': 0, 'user': 1})
            list_of_users = [v['user'] for v in var]
            if user not in list_of_users:
                print('nu se gaseste')
                var = db.phrases.aggregate([
                    {"$sample": {"size": 1}}
                ])
                for item in var:
                    id = item['id']
                    passphrase = item['pass']
                    user_history = [id]
                    db.istoricPhrases.insert_one(
                        {
                            'user': user,
                            'last_use': user_history
                        }
                    )
                    break
            else:
                print('l-am gasit')
                var = db.istoricPhrases.find({"user": user})[0]
                user_history = var['last_use']
                _id = var['_id']

                var = db.phrases.aggregate([
                    {'$match': {'id': {'$nin': user_history}}},
                    {'$sample': {'size': 1}}]
                )
                for item in var:
                    id = item['id']
                    passphrase = item['pass']
                    if len(user_history) >= 500:
                        user_history = user_history[1:]
                    user_history.append(id)
                    db.istoricPhrases.find_one_and_update(
                        {"_id": ObjectId(_id)},
                        {"$set":
                             {'last_use': user_history}
                         }
                    )
                    break
            return passphrase
        except Exception as e:
            print(e)

#
# rW = RandomWord()
# if __name__ == '__main__':
#     print(rW.takePhraseForDB("maria"))
