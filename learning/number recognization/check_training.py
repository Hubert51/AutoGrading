import numpy as np
import cv2
import sys
from sample.database.database import Database
import random


if __name__ == '__main__':
    if len(sys.argv) >= 3:
        print("Please input check_training.py number/percent of data")

    db = Database("Ruijie", "gengruijie123", "142.93.59.116", "Student_grade")
    data = db.queryColsData("machine_learning", ["result", "img"] )
    samples = []
    response = [] # np.array(dtype=np.float32)
    for item in data:
        # print(item)
        samples.append(item[1].strip("[").strip("]").split(", "))
        response.append(item[0])
    samples = np.array(samples, dtype=np.float32)
    response = np.array(response, dtype=np.float32)

    data_size = len(samples)

    number = 0
    if type(sys.argv[1]) == float:
        number = int(data_size * sys.argv[1])
    else:
        try:
            number = int(sys.argv[1])
        except:
            print("input value is invalid")
            exit(1)

    index = np.random.randint(0, data_size, number)
