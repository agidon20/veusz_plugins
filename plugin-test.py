# Copyright 2012 Dave Hughes.
#
# This file is part of veusz-plugins.
#
# veusz-plugins is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# veusz-plugins is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# veusz-plugins.  If not, see <http://www.gnu.org/licenses/>.

"""Plugin supporting import of SQLite query results into Veusz"""


import sqlite3
import veusz_plugins.sqlite_stored_procs as sp
from veusz_plugins.utils import sanitize_names#,unicode
import numpy as np
import re


class ImportDataset1D(object):
    """Return 1D dataset."""
    def __init__(self, name, data=None, serr=None, perr=None, nerr=None):
        """1D dataset
        name: name of dataset
        data: data in dataset: list of floats or numpy 1D array
        serr: (optional) symmetric errors on data: list or numpy array
        perr: (optional) positive errors on data: list or numpy array
        nerr: (optional) negative errors on data: list or numpy array

        If errors are returned for data implement serr or nerr and perr.
        nerr should be negative values if used.
        perr should be positive values if used.
        """

class ImportDataset2D(object):
    """Return 2D dataset."""
    def __init__(self, name, data, rangex=None, rangey=None):
        """2D dataset.
        name: name of dataset
        data: 2D numpy array of values or list of lists of floats
        rangex: optional tuple with X range of data (min, max)
        rangey: optional tuple with Y range of data (min, max)
        """

class ImportDatasetText(object):
    """Return a text dataset (only available in Veusz 1.9 or greater)."""
    def __init__(self, name, data):
        """A text dataset
        name: name of dataset
        data: data in dataset: list of strings
        """

class ImportPluginParams(object):
    """Parameters to plugin are passed in this object."""
    def __init__(self, filename, encoding, field_results):
        self.filename = filename
        self.encoding = encoding
        self.field_results = field_results

    def openFileWithEncoding(self):
        """Helper to open filename but respecting encoding."""
        
class Field(object):
    """A class to represent an input field on the dialog or command line."""
    def __init__(self, name, descr=None, default=None):
        """name: name of field
        descr: description to show to user
        default: default value."""


class ImportField(Field):
    """dummy class"""


class FieldBool(ImportField):
    """A check box on the dialog."""

class FieldText(ImportField):
    """Text entry on the dialog."""

class FieldFloat(ImportField):
    """Enter a floating point number."""

class FieldCombo(ImportField):
    """Drop-down combobox on dialog."""
    def __init__(self, name, descr=None, default=None, items=(),
                 editable=True):
        """name: name of field
        descr: description to show to user
        default: default value
        items: items in drop-down box
        editable: whether user can enter their own value."""
        
        
        
#data contains two columns, one name and the other comma separated values


query = "SELECT 'ap0>300um' as dist2soma1, arr(heights,0) as heights1 FROM bAPDendStep_Properties_agg_vertical where spike_num == 0 and dist2soma >300 \
;[field]:SELECT 'ap_max>300um' as dist2soma2, arr_max(heights) as heights2 FROM bAPDendStep_Properties_agg_vertical where spike_num == 0 and dist2soma >300;"
query ="{sweet}:[field]:SELECT dend_id || '_' || state_id as id, heights, i_dends FROM bAPDendStep_Properties_agg_vertical where spike_num == 0;\
SELECT arr(heights,0) as 'ap0_gt_300um' FROM bAPDendStep_Properties_agg_vertical where spike_num == 0 and dist2soma >300;\
SELECT arr_max(heights) as 'ap_max_lt_300um' FROM bAPDendStep_Properties_agg_vertical where spike_num == 0 and dist2soma <300;\
SELECT arr(heights,0) as 'ap0_gt_300um' FROM bAPDendStep_Properties_agg_vertical where spike_num == 0 and dist2soma >300;\
SELECT arr_max(heights) as 'ap_max_lt_300um' FROM bAPDendStep_Properties_agg_vertical where spike_num == 0 and dist2soma <300;\
"

query = "Select 'all',group_concat(height) as height, group_concat(x) as x from (\nSELECT dendriteid, arr_norm(height,-1) as height, arr_norm(id_,-2) as x FROM dAP_properties_agg)\nUNION\nSELECT dendriteid, height as height, id_ as x FROM dAP_properties_agg"


class p(object):
    
    class field(object):
        def __init__(self):
            self.query = query;
            
            
        def get(self,s):
            return self.query;
    
    field_results = field()
    filename = 'C:/Users/agidon20/OneDrive - charite.de/Human/database/data/Human.sqlite'
    def __init__(self):
        self.field_results = self.field()
        self.filename = 'C:/Users/agidon20/OneDrive - charite.de/Human/database/data/Human.sqlite'




