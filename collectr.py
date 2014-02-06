from Cocoa import *
from Foundation import NSObject
import os.path, re, subprocess
import xml.etree.ElementTree as etree
from time import sleep
 
class collectrController(NSWindowController):
    volumesTextField = objc.IBOutlet()
    xmlTextField = objc.IBOutlet()
    outputTextField = objc.IBOutlet()
    typeXMLTextField = objc.IBOutlet()
    typeSourceTextField = objc.IBOutlet()
    txtOnlyTextField = objc.IBOutlet()
    logTextView = objc.IBOutlet()
 
    def windowDidLoad(self):
        NSWindowController.windowDidLoad(self)
 
        # init value
        self.typeXML = 'F'
        self.typeSource = 'R'
        self.createTXTOnly = 0
        self.outputTxt = '/tmp/collectr.txt'
        self.volumes = NSArray.arrayWithObject_(NSURL.URLWithString_("file://localhost/Volumes/"))
        self.outputPath = ''

    @objc.IBAction
    def setVolumesDialog_(self, sender):
        # Volume name where to search R3D files
        
        # Создать диалог
        openDlg = NSOpenPanel.openPanel()
    
        #Свойства диалога
        openDlg.setCanChooseFiles_(False)
        openDlg.setCanChooseDirectories_(True)
        openDlg.setAllowsMultipleSelection_(True)
        openDlg.setDirectoryURL_(NSURL.URLWithString_("file://localhost/Volumes/"))
        openDlg.setResolvesAliases_(True)
    
        # Вывести диалог модально
        # Если запуск вернул нажатие кнопки OK - обработать выбранные файлы
        if openDlg.runModal() == NSFileHandlingPanelOKButton:
        
            # Список выбранных файлов
            self.volumes = openDlg.URLs()
            volumesString = ''
            for item in self.volumes:
                fileName = item.lastPathComponent()
                item = item.path()
                volumesString = volumesString + item + '; '
                 
            self.volumesTextField.setStringValue_(volumesString[:-2])
               
        # // Показать выбранные файлы
        # for i in self.volumes:
        #     self.alert = NSAlert.alloc().init()
        #     self.alert.setMessageText_(i)
        #     self.alert.runModal()
 
    @objc.IBAction
    def setXMLDialog_(self, sender):
        # Input XML file name

        # Создать диалог
        openDlg = NSOpenPanel.openPanel()
    
        #Свойства диалога
        openDlg.setCanChooseFiles_(True)
        openDlg.setCanChooseDirectories_(False)
        openDlg.setAllowsMultipleSelection_(False)
        openDlg.setAllowedFileTypes_(NSArray.arrayWithObject_('xml'))
        openDlg.setResolvesAliases_(True)
    
        # Вывести диалог модально
        # Если запуск вернул нажатие кнопки OK - обработать выбранные файлы
        if openDlg.runModal() == NSFileHandlingPanelOKButton:
        
            # Список выбранных файлов
            # self.xmlFile = openDlg.URLs().objectAtIndex_(0).absoluteString()
            self.xmlFile = openDlg.URLs().objectAtIndex_(0)#.lastPathComponent()

            self.xmlTextField.setStringValue_(self.xmlFile.path())

            if self.xmlFile.pathExtension() != 'xml':
                alert = NSAlert.alloc().init()
                alert.setMessageText_('Please select XML file')#.componentsJoinedByString_(",\n"))
                alert.runModal()

        
    @objc.IBAction
    def setTypeXML_(self, sender):
        # [F]inal Cut Pro or [D]avinci Resolve

        self.typeXML = sender.selectedItem().toolTip()

        self.typeXMLTextField.setStringValue_(self.typeXML)

    @objc.IBAction
    def setTypeSource_(self, sender):
        # [A]rri Alexa or [R]3D source files

        self.typeSource = sender.selectedItem().toolTip()

        self.typeSourceTextField.setStringValue_(self.typeSource)

    @objc.IBAction
    def setPath_(self, sender):
        # Path where to copy R3D files
        
        # Создать диалог
        openDlg = NSOpenPanel.openPanel()
    
        #Свойства диалога
        openDlg.setCanChooseFiles_(False)
        openDlg.setCanChooseDirectories_(True)
        openDlg.setAllowsMultipleSelection_(False)
        openDlg.setResolvesAliases_(True)
    
        # Вывести диалог модально
        # Если запуск вернул нажатие кнопки OK - обработать выбранные файлы
        if openDlg.runModal() == NSFileHandlingPanelOKButton:
        
            # Список выбранных файлов
            self.outputPath = openDlg.URLs().objectAtIndex_(0)

            self.outputTextField.setStringValue_(self.outputPath)

    @objc.IBAction
    def setOutputTxt_(self, sender):
        # Output TXT file name
        
        # Создать диалог
        saveDlg = NSSavePanel.savePanel()
    
        #Свойства диалога
        saveDlg.setCanChooseFiles_(True)
        saveDlg.setCanChooseDirectories_(False)
        saveDlg.setAllowsMultipleSelection_(False)
        saveDlg.setAllowedFileTypes_(NSArray.arrayWithObject_('txt'))
        saveDlg.setResolvesAliases_(True)
    
        # Вывести диалог модально
        # Если запуск вернул нажатие кнопки OK - обработать выбранные файлы
        if saveDlg.runModal() == NSFileHandlingPanelOKButton:
        
            # Список выбранных файлов
            self.outputTxt = saveDlg.filename()#.objectAtIndex_(0)

            # alert = NSAlert.alloc().init()
            # alert.setMessageText_(self.outputTxt)#.componentsJoinedByString_(",\n"))
            # alert.runModal()
            self.outputTextField.setStringValue_(self.outputTxt)

    @objc.IBAction
    def createTXTOnly_(self, sender):
        # [Y] - Makes only txt file with source filenames without find and copy
        
        self.createTXTOnly = sender.state()

        if self.createTXTOnly:
            self.txtOnlyTextField.setStringValue_("YES")
        else:
            self.txtOnlyTextField.setStringValue_("NO")

    @objc.IBAction
    def start_(self, sender):
        # start

        #Set input XML filename from args
        xmlName = self.xmlFile.path()

        # Set text filename from args or by default
        if self.outputTxt == '/tmp/collectr.txt':
            txtName = '/tmp/' + self.xmlFile.lastPathComponent().replace(self.xmlFile.pathExtension(), 'txt')
        else:
            txtName = self.outputTxt.path()
        
        

        volumesString = ''
        for item in self.volumes:
            fileName = item.lastPathComponent()
            item = item.path()#.replace(fileName, '')
            volumesString = volumesString + item + '; '
        
        self.logTextView.insertText_('\n' + 'R3D files will search in ' + volumesString[:-2] + '...' + '\n')

        # Set path to copy R3D files
        # pathName = self.outputPath
        if self.outputPath == '':
            pathName = self.xmlFile.path().replace(self.xmlFile.lastPathComponent(), '')
        else:
            pathName = self.outputPath.path()
        self.logTextView.insertText_('R3D files will be copied to ' + pathName + '\n')

        #Select XML schema query
        if self.typeXML == 'F':
            xmlPath = ".//sequence/media/video/track/clipitem/file/name" # From Final Cut
        else:
            xmlPath = ".//VideoTrackVec/Element/Sm2TiTrack/Items/Element/Sm2TiVideoClip/MediaReelNumber" # From Davinci Resolve

        #Regexp for search in XML
        if self.typeSource == 'R':
            xmlSearch = "^[A-Z]\d{3}_[A-Z]\d{3}_\d{4}\w{2}" # For R3D
        else:
            xmlSearch = "^[A-Z]\d{3}[A-Z]\d{3}_\d{4}\w{2}" # For Alexa

        #Make text file with all R3D filenames from XML
        fileCount = 0
        if not os.path.exists(txtName):
            txtfile = open(txtName, 'w+')
            tree = etree.parse(xmlName)
            root = tree.getroot()
            for elem in root.findall(xmlPath):
                match = re.match(xmlSearch, elem.text) 
                if match:
                    txtfile.write(elem.text + '\n')
                    fileCount += 1
            self.logTextView.insertText_('Found ' + str(fileCount) + ' cut(s)' + '\n')
            txtfile.close
            txtfile = open(txtName, 'r')
            tempurls = txtfile.readlines()
            pathurls = list(set(tempurls))
            fileCount = len(pathurls)
            txtfile.close
            self.logTextView.insertText_('Found ' + str(fileCount) + ' file(s)' + '\n')
        else:
            self.logTextView.insertText_('Text file already exists, reading contents...' + '\n')



        if self.createTXTOnly != 'YES':
            sleep(3)

            #Open text file and read content

            txtfile = open(txtName, 'r')
            self.logTextView.insertText_('Open textfile on read\n')
            tempurls = txtfile.readlines()
            self.logTextView.insertText_('read line in temp\n')
            pathurls = list(set(tempurls))
            self.logTextView.insertText_('delite dublicate\n')
            fileCount = len(pathurls)
            self.logTextView.insertText_('Calculate lenght list\n')
            txtfile.close
            self.logTextView.insertText_('Close file\n')

            lineCount = 1
            R3Dname = ''

            #Find and copy R3D files
            for item in self.volumes:
                volName = item.path()
                directoryToScan = volName
                txtfile = open(txtName, 'w+')
                localFileManager = NSFileManager.defaultManager()
                contents, error = localFileManager.contentsOfDirectoryAtURL_includingPropertiesForKeys_options_error_(
                    item, 
                    NSArray.arrayWithObject_(NSURLIsDirectoryKey), 
                    NSDirectoryEnumerationSkipsHiddenFiles, None)
                # self.logTextView.insertText_('\n\n')
                # for item in contents:
                #     self.logTextView.insertText_(item.path() + '\n')
                # self.logTextView.insertText_('\n\n')

                # dirEnumerator, error = localFileManager.enumeratorAtURL_includingPropertiesForKeys_options_errorHandler_(
                #     item, 
                #     NSArray.arrayWithObject_(NSURLIsDirectoryKey), 
                #     NSDirectoryEnumerationSkipsHiddenFiles, 
                #     None)
                # names, error = NSString.stringWithContentsOfFile_encoding_error_(
                #     u"/usr/share/dict/propernames",
                #     NSASCIIStringEncoding, None)
                # dirEnumerator = localFileManager.componentsToDisplayForPath_(directoryToScan)
                # alert = NSAlert.alloc().init()
                # alert.setMessageText_(dirEnumerator)#.componentsJoinedByString_(",\n"))
                # alert.runModal()
                # theArray = NSMutableArray.array()

                for filename in pathurls:
                    for item in contents:
                        self.logTextView.insertText_(item.path() + '\n')
                        if item.lastPathComponent() == '.Trashes':
                            continue
                        finded = self.findRAW(item.path(), filename)

                        if finded:
                            self.logTextView.insertText_(filename.rstrip('\n') + ' --------------- ' + str(lineCount) + ' of ' + str(fileCount) + '\n')
                            subprocess.call(['cp', '-R', finded.rstrip(), pathName])
                            self.logTextView.insertText_(finded + '\n')
                            lineCount += 1
                        else:
                            txtfile.write(filename)
                    
        elif self.createTXTOnly == 'YES':
            return 0

        self.logTextView.insertText_('Found and copied ' + str(lineCount-1) + ' file(s) of ' + str(fileCount) + '\n')
 
    # def updateDisplay(self):
    #     self.counterTextField.setStringValue_(self.count)
    def findRAW(self, path, rawName):
        if self.typeSource == 'R':
            R3Dname = rawName[0:16] + '.RDC' # RED
            finded = subprocess.check_output(['find', path, '-type', 'd', '-name', R3Dname]) # RED
        else:
            R3Dname = rawName[0:20] + '*' + '.mov' # Alexa
            finded = subprocess.check_output(['find', path, '-type', 'f', '-name', R3Dname])
        return finded
 
if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    
    # Initiate the contrller with a XIB
    viewController = collectrController.alloc().initWithWindowNibName_("collectr")
 
    # Show the window
    viewController.showWindow_(viewController)
 
    # Bring app to top
    NSApp.activateIgnoringOtherApps_(True)
    
    from PyObjCTools import AppHelper
    AppHelper.runEventLoop()