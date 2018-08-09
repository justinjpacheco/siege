import sys
import os
import uuid
import json

def create(user):

    users_dir = '/data/users'

    if not os.path.isdir(users_dir):
      os.mkdir(users_dir)

    user_id = str(uuid.uuid4())
    user_file = "{0}.json".format(os.path.join(users_dir,user_id))


    data = {
      "id": user_id,
      "username": user['username']
    }

    with open(user_file,"w+") as file:
      file.write(json.dumps(data,indent=4,sort_keys=True))

    return data
