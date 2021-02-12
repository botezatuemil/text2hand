from cv2 import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from imutils import contours
import random
import docx


class get_characters():
  
    def get_transparent_alphachannel(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # threshold input image as mask and invert the mask
        mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1]
        mask = 255 - mask

        result = img.copy()
        result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)

        result[:, :, 3] = mask 
        cv2.imwrite("C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\Resources\\alpha.png", result)
        return result


    def get_boxes(self, img, imgAlpha):

        # Load image, grayscale, and adaptive threshold
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,57,5)
        
        # Filter out all numbers and noise to isolate only boxes
        cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        for c in cnts:
            area = cv2.contourArea(c)
            if area < 5000:
                cv2.drawContours(thresh, [c], -1, (0,0,0), -1)


        # Fix horizontal and vertical lines
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,5))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, vertical_kernel, iterations=9)
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,1))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, horizontal_kernel, iterations=6)
        
        cv2.imshow("TRESH", thresh)
        # Sort by top to bottom and each row by left to right
        invert = 255 - thresh
        cnts = cv2.findContours(invert, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        (cnts, _) = contours.sort_contours(cnts, method="top-to-bottom")
        
        alphabet_rows = []
        row = []
        for (i, c) in enumerate(cnts, 1):
            area = cv2.contourArea(c)
            if area < 50000:
                row.append(c)
                if i % 10 == 0:  
                    (cnts, _) = contours.sort_contours(row, method="left-to-right")
                    alphabet_rows.append(cnts)
                    row = []
        
        # Iterate through each box
        countsquare = 97
        count = 33
        contor = 0
        
        for row in alphabet_rows:
            for c in row:
                contor += 1
                mask = np.zeros(img.shape, dtype=np.uint8)
                cv2.drawContours(mask, [c], -1, (255,255,255), -1)
                result = cv2.bitwise_and(img, mask)
                result[mask==0] = 255
                result = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
                result = cv2.adaptiveThreshold(result,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,5,5)
                cntours, hierarchy = cv2.findContours(result, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                
                x, y, w, h = 0, 0, 0, 0
                countsquare += 1
                biggest = 0

                #get the biggest contour to avoid false detection
                for cnt in cntours:
                    area = cv2.contourArea(cnt)
                    if area < 5000 and area >= biggest and area > 50:
                        biggest = area
                        myCnt = cnt
                        
                # get the coordinates of the upper and lower corner of the letter and crop the letters
                peri = cv2.arcLength(myCnt, True)
                approx = cv2.approxPolyDP(myCnt, 0.01*peri, True)
                x, y, w, h = cv2.boundingRect(approx)
                #cv2.drawContours(img, [myCnt], -1, (0, 255, 0), 1)
                imgCropped = imgAlpha[y - 2 : y + h + 2, x - 2 : x + w + 2]

                # take the uppercase
                if count == 34:
                    count = 39

                if count == 42:
                    count = 44

                if count == 45:
                    count = 46
                
                if count == 47:
                    count = 48

                # take the symbol need to fix this
                if count == 59:
                    count = 63

                if count == 64:
                    count = 65 

                if count == 91:
                    count = 97 

                cv2.imwrite("C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\Resources\\a"+ str(count) + ".png", imgCropped)
                count += 1

        cv2.waitKey(175)
    

class get_file_handwrite():     

    def write_on_txt(self, preference):
        gap, ht = 30, 50
        number = 0
        spaces = 0
        tab = 0
        isSpace = False
        isTab = False
        fullText = []

        # if the user use docx document
        if preference == 1:
            doc = docx.Document("C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\content.docx")
            
            # save the content in variable
            for para in doc.paragraphs:
                fullText.append(para.text)
            fullText = '\n'.join(fullText)

            # overwrite the txt
            with open('C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\dummy.txt', 'w') as f:
                for item in fullText:
                    f.write("%s" % item)

            # overwrite the txt
            with open('C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\dummy2.txt', 'w') as f:
                for item in fullText:
                    f.write("%s" % item)
        
        # open the files
        txt = open("C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\dummy.txt")
        txt2 = open("C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\dummy2.txt")
        BG=Image.open("C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\background1.png") 

        backup = BG.copy()
        contentTXT = txt2.read().replace("\n", " ")
        

        for i in txt.read().replace("\n", " "):  
            different = 0

            # count how many letters it follows (the next word) and calcute the dimension of it to know 
            # if we need to get a new line to avoid the wrong speration of it
            if ord(i) != ord(' '):
                number += 1
            else:
                number += 1
                for k in range(number, len(contentTXT)):
                    different += 1
                    if ord(contentTXT[k]) == ord(' ') or ord(contentTXT[k]) == 9:
                        break

            # for TXT if we have more than 3 spaces that means a new line with indentation
            if ord(i) == ord(' '):
                spaces += 1
            else:
                if spaces >= 3:
                    ht += 60 + random.randint(15, 30)
                    gap = spaces * 21
                    isSpace = True
                spaces = 0

            # for DOCX if we have at least a tab that means a new line with indentation
            if ord(i) == 9:
                tab += 1
            else:
                if tab >= 1:
                    ht += 60 + random.randint(15, 30)
                    gap = tab * 90
                else:
                    if gap + different * 30 > BG.width:
                        ht += 60 + random.randint(15, 30)
                        gap = 0
                tab = 0
            
            
            # open the letters with the ascii code of the letter that we read from the file
            try:
                cases = Image.open("C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\Resources\\a" + str(ord(i)) + ".png").convert('RGBA')
            except:
                print("error")

            # special cases to move the biggest letter up and the lowers letter down
            if ord(i) == ord('b') or ord(i) == ord('d') or ord(i) == ord('f') or ord(i) == ord('h') or ord(i) == ord('k') or ord(i) == ord('l') or ord(i) == ord('t') or ord(i) >= 65 and ord(i) <= 90 or ord(i) == 39 or ord(i) == 63:
                backup.paste(cases, (gap-8, ht-10), cases) 
            elif ord(i) == ord('.') or ord(i) == ord(','):
                backup.paste(cases, (gap-8, ht+15), cases) 
            else:
                backup.paste(cases, (gap-8, ht), cases)

            
            # a new gap for every letter with random case
            gap += cases.width + random.randint(-2, -1)

        backup.save('C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\new.png')
        
            
if __name__ == "__main__":

    img = cv2.imread("C:\\Emil\\Proiecte\\Python\\Proiecte_Python\\Automation\\Text2Hand\\alphabet22.png")
    
    #img = cv2.resize(img, (892, 267)) 
    #img = cv2.resize(img, (850, 1169))

    # crop the file and save only the table
    # x, y, w, h = 150, 195, 1354, 460 
    x, y, w, h = 176, 210, 1349, 768
    img = img[y:y+h, x:x+w]


    # 0 for txt and 1 for word file
    preference = 1 
    # x, y, w, h = 153, 198, 1357, 998 
    # img = img[y:y+h, x:x+w]
    
    #imgAlpha = get_characters().get_transparent_alphachannel(img)
    #get_characters().get_boxes(img, imgAlpha)
    get_file_handwrite().write_on_txt(preference)
    
    cv2.waitKey(0)
