import os
import reader
import json
from PIL import Image

class Converter(object):



    def convertOnePose(self, poseName, sourcePath, destinationFolder, user="", description=""):
        """
        convert one pose to the new system
        """
        posereader = reader.PoseReader(sourcePath)

        data = {
            'metadata' : 
                {
                    'ctime':'0',
                    'version':'1.0.0',
                    'user':user,
                    'mayaSceneFile':'',
                    'mayaVersion':'2018',
                    'description':description
                },
            'objects': posereader.data()
        }

        poseName = poseName.replace('/','_')
        path = os.path.join(destinationFolder, poseName+'.pose')
        if os.path.exists(path) == False:
            os.mkdir(path)

        with open(os.path.join(path,'pose.json'), 'w') as fp:
            json.dump(data, fp, indent=4, sort_keys=True)

        #convert the screenshot
        imagePath = sourcePath.replace('.xml','.png')
        if os.path.exists(imagePath):
            im = Image.open(sourcePath.replace('.xml','.png'))
            im.save(os.path.join(path,'thumbnail.jpg'))


    def convertOneTab(self, sourcePath, destinationFolder, user="", description=""):
        """
        convert one tab of the old library into studio library
        """
        sourceFolder = os.path.split(sourcePath)[0]

        tabreader = reader.TabReader(sourcePath)

        for pose in tabreader.data().keys():
            posePath = os.path.join(sourceFolder, tabreader.data()[pose]['file'])

            if os.path.exists(posePath):
                self.convertOnePose(pose, posePath, destinationFolder, user, description)



    def convertOneLibrary(self, sourcePath, destinationFolder, description=""):
        """
        convert one library from the old system to the new system
        """
        sourceFolder = os.path.split(sourcePath)[0]

        libreader = reader.LibReader(sourcePath)
        
        #read all the Tabs
        for tab in libreader.data().keys():

            destinationTabFolder = os.path.join(destinationFolder, tab)
            if os.path.exists(destinationTabFolder) == False:
                os.makedirs(destinationTabFolder)
            
            tabPath = os.path.join(sourceFolder, libreader.data()[tab]['file'])

            #owner
            user = "supervisor"
            if "user" in sourcePath:
                user = sourcePath.split('/user/')[1].split('/')[0]

            if os.path.exists(tabPath):
                self.convertOneTab(tabPath, destinationTabFolder, user=user, description=description)

    def convertPoseLibrary(self, rootPath, destinationFolder, description=""):
        """
        convert the entire library
        """
        #first let's find all the lib.xml
        for root, dirs, files in os.walk(rootPath, topdown=True):
            for name in files:
                if name == "lib.xml":
                    libPath = os.path.join(root, name)
                    libDestFolder = root.replace(rootPath, destinationFolder) + ".lib"

                    if "user" in libDestFolder:
                        user = libDestFolder.split('/user/')[1].split('/')[0]
                        libDestFolder = libDestFolder.replace("/user/"+user, "/user/"+ user + ".user")
                    
                    if os.path.exists(libDestFolder) == False:
                        os.makedirs(libDestFolder)
                    
                    print "CONVERTING", libPath
                    if os.path.exists(libPath):
                        self.convertOneLibrary(libPath, libDestFolder, description)


                
