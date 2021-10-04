
from pymongo import MongoClient

if __name__ == '__main__':

    client = MongoClient('localhost', 27017)
    db = client['instafollowers']
    user_name = 'cashcats'

    with open('followers.txt', 'w') as file:
        for doc in db.followers.find({'parent_name': user_name}):
            file.write(f'{str(doc)} \n')

    with open('following.txt', 'w') as file:
        for doc in db.following.find({'parent_name': user_name}):
            file.write(f'{str(doc)} \n')
