# vim: set et sw=4 sts=4:

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

from __future__ import (
    unicode_literals,
    print_function,
    absolute_import,
    division,
    )

from veusz.plugins import (
    ImportPlugin,
    ImportDataset1D,
    ImportDatasetText,
    FieldText,
    importpluginregistry,
    )

import sqlite3
import veusz.plugins.sqlite_stored_procs as sp
from veusz.plugins.utils import sanitize_names
import numpy as np
import re

#data contains two columns, one name and the other comma separated values


class ImportPluginSQLite(ImportPlugin):
    """A plugin supporting SQLite databases"""

    name = 'SQLite import row wise'
    author = 'Albert Gidon based on Dave Hughes <dave@waveform.org.uk>'
    description = 'Reads data from queries against an SQLite database with two columns (names, data) data is comma separated values string'

    def __init__(self):
        ImportPlugin.__init__(self)
        self.fields = [
            FieldText('query', descr='SQL query'),
        ]

    def getPreview(self, params):
        try:
            conn = sqlite3.connect(params.filename)
            sp.register(conn)
            cursor = conn.cursor()
            # List the tables in the database
            try:
                cursor.execute("""\
                    SELECT name
                    FROM sqlite_master
                    WHERE type = 'table' OR type == 'view'
                    ORDER BY name""")
                result = 'Database contains the following tables:\n'
                result += '\n'.join(row[0] for row in cursor)
            finally:
                conn.rollback()
            # Test the user's query (if any)
            query = params.field_results.get('query')
            if query:
                try:
                    cursor.execute(query)
                finally:
                    conn.rollback()
            return (result, True)
        except sqlite3.Error as exc:
            return (unicode(exc), False)
   
       
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
                        for value in column], serr=np.ones_like(column) ) )
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
                #bacause all arrays are represented as strings, if there is a scalar, change it to string as well.
                if(not isinstance(d,str)):
                    d = str(d)
                csv = np.array(list(map(float,d.split(','))))
                result.append(ImportDataset1D(
                        prefix + name, data=[
                            # Import NULL values as NaN in numeric datasets
                            float('NaN') if value is None else float(value)
                            for value in csv], serr=np.ones_like(csv)))
        #finally keep the query in another variable.


        return result

importpluginregistry.append(ImportPluginSQLite)



