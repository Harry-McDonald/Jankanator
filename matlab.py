import matlab.engine
import numpy
import cv2

eng = matlab.engine.start_matlab()

IM = cv2.imread('Image1',Simple1.jpg) # saves image

sigma = 20  # How Blurry
GAUSS = eng.imgaussfilt(IM,sigma)
#figure
#imshow(GAUSS), title('Gauss Applied')

#rg2lab
lab_IM = eng.rgb2lab(GAUSS)
#figure 
#imshow(lab_IM), title('rgb2lab_GAUSS')


#Classify the Colors in 'a*b*' Space Using K-Means Clustering
ab = eng.lab_IM(:,:,2:3)
ab = eng.im2single(ab)
nColors = 3

# repeat the clustering 3 times to avoid local minima
pixel_labels = eng.imsegkmeans(ab,nColors,'NumAttempts',3)  #Use imsegkmeans to cluster the objects into three clusters.
#figure
#imshow(pixel_labels,[])
#title('Image Labeled by Cluster Index')

#MASKING OVER
mask1 = pixel_labels==1 # 1 overlays everything not black after the segmentation
cluster1 = GAUSS .* uint8(mask1) 
#figure
#imshow(cluster1)
#title('Objects in Cluster 1')

#GREYSCALE
im = eng.rgb2gray(cluster1) 
#figure
#imshow(im)
#title('GREY SCALE')

#Converting to BW
level = 0.1
BW = eng.im2bw(im, level)
#figure
#imshow(BW)

#Splitting the image into zones
scaled = eng.imresize(BW, [256 256])
rect1 = [1 146 51 146]
rect2 = [52 146 51 146]
rect3 = [103 146 51 146] 
rect4 = [154 146 51 146] 
rect5 = [205 146 51 146] 
crop1 = eng.imcrop(scaled,rect1) 
crop2 = eng.imcrop(scaled,rect2) 
crop3 = eng.imcrop(scaled,rect3) 
crop4 = eng.imcrop(scaled,rect4) 
crop5 = eng.imcrop(scaled,rect5) 

CROP1 = eng.double(crop1) 
CROP2 = eng.double(crop2) 
CROP3 = eng.double(crop3) 
CROP4 = eng.double(crop4) 
CROP5 = eng.double(crop5) 

num1 = eng.nnz(~CROP1) 
num2 = eng.nnz(~CROP2) 
num3 = eng.nnz(~CROP3) 
num4 = eng.nnz(~CROP4) 
num5 = eng.nnz(~CROP5) 
cell_list = [num1 num2 num3 num4 num5]
pathtotrav = eng.min(cell_list)
'''