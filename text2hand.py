from cv2 import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


class get_characters():

    def read_image(self):
        img = cv2.imread("C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\alphabet6.png")
        return img


    def threshold_image(self, img):
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower = np.array([162, 15, 88])
        upper = np.array([179, 255, 255])
        mask = cv2.inRange(imgHSV, lower, upper)
        imgResult = cv2.bitwise_and(img, img, mask=mask)
        #cv2.imshow("RESULT", imgResult)
        cv2.imwrite("C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\Resources\\alphaGrid.png", imgResult)
        return imgResult
        


    def get_transparent_alphachannel(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # threshold input image as mask
        mask = cv2.threshold(gray, 15 0, 255, cv2.THRESH_BINARY)[1]
        mask = 255 - mask
        #cv2.imshow("MASK", mask)
        # kernel = np.ones((3,3), np.uint8)
        # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        # mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        
        #mask = cv2.GaussianBlur(mask, (0,0), sigmaX=2, sigmaY=2, borderType = cv2.BORDER_DEFAULT)
        
        #mask = (2*(mask.astype(np.float32))-255.0).clip(0,255).astype(np.uint8)

        result = img.copy()
        result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)

        result[:, :, 3] = mask
        # cv2.imshow("RESULT", result)
        cv2.imwrite("C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\Resources\\alpha.png", result)
        return result

        

    def getContours(self, imgCanny, img, imgAlpha):
        contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        x, y, w, h = 0, 0, 0, 0
        count = 97

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 1:
                peri = cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, 0.01*peri, True)
                x, y, w, h = cv2.boundingRect(approx)
                cv2.drawContours(img, cnt, -1, (0, 255, 0), 1)
                imgCropped = imgAlpha[y - 2 : y + h + 2, x - 2 : x + w + 2]

                #cv2.imwrite("C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\Resources\\a"+ str(count) + ".png", imgCropped)
                count += 1
                
        cv2.imshow("COUNTOURS", img)
            

class get_file_handwrite():

    def write_on_txt(self):
        gap, ht = 30, 30
        txt = open("C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\dummy.txt")
        BG=Image.open("C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\background.png") 
        backup = BG.copy()
        
        for i in txt.read().replace("\n", ""):   
            try:
                cases = Image.open("C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\Resources\\a" + str(ord(i)) + ".png")
            except:
                print("error")

            backup.paste(cases, (gap, ht), cases)
            gap += cases.width
            
        backup.save('C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\new.png')
        
              

if __name__ == "__main__":

    img = get_characters().read_image()
    img = cv2.resize(img, (924, 693)) 
    
    imgAlpha = get_characters().get_transparent_alphachannel(img)
    imgGrid = get_characters().threshold_image(imgAlpha)

    imgCanny = cv2.Canny(imgGrid, 200, 400)
    cv2.imshow("Canny", imgCanny)

    get_characters().getContours(imgCanny, img, imgAlpha)
    #cv2.imshow("original", img)

    #get_file_handwrite().write_on_txt()
    
    

    cv2.waitKey(0)
