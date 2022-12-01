from imports import *

#================================================================
#
# Function: checkImages(dir, starting = False)
#
# Description: This function takes in the directory passed to it 
#              from the command line and creates an array of PIL
#              images from it that we can manipulate with OpenCV
#              to fit in the confines specified. It also
#              preserves the ordering in which the images appear
#              in the directory.
#
#              The newly added "starting" variable controls 
#              whether or not the program should check to see
#              if any images were actually found in the entire 
#              directory and subdirectory trees
#
# Returns: ImgList | type: array of images
#
#================================================================
def checkImages(dir, starting = False):

    #array of images and paths
    ImgList = []
    ImgPathList = []

    #image types that we recognize
    valid_images = [".jpg",".gif",".png", ".jpeg"]

    #get order for depth-first preservation

    #get list of dirs only
    dirlist = [x for x in os.listdir(dir) if os.path.isdir(os.path.join(dir, x))]
    #get list of files only
    filelist = [x for x in os.listdir(dir) if not os.path.isdir(os.path.join(dir, x))]

    #get all images in directory
    try:
        for file in (filelist + dirlist):

            #recurse if 'file' in directory is directory
            if os.path.isfile(dir + "/" + file) == False:

                #recurse and join the results
                tmpimg, tmppath = checkImages(dir + "/" + file)
                ImgList = ImgList + tmpimg
                ImgPathList = ImgPathList + tmppath
                
            #if file ends in a file extension associated with an image, we take it
            if os.path.splitext(file)[1].lower() in valid_images:

                #add another try except block to protect this portion of the code
                try:
                    ImgList.append(cv2.imread(os.path.join(dir, file)))
                except exception:
                    print("Reading of one of the image files has failed. Program will now exit.")
                    sys.exit(-1)

                #add path of image to list of paths
                ImgPathList.append(os.path.join(dir, file))

    except Exception:
        print("Malformed directory: " + dir + " Skipping....")

    #check to see if the directory is devoid of images
    #AKA check to see if our imgList is empty
    if starting == True:
        if len(ImgList) == 0:
            print("No images were found in the provided directory: " + dir + "\nProgram will now exit.")
            sys.exit(-1)

    #return array of image data
    return ImgList, ImgPathList