import sqlite3
import os
dir = os.listdir('./DBbackup')
counter = 0
for file in dir:
    counter += 1
    if file == 'dumps':
        print('passing dumps')
        continue
    con = sqlite3.connect('./DBbackup/' + file)
    with open('./DBbackup/dumps/'+file.strip('.db')+'.sql', 'w') as f:
        for line in con.iterdump():
            f.write('%s\n' % line)
    print(f'done creating dumps for {file}, done {counter}')

con = sqlite3.connect('./DBbackup/BTCUSDT.db')
cur = con.cursor()

dir = os.listdir('./DBbackup/dumps')
counter = 0
for file in dir:
    if file == 'BTCUSDT.sql':
        print(f'passing {file}')
        continue
    counter += 1
    f = open('./DBbackup/dumps/'+file, 'r')
    sql = f.read()  # watch out for built-in `str`
    cur.executescript(sql)
    print(f'done importing dumps for {file}, done {counter}')

