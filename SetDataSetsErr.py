import veusz.plugins as plugins
import numpy as np
import re

class SetDataSetErrPlugin(plugins.DatasetPlugin):
    """Dataset plugin to shift a dataset."""

    # tuple of strings to build position on menu
    menu = ('DataSets set errors',)

    # internal name for reusing plugin later
    name = 'DataSetSetErr'

    # string which appears in status bar
    description_short = 'Set an error to the database based on an expression'
    
    # string goes in dialog box
    description_full = ('Set an error to the database based on an expression')
    
    def __init__(self):
        """Define input fields for plugin."""
        self.fields = [
            plugins.FieldDatasetMulti('dsmulti', 'add here databases', default='.*'),
            plugins.FieldText('exp', 'expression to apply --> symmetric error', default='1'),            
            ]
        print('here')

    def getDatasets(self, fields):
#       """Get output datasets."""
        self.dsout = []
        for d in fields['dsmulti']:
            if d.strip() != '':
                self.dsout.append( plugins.Dataset1D(d.strip()) )
        if len(self.dsout) == 0:
            raise plugins.DatasetPluginException('Needs at least one output dataset')

        return self.dsout
#        

    def updateDatasets(self, fields, helper):
        """Do shifting of dataset.
        This function should *update* the dataset(s) returned by getDatasets
        """
        # get the input dataset - helper provides methods for getting other
        # datasets from Veusz
        
        if(fields['exp'] == ''):
            math_exp = '1'
        else:
            math_exp = fields['exp'].replace('data','ds.data')
        for ds in self.dsout:
            err = eval(math_exp,locals(),globals()) * ds.data
#                ds.update(data=ds.data, serr=err,perr=ds.perr, nerr=ds.nerr)
            ds.update(data=ds.data,serr = err, perr = ds.perr, nerr=ds.nerr)
        
# add plugin classes to this list to get used
plugins.datasetpluginregistry.append(SetDataSetErrPlugin)