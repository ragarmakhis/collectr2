from Cocoa import *
from Foundation import NSObject
 
class collectrController(NSWindowController):
    volumesTextField = objc.IBOutlet()
    xmlTextField = objc.IBOutlet()
    outputTextField = objc.IBOutlet()
 
    def windowDidLoad(self):
        NSWindowController.windowDidLoad(self)
 
        # Start the counter
        # self.count = 0

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
            self.volumesString = ''
            for item in self.volumes:
                item = item.absoluteString()#.replace('file://localhost/Volumes/','')
                self.volumesString = self.volumesString + item.replace('file://localhost','') + '; '
                 
            self.volumesTextField.setStringValue_(self.volumesString[:-2])
               
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
        openDlg.setAllowedFileTypes_(['xml'])
        openDlg.setResolvesAliases_(True)
    
        # Вывести диалог модально
        # Если запуск вернул нажатие кнопки OK - обработать выбранные файлы
        if openDlg.runModal() == NSFileHandlingPanelOKButton:
        
            # Список выбранных файлов
            self.volumes = openDlg.URLs()
            self.volumesString = ''
            for item in self.volumes:
                item = item.absoluteString()#.replace('file://localhost/Volumes/','')
                self.volumesString = self.volumesString + item.replace('file://localhost','') + '; '
                 
            self.volumesTextField.setStringValue_(self.volumesString[:-2])

    @objc.IBAction
    def setTypeXML_(self, sender):
        # [F]inal Cut Pro or [D]avinci Resolve

        pass

    @objc.IBAction
    def setTypeSource_(self, sender):
        # [A]rri Alexa or [R]3D source files

        pass

    # @objc.IBAction
    # def setOutputTXT_(self, sender):
    #     # Output TXT file name

    #     pass

    @objc.IBAction
    def setPath_(self, sender):
        # Path where to copy R3D files
        
        pass

    @objc.IBAction
    def createTXTOnly_(self, sender):
        # [Y] - Makes only txt file with source filenames without find and copy
        
        pass

    @objc.IBAction
    def start_(self, sender):
        # start
        
        pass
 
    # def updateDisplay(self):
    #     self.counterTextField.setStringValue_(self.count)
 
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