# We can only iterate through the cursor once (standard forward-only
# semantics) so here we convert the query result to a list for further
# processing
class ImportPluginSQLite(object):
    """A plugin supporting SQLite databases"""

    name = 'SQLite import'
    author = 'Dave Hughes <dave@waveform.org.uk>'
    description = 'Reads data from queries against an SQLite database'
    arr_queries = ""
    
    def __init__(self):
        self.name = "SQlite import"
        
    def doImport(self,params):
        
        field_patt = "\[([^)]*)\]:"
        query_title_patt = "{([^)]*)}:" 
        conn = sqlite3.connect(params.filename)
        sp.register(conn)        
        cursor = conn.cursor()

        orig_str_queries = params.field_results.get('query')
        matchobj = re.search(query_title_patt,orig_str_queries,flags=re.IGNORECASE)      
        if(matchobj == None):  
            _query_ = "_query_"
            str_queries = orig_str_queries
        else:
            _query_ = matchobj.group(1)
            str_queries = re.sub(query_title_patt,"",orig_str_queries ,flags=re.IGNORECASE)
        
        arr_queries = str_queries.split(";")
        arr_queries = [ x.strip() for x in arr_queries] #clean the list
        arr_queries = [ x for x in arr_queries if (x != '')] #clean the list
        arr_queries = [ x for x in arr_queries if (x)] #clean the list
        
       

        
        result = []
        result = result + [ImportDatasetText(_query_, data=[orig_str_queries ])]

        for (i,q) in enumerate(arr_queries):
            matchobj = re.search(field_patt,q,flags=re.IGNORECASE)  
            if(matchobj == None):                
                cursor.execute(q)
                result = result + self.doImport_columns_as_arrays(params, cursor)
            else:
                field_name = matchobj.group(1)
                if(field_name[0:3] == 'col'):
                    q_ = re.sub(field_patt,"",q,flags=re.IGNORECASE)
                    cursor.execute(q_)
                    result = result + self.doImport_columns_as_arrays(params, cursor)
                elif(field_name[0:3] == 'fie'):
                    q_ = re.sub(field_patt,"",q,flags=re.IGNORECASE)
                    cursor.execute(q_)
                    result = result + self.doImport_fields_as_arrays( params, cursor)
            result = result + [ImportDatasetText(_query_ + '[' + str(i) + ']', data=[q])]
        return result
        
        
    def doImport_columns_as_arrays(self, params, cursor):       
        # We can only iterate through the cursor once (standard forward-only
        # semantics) so here we convert the query result to a list for further
        # processing
        data = [row for row in cursor]
        # Transpose the data from a list of row-tuples to a list of columns
        data = [
            [row[i] for row in data]
            for i, col in enumerate(cursor.description)]
        # Figure out the dataset name and type for each column
        names = sanitize_names(col[0] for col in cursor.description)
        classes = [
            ImportDatasetText if any(isinstance(value, str) for value in column) else ImportDataset1D
            for column in data]
        result = []
        for (name, cls, column) in zip(names, classes, data):
            if cls is ImportDataset1D:
                result.append(ImportDataset1D(
                    name, data=[
                        # Import NULL values as NaN in numeric datasets
                        float('NaN') if value is None else float(value)
                        for value in column]))
            else:
                result.append(ImportDatasetText(
                    name, data=[
                        # Import NULL values as blank strings in text datasets
                        '' if value is None else value
                        for value in column]))
        return result
    
    
    def doImport_fields_as_arrays(self, params, cursor):
        # We can only iterate through the cursor once (standard forward-only
        # semantics) so here we convert the query result to a list for further
        # processing
        data = [row for row in cursor]
        # Transpose the data from a list of row-tuples to a list of columns
        data = [
            [row[i] for row in data]
            for i, col in enumerate(cursor.description)]
        # Figure out the dataset name and type for each column
        # firs column must contain all the names for the arrays.
        names = sanitize_names('_' + str(name) for name in data[0])
        result = []

        for (i,desc) in enumerate(cursor.description[1:]):
            prefix = desc[0];
            for (name, d) in zip(names, data[i+1]): 
                csv = np.array(list(map(float,d.split(','))))
                result.append(ImportDataset1D(
                        prefix + name, data=[
                            # Import NULL values as NaN in numeric datasets
                            float('NaN') if value is None else float(value)
                            for value in csv]))
        #finally keep the query in another variable.


        return result


params = p();
test = ImportPluginSQLite();
results = test.doImport(params)
#print (results)
