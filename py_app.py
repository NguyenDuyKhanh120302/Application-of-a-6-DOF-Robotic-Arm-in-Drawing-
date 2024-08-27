import customtkinter
from tkinter import filedialog
import tkinter
import make_obj
import make_lib
import matplotlib.pyplot as plt
import random as rd
import cv2
import math
import os

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("DRAWING IMAGE")
        self.geometry(f"{600}x{350}")

        # Input image
        self.label_input = customtkinter.CTkLabel(self, text="INPUT IMAGE", anchor="w")
        self.label_input.place(x=25, y=30)
        self.button_input = customtkinter.CTkButton(self, text="BROWSE", command=self.browse_img, width=100)
        self.button_input.place(x=455, y=30)
        self.textbox = customtkinter.CTkTextbox(self, width=300, height=1)
        self.textbox.place(x=150, y=30)

        # Output point to draw
        self.label_ouput = customtkinter.CTkLabel(self, text="OUTPUT POINT ", anchor="w")
        self.label_ouput.place(x=25, y=80)
        self.label_ouput = customtkinter.CTkButton(self, text="BROWSE", command=self.browse_point_dir, width=100)
        self.label_ouput.place(x=455, y=80)
        self.textbox_point_dir = customtkinter.CTkTextbox(self, width=300, height=1)
        self.textbox_point_dir.place(x=150, y=80)

        # Output folder for points before inverse kinematics
        #self.label_points = customtkinter.CTkLabel(self, text="OUT CORNER DIR", anchor="w")
        #self.button_points.place(x=455, y=130)
        #self.textbox_corner_dir = customtkinter.CTkTextbox(self, width=300, height=1)
       #self.textbox_corner_dir.place(x=150, y=130)

        # Input scalar
        self.label_scalar = customtkinter.CTkLabel(self, text="SCALE INPUT IMAGE", anchor="w")
        self.label_scalar.place(x=25, y=130)
        self.scalar_x = customtkinter.CTkLabel(self, text="SCALE X", anchor="w")
        self.scalar_x.place(x=175, y=130)
        self.scalar_x_input = customtkinter.CTkTextbox(self, width=100, height=1)
        self.scalar_x_input.place(x=255, y=130)
        self.scalar_y = customtkinter.CTkLabel(self, text="SCALE Y", anchor="w")
        self.scalar_y.place(x=375, y=130)
        self.scalar_y_input = customtkinter.CTkTextbox(self, width=100, height=1)
        self.scalar_y_input.place(x=455, y=130)
        #self.scalar_rowx = customtkinter.CTkLabel(self, text="ROW X", anchor="w")
        #self.scalar_rowx.place(x=50, y=230)
        #self.scalar_rowx_input = customtkinter.CTkTextbox(self, width=100, height=1)
        #self.scalar_rowx_input.place(x=100, y=230)
        #self.scalar_rowy = customtkinter.CTkLabel(self, text="ROW Y", anchor="w")
        #self.scalar_rowy.place(x=50, y=280)
        #self.scalar_rowy_input = customtkinter.CTkTextbox(self, width=100, height=1)
        #self.scalar_rowy_input.place(x=100, y=280)

        # Choose draw contour or not
        self.label_mode = customtkinter.CTkLabel(self, text="DRAW CONTOUR")
        self.label_mode.place(x=240, y=230)
        self.button_mode = customtkinter.CTkButton(self, text="OFF", command=self.simpletoggle, width=100)
        self.button_mode.place(x=455, y=230)

        # Process image
        self.label_generate = customtkinter.CTkLabel(self, text="GENERATE CONTOUR")
        self.label_generate.place(x=240, y=180)
        self.button_main = customtkinter.CTkButton(self, text="GENERATE", command=self.generate, width=100)
        self.button_main.place(x=455, y=280)

        # Option menu
        #self.label_system = customtkinter.CTkLabel(self, text="SYSTEM APPERANCE")
        #self.label_system.place(x=25, y=230)
        #self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self, values=["Dark", "Light", "System"], command=self.change_appearance_mode_event)
        #self.appearance_mode_optionemenu.place(x=25, y=280)

        # Option contour
        #self.label_system = customtkinter.CTkLabel(self, text="COUNTOUR METHOD")
        #self.label_system.place(x=240, y=230)
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self, values=["External","List"])
        self.appearance_mode_optionemenu.place(x=455, y=180)

    def simpletoggle(self):
        if self.button_mode.cget("text") == 'ON':
            self.button_mode.configure(text='OFF')
        else:
            self.button_mode.configure(text='ON')
    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def get_mode(self):
        if self.button_mode.cget("text") == 'ON':
            return 1
        else:
            return 0
        
    def browse_img(self):
        file = filedialog.askopenfile(mode='r', initialdir = "D:/")
        self.textbox.delete(1.0,  tkinter.END)
        self.textbox.insert(1.0,  str(file.name))

    def browse_point_dir(self):
        dir = filedialog.askdirectory(initialdir = "D:/")
        self.textbox_point_dir.delete(1.0,  tkinter.END)
        self.textbox_point_dir.insert(1.0,  str(dir))

    #def browse_corner_dir(self):
       # dir = filedialog.askdirectory(initialdir = "D:/")
        #self.textbox_corner_dir.delete(1.0,  tkinter.END)
        #self.textbox_corner_dir.insert(1.0,  str(dir))

    def process_image_data(self):
        ratio_scale_width = self.scalar_x_input.get(1.0, "end-1c")
        ratio_scale_height = self.scalar_y_input.get(1.0, "end-1c")

        blur_kernel = [3, 3]

        binary_thresh_hold = 100

        canny_low_thresh_hold = 100
        canny_high_thresh_hold = 200

        return [ratio_scale_width, ratio_scale_height, blur_kernel, binary_thresh_hold, canny_low_thresh_hold, canny_high_thresh_hold]

    def processing_image(self, image):
        [ratio_scale_width, ratio_scale_height, blur_kernel, binary_thresh_hold, canny_low_thresh_hold, canny_high_thresh_hold] = self.process_image_data()

        img = make_obj.processed_image(image)

        img_origin = img.final_img()

        if ratio_scale_width == "" and ratio_scale_height == "":
            img_after_scale = img_origin
        else:
            if ratio_scale_width == "":
                img_after_scale = img.scale_img(1, int(ratio_scale_height))
            elif ratio_scale_height == "":
                img_after_scale = img.scale_img(int(ratio_scale_width), 1)
            else:
                img_after_scale = img.scale_img(int(ratio_scale_width), int(ratio_scale_height))

        img.to_gray()

        img.equal_hist()

        img.blur(blur_kernel)

        img.to_binary(binary_thresh_hold)

        img_canny = img.to_edge_canny(canny_low_thresh_hold, canny_high_thresh_hold)

        method = self.appearance_mode_optionemenu.get()
        if method == "List":
            contour = img.find_contour_list()
        elif method == "Tree":
            contour = img.find_contour_tree()
        elif method == "External":
            contour = img.find_contour_external()

        img_after_final = img.final_img()

        return [img_after_scale, img_after_final, contour]

    def generate(self):
        mode = self.get_mode()
        img_path = self.textbox.get(1.0, "end-1c")
        #corner_dir = self.textbox_corner_dir.get(1.0, "end-1c") + r"\Text_contour_corner"
        point_dir = self.textbox_point_dir.get(1.0, "end-1c") + r"\Text_contour_point"

        if img_path == " or point_dir == ":
            customtkinter.showerror("Error", "Please select input image, pre-IK points directory, and output directory.")
            return

        make_lib.make_dir(point_dir)
        make_lib.delete_all_files(point_dir)
        #make_lib.make_dir(corner_dir)
        #make_lib.delete_all_files(corner_dir)


        image = cv2.imread(img_path)
        [img_after_scale, img_after_final, contour] = self.processing_image(image)

        if mode:
            contour_index = -1
            contour_color = (rd.randint(0, 255), rd.randint(0, 255), rd.randint(0, 255))
            cv2.drawContours(img_after_scale, contour, contour_index, contour_color, thickness=5)

        full_dataset = make_lib.get_xy_list_from_contour(contour)

        Row_x = 843 #250
        Row_y = 843 #-302

        Px_o = 547
        Py_o = 129
        Pz_o = 382
        Px_x = 549
        Py_x = -123
        Pz_x = 380
        Px_y = 394
        Py_y = 126
        Pz_y = 238

        for j in range(len(contour)):
            x = []
            y = []
            #file_corner = open(corner_dir + r"\file_corner_{}.txt".format(j), "w")
            file_point = open(point_dir + r"\file_point_{}.txt".format(j), "w")
            #file_corner.write(str(full_dataset[j][0]) + "\n")
            #file_point.write(str(full_dataset[j][0]) + "\n")
            set_step = 1
            step = set_step
            count_step = 0

            for ele in full_dataset[j]:
                ele_x = int(ele[(ele.index("[") + 1) : ele.index(",")])
                ele_y = int(ele[(ele.index(",") + 1) : ele.index("]")])
                x.append(ele_x)
                y.append(ele_y)

            for i in range(len(full_dataset[j])):
                try:
                    ans = (y[i] - y[i + 1]) * (x[i + 2] - x[i + 1]) + (x[i + 1] - x[i]) * (y[i + 2] - y[i + 1])
                    if ans == 0:
                        continue
                    else:
                        px = x[i]
                        py = y[i]
                        #pz = 0
                        dx_x = (Px_x-Px_o+1)/(Row_x-1)
                        dx_y = (Py_x-Py_o+1)/(Row_x-1)
                        dx_z = (Pz_x-Pz_o+1)/(Row_x-1)
                        dy_x = (Px_y-Px_o+1)/(Row_y-1)
                        dy_y = (Py_y-Py_o+1)/(Row_y-1)
                        dy_z = (Pz_y-Pz_o+1)/(Row_y-1)
                        Px_matrix = Px_o+  dx_x*px + dy_x*py
                        Py_matrix = Py_o + dx_y*px + dy_y*py
                        Pz_matrix = Pz_o + dx_z*px + dy_z*py

                        x_c = Px_matrix - (245.0*(math.sqrt(2)/2))
                        y_c = Py_matrix 
                        z_c = Pz_matrix + (245.0*(math.sqrt(2)/2))
                        # tinh_theta1
                        theta1_tam = math.atan(y_c/x_c)
                        if (x_c > 0):
                            theta1 = math.degrees(theta1_tam)
                        else:   
                            if (y_c < 0):
                                theta1 = math.degrees(theta1_tam) - 180.0   
                            else:
                                theta1 = math.degrees(theta1_tam) + 180.0 
                        if (theta1 < 0):
                            theta1 = theta1 + 360.0  
                        theta1_rad = math.radians(theta1)    
                        # tinh_theta2
                        t = (math.cos(theta1_rad)*x_c + math.sin(theta1_rad)*y_c)*(math.cos(theta1_rad)*x_c + math.sin(theta1_rad)*y_c) + (295.0 - z_c)*(295.0 - z_c) + 230.0*230.0  
                        u = 50.0*50.0 + 270.0*270.0 
                        n = (t - u)/(2*230.0) 
                        a = (math.cos(theta1_rad)*x_c + math.sin(theta1_rad)*y_c)
                        b = 295.0 - z_c
                        theta2_ba_tam = math.atan(b/a)
                        if (a > 0):
                            theta2_ba = math.degrees(theta2_ba_tam)
                        else:   
                            if (b < 0):
                                theta2_ba = math.degrees(theta2_ba_tam) - 180.0   
                            else:
                                theta2_ba = math.degrees(theta2_ba_tam) + 180.0 
                            
                        theta2_2_tam = math.atan(math.sqrt(a*a +b*b - n*n)/n)
                        if (n >= 0):
                            theta2_tam = math.degrees(theta2_2_tam)
                        else:   
                            if (math.sqrt(a*a +b*b - n*n) < 0):
                                theta2_tam = math.degrees(theta2_2_tam) - 180.0   
                            else:
                                theta2_tam = math.degrees(theta2_2_tam) + 180.0 
                        theta2 = theta2_ba - theta2_tam #theta2      
                        if (theta2 < 0):
                            theta2 = theta2 + 360.0 
                        theta2_rad = math.radians(theta2)
                            
                        # tinh_theta3  
                        k = (math.cos(theta1_rad)*x_c + math.sin(theta1_rad)*y_c)*(math.cos(theta1_rad)*x_c + math.sin(theta1_rad)*y_c) + (z_c-295.0)*(z_c-295.0) 
                        q = 50.0*50.0 + 230.0*230.0 + 270.0*270.0
                        m = (k-q)/(2*230.0)  
                        theta3_2_tam = math.atan(m/(math.sqrt(270*270+50.0*50.0-m*m)))
                        if (math.sqrt(270*270+50.0*50.0-m*m) > 0):
                            theta3_tam = math.degrees(theta3_2_tam)
                        else:   
                            if (m < 0):
                                theta3_tam = math.degrees(theta3_2_tam) - 180.0   
                            else:
                                theta3_tam = math.degrees(theta3_2_tam) + 180.0 
                        theta3 = math.degrees(math.atan(50.0/270.0)) - theta3_tam #theta2      
                        if (theta3 < 0):
                            theta3 = theta3 + 360.0
                        theta3_rad = math.radians(theta3)    
                        # tinh beta alpha gamma
                        # beta
                        beta_tam =math.atan(math.sqrt(0.5*(math.cos(theta1_rad)*math.cos(theta1_rad)+1))/((0.0-math.sqrt(2)/2)*math.sin(theta1_rad)))  
                        if (((0.0-math.sqrt(2)/2)*math.sin(theta1_rad)) > 0):
                            beta = math.degrees(beta_tam)
                        else:   
                            if (math.atan(math.sqrt(0.5*(math.cos(theta1_rad)*math.cos(theta1_rad)+1))) < 0):
                                beta = math.degrees(beta_tam) - 180.0   
                            else:
                                beta = math.degrees(beta_tam) + 180.0  
                        if (((0.0-math.sqrt(2)/2)*math.sin(theta1_rad)) == 0):  
                            beta_tam = 90.0
                            beta = beta_tam  
                        beta_rad = math.radians(beta) 
                        # alpha
                        alpha_tam = math.atan((((math.sqrt(2)/2)*(math.cos(theta2_rad+theta3_rad)-math.sin(theta2_rad+theta3_rad)*math.cos(theta1_rad)))/(math.sin(beta_rad)))/(((math.sqrt(2)/2)*(math.sin(theta2_rad+theta3_rad)+math.cos(theta2_rad+theta3_rad)*math.cos(theta1_rad)))/(math.sin(beta_rad))))
                        if ((((math.sqrt(2)/2)*(math.sin(theta2_rad+theta3_rad)+math.cos(theta2_rad+theta3_rad)*math.cos(theta1_rad)))/(math.sin(beta_rad))) > 0):
                            alpha = math.degrees(alpha_tam)
                        else:   
                            if ((((math.sqrt(2)/2)*(math.cos(theta2_rad+theta3_rad)-math.sin(theta2_rad+theta3_rad)*math.cos(theta1_rad)))/(math.sin(beta_rad))) < 0):
                                alpha = math.degrees(alpha_tam) - 180.0   
                            else:
                                alpha = math.degrees(alpha_tam) + 180.0  
                        if ((((math.sqrt(2)/2)*(math.sin(theta2_rad+theta3_rad)+math.cos(theta2_rad+theta3_rad)*math.cos(theta1_rad)))/(math.sin(beta_rad))) == 0):  
                            alpha_tam = 90.0
                            alpha = alpha_tam 
                        alpha_rad = math.radians(alpha)      
                        # gamma
                        gamma_tam = math.atan(((0.0 - math.cos(theta1_rad))/(math.sin(beta_rad)))/((math.sqrt(2)/2)*(math.sin(theta1_rad))/(math.sin(beta_rad))))   
                        if (((math.sqrt(2)/2)*(math.sin(theta1_rad))/(math.sin(beta_rad))) > 0):
                            gamma = math.degrees(gamma_tam)
                        else:   
                            if (((0.0 - math.cos(theta1_rad))/(math.sin(beta_rad))) < 0):
                                gamma = math.degrees(gamma_tam) - 180.0   
                            else:
                                gamma = math.degrees(gamma_tam) + 180.0  
                        if (((math.sqrt(2)/2)*(math.sin(theta1_rad))/(math.sin(beta_rad))) == 0):  
                            gamma_tam = -90.0
                            gamma = gamma_tam  
                        gamma_rad = math.radians(gamma)
                        # tinh theta4
                        theta4_tam = math.atan((0.0 - math.cos(beta_rad))/((math.cos(alpha_rad))*(math.sin(beta_rad)))) 
                        rnd4_1 = round((0.0 - math.cos(beta_rad)),1) 
                        rnd4_2 = round(((math.cos(alpha_rad))*(math.sin(beta_rad))),1) 
                        if (((math.cos(alpha_rad))*(math.sin(beta_rad))) > 0):
                            theta4 = math.degrees(theta4_tam)
                        else:   
                            if ((0.0 - math.cos(beta_rad)) < 0):
                                theta4 = math.degrees(theta4_tam) - 180.0   
                            else:
                                theta4 = math.degrees(theta4_tam) + 360.0
                        if ((0.0 - math.cos(beta_rad))/((math.cos(alpha_rad))*(math.sin(beta_rad))) ==1): 
                            if (rnd4_1== 0.0): 
                                theta4_tam = 0.0
                                theta4 = math.degrees(theta4_tam)      
                        if (theta4 < 0):
                            theta4 = theta4 + 180.0 
                        # tinh theta 5
                        theta5_tam = math.atan((math.sqrt(1-(math.sin(alpha_rad)*math.sin(beta_rad))*(math.sin(alpha_rad)*math.sin(beta_rad))))/(math.sin(alpha_rad)*math.sin(beta_rad)))
                        rnd5_1 = round((math.sqrt(1-(math.sin(alpha_rad)*math.sin(beta_rad))*(math.sin(alpha_rad)*math.sin(beta_rad)))),1) 
                        rnd5_2 = round((math.sin(alpha_rad)*math.sin(beta_rad)),1) 
                        if ((math.sin(alpha_rad)*math.sin(beta_rad)) > 0):
                            theta5 = math.degrees(theta5_tam)
                        else:   
                            if ((math.sqrt(1-(math.sin(alpha_rad)*math.sin(beta_rad))*(math.sin(alpha_rad)*math.sin(beta_rad)))) < 0):
                                theta5 = math.degrees(theta5_tam) - 180.0   
                            else:
                                theta5 = math.degrees(theta5_tam) + 180.0
                        if ((math.sqrt(1-(math.sin(alpha_rad)*math.sin(beta_rad))*(math.sin(alpha_rad)*math.sin(beta_rad))))/(math.sin(alpha_rad)*math.sin(beta_rad)) ==1): 
                            if (rnd5_1== 0.0): 
                                theta5_tam = 0.0
                                theta5 = math.degrees(theta5_tam)      
                        if (theta5 < 0):
                            theta5 = theta5 + 360.0 
                       
                        
                        theta1 = round(theta1*100000)
                        theta2 = round(theta2*100000)
                        theta3 = round(theta3*100000)
                        theta4 = round(theta4*100000)
                        theta5 = round(theta5*100000)
                        #file_corner.write(f"[{theta1}, {theta2},{theta3},{theta4},{theta5}]\n")
                        file_point.write(str(full_dataset[j][i]) + "\n")
                except:
                    break
            file_point.write(str(full_dataset[j][0]) + "\n")
            file_point.close()
            #file_corner.close()



        plt.subplot(1, 2, 1)
        plt.imshow(cv2.cvtColor(img_after_scale, cv2.COLOR_BGR2RGB))
        plt.title("origin")

        plt.subplot(1, 2, 2)
        plt.imshow(img_after_final)#_flipped)
        plt.title("edge")
        plt.show()

if __name__ == "__main__":
    app = App()
    app.mainloop()
