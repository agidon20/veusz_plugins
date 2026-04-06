import veusz.plugins as plugins
import re
import os
import numpy as np

class SettingsCollectorPlugin(plugins.ToolsPlugin):
    """Dataset plugin to shift a dataset."""

    # tuple of strings to build position on menu
    menu = ('Collect Settings',)

    # internal name for reusing plugin later
    name = 'SettingsCollector'

    # string which appears in status bar
    description_short = 'Collect settings from widgets with name/type match'
    
    # string goes in dialog box
    description_full = ('Get an array of a single setting from multiple'
                        'widgets of the given name pattern (outputs are _output_ (and _output_x_).')
    
    def __init__(self):
        """Define input fields for plugin."""
        self.fields = [
            #plugins.FieldDataset('color_ds', 'Color dataset'),
           
            #plugins.FieldDataset('ds_out', 'Output dataset name'),
            plugins.FieldBool("is_widget", "Collect from widget?",default=False),
            plugins.FieldWidget("widget", "Start from widget", default=""),
            plugins.FieldText("widget_regexp", """(obligatory) REGEXP: widget match (e.g. fit_2[3-4]_([asd])""",default = 'fit_width_([0-9]+)'),
            plugins.FieldText("widget_type", "(obligatory) type of property within the widget", default=".*"),
            plugins.FieldText("setting_path", "(obligatory) Name/path of property within the widget", default="values"),
            plugins.FieldText("sub_setting_path", "Name/path of property within the setting group", default="a"),
       
        
            plugins.FieldBool("is_dataset", "Collect from datasets?",default=False),
            plugins.FieldText("dataset_regexp", """(obligatory) REGEXP: dataset match (e.g. fit_2[3-4]_([asd]). Support only 1D""",default = 'width_([0-9]+)'),
            plugins.FieldBool("is_mean", "[MEAN] get mean of each dataset as an array?",default=False),
            plugins.FieldBool("is_max", "[MAX] get max of each dataset as an array?",default=False),
            plugins.FieldBool("is_min", "[MIN] get min of each dataset as an array?",default=False),
            plugins.FieldBool("is_std", "[STD] get standard diviation of each dataset as an array?",default=False),
            plugins.FieldBool("is_first", "[FIRST] get first element of each dataset as an array?",default=False),
            plugins.FieldBool("is_last", "[LAST] get last element of each dataset as an array?",default=False),            
       ]

    def copy_to_clipboard(text):
        command = 'echo | set /p nul=' + text.strip() + '| clip'
        os.system(command)   
    
    
    def apply_to_widget(self,ifc, fields):
        fromwidget = ifc.Root.fromPath(fields['widget'])
        patt = fields['widget_regexp'].strip()
        sett = fields['setting_path'].strip()
        subsett = fields["sub_setting_path"].strip()
        wtype = fields["widget_type"].strip()
        output = []
        xoutput = []
        val = None
#        # loop over every xy widget including and below fromwidget
        i = ""
        for w in fromwidget.WalkWidgets():
            matchobj = re.match(patt,w.name,flags=re.IGNORECASE)
            if patt and matchobj:
                if(matchobj.lastindex > 0 ):
                    x = matchobj.group(1) #additional value from the widget
                else:
                    x = None
                    
                if wtype and re.match(wtype,w.widgettype,flags=re.IGNORECASE):
                    i = i + w.name + " "
                    ifc.To(w.path)
                    val = ifc.Get(sett)
                    if(type(val) is dict):
                        val = val[subsett]
                        
                        
                    if(isinstance(val, (float,int) )):
                        if(x):
                            xoutput = np.append(xoutput,x)#numpy array
                        output = np.append(output,val)#numpy array
                    if(isinstance(val,(str))):
                        output.append(val)#string list
                        
        if(val): #there is something in there           
            if(type(val) is str):
                ifc.SetDataText("_output_",output)
                ifc.TagDatasets('collector','')
            if(type(val) is float):
                if(x):
                    ifc.SetData("_output_x_",xoutput)
                    ifc.TagDatasets('collector',['_output_x_'])
                ifc.SetData("_output_",output)
                ifc.TagDatasets('collector',['_output_'])


                 
    def apply_to_dataset(self,ifc, fields):
        datasets = ifc.GetDatasets()
        patt = fields['dataset_regexp'].strip()
        is_mean = fields['is_mean']
        is_max = fields["is_max"]
        is_min = fields["is_min"]
        is_std = fields["is_std"]
        is_first = fields["is_first"]
        is_last = fields["is_last"]
        
        output_mean = []
        output_max = []
        output_min = []
        output_first = []
        output_last = []
        output_std = []
        xoutput = []
        val = []
        dtype1 = None
