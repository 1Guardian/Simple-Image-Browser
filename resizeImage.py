from imports import *

#================================================================
#
# Function: resizeImage(image, x, y, metaData)
#
# Description: This function is pretty simple, it takes in the
#              the arguments passed from the command line and 
#              resizes the images to fit within the confines 
#              specfied. 
#
# Returns: resizedImg | type: openCV image 
#    OR
# Returns: image | original image unchanged
#
#================================================================
def resizeImage(image, x, y, metaData):

    #variables to control decision making
    biggerX = False
    biggerY = False

    #check to see if image needs to be resized at all
    if (metaData.get("sizeX") > x):
        biggerX = True
    if (metaData.get("sizeY") > y):
        biggerY = True

    #deal with posibility that both exceed specified bounds
    #method: compare sizes and take the larger one
    if (biggerX == True == biggerY):
        biggerX = metaData.get("sizeX") > metaData.get("sizeY")
        biggerY = metaData.get("sizeX") < metaData.get("sizeY")
        
        #make sure we don't have an issue of the image being the same
        #size over in both dimensions
        if (biggerX == False == biggerY):
            biggerX = True

    if(biggerX):

        #get multiplying factor
        delta = metaData.get("sizeX") / x

        #scale the image 
        newSize = (math.floor(metaData.get("sizeX") / delta), math.floor(metaData.get("sizeY") / delta))

        #add try catch protection to the openCV calls specifically
        try:
            resizedImg = cv2.resize(image, newSize)
        except exception:
            print("Resizing provided image failed. Perhaps the image path was empty or invalid. Exiting.")
            sys.exit(-1)
        
        #return image
        return resizedImg

    elif(biggerY):

        #get multiplying factor
        delta = metaData.get("sizeY") / y

        #scale the image 
        newSize = (math.floor(metaData.get("sizeX") / delta), math.floor(metaData.get("sizeY") / delta))

        #add try catch protection to the openCV calls specifically
        try:
            resizedImg = cv2.resize(image, newSize)
        except exception:
            print("Resizing provided image failed. Perhaps the image path was empty or invalid. Exiting.")
            sys.exit(-1)
        
        #return image
        return resizedImg
    
    #else, image fit, exit
    return image