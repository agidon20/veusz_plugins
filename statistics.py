import sys

import veusz.plugins as plugins
import numpy as np
import scipy.stats as st

class mystats(plugins.DatasetPlugin):
    """Dataset plugin to shift a dataset."""

    # tuple of strings to build position on menu
    menu = ('stats',)

    # internal name for reusing plugin later
    name = 'stats'

    # string which appears in status bar
    description_short = 'Get dataset corresponding to the mean of a number of datasets'
    
    # string goes in dialog box
    description_full = ('Get dataset corresponding to the mean of a number of datasets')
    
    def __init__(self):
        """Define input fields for plugin."""
        self.fields = [
            plugins.FieldDatasetMulti('ds_in', 'Input dataset'),
            plugins.FieldDataset('ds_out', 'Output dataset name'),
            ]

    def getDatasets(self, fields):
        """Returns single output dataset (self.dsout).
        This method should return a list of Dataset objects, which can include
        Dataset1D, Dataset2D and DatasetText
        """

        # raise DatasetPluginException if there are errors
        if fields['ds_out'] == '':
            raise plugins.DatasetPluginException('Invalid output dataset name')

        # make a new dataset with name in fields['ds_out']
        self.ds_out = plugins.Dataset1D(fields['ds_out'])

        # return list of datasets
        return [self.ds_out]

    def updateDatasets(self, fields, helper):
        """Do shifting of dataset.
        This function should *update* the dataset(s) returned by getDatasets
        """

        # get the input dataset - helper provides methods for getting other
        # datasets from Veusz
        
        ds_func = np.array(st.gmean(fields['ds_in']))
        ds_errorbar = np.array(st.gmean(fields['ds_in']))
        


        # just to be explicit
        #newdata = ds_mean

        # update output dataset with input dataset (plus value) and errorbars
#        self.ds_out.update(data=ds_mean,
#                           serr=ds_in.serr, perr=ds_in.perr, nerr=ds_in.nerr)
        self.ds_out.update(data=ds_func, serr=ds_errorbar)

# add plugin classes to this list to get used
plugins.datasetpluginregistry.append(mystats)