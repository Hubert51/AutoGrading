import cv2
import numpy as np
import sys
from sample.database.database import Database
# from learning.number_recognization.seperate_number import store_data
from seperate_number import store_data

class Point(object):
    def __init__(self, ):
        pass



def overlap(cnt1, cnt2):
    [x1, y1, w1, h1] = cv2.boundingRect(cnt1)
    [x2, y2, w2, h2] = cv2.boundingRect(cnt2)
    if x1 > x2+w2 or x2 > x1+w1:
        return False

    if y1 > y2+h2 or y2 > y1+h1:
        return False


def enclose(inner, outer):
    '''
    :param cnt1:
    :param cnt2:
    :return: True if inner in outer
             False if cnt1 does not in cnt2
    '''
    [x1, y1, w1, h1] = cv2.boundingRect(inner)
    [x2, y2, w2, h2] = cv2.boundingRect(outer)
    if x1 > x2 and x1+w1 < x2+w2 and y1 > y2 and y1+h1 < y2+h2:
        return True

    return False


def training():
    db = Database("Ruijie", "XXXXXXXX", "142.93.59.116", "Student_grade")
    data = db.queryColsData("machine_learning", ["result", "img"] )
    samples = []
    response = [] # np.array(dtype=np.float32)
    for item in data:
        # print(item)
        samples.append(item[1].strip("[").strip("]").split(", "))
        response.append(item[0])



    # data = np.array(data)
    # print(data)
    samples = np.array(samples, dtype=np.float32)
    response = np.array(response, dtype=np.float32)
    # sys.exit(1)
    model = cv2.ml.KNearest_create()
    model.train(samples, cv2.ml.ROW_SAMPLE, response)
    return model


def clean_cnt(contours, im):
    new_contours = []
    height, weight, _ = im.shape
    max_area = 0.01 * height * weight
    for cnt in contours:
        [x,y,w,h] = cv2.boundingRect(cnt)
        if cv2.contourArea(cnt)>10 and h > 10 and cv2.contourArea(cnt)<max_area:
            new_contours.append(cnt)

    contours = new_contours

    new_contours = []
    i = 0
    while i != len(contours):
        j = 0
        while j <  len(contours):
            if i == j :
                j += 1
                continue
            if enclose(contours[i], contours[j]):
                contours.pop(i)
                i -= 1
            j += 1
        i += 1


    return contours



if __name__ == '__main__':
    #######   training part   ###############
    model = training()
    # samples = np.loadtxt('generalsample.txt',np.float32)
    # responses = np.loadtxt('generalresponse.txt',np.float32)
    # responses = responses.reshape((responses.size,1))
    #
    # model = cv2.ml.KNearest_create()
    # model.train(samples, cv2.ml.ROW_SAMPLE, responses)

    ############################# testing part  #########################


    # im_name = input("Enter the name of the image to learn: ")

    im = cv2.imread("test_image/learning3.png")
    scale1 = 700 / im.shape[0]
    im = cv2.resize(im, (int(im.shape[1]*scale1), int(im.shape[0]*scale1)) )
    im_copy = im.copy()
    # im = cv2.resize(im, None,fx = 0.4, fy = 0.4, interpolation = cv2.INTER_LINEAR)
    out = np.zeros(im.shape,np.uint8)
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,6)
    kernel = np.ones((2, 2), np.uint8)
    erosion = cv2.erode(thresh, kernel, iterations=1)

    new_sample = np.empty((0,100))
    new_response = []

    image,contours,hierarchy = cv2.findContours(erosion,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    print("The number of Cnt before clean is {}".format(len(contours)))
    contours = clean_cnt(contours, im)
    print("The number of Cnt after clean is {}".format(len(contours)))


    for cnt in contours:
        [x,y,w,h] = cv2.boundingRect(cnt)
        cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),1)
        roi = erosion[y:y+h,x:x+w]
        roismall = cv2.resize(roi,(10,10))
        roismall = roismall.reshape((1,100))
        roismall = np.float32(roismall)
        retval, results, neigh_resp, dists = model.findNearest(roismall, 1)
        string = str(int((results[0][0])))
        cv2.putText(out,string,(x,y+h),0,1,(0,255,0))

        cv2.imshow('im', im)
        cv2.imshow('out',out)

        sample = roismall.reshape((1, 100))
        key = cv2.waitKey(0)
        cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),1)

        print(key)
        if key == 13 or key == 32:
            new_response.append(int((results[0][0])))
            print("correct", int((results[0][0])))
        elif key == 27:
            break
        else:
            new_response.append(key)
            print("wrong", int(chr(key)))

        new_sample = np.append(new_sample, sample, 0)

    cv2.destroyAllWindows()
    new_sample = new_sample.astype(dtype=int)

    answer = input("Do you want to store data into database(y/n) -> ")
    if answer != 'Y' and answer != 'y':
        sys.exit(0)

    db_name = "Student_grade"
    data = []
    db = Database("Ruijie", "XXXXXXXX", "142.93.59.116", db_name)
    assert len(new_response) == len(new_sample)
    for i in range(len(new_sample)):
        db.insert_data([ new_response[i], list(new_sample[i]) ], "machine_learning")




    # np.savetxt("tmpsamples.txt", new_sample)
    # np.savetxt("tmpresponses.txt", new_response)
    #
    # tmp = open("tmpsamples.txt", "r")
    # sample = open("generalsample.txt", "a")
    #
    # for line in tmp:
    #     sample.write(line)
    #
    # sample.close()
    # tmp.close()
    #
    # tmp = open("tmpresponses.txt", "r")
    # response = open("generalresponse.txt", "a")
    #
    # for line in tmp:
    #     response.write(line)
    #
    # response.close()
    # tmp.close()
