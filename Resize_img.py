import cv2 as cv

img = cv.imread('Images\imd_logo.png')

L_scale = 25
W_scale = 35

width = int(img.shape[1] * W_scale/100)
length = int(img.shape[0] * L_scale/100)

resize = cv.resize(img, (width, length))
cv.imshow("Resize IMG", resize)
#cv.imwrite("imd_logo1.png", resize)

print(img.shape)
print(resize.shape)

cv.waitKey(0)
cv.destroyAllWindows()


'''पृथ्वी विज्ञान मंत्रालय 
MINSITRY OF EARTH SCIENCES
भारत मौसम विज्ञान विभाग 
INDIA METEOROLOGICAL DEPARTMENT
प्रादेशिक मौसम केंद्र, नई दिल्ली
REGIONAL METEOROLOGICAL CENTER, NEW DELHI'''