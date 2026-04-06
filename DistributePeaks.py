import veusz.plugins as plugins
import re
import numpy as np


class DistributePeaks(plugins.ToolsPlugin):
    """Dataset plugin to shift a dataset."""

    # tuple of strings to build position on menu
    menu = ('Distribute by the peak of the traces...',)

    # internal name for reusing plugin later
    name = 'DistributePeaks'

    # string which appears in status bar
    description_short = 'align all the peaks at x = 0'
    
    # string goes in dialog box
    description_full = (""" Order is important.""")
    
    def __init__(self):
        """Define input fields for plugin."""
        self.fields = [
            plugins.FieldWidget("widget", "Create xy's under this widget", default="" , widgettypes=("graph")),
            plugins.FieldText("xy", "REGEXP: Match for dataset",default = 'xy(.*)'),
            plugins.FieldText('xstart', 'find extermum from here',default = '0'),
            plugins.FieldText('xend', 'find extermum to here',default = '1000'),
            plugins.FieldText('xspacing', 'make spaces between each peak',default = '10'),
            plugins.FieldBool('create_dataset', 'When checked, the min, max and diff will be created',default=False),
            plugins.FieldBool('use_only_visible', 'When checked, only visible widgets are used',default=True)
       
            ]


              
                
    def apply(self, ifc, fields):
        """Do the randomizing."""
        parent_widget = ifc.Root.fromPath(fields['widget'])
        xstart = float(fields['xstart'].strip())
        xend = float(fields['xend'].strip())
        xspacing = fields['xspacing'].strip() #remain a string
        output_min =np.array([])
        output_max = np.array([])
        use_only_visible = fields['use_only_visible']
        for i,d in enumerate(parent_widget.WalkWidgets(widgettype='xy')):
            matchobj = re.search(fields['xy'],d.name,flags=re.IGNORECASE)      
            if matchobj is not None:
                if(not d.hide.val) or (d.hide.val and not use_only_visible):
                    #first remove the old addition
                    d.xData.val = d.xData.val.split(" + ")[0]
                    d.yData.val = d.yData.val.split(" + ")[0]
                    xdata = np.array(ifc.GetData( d.xData.val )[0])
                    ydata = np.array(ifc.GetData( d.yData.val )[0])
                    ind_xstart = next(x for x, val in enumerate(xdata) if val > xstart)
                    ind_xend = next(x for x, val in enumerate(xdata) if val > xend)
                    ind_max = np.argmax(ydata[ind_xstart:ind_xend])
                    output_min = np.append(output_min, np.min(ydata[ind_xstart+ind_max:ind_xend]) )
                    output_max = np.append(output_max, ydata[ind_xstart+ind_max] )
                  
                    dx = xdata[ind_max + ind_xstart]
                    d.xData.val = d.xData.val + " + ( " + xspacing + "*" + str(i) + " -" + str(dx) + ")"
        if(fields['create_dataset']):
            ifc.SetData("_output_min_",output_min)
            ifc.SetData("_output_max_",output_max)
            ifc.SetData("_output_diff_",output_max -output_min)
                #then add the new addition
                #if(xoff not in ("","0")): d.xData.val = d.xData.val + " + " + str(i) + "*" + xoff
                #if(yoff not in ("","0")): d.yData.val = d.yData.val + " + " + str(i) + "*" + yoff
# add plugin classes to this list to get used
plugins.toolspluginregistry.append(DistributePeaks)