import os
from os import path

# format: user-id wins losses

def write_game_result(file, winner, loser):
    data = read_stats(file)
    
    data[winner] = data.get(winner, [0, 0])
    data[loser] = data.get(loser, [0, 0])
    data[winner][0] += 1
    data[loser][1] += 1

    write_stats(file, data)
        

def read_stats(file):
    data = {}

    if path.exists(file):
        with open(file, "r") as f:
            for line in f.readlines():
                tokens = [ int(x) for x in line.split() ]
                data[tokens[0]] = [tokens[1], tokens[2]]

    return data

def write_stats(file, data):
    tmp = str(file) + ".tmp"

    with open(tmp, "w") as f:
        for user, score in data.items():
            f.write('{0} {1} {2}\n'.format(user, score[0], score[1]))
        f.flush()
        os.fsync(f.fileno()) 

    os.rename(tmp, file)

def get_stats(file):
    return read_stats(file)
