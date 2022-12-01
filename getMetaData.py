from imports import *

#================================================================
#
# Function: getMetaData(image)
#
# Description: This function gets the metadata of the passed
#              image file. MetaData collected includes: name
#              path, image file type, image size, number of 
#              pixels, and image file size
#
# Returns: metaData | type: dictionary of metadata
#
#================================================================
def getMetaData(image, imagePath):

    #dict of metadata for image
    metaData = dict()

    #add name to dict
    metaData.update({"name": os.path.basename(imagePath)})

    #add path to dict
    metaData.update({"path": imagePath})

    #add file extension to dict
    metaData.update({"ext": os.path.splitext(os.path.basename(imagePath))[1]})

    #get image size (x and y)
    y, x, a = image.shape 
    metaData.update({"sizeX": x})
    metaData.update({"sizeY": y})

    #get image size (total pixels)
    metaData.update({"pixelCt": x*y})

    #get image size (bytes)
    metaData.update({"byteSize": os.stat(imagePath).st_size})

    return metaData
