import webbrowser
class ViewSource:
   def addMenuItem(obj:object, url:str):
      """
      Adds a "View Source" context menu item to the context menu of the given object.
      Parameters:
         obj:object — The object to attach the context menu item to.
         url:str — The URL of the source viewer that the "View Source" item should open in the browser.
      
      How to use:
         obj must be a tkinter Menu object. To get the desired results, use code similar to https://stackoverflow.com/questions/12014210/tkinter-app-adding-a-right-click-context-menu for the context menu
      """
      obj.add_command(label="View Source",command=lambda: webbrowser.open(url=url))
