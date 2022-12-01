#==============================================================================
#
# Class : CS 5420
#
# Author : Tyler Martin
#
# Project Name : Project 1 | Image Browser 
#
# Date: 9-14-2022
#
# Description: This is a simple image browser programmed in python using: 
#              opencv, PIL, tkinter, numpy, sys, getopt, os, and
#              math modules. The image browser takes in a path with the switch
#              -d or --dir, and searches for images in that directory and all
#              sub directories. Images that are found are either displayed in 
#              a 720x1080 resolution, or a new resolution can be specified by
#              -r or --rows switch and -c or --columns switch, with rows 
#              corresponding to 'x' size and columns corresponding to 'y' size
#
# Notes: Since I know you prefer to read and work in C++, this file is set
#        up to mimic a standard C/C++ flow style, including a __main__()
#        declaration for ease of viewing. Also, while semi-colons are not 
#        required in python, they can be placed at the end of lines anyway, 
#        usually to denote a specific thing. In my case, they denote globals, 
#        and global access, just to once again make it easier to parse my code
#        and see what it is doing and accessing.
#
#==============================================================================

#"header" file imports
from imports import *
from checkImages import *
from getMetaData import *
from resizeImage import *

#================================================================
#
# GLOBALS
#
#================================================================
currentImg = 0;
maxSize = 0;
ImgList = [];
ImagePathList = [];
x = 1080;
y = 720;

#================================================================
#
# Class: ImageBox
#
# Description: This class serves as the GUI for the application.
#              It opens displaying the first image in the directory
#              and can cycle between other images present in the 
#              directory. It also displays metadata associated with
#              the image being displayed. It is included here along
#              with main, because while python can import other files
#              and functions similar to headers, for functions to be
#              imported, it requires mass re-importing to make sure 
#              the class has the access it needs, which slows the 
#              program down and causes tight coupling. 
#
#================================================================
class imageBox(Tk):
    def __init__(self):
        super().__init__()
        
        #gain temporary access to globals
        global ImgList;
        global ImagePathList;
        global x;
        global y;

        #setup the basic window features
        self.title('Image Browser')
        self.resizable(0, 0)

        #set the window dimensions
        self.geometry(str(x) + 'x' + str(y))

        #making an imageBox frame
        self.imgBox = Frame(self, relief = RIDGE, borderwidth = 0)
        self.imgBox.pack(side = TOP)

        #convert our image back to PIL format
        #(essentially just swapping bgr pixel
        # order to rgb for pil)
        self.blue, self.green, self.red = cv2.split(resizeImage(ImgList[currentImg], x, y, getMetaData(ImgList[currentImg], ImagePathList[currentImg])))
        self.img = cv2.merge((self.red, self.green, self.blue))
        self.icon = ImageTk.PhotoImage(image = Image.fromarray(self.img))

        #anchoring the image to the widget
        #(I have no idea what this does, but
        #from what I have read, the C side of 
        #python requires that Tkinter image
        #references have an 'anchor' point
        #which is literally just a pointer
        #on the C side, so we just force it to
        #make one by making a hard reference)
        #Likely not needed anymore due to 
        #removing the updating function, but will
        #keep here for future material reference.
        self.icon_size = Label(self.imgBox)
        self.icon_size.image = self.icon
        self.icon_size.configure(image = self.icon)
        self.icon_size.pack(side = LEFT)

        #getting the image info to display
        self.currentMetaData = getMetaData(ImgList[currentImg], ImagePathList[currentImg])
        self.info = ("Name:" + self.currentMetaData.get("name") + "\n"
                + "Path: " + ImagePathList[currentImg] + "\n"
                + "Image Type: " + self.currentMetaData.get("ext") + "\n"
                + "File Size (bytes): " + str(self.currentMetaData.get("byteSize")) + "\n"
                + "Columns: " + str(self.currentMetaData.get("sizeX")) + "\n"
                + "Rows: " + str(self.currentMetaData.get("sizeY")) + "\n"
                + "Pixel Count: " + str(self.currentMetaData.get("pixelCt")) + "\n"
        )

        #setup simple handling protocol for if user
        #uses the window manager to close the program
        #instead of 'q'
        self.protocol("WM_DELETE_WINDOW", self.close_gracefully)

        #binding events to the window so we can have instant
        #callback functions for the cycling of images
        self.bind("<Key>", self.key_handler)

        #address menu options so that the messageBox actually
        #displays the text correctly (*NIX ONLY OPTIONS)
        self.option_add('*Dialog.msg.width', 50)
        self.option_add('*Dialog.msg.font', 'Helvetica 12')
        self.option_add("*Dialog.msg.wrapLength", "7i")

        #make a simple menu to better display the file information
        self.menubar = Menu(self) 
        self.about = Menu(self.menubar, tearoff = 0)  
        self.about.add_command(label = "About Image", command = self.aboutImage)  
        self.menubar.add_cascade(label = "About", menu = self.about) 
        self.config(menu = self.menubar)

    #===========================================
    #this is a very simple function that is
    #called when the window is closed via
    #the window manager so that the program
    #does not hang. It's only purpose is to
    #visually be nicer than including a lambda
    #function in the protocol designated to
    #handle window closing events above.
    #===========================================
    def close_gracefully(self):
        sys.exit(0)

    #===========================================
    #this is another incredibly simple function
    #which just handles incoming requests for 
    #information about the image being displayed
    #fired from the menubar option "About"
    #===========================================
    def aboutImage(self):
        messagebox.showinfo('About Image', self.info)

    #===========================================
    #this is a callback function. It is fired
    #when a bind event happens to check for a key
    #fire event. If a valid key fire is detected,
    #globals are updated, and the displayed image
    #is as well
    #===========================================
    def key_handler(self, event):
        #gain access to the global
        global currentImg;
        global maxSize;
        global ImgList;
        global ImagePathList;
        global x;
        global y;
        action = event.keysym;

        #listen for keystrokes
        if action == 'q':
            quit();
        if action == 'p':
            if (currentImg > 0):
                currentImg -= 1 
        if action == 'n':
            if (maxSize - 1 > currentImg):
                currentImg += 1 
        if action == 'space':
            if (maxSize -1 > currentImg):
                currentImg += 1 

        #loop over image until it fits correctly
        resizedImage = resizeImage(ImgList[currentImg], x, y, getMetaData(ImgList[currentImg], ImagePathList[currentImg]))
        while (resizedImage.shape[0] > y or resizedImage.shape[1] > x):
            resizedImage = resizeImage(resizedImage, x, y, {"sizeX": resizedImage.shape[1], "sizeY": resizedImage.shape[0]})

        #convert our image back to PIL format
        #(essentially just swapping bgr pixel
        # order to rgb for pil)
        self.blue, self.green, self.red = cv2.split(resizedImage)
        self.img = cv2.merge((self.red, self.green, self.blue))
        self.icon = ImageTk.PhotoImage(image = Image.fromarray(self.img))

        #same refernce 'achor' stuff, but now we update
        #the image instead of making a new one
        self.icon_size.image = self.icon
        self.icon_size.configure(image = self.icon)

        #getting the image info to update if needed
        self.currentMetaData = getMetaData(ImgList[currentImg], ImagePathList[currentImg])
        self.info = ("Name:" + self.currentMetaData.get("name") + "\n"
                + "Path: " + ImagePathList[currentImg] + "\n"
                + "Image Type: " + self.currentMetaData.get("ext") + "\n"
                + "File Size (bytes): " + str(self.currentMetaData.get("byteSize")) + "\n"
                + "Columns: " + str(self.currentMetaData.get("sizeX")) + "\n"
                + "Rows: " + str(self.currentMetaData.get("sizeY")) + "\n"
                + "Pixel Count: " + str(self.currentMetaData.get("pixelCt")) + "\n"
        )

        #print the info to the terminal as well as the GUI
        print(self.info)

