import numpy as np
import cv2 as cv
img = cv.imread('./test/Sainsbury.jpeg')
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
 
# find Harris corners
gray = np.float32(gray)
dst = cv.cornerHarris(gray,5,3,0.06)
dst = cv.dilate(dst,None)
ret, dst = cv.threshold(dst,0.001*dst.max(),255,0)
dst = np.uint8(dst)
 
# find centroids
ret, labels, stats, centroids = cv.connectedComponentsWithStats(dst)
 
# define the criteria to stop and refine the corners
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.001)
corners = cv.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)
 
# Now draw them
res = np.hstack((centroids,corners))
res = res.astype(int)
img[res[:,1],res[:,0]]=[0,0,255]
img[res[:,3],res[:,2]] = [0,255,0]

cv.imwrite('harris_response.jpeg', dst) 
cv.imwrite('thresholded_corners.jpeg', dst)
print(f"Found {len(centroids)} corner candidates")