#        # loop over every xy widget including and below fromwidget
        for d in datasets:
            matchobj = re.match(patt,d,flags=re.IGNORECASE)
            if patt and matchobj:
                
                if(dtype1 == None):
                    dtype1 = ifc.GetDataType(d)
                dtype = ifc.GetDataType(d)
                if(not dtype == dtype1):
                     raise plugins.DatasetPluginException('all datasets must be the same type as the first one.')
                   
                if( dtype == '1d'):
                    val = ifc.GetData(d)[0]

                    if(is_min):
                        output_min = np.append(output_min,np.min(val))
                    if(is_max):
                        output_max = np.append(output_max,np.max(val))
                    if(is_mean):
                        output_mean = np.append(output_mean,np.mean(val))
                    if(is_std):
                        output_std = np.append(output_std,np.std(val))
                    if(is_first):
                        output_first = np.append(output_first,val[0])
                    if(is_last):
                        output_last = np.append(output_last,val[-1])
                        
                if(dtype == 'text' or dtype == 'datetime'):
                    val = ifc.GetData(d)
                    if(is_first):
                        output_first = np.append(output_first,val[0])
                    if(is_last):
                        output_last = np.append(output_last,val[-1])
                if(not (dtype == 'text' or dtype == 'datetime' or dtype == '1d')):
                    raise plugins.DatasetPluginException('Support only 1d, Text and datetime types')
                else:
                    if(not matchobj == None):
                        if(matchobj.lastindex > 0 ):
                            x = matchobj.group(1) #additional value from the widget
                            xoutput = np.append(xoutput,x) #numpy array
                        else:
                            x = None
                    
                        
        if(not val == []): #there is something in there        
            if(x):
                ifc.SetData("_output_x_",xoutput)
                ifc.TagDatasets('collector',['_output_x_'])

            if(dtype1 == '1d'):
                if(not output_min == []):
                    ifc.SetData("_output_min_",output_min)
                    ifc.TagDatasets('collector',['_output_min_'])
                if(not output_max == []):
                    ifc.SetData("_output_max_",output_max)
                    ifc.TagDatasets('collector',['_output_max_'])
                if(not output_mean == []):
                    ifc.SetData("_output_mean_",output_mean)
                    ifc.TagDatasets('collector',['_output_mean_'])
                if(not output_std == []):
                    ifc.SetData("_output_std_",output_std)
                    ifc.TagDatasets('collector',['_output_std_'])
                if(not output_first == []):
                    ifc.SetData("_output_first_",output_first)
                    ifc.TagDatasets('collector',['_output_first_'])
                if(not output_last == []):
                    ifc.SetData("_output_last_",output_last)       
                    ifc.TagDatasets('collector',['_output_last_'])
                    
            if(dtype1 == 'text'):
                if(not output_first == []):
                    ifc.SetDataText("_output_first_",output_first)
                    ifc.TagDatasets('collector',['_output_first_'])
                if(not output_last == []):
                    ifc.SetDataText("_output_last_",output_last)
                    ifc.TagDatasets('collector',['_output_last_'])
            if(dtype1 == 'datetime'):
                if(not output_first == []):
                    ifc.SetDataDateTime("_output_first_",output_first)
                    ifc.TagDatasets('collector',['_output_first_'])
                if(not output_last == []):
                    ifc.SetDataDateTime("_output_last_",output_last)   
                    ifc.TagDatasets('collector',['_output_last_'])

        
    def apply(self, ifc, fields):
        #ifc.SetVerbose(v=True)
        #ifc is actually explained in the veusz manual API
        is_widget = fields['is_widget']
        is_dataset = fields['is_dataset']
        if(is_widget):
            self.apply_to_widget(ifc,fields)
        if(is_dataset):
            self.apply_to_dataset(ifc,fields)
        

# add plugin classes to this list to get used
plugins.toolspluginregistry.append(SettingsCollectorPlugin)