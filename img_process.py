import make_obj
import make_lib
import matplotlib.pyplot as plt
import random as rd
import cv2
import os

def process_image_data():
    ratio_scale_width = 2
    ratio_scale_height = 2

    blur_kernel = [3, 3]

    binary_thresh_hold = 100

    canny_low_thresh_hold = 100
    canny_high_thresh_hold = 200

    return [ratio_scale_width, ratio_scale_height, blur_kernel, binary_thresh_hold, canny_low_thresh_hold, canny_high_thresh_hold]

def processing_image(image):
    [ratio_scale_width, ratio_scale_height, blur_kernel, binary_thresh_hold, canny_low_thresh_hold, canny_high_thresh_hold] = process_image_data()

    img = make_obj.processed_image(image)

    img_after_scale = img.scale_img(ratio_scale_width, ratio_scale_height)

    img.to_gray()

    img.equal_hist()

    img.blur(blur_kernel)

    img.to_binary(binary_thresh_hold)

    img.to_edge_canny(canny_low_thresh_hold, canny_high_thresh_hold)

    contour = img.find_contour()

    img_after_final = img.final_img()

    return [img_after_scale, img_after_final, contour]

def main(mode):
    #path = r"D:\sandbox\DATN\Code\img\bat.jpg"
    path = r"D:\ANH\Hinh1_Twitter.jpg"

    image = cv2.imread(path)

    [img_after_scale, img_after_final, contour] = processing_image(image)

    if mode:
        contour_index = -1
        contour_color = (rd.randint(0, 255), rd.randint(0, 255), rd.randint(0, 255))
        cv2.drawContours(img_after_scale, contour, contour_index, contour_color, thickness = 5)

    full_dastaset = make_lib.get_xy_list_from_contour(contour)

    dir = os.getcwd() + r"\Text_contour"
    make_lib.make_dir(dir)
    make_lib.delete_all_files(dir)

    for j in range(len(contour)):
        x = []
        y = []
        file = open(dir + r"\file_point_{}.txt".format(j), "w")
        set_step = 1
        step = set_step
        count_step = 0

        for ele in full_dastaset[j]:
            ele_x = int(ele[(ele.index("[") + 1) : ele.index(",")])
            ele_y = int(ele[(ele.index(",") + 1) : ele.index("]")])
            x.append(ele_x)
            y.append(ele_y)

        for i in range(0, len(full_dastaset[j])):
            try:
                ans = (y[i] - y[i + 1]) * (x[i + 2] - x[i + 1]) + (x[i + 1] - x[i]) * (y[i + 2] - y[i + 1])
                if ans == 0:
                    continue
                else:
                    # if step > count_step:
                    #     file.write(str(full_dastaset[j][i]) + "\n")
                    #     step = step - 1
                    # else:
                    #     step = set_step
                    #     continue
                    file.write(str(full_dastaset[j][i]) + "\n")
            except:
                break

        file.write(str(full_dastaset[j][0]) + "\n")
        file.close()

    plt.subplot(1,2,1)
    plt.imshow(cv2.cvtColor(img_after_scale, cv2.COLOR_BGR2RGB))
    plt.title("origin")

    plt.subplot(1,2,2)
    plt.imshow(img_after_final)
    plt.title("edge")
    plt.show()

if __name__ == "__main__":
    mode = 1
    main(mode)