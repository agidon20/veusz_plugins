import veusz.plugins as plugins
import re
import numpy as np

class FitWidgetFromDataSets(plugins.ToolsPlugin):
    """Dataset plugin to shift a dataset."""

    # tuple of strings to build position on menu
    menu = ('Create Fit from Datasets...',)

    # internal name for reusing plugin later
    name = 'FitFromDatasets'

    # string which appears in status bar
    description_short = 'Generating a Fit widget from a list of datasets by regular expressions'
    
    # string goes in dialog box
    description_full = (""" you need to have consistency between the naming of the x and the y data
for example if you have two datasets Y_[0-9]* and X_[0-9]*, then the number part of the datasets
should be the same to indicate to veuzs to bind them. 
Then you have to specify exactly what part of y data is going to be bounded to x data.
for example, if you have 
height_123123.. for y and x_123123.. for x then
Y widget will be: height_[0-9]* 
Match Y widget will be: height_([0-9]) - not that the paranthesis say that this is group {2}
X widget will be: x_{2}""")
    
    def __init__(self):
        """Define input fields for plugin."""
        self.fields = [
            plugins.FieldWidget("widget", "Create fits under this widget", default=""),
            plugins.FieldText("data", "REGEXP: Match for source dataset",default = 'height_([0-9]+)'),
            plugins.FieldText('Y', 'fit Y (example: ones(10)*{0}, x{1}; {0}=enum; {1} fullname; {2}=match_data',default = 'width_{2} * height_{2}'),
            plugins.FieldText('X', 'fit X (example: ones(10)*{0}, x{1}; {0}=enum; {1} fullname; {2}=match_data',default = 'isoma_{2}'),
            ]


              
                
    def apply(self, ifc, fields):
        """Do the randomizing."""
        datasets = ifc.GetDatasets()
        ifc.To(fields['widget'])
        for i,d in enumerate(datasets):
            matchobj = re.search(fields['data'],d,flags=re.IGNORECASE)      
            if matchobj is not None:
                ydata = fields['Y'].format(i,d,matchobj.group(1))
                xdata = fields['X'].format(i,d,matchobj.group(1))
                f = ifc.Add('fit', name='fit_' + d, yData=ydata, xData=xdata)
                data = ifc.GetData(xdata)[0] #get the part of the data
                f.min = float(np.nanmin(data))
                f.max = float(np.nanmax(data))
# add plugin classes to this list to get used
plugins.toolspluginregistry.append(FitWidgetFromDataSets)