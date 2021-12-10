
# test script represents main methods



from database import Database
from parser import parse
# Create db:
db =Database()

# Create tables:

db.cmd(parse('''

CREATE cats (cat_id INDEXED, cat_owner_id INDEXED, cat_name);

'''))

db.cmd(parse('''

CREATE owners (owner_id INDEXED, age INDEXED, name);

'''))

# add values

db.cmd(parse('''

INSERT INTO owners(2, 25, Kolya);

'''))
db.cmd(parse('''

INSERT INTO owners(53, 535, Vasya);

'''))
db.cmd(parse('''

INSERT INTO owners(222, 15, Dima);

'''))

db.cmd(parse('''

INSERT INTO cats(22, 7, Murzik);

'''))
db.cmd(parse('''

INSERT INTO cats(99, 0, Pushok);

'''))
db.cmd(parse('''

INSERT INTO cats(666, -5, doggy);

'''))


# delete

db.cmd(parse('''

DELETE cats WHERE name = Murzik
;

'''))

# select

db.cmd(parse('''
SELECT *  FROM owners
  

'''))

print()
print()

db.cmd(parse('''
SELECT *  FROM cats WHERE name != Muerzik
  

'''))