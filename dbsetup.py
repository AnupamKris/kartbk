from tinydb import TinyDB, Query
from bcrypt import hashpw, gensalt

db = TinyDB('user.json')


# data = {
#     'name': "event1",
#     'date': "2020-01-01",
#     'content': "Lorem ipsum dolor sit amet consectetur adipisicing elit. Recusandae commodi cupiditate deserunt, magnam amet veritatis quasi. Deserunt labore eum doloribus quis possimus iusto aspernatur consectetur. Alias nihil dolorem voluptatibus error dolore ea doloribus doloremque architecto ullam ratione, nisi eligendi id a aliquam officiis. Facere exercitationem assumenda, optio ex laborum ab.",
#     "images": [
#         "images\SetupScr.png",
#         "images\\vlcsnap-2024-04-11-22h31m39s779.png",
#         "images\\vlcsnap-2024-04-11-22h32m25s744.png"
#     ]
# }


data = {"username": "admin", "password": hashpw(
    "admin".encode(), gensalt()).decode()}

db.insert(data)
