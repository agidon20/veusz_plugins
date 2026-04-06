import veusz.plugins as plugins
import re
import os
import numpy as np

class SettingsIteratorPlugin(plugins.ToolsPlugin):
    """Dataset plugin to shift a dataset."""

    # tuple of strings to build position on menu
    menu = ('Get Settings Array',)

    # internal name for reusing plugin later
    name = 'SettingsArray'

    # string which appears in status bar
    description_short = 'Get array of property value from a set of widget'
    
    # string goes in dialog box
    description_full = ('Get an array of a single setting from multiple'
                        'widgets of the given name pattern.')
    
    def __init__(self):
        """Define input fields for plugin."""
        self.fields = [
            #plugins.FieldDataset('color_ds', 'Color dataset'),
           
            #plugins.FieldDataset('ds_out', 'Output dataset name'),
            plugins.FieldWidget("widget", "Start from widget", default="/"),
            plugins.FieldText("patt", """REGEXP: Search for number in widget name()
                                        e.g. xy([1-5])
                                        the number searched should be 
                                        within round brackets.""",default = '\[:(.*):\]'),
            plugins.FieldText("setting_path", "Name/path of property within the widget", default="xData"),
            ]

    def copy_to_clipboard(text):
        command = 'echo | set /p nul=' + text.strip() + '| clip'
        os.system(command)   
    
    def apply(self, ifc, fields):
        
        #ifc is actually explained in the veusz manual API
        fromwidget = ifc.Root.fromPath(fields['widget'])
        patt = fields['patt'].strip()
        self.ds_out.update(data=[1,2,3,1,1], serr=[1,1,2,2,1])  

#        widgets = []
#        # loop over every xy widget including and below fromwidget
        for w in fromwidget.WalkWidgets():
            if patt and re.match(patt,w.name,flags=re.IGNORECASE):
                widgets.append(w)
#
        ifc.To(fields['widget'])
        output = np.array([])
        for idx, widget in enumerate(widgets):
            matchobj = re.search(fields['patt'],widget.name,flags=re.IGNORECASE)
            if(matchobj == None):
                continue
            output = np.append(output,widget.Get(fields['setting_path']))
        
        ifc.SetDataND("_output_",output)

#            val = (float(matchobj.group(1)) - color_min) /  (color_max - color_min)
#            if (val > 1):
#                val = 1
#            elif(val < 0):
#                val = 0
#
#            color_ind = int(255.0 * val)
#            if cvals[color_ind,3] == 255:
#                # opaque
#                col = "#%02x%02x%02x" % (
#                    cvals[color_ind,0], cvals[color_ind,1], cvals[color_ind,2])
#            else:
#                # with transparency
#                col = "#%02x%02x%02x%02x" % (
#                    cvals[color_ind,0], cvals[color_ind,1], cvals[color_ind,2], cvals[color_ind,3])
#                
#            widget.PlotLine.color.val = col
            


# add plugin classes to this list to get used
plugins.toolspluginregistry.append(SettingsIteratorPlugin)