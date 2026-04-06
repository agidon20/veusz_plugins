import veusz.plugins as plugins
import re


class LineColorSetPlugin(plugins.ToolsPlugin):
    """Dataset plugin to shift a dataset."""

    # tuple of strings to build position on menu
    menu = ('Set lines color',)

    # internal name for reusing plugin later
    name = 'SetLineColors'

    # string which appears in status bar
    description_short = 'assign xy colors by value in their name'
    
    # string goes in dialog box
    description_full = ('Set the color of a set of lines automatically from a colormap. '
                        'This text goes into the dialog box.')
    
    def __init__(self):
        """Define input fields for plugin."""
        self.fields = [
            #plugins.FieldDataset('color_ds', 'Color dataset'),
           
            #plugins.FieldDataset('ds_out', 'Output dataset name'),
            
            plugins.FieldWidget("widget", "Start from widget", default=""),
            plugins.FieldText("patt", """REGEXP: Search for number in widget name()
                                        e.g. xy([1-5])
                                        the number searched should be 
                                        within round brackets.""",default = '\[:(.*):\]'),
            plugins.FieldColormap("colormap", "Colormap", default="cool-warm"),
            plugins.FieldFloat('color_scale_min', 'Color min value', default=0.),
            plugins.FieldFloat('color_scale_max', 'Color max value', default=500.),
            plugins.FieldBool("invert", "Invert colormap", default=False),
            plugins.FieldBool("plotline", "color plot line", default=True),
            plugins.FieldBool("markerfill", "color marker fill", default=False),
            plugins.FieldBool("markerline", "color marker line", default=False),


          #  plugins.FieldColor('color2', "End of color range", default='#ff0004'),            
            ]


              
                
    def apply(self, ifc, fields):
        """Do the randomizing."""

        fromwidget = ifc.Root.fromPath(fields['widget'])
        patt = fields['patt'].strip()

        # get list of RGBA values
        cm = ifc.GetColormap(
            fields["colormap"], invert=fields["invert"],
            nvals=256) #probably impossible to destinguqish at this resolution
 
        color_min = fields['color_scale_min']
        color_max = fields['color_scale_max']
        
        # convert colors to #XXXX format
        i = 0
        for idx, widget in enumerate(fromwidget.WalkWidgets(widgettype='xy')):
            matchobj = re.search(patt,widget.name,flags=re.IGNORECASE)
            if(matchobj == None): continue
            val = float(i); i = i + 1
            if(len(matchobj.groups()) > 0): val = float(matchobj.group(1))
            val = (val - color_min) /  (color_max - color_min)
            if (val > 1): val = 1
            if (val < 0): val = 0
    
            color_ind = int(255.0 * val)
            if cm[color_ind,3] == 255:
                    # opaque
                col = "#%02x%02x%02x" % tuple(cm[color_ind,0:3])
            else:
                    # with transparency
                col = "#%02x%02x%02x%02x" % tuple(cm[color_ind,0:4])
                    
            if(fields['plotline']): widget.PlotLine.color.val = col
            if(fields['markerfill']): widget.MarkerLine.color.val = col
            if(fields['markerline']): widget.MarkerFill.color.val = col
            
            


# add plugin classes to this list to get used
plugins.toolspluginregistry.append(LineColorSetPlugin)