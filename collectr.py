from Cocoa import *
from Foundation import NSObject
 
class collectrController(NSWindowController):
    counterTextField = objc.IBOutlet()
 
    def windowDidLoad(self):
        NSWindowController.windowDidLoad(self)
 
        # Start the counter
        self.count = 0

    @objc.IBAction
    def setVolumesDialog_(self, sender):
        #pass
        #Создать диалог
        self.openDlg = NSOpenPanel.openPanel()
    
        #Свойства диалога
        self.openDlg.setCanChooseFiles(False)
#        openDlg.setCanChooseDirectories(True)
#        openDlg.setAllowsMultipleSelection(True)
#        openDlg.setDirectoryURL(NSURL.URLWithString("/Volumes"))
#        openDlg.setResolvesAliases(True)
    
        # Вывести диалог модально
        # Если запуск вернул нажатие кнопки OK - обработать выбранные файлы
        if self.openDlg.runModal() == NSFileHandlingPanelOKButton:
        
            # Список выбранных файлов
            self.files = self.openDlg.URLs()
            self.counterTextField.setStringValue_(self.files)
#        
#        // Показать выбранные файлы
#        NSAlert *alert = [[NSAlert alloc] init];
#        [alert setMessageText:[files componentsJoinedByString:@",\n"]];
#        [alert runModal];
 
    @objc.IBAction
    def increment_(self, sender):
        self.count += 1
        self.updateDisplay()
 
    @objc.IBAction
    def decrement_(self, sender):
        self.count -= 1
        self.updateDisplay()
 
    def updateDisplay(self):
        self.counterTextField.setStringValue_(self.count)
 
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