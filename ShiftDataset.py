import veusz.plugins as plugins

class ShiftDatasetPlugin(plugins.DatasetPlugin):
    """Dataset plugin to shift a dataset."""

    # tuple of strings to build position on menu
    menu = ('Shift by constant',)

    # internal name for reusing plugin later
    name = 'ShiftConst'

    # string which appears in status bar
    description_short = 'Shift dataset by a constant'
    
    # string goes in dialog box
    description_full = ('Shift a dataset by a constant. '
                        'This text goes into the dialog box.')
    
    def __init__(self):
        """Define input fields for plugin."""
        self.fields = [
            plugins.FieldDataset('ds_in', 'Input dataset'),
            plugins.FieldFloat('value', 'Value', default=0.),
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
        ds_in = helper.getDataset(fields['ds_in'])
        # get the value to add
        v = fields['value']

        # just to be explicit
        newdata = ds_in.data + v

        # update output dataset with input dataset (plus value) and errorbars
        self.ds_out.update(data=newdata,
                           serr=ds_in.serr, perr=ds_in.perr, nerr=ds_in.nerr)

# add plugin classes to this list to get used
plugins.datasetpluginregistry.append(ShiftDatasetPlugin)