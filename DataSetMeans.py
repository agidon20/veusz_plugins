import veusz.plugins as plugins
import numpy as np

class MeanDatasestPlugin(plugins.DatasetPlugin):
    """Dataset plugin to shift a dataset."""

    # tuple of strings to build position on menu
    menu = ('DataSets means',)

    # internal name for reusing plugin later
    name = 'DataSetMeans'

    # string which appears in status bar
    description_short = 'Get dataset corresponding to the mean of a number of datasets'
    
    # string goes in dialog box
    description_full = ('Get dataset corresponding to the mean of a number of datasets')
    
    def __init__(self):
        """Define input fields for plugin."""
        self.fields = [
            plugins.FieldDatasetMulti('ds_in', 'Input dataset'),
            plugins.FieldText('func', 'numpy function (e.g. mean, std)', default='mean'),
            plugins.FieldText('errorbar', 'numpy function (e.g. mean, std)', default='std'),            
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
        if(fields['func'] == ''):
            func = 'mean'
        else:
            func = fields['func']        
        
        if(fields['errorbar'] == ''):
            errorbar = 'std'
        else:
            errorbar = fields['errorbar']        
        
        ds_func = np.ndarray(0)
        ds_errorbar = np.ndarray(0)
        
        for d in fields['ds_in']:
            ds = helper.getDataset(d)
            data = ds.data[~np.isnan(ds.data)]
            md = eval('np.' + func + '(data)',locals(),globals())
            ds_func = np.append(ds_func,md)
            md = eval('np.' + errorbar + '(data)',locals(),globals())
            ds_errorbar = np.append(ds_errorbar,md)
             
            


        # just to be explicit
        #newdata = ds_mean

        # update output dataset with input dataset (plus value) and errorbars
#        self.ds_out.update(data=ds_mean,
#                           serr=ds_in.serr, perr=ds_in.perr, nerr=ds_in.nerr)
        self.ds_out.update(data=ds_func, serr=ds_errorbar)

# add plugin classes to this list to get used
plugins.datasetpluginregistry.append(MeanDatasestPlugin)