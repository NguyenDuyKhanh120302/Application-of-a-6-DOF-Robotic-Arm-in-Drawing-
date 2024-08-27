import cv2

class processed_image:
    def __init__(self, img):
        self.img = img

    def scale_img(self, ratio_scale_width, ratio_scale_height):
        self.img = cv2.resize(self.img, (int(self.img.shape[1]/ratio_scale_width), int(self.img.shape[0]/ratio_scale_height)))
        return self.img

    def to_gray(self):
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        return self.img

    def equal_hist(self):
        self.img = cv2.equalizeHist(self.img)
        return self.img

    def blur(self, kernel):
        self.img = cv2.blur(self.img, kernel)
        return self.img

    def to_binary(self, thresh):
        self.img = cv2.threshold(self.img, thresh, 255, cv2.THRESH_BINARY)[1]
        return self.img

    def to_edge_canny(self, thresh_low, thresh_high):
        self.img = cv2.Canny(self.img, thresh_low, thresh_high)
        return self.img

    def find_contour_list(self):
        contour,_ = cv2.findContours(self.img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        return contour

    def find_contour_tree(self):
        contour,_ = cv2.findContours(self.img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        return contour

    def find_contour_external(self):
        contour,_ = cv2.findContours(self.img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        return contour
    
    def final_img(self):
        return self.img