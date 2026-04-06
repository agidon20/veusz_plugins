import veusz.plugins as plugins
import re


class DistributeXY(plugins.ToolsPlugin):
    """Dataset plugin to shift a dataset."""

    # tuple of strings to build position on menu
    menu = ('Distribute xy...',)

    # internal name for reusing plugin later
    name = 'DistributeXY'

    # string which appears in status bar
    description_short = 'Add constant to xy widget at the x and the y data'
    
    # string goes in dialog box
    description_full = (""" Order is important.""")
    
    def __init__(self):
        """Define input fields for plugin."""
        self.fields = [
            plugins.FieldWidget("widget", "Create xy's under this widget", default=""),
            plugins.FieldText("xy", "REGEXP: Match for dataset",default = 'xy(.*)'),
            plugins.FieldText('xoffset', 'Add factor to x data',default = '20'),
            plugins.FieldText('yoffset', 'Add factor to y data',default = '20'),
       
            ]


              
                
    def apply(self, ifc, fields):
        """Do the randomizing."""
        parent_widget = ifc.Root.fromPath(fields['widget'])
        xoff = fields['xoffset'].strip()
        yoff = fields['yoffset'].strip()
        for i,d in enumerate(parent_widget.WalkWidgets(widgettype='xy')):
            matchobj = re.search(fields['xy'],d.name,flags=re.IGNORECASE)      
            if matchobj is not None:
                #first remove the old addition
                d.xData.val = d.xData.val.split(" + ")[0]
                d.yData.val = d.yData.val.split(" + ")[0]
                #then add the new addition
                if(xoff not in ("","0")): d.xData.val = d.xData.val + " + " + str(i) + "*" + xoff
                if(yoff not in ("","0")): d.yData.val = d.yData.val + " + " + str(i) + "*" + yoff
# add plugin classes to this list to get used
plugins.toolspluginregistry.append(DistributeXY)