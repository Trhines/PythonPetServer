TABLES = {}

#collective- uuid, collectiveName, collectiveMembers(has many users, foreign key)
TABLES['collective'] = (
    "CREATE TABLE `collective` ("
    " `collective_id` int NOT NULL AUTO_INCREMENT,"
    " `collective_name` varchar(30) NOT NULL,"
    " PRIMARY KEY (`collective_id`)"
    ")"
)

#user- uuid, email, password, collective(has one collective, foreign key)
TABLES['user'] = (
    "CREATE TABLE `user` ("
    " `user_id` int NOT NULL AUTO_INCREMENT,"
    " `collective_id` int,"
    " `name` varchar(30) NOT NULL,"
    " PRIMARY KEY (`user_id`),"
    " FOREIGN KEY (`collective_id`) REFERENCES `collective` (`collective_id`)"
    ")"
)

#like- uuid, animalID, location, user(user that created the like), collective(what collective taht user is in)
TABLES['likes'] = (
    "CREATE TABLE `likes` ("
    " `like_id` int NOT NULL AUTO_INCREMENT,"
    " `animal_type` varchar(30) NOT NULL,"
    " `collective_id` int NOT NULL,"
    " `user_id` int NOT NULL,"
    " FOREIGN KEY (`collective_id`) REFERENCES `collective` (`collective_id`),"
    " FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),"
    " PRIMARY KEY (`like_id`)"
    ")"
)

#match- created when one collective contains a like with the same animalID, contains same info with new uuid
TABLES['matches'] = (
    "CREATE TABLE `matches` ("
    " `match_id` int NOT NULL AUTO_INCREMENT,"
    " `animal_type` varchar(30) NOT NULL,"
    " `collective_id` int NOT NULL,"
    " FOREIGN KEY (`collective_id`) REFERENCES `collective` (`collective_id`),"
    " PRIMARY KEY (`match_id`)"
    ")"
)


