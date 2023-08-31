from __future__ import print_function
import sys
import cv2 as cv
import os
from datetime import datetime
from pathlib import Path
import math


def main(argv):
    if (len(argv) < 4):
        print('Not enough parameters')
        print('Usage:\nmatch_templ1ate_demo.py <image_name> <templ1ate_name> [<mask_name>]')
        return -1

    ## [load_image]
    global img
    global img2
    global templ1
    global filename
    global templ2
    global templ12
    global templ22

    filename = argv[5]

    if (len(argv) > 6):
        global use_img_rotate
        use_img_rotate = True
    else:
        use_img_rotate = False

    match_method = cv.TM_CCOEFF_NORMED
    ## [load_image]
    if img is None:
        print("Failed to load image", argv[1])
        return -1

    img = cv.imread(argv[1], cv.IMREAD_COLOR)
    img2 = cv.imread(argv[7], cv.IMREAD_COLOR)
    templ1 = cv.imread(argv[2], cv.IMREAD_COLOR)
    templ2 = cv.imread(argv[3], cv.IMREAD_COLOR)
    templ12 = cv.imread(argv[8], cv.IMREAD_COLOR)
    templ22 = cv.imread(argv[9], cv.IMREAD_COLOR)

    if argv[4] == False:
        if use_img_rotate == True:
            # MatchingMethod(match_method,argv[6],argv[5])
            is_acc(match_method, argv[6], argv[5], argv[7])
        else:
            folder_name = 'single_test'
            MatchingMethod(match_method, 1, folder_name)

    else:
        rotate_angle = argv[4]
        for i in range(rotate_angle):
            ##rotate
            # Get the image shape
            (h, w) = templ1.shape[:2]

            # Calculate the center of the image
            center = (w // 2, h // 2)

            # Perform the rotation
            angle = i  # Degrees
            scale = 1.0  # Scale factor
            M = cv.getRotationMatrix2D(center, angle, scale)
            templ1 = cv.warpAffine(templ1, M, (w, h))
            match_method = cv.TM_CCOEFF_NORMED

            if use_img_rotate == True:
                # MatchingMethod(match_method,i,argv[5])
                is_acc(match_method, i, argv[5], argv[7])
                # print(argv[5])
            else:
                folder_name = 'single_test'
                MatchingMethod(match_method, i, folder_name)
                # print(folder_name)

    return 0
    ## [wait_key]


def MatchingMethod(param, i, folder_name):
    global match_method
    match_method = param
    ## [copy_source]
    img_display = img.copy()
    ## [copy_source]
    ## [match_templ1ate]
    method_accepts_mask = (cv.TM_SQDIFF == match_method or match_method == cv.TM_CCORR_NORMED)
    result1 = cv.matchTemplate(img, templ1, match_method)
    result2 = cv.matchTemplate(img, templ2, match_method)

    ## [match_templ1ate]

    ## [normalize]
    cv.normalize(result1, result1, 0, 1, cv.NORM_MINMAX, -1)
    cv.normalize(result2, result2, 0, 1, cv.NORM_MINMAX, -1)
    ## [normalize]
    ## [best_match]
    _minVal, _maxVal, minLoc, maxLoc = cv.minMaxLoc(result1, None)
    _minVal2, _maxVal2, minLoc2, maxLoc2 = cv.minMaxLoc(result2, None)
    ## [best_match]

    ## [match_loc]
    if (match_method == cv.TM_SQDIFF or match_method == cv.TM_SQDIFF_NORMED):
        matchLoc = minLoc
    else:
        matchLoc = maxLoc
    if (match_method == cv.TM_SQDIFF or match_method == cv.TM_SQDIFF_NORMED):
        matchLoc2 = minLoc2
    else:
        matchLoc2 = maxLoc2
    ## [match_loc]
    # print(matchLoc)
    # print(matchLoc2)
    ## [imshow]
    loc = str(matchLoc)
    locx = str(matchLoc[0])
    locy = str(matchLoc[1])
    loc2 = str(matchLoc2)
    locx2 = str(matchLoc2[0])
    locy2 = str(matchLoc2[1])
    cv.rectangle(img_display, matchLoc, (matchLoc[0] + templ1.shape[0], matchLoc[1] + templ1.shape[1]), (0, 0, 255), 2,
                 8, 0)
    cv.rectangle(result1, matchLoc, (matchLoc[0] + templ1.shape[0], matchLoc[1] + templ1.shape[1]), (0, 0, 0), 2, 8, 0)
    cv.rectangle(img_display, matchLoc2, (matchLoc2[0] + templ2.shape[0], matchLoc2[1] + templ2.shape[1]), (255, 0, 0),
                 2, 8, 0)
    cv.rectangle(result1, matchLoc, (matchLoc2[0] + templ2.shape[0], matchLoc2[1] + templ2.shape[1]), (0, 0, 0), 2, 8,
                 0)
    cv.putText(img_display, loc, (208, 55), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv.putText(img_display, loc2, (208, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    # cv.imshow(image_window, img_display)
    # cv.imshow(result1_window, result1)

    start_point = (int(matchLoc[0] + (templ1.shape[1]) / 2), int(matchLoc[1] + (templ1.shape[0]) / 2))
    end_point = (int(matchLoc2[0] + (templ2.shape[1]) / 2), int(matchLoc2[1] + (templ2.shape[0]) / 2))
    color = (0, 255, 0)
    thickness = 10

    cv.line(img_display, start_point, end_point, color, thickness)
    if end_point[0] - start_point[0] == 0:
        tan = 0
    else:
        tan = (end_point[1] - start_point[1]) / (end_point[0] - start_point[0])
    # print(tan)
    theta_rad = math.atan(tan)
    theta_deg = math.degrees(theta_rad)
    theta_deg = round(theta_deg, 1)
    # print(theta_deg)
    cv.putText(img_display, 'angle(deg) : ' + str(theta_deg), (500, 80), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)

    cv.imwrite('./symbol/img_result/test/' + filename + '/' + str(i) + ".jpg", img_display)
    f.write(folder_name + ',' + str(i) + ',' + locx + ',' + locy + locx2 + ',' + ',' + locy2 + '\n')
    # print(filename+'/'+str(i))
    # if matchLoc[0] and matchLoc[1] != 285:
    # g.write(str(folder_name)+','+str(i)+','+locx+','+locy+'\n')
    ## [imshow]
    pass


def is_acc(param, i, folder_name, k):
    global match_method
    match_method = param
    (w1, h1) = img.shape[:2]
    roi_width = int(w1 / 2)
    roi_height = int(h1 / 2)
    roi_width2 = int(w1 / 3)
    roi_height2 = int(h1 / 3)

    # ROI 시작점과 종료점 좌표 계산
    # start_x = w1 - roi_width
    # start_y = h1 - roi_height
    # end_x = w1
    # end_y = h1
    # print(w1,h1)
    ## [copy_source]
    img_display = img.copy()
    img2_display = img2.copy()
    ## [copy_source]
    ## [match_templ1ate]
    method_accepts_mask = (cv.TM_SQDIFF == match_method or match_method == cv.TM_CCORR_NORMED)
    # result1 = cv.matchTemplate(img, templ1, match_method)
    result1 = cv.matchTemplate(img[roi_width2:w1 - roi_width2, roi_height2:h1 - roi_height2], templ1, match_method)
    # result2 = cv.matchTemplate(img, templ2, match_method)
    result2 = cv.matchTemplate(img[roi_width:, roi_height:], templ2, match_method)
    result11 = cv.matchTemplate(img2, templ12, match_method)
    result12 = cv.matchTemplate(img2, templ22, match_method)

    ## [match_templ1ate]
    # 입력 이미지 크기 확인
    image_height, image_width = img.shape[:2]
    #
    # # 관심영역(ROI) 크기 계산
    roi_width = int(image_width / 2)
    roi_height = int(image_height / 2)
    roi_width2 = int(image_width / 3)
    roi_height2 = int(image_height / 3)

    # ROI 시작점과 종료점 좌표 계산

    ## [normalize]
    cv.normalize(result1, result1, 0, 1, cv.NORM_MINMAX, -1)
    cv.normalize(result2, result2, 0, 1, cv.NORM_MINMAX, -1)
    cv.normalize(result11, result11, 0, 1, cv.NORM_MINMAX, -1)
    cv.normalize(result12, result12, 0, 1, cv.NORM_MINMAX, -1)
    ## [normalize]
    ## [best_match]
    _minVal, _maxVal, minLoc, maxLoc = cv.minMaxLoc(result1, None)
    _minVal2, _maxVal2, minLoc2, maxLoc2 = cv.minMaxLoc(result2, None)
    _minVal3, _maxVal3, minLoc3, maxLoc3 = cv.minMaxLoc(result11, None)
    _minVal4, _maxVal4, minLoc4, maxLoc4 = cv.minMaxLoc(result12, None)
    ## [best_match]

    ## [match_loc]
    if (match_method == cv.TM_SQDIFF or match_method == cv.TM_SQDIFF_NORMED):
        matchLoc = minLoc
    else:
        matchLoc = maxLoc
    if (match_method == cv.TM_SQDIFF or match_method == cv.TM_SQDIFF_NORMED):
        matchLoc2 = minLoc2
    else:
        matchLoc2 = maxLoc2
    if (match_method == cv.TM_SQDIFF or match_method == cv.TM_SQDIFF_NORMED):
        matchLoc3 = minLoc3
    else:
        matchLoc3 = maxLoc3
    if (match_method == cv.TM_SQDIFF or match_method == cv.TM_SQDIFF_NORMED):
        matchLoc4 = minLoc4
    else:
        matchLoc4 = maxLoc4
    ## [match_loc]
    # print(matchLoc)
    # print(matchLoc2)
    ## [imshow]
    loc = str(matchLoc)
    locx = str(matchLoc[0])
    locy = str(matchLoc[1])
    loc2 = str(matchLoc2)
    locx2 = str(matchLoc2[0])
    locy2 = str(matchLoc2[1])
    loc3 = str(matchLoc3)
    locx3 = str(matchLoc3[0])
    locy3 = str(matchLoc3[1])
    loc4 = str(matchLoc4)
    locx4 = str(matchLoc4[0])
    locy4 = str(matchLoc4[1])
    cv.rectangle(img_display, (matchLoc[0] + roi_width2, matchLoc[1] + roi_height2),
                 (matchLoc[0] + templ1.shape[0] + roi_width2, matchLoc[1] + templ1.shape[1] + roi_height2), (0, 0, 255),
                 2,
                 8, 0)
    # cv.rectangle(result1, (matchLoc[0] + roi_width, matchLoc[1] + roi_height),
    #              (matchLoc[0] + templ1.shape[0] + roi_width, matchLoc[1] + templ1.shape[1] + roi_height), (0, 0, 255), 2,
    #              8, 0)
    cv.rectangle(img_display, (matchLoc2[0] + roi_width, matchLoc2[1] + roi_height),
                 (matchLoc2[0] + templ2.shape[0] + roi_width, matchLoc2[1] + templ2.shape[1] + roi_height), (255, 0, 0),
                 2, 8, 0)
    # cv.rectangle(result1, (matchLoc2[0] + roi_width2, matchLoc2[1] + roi_height2),
    #              (matchLoc2[0] + templ2.shape[0] + roi_width2, matchLoc2[1] + templ2.shape[1] + roi_height2), (255, 0, 0),
    #              2, 8, 0)
    cv.putText(img_display, loc, (208, 55), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv.putText(img_display, loc2, (208, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    # cv.imshow(image_window, img_display)
    # cv.imshow(result1_window, result1)

    start_point = (
    roi_width2 + int(matchLoc[0] + (templ1.shape[1]) / 2), int(roi_height2 + matchLoc[1] + (templ1.shape[0]) / 2))
    end_point = (
    int(roi_width + matchLoc2[0] + (templ2.shape[1]) / 2), int(matchLoc2[1] + (templ2.shape[0]) / 2) + roi_height)
    start_point2 = (int(matchLoc3[0] + (templ1.shape[1]) / 2), int(matchLoc3[1] + (templ1.shape[0]) / 2))
    end_point2 = (int(matchLoc4[0] + (templ2.shape[1]) / 2), int(matchLoc4[1] + (templ2.shape[0]) / 2))
    color = (0, 255, 0)
    thickness = 10

    cv.line(img_display, start_point, end_point, color, thickness)
    cv.line(img2_display, start_point2, end_point2, color, thickness)
    if end_point[0] - start_point[0] == 0:
        tan = 0
    else:
        tan = (end_point[1] - start_point[1]) / (end_point[0] - start_point[0])
    if end_point2[0] - start_point2[0] == 0:
        tan2 = 0
    else:
        tan2 = (end_point2[1] - start_point2[1]) / (end_point2[0] - start_point2[0])

    # print(tan)
    theta_rad = math.atan(tan)
    theta_deg = math.degrees(theta_rad)
    theta_deg = round(theta_deg, 1)

    theta_rad2 = math.atan(tan2)
    theta_deg2 = math.degrees(theta_rad2)
    theta_deg2 = round(theta_deg2, 1)
    if (35 < theta_deg < 60):
        pass
    else:
        theta_deg = 180

    if (0 == theta_deg2 or 80 <= abs(theta_deg2) <= 90 or -90 <= theta_deg2 <= -40):
        pass
    else:
        theta_deg2 = 180

    # print(theta_deg)
    cv.putText(img_display, 'angle(deg) : ' + str(theta_deg), (500, 80), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
    cv.putText(img2_display, 'angle(deg) : ' + str(theta_deg2), (500, 80), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)
    cv.imwrite('./symbol/img_result/test/' + filename + '/' + str(i) + ".jpg", img_display)
    cv.imwrite('./symbol/img_result/test/' + filename + '_2' + '/' + str(i) + ".jpg", img2_display)
    theta_brake = abs(theta_deg2)

    if 90 > theta_brake > 80 or theta_deg2 == 0:
        acc.write(folder_name + ',' + str(i) + ',' + str(theta_deg) + ',' + ',' + str(theta_brake) + '\n')  # acc
    else:
        acc.write(folder_name + ',' + str(i) + ',' + ',' + str(theta_deg) + ',' + str(theta_brake) + '\n')  # brake

    # print(filename+'/'+str(i))
    # if matchLoc[0] and matchLoc[1] != 285:
    # g.write(str(folder_name)+','+str(i)+','+locx+','+locy+'\n')
    ## [imshow]

    pass


if __name__ == "__main__":
    # print(sys.argv)

    now = datetime.now()
    filename = datetime.now().strftime("%m-%d-%H%M%S")
    try:
        os.mkdir("./symbol/img_result/test/" + filename)
    except:
        pass
    try:
        os.mkdir("./symbol/img_result/test/" + filename + '_2')
    except:
        pass

    f = open("./data/test/" + filename + ".csv", 'a', encoding='utf-8')
    f.write("img_angle" + ',' + "templ1ate_rotating_angle" + ',' + 'x' + ',' + 'y' + '\n')

    acc = open("./data/test/" + filename + "acc.csv", 'a', encoding='utf-8')
    acc.write("filename" + ',' + "number" + ',' + 'b.angle' + ',' + 'a.angle' + ',' + 's.angle' + '\n')

    brake = open("./data/test/" + filename + "brake.csv", 'a', encoding='utf-8')
    brake.write("filename" + ',' + "number" + ',' + 'angle' + '\n')

    g = open("./data/test/fail/" + filename + ".csv", 'a', encoding='utf-8')
    g.write("img_number" + ',' + "templ1ate_rotating" + ',' + 'x' + ',' + 'y' + ',' + 'x' + ',' + 'y' + '\n')

    folder_path = "./Video/15frame/1111/"
    file_list = os.listdir(folder_path)
    file_count = len(file_list)

    img_rotate = file_count
    folder_path2 = "./Video/15frame/1122/"
    file_list2 = os.listdir(folder_path2)
    file_count2 = len(file_list2)
    img_rotate2 = file_count2
    img_rotate=min(file_count,file_count2)

    rotate = False
    script_dir = os.path.dirname(__file__)

    # image22=os.path.join(script_dir,"Video","1111","4.jpg")
    # image22=cv.imread(image22,cv.IMREAD_COLOR)
    # print(image22.shape[:2])
    # templ1 = image22[300:500,550:750]
    # templ2 = image22[420:620,700:900]
    # cv.imshow('test',templ1)
    # cv.imshow('test2',templ2)
    # cv.waitKey(0)

    templ1 = os.path.join(script_dir, "symbol", "11.jpg")
    templ2 = os.path.join(script_dir, "symbol", "22.jpg")
    templ12 = os.path.join(script_dir, "symbol", "33.jpg")
    templ22 = os.path.join(script_dir, "symbol", "44.jpg")
    if img_rotate == None:
        img = os.path.join(script_dir, "symbol", "img", "5.jpg")
        image = (None, img, templ1, rotate, filename)
        # print(image)
        main(image)
        f.close()
        g.close()

    else:
        for i in range(img_rotate):
            if i % 1 == 0:
                try:
                    img = os.path.join(script_dir, "Video", "15frame" ,"1111", str(i) + ".jpg")
                    templ1 = os.path.join(script_dir, "symbol", "11.jpg")
                    templ2 = os.path.join(script_dir, "symbol", "22.jpg")
                    templ12 = os.path.join(script_dir, "symbol", "33.jpg")
                    templ22 = os.path.join(script_dir, "symbol", "44.jpg")
                    img2 = os.path.join(script_dir, "Video","15frame", '1122', str(i) + ".jpg")
                    image = (None, img, templ1, templ2, rotate, filename, i, img2, templ12, templ22)
                    # print(image)
                    main(image)
                except:
                    # print("!")
                    pass
            else:
                pass
        acc.close()
        brake.close()
        f.close()
        g.close()