#================================================================
#
# Function: __main__
#
# Description: This function is the python equivalent to a main
#              function in C/C++ (added just for ease of your
#              reading, it has no practical purpose)
#
#================================================================

def __main__(argv):

    #gain access to our globals
    global maxSize;
    global currentImg;
    global ImgList;
    global ImagePathList;
    global x;
    global y;

    #variable to hold path
    path = "nothing"

    # get arguments and parse
    try:
      opts, args = getopt.getopt(argv,"h:r:c:d:")
    except getopt.GetoptError:
        print("browser.py -h  -r <rows> -c <columns> -d <directory>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == ("-h"):
            print("browser.py -h  -r <rows> -c <columns> -d <directory>")
            sys.exit(2)
        elif opt in ("-d", "--dir"):
            #make sure we don't get passed a file as a directory
            if (os.path.isdir(arg)):
                path = arg
        elif opt in ("-r", "--rows"):
            #make sure we get a real possible value
            if (int(arg) > 0):
                y = int(arg)
        elif opt in ("-c", "--columns"):
            #make sure we get a real possible value
            if (int(arg) > 0):
                x = int(arg)

    #make sure we got at the least, a path
    if (path == "nothing"):

        #check to see if we got passed a directory without a flag
        for possiblePath in sys.argv:
            if (os.path.exists(possiblePath) and os.path.isdir(possiblePath)):
                path = possiblePath
        
        if (path == "nothing"):
            print("you must provide a path to start with!")
            sys.exit(2)

    #test image grabbing, getting metadata, converting to openCV, and resizing
    ImgList, ImagePathList = checkImages(path, True)
        
    #set max size global
    maxSize = len(ImgList)

    #make the imagebrowser gui
    ws = imageBox()
    ws.mainloop()

#start main
argv = ""
__main__(sys.argv[1:])
