import mysql.connector
from mysql.connector import errorcode
import random
from schemas import TABLES
from seedData import USER_NAMES, GROUP_NAMES, ANIMAL_TYPES

try:
  db = mysql.connector.connect(user='root',
                                password='Greeksaregeeks1!',
                                database='sample_data')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

cursor = db.cursor()

for schema in reversed(TABLES):
  cursor.execute(f"DROP TABLE IF EXISTS {schema}")
print("Old data dropped")

for schema in TABLES:
    table_description = TABLES[schema]
    try:
        print(f"Creating table {schema}")
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print(f"{schema} already exists")
        else:
            print(err.msg)

print("\n--- tables created ---\n")

#generate users
for names in USER_NAMES:
  try:
    query = ("INSERT INTO user (name) VALUES (%s)")
    data = (f'{names}',)
    cursor.execute(query, data)
    db.commit()
  
  except mysql.connector.Error as err:
    print(err.msg)
print('\n--- users generated ---\n')

#generate groups
for groups in GROUP_NAMES:
  try:
    query = ("INSERT INTO collective (collective_name) VALUES (%s)")
    data = (f'{groups}',)
    cursor.execute(query, data)
    db.commit()

  except mysql.connector.Error as err:
    print(err.msg)
print('\n--- groups generated ---\n')

#assign users to existing groups
cursor.execute("SELECT collective_id FROM collective")
collectives = cursor.fetchall()
cursor.execute("SELECT user_id FROM user")
users = cursor.fetchall()

for id in users:
  try:
    update_user = ("UPDATE user SET collective_id = %s WHERE user_id = %s")
    user_args = (random.choice(collectives)[0], id[0])
    cursor.execute(update_user, user_args)
    db.commit()
  except mysql.connector.Error as err:
    print(err.msg)
print('\n--- groups assigned ---\n')

#make users/collectives "like" and "match" with animals
cursor.execute("SELECT user_id, collective_id FROM user")
user_data = cursor.fetchall()

for user in user_data:

  for x in range(0, 5):
    animal = random.choice(ANIMAL_TYPES)
    user_id = user[0]
    coll_id = user[1]

    #this chunk creates the likes
    try:
      query = ("INSERT INTO likes (animal_type, user_id, collective_id) VALUES (%s, %s, %s)")
      args = (animal, user_id, coll_id)
      cursor.execute(query, args)
      db.commit()
    except mysql.connector.Error as err:
      print(err.msg)

    #checks for potential matches
    try:
      query = ("SELECT * FROM likes WHERE animal_type = %s AND collective_id = %s")
      arg = (animal, coll_id)
      cursor.execute(query, arg)
      matches = cursor.fetchall()
      #if like exists check for matches
      if(len(matches)>0):
        try:
          #checks if match already exists
          query = ("SELECT * FROM matches WHERE animal_type = %s AND collective_id = %s")
          args = (animal, coll_id)
          cursor.execute(query, args)
          existing_matches = cursor.fetchall()
          #if no match exists, add match
          if(len(existing_matches)==0):
            try:
              query = ("INSERT INTO matches (animal_type, collective_id) VALUES (%s, %s)")
              args = (animal, coll_id)
              cursor.execute(query, args)
              db.commit()
            except mysql.connector.Error as err:
              print(err.msg)
        except mysql.connector.Error as err:
          print(err.msg)
    except mysql.connector.Error as err:
      print(err.msg)
print('\n--- likes and matches added ---\n')

#pandas