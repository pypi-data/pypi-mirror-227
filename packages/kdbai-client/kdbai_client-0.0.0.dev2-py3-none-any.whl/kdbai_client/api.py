from __future__ import annotations

from datetime import datetime
import json
import os
from typing import Any, Dict, List, Optional
from urllib import parse, request
import urllib.error

import pandas as pd


os.environ['QARGS'] = '--unlicensed'
import pykx as kx  # noqa: E402


# Minimum datetime/timestmp supported by q/kdb+
MIN_DATETIME = datetime(1707, 9, 22, 0, 12, 43, 145224)
# Maximum datetime/timestamp supported by q/kdb+
MAX_DATETIME = datetime(2262, 4, 11, 23, 47, 16, 854775)


_qtype_to_dtype = dict(
    boolean='bool',
    guid='str',
    byte='uint8',
    short='int16',
    int='int32',
    long='int64',
    real='float32',
    float='float64',
    string='bytes',
    symbol='str',
    timestamp='datetime64[ns]',
    month='datetime64[M]',
    date='datetime64[D]',
    timespan='timedelta64[ns]',
    minute='timedelta64[m]',
    second='timedelta64[s]',
    time='timedelta64[ms]',
)
_dtype_to_qtype = {v: k for k, v in _qtype_to_dtype.items()}
for key in list(_qtype_to_dtype.keys()):
    _qtype_to_dtype[f'{key}s'] = _qtype_to_dtype[key]


class Session(object):
    """Session represents a connection to a KDB.AI instance."""

    PROTOCOL  = 'https'
    HOST   = 'localhost'
    PORT   = 443

    CONFIG_PATH = '/api/v1/config/table'
    CREATE_PATH = '/api/v1/config/table/%s'
    DROP_PATH   = '/api/v1/config/table/%s'
    QUERY_PATH  = '/api/v1/data'
    INSERT_PATH = '/api/v1/insert'
    SEARCH_PATH = '/api/v1/kxi/search'

    def __init__(
        self,
        api_key = None,
        *,
        host: str = HOST,
        port: int = PORT,
        protocol: str = PROTOCOL,
    ):
        """Create a REST API connection to a KDB.AI host.

        Args:
            api_key (str): API Key to be used for authentication.
            host (str): Host name or IP address of the KDB.AI server to connect.
            port (int): REST API gateway port on KDB.AI server.
            protocol (str): `http` or `https`.

        Example:
            Open a session on KDB.AI Cloud with an api key:

            ```python
            session = Session(api_key='YOUR_API_KEY')
            ```

            Open a session on a custom KDB.AI instance on http://localhost:8082:

            ```python
            session = kdbai.Session(host='localhost', port=8082, protocol='http')
            ```
        """
        self.api_key = api_key
        self.host = host
        self.port = port
        self.protocol = protocol

    def config(self) -> Dict:
        """Retrieve the server configuration.

        Returns:
                A `dict` containing all metadata of the KDB.AI instance.
        """
        try:
            return self._config()
        except Exception:
            raise KDBAIException('Failed to retrieve the configuration.')

    def list(self) -> List[str]:
        """Retrieve the list of tables.

        Returns:
            A list of strings with the names of the existing tables.

        Example:
            ```python
            table.list()
            ["trade", "quote"]
            ```
        """
        try:
            return self._list()
        except Exception:
            raise KDBAIException('Failed to retrieve the list of tables.')

    def table(self, name: str) -> Table:
        """Retrieve an existing table.

        Args:
            name (str): Name of the table to retrieve.

        Returns:
                A `Table` object representing the KDB.AI table.

        Example:
            Retrieve the `trade` table:

            ```python
            table = session.table("trade")
            ```
        """
        return Table(name=name, session=self)

    def create_table(self, name, schema):
        """Create a table with a schema

        Args:
            name (str): Name of the table to create.
            schema (dict): Schema of the table to create. This schema must contain a list of columns. All columns
                must have either a `pytype` or a `qtype` specified except the column of vectors.
                One column of vector embeddings may also have a `vectorIndex` attribute with the configuration of the
                index for similarity search - this column is implicitly an array of `float32`.

        Raises:
            KDBAIException: Raised when a error happens during the creation of the table.

        Example:
            ```python
            schema = {'columns': [{'name': 'id', 'pytype': 'str'},
                                  {'name': 'tag', 'pytype': 'str'},
                                  {'name': 'text', 'pytype': 'bytes'},
                                  {'name': 'embeddings',
                                   'vectorIndex': {'dims': 1536, 'metric': 'L2', 'type': 'flat'}}]}
            ```
        """
        try:
            schema, use_time_sym_columns = self._format_schema_to_q(schema)
            self._create_table(name, schema)

            # TODO: Improve this, needs to give kdbai-db some time to create the table
            import time
            time.sleep(5)

            return Table(name=name, session=self, use_time_sym_columns=use_time_sym_columns)
        except urllib.error.HTTPError as e:
            raise KDBAIException(f'Failed to create the new table named {name} with schema {schema}.', e=e)
        except KDBAIException as e:
            raise e
        except Exception:
            raise KDBAIException(f'Failed to create the new table named {name} with schema {schema}.')

    def _format_schema_to_q(self, schema):
        out = {}
        out['type'] = 'splayed'
        use_time_sym_columns = False
        if schema['columns'][0]['name'] == 'time' \
            and schema['columns'][1]['name'] == 'sym':
            use_time_sym_columns = True
            out['columns'] = []
        else:
            out['columns'] = [dict(name='time', type='timespan'),
                              dict(name='sym', type='symbol', attrMem='grouped')]
            use_time_sym_columns = False
        for column in schema['columns']:
            out_col = dict(name=column['name'])
            if 'qtype' in column:
                out_col['type'] = column['qtype']
            elif 'pytype' in column:
                out_col['type'] = _dtype_to_qtype[column['pytype']]
            else:
                if 'vectorIndex' not in column:
                    raise KDBAIException('Invalid column, missing `pytype` or `qtype`.')
            if 'vectorIndex' in column:
                out_col['vectorIndex'] = column['vectorIndex']
                out_col['type'] = 'reals'
            if column['name'] == 'sym':
                out_col['attrMem'] = 'grouped'
            out['columns'].append(out_col)
        return out, use_time_sym_columns

    def _create_table(self, name, schema):
        body = self._rest_post_json(self.CREATE_PATH % name, schema)
        return self._create_table_status(body)

    def _create_table_status(self, body):
        if 'message' in body and body['message'] == 'success':
            return True
        else:
            raise KDBAIException(body)

    def _config(self):
        return self._rest_get(Session.CONFIG_PATH)

    def _list(self):
        config = self._config()
        tables = list(config.keys())
        return tables

    def _rest_get(self, path):
        url = parse.urljoin(f'{self.protocol}://{self.host}:{self.port}', path)
        headers = {}
        if self.api_key is not None:
            headers['Authorization'] = f'Key {self.api_key}'
        req = request.Request(url, headers=headers)
        res = request.urlopen(req)
        body = json.loads(res.read().decode('utf-8'))
        return body

    def _rest_post_json(self, path, data):
        url = parse.urljoin(f'{self.protocol}://{self.host}:{self.port}', path)
        headers = {'Content-type': 'application/json'}
        if self.api_key is not None:
            headers['Authorization'] = f'Key {self.api_key}'
        req = request.Request(url,
                              method='POST',
                              headers=headers,
                              data=json.dumps(data).encode('utf-8'))
        res = request.urlopen(req)
        body = json.loads(res.read().decode('utf-8'))
        return body

    def _rest_post_json_to_qipc(self, path, data):
        url = parse.urljoin(f'{self.protocol}://{self.host}:{self.port}', path)
        headers = {'Content-type': 'application/json',
                   'Accept': 'application/octet-stream'}
        if self.api_key is not None:
            headers['Authorization'] = f'Key {self.api_key}'
        req = request.Request(url,
                              method='POST',
                              headers=headers,
                              data=json.dumps(data).encode('utf-8'))
        res = request.urlopen(req)
        res = kx._wrappers.deserialize(res.read())._unlicensed_getitem(1)
        return self._format_qipc_result(res)

    def _rest_delete(self, path):
        url = parse.urljoin(f'{self.protocol}://{self.host}:{self.port}', path)
        headers = {'Accept': 'application/json'}
        if self.api_key is not None:
            headers['Authorization'] = f'Key {self.api_key}'
        req = request.Request(url, method='DELETE', headers=headers)
        res = request.urlopen(req)
        body = json.loads(res.read().decode('utf-8'))
        return body

    def _format_qipc_result(self, res):
        if type(res) is kx.Table:
            return res.pd()
        elif isinstance(res, kx.Vector):
            result = []
            for i in range(len(res)):
                result.append(res._unlicensed_getitem(i).pd())
            return result
        else:
            raise KDBAIException('Not implemented.')

    def _rest_post_qipc(self, path, table, data):
        url = parse.urljoin(f'{self.protocol}://{self.host}:{self.port}', path)
        headers = {'Content-type': 'application/octet-stream'}
        if self.api_key is not None:
            headers['Authorization'] = f'Key {self.api_key}'
        req = request.Request(url,
                              method='POST',
                              headers=headers,
                              data=kx._wrappers._to_bytes(6, kx.toq([table, data]), 1)[1])
        request.urlopen(req)
        return True


class Table:
    """KDB.AI table."""

    def __init__(self, name: str, *, session: Session, **kwargs):
        """kdbai_client.Table

        Table object shall be created with `session.create_table(...)` or retrieved with `session.table(...)`.
        This constructor shall not be used directly.
        """
        self.name = name
        self.session = session

        self._use_time_sym_columns = None
        if 'use_time_sym_columns' in kwargs:
            self._use_time_sym_columns = kwargs['use_time_sym_columns']

        try:
            tables = self.session._list()
        except urllib.error.HTTPError as e:
            raise KDBAIException('Failed to retrieve the list of tables.', e=e)
        except Exception:
            raise KDBAIException('Failed to retrieve the list of tables.')

        self._check_table_name(tables)

    def _check_table_name(self, tables: list):
        if self.name not in tables:
            raise KDBAIException(f'Failed to retrieve the table named: {self.name}.')
        return True

    def schema(self) -> Dict:
        """Retrieve the schema of the table.

        Raises:
            KDBAIException: Raised when an error occurs during schema retrieval

        Returns:
            A `dict` containing the table name
                and the list of column names and appropriate numpy datatypes.

        Example:
            ```python
            table.schema()

            {'columns': [{'name': 'id', 'pytype': 'str', 'qtype': 'symbol'},
                          {'name': 'tag', 'pytype': 'str', 'qtype': 'symbol'},
                          {'name': 'text', 'pytype': 'bytes', 'qtype': 'string'},
                          {'name': 'embeddings',
                           'pytype': 'float32',
                           'qtype': 'reals',
                           'vectorIndex': {'dims': 1536, 'metric': 'L2', 'type': 'flat'}}]}
            ```
        """
        try:
            config = self.session._config()
            schema = config[self.name]
            return self._format_schema_to_py(schema)
        except Exception:
            raise KDBAIException(f'Failed to retrieve the schema of table named: {self.name}.')


    def _format_schema_to_py(self, schema: dict):
        schema.pop('type')
        if self._use_time_sym_columns is False:
            schema['columns'] = schema['columns'][2:]
        for column in schema['columns']:
            column['qtype'] = column.pop('type')
            column['pytype'] = self._translate_qtype(column['qtype'])
            if 'attrMem' in column:
                column.pop('attrMem')
        return schema

    def _translate_qtype(self, qtype: int):
        return _qtype_to_dtype.get(qtype, 'object')

    def insert(self, data):
        """Insert data into the table.

        Args:
            data (DataFrame): Pandas dataframe with column names/types matching the target table.

        Raises:
            KDBAIException: Raised when an error occurs during insert.
        """
        try:
            return self.session._rest_post_qipc(Session.INSERT_PATH, self.name, data)
        except urllib.error.HTTPError as e:
            raise KDBAIException(f'Failed to insert data in table named: {self.name}.', e=e)
        except Exception:
            raise KDBAIException(f'Failed to insert data in table named: {self.name}.')

    def query(
        self,
        filter: Optional[List[list]] = None,
        group_by: Optional[str] = None,
        aggs: Optional[List[list]] = None,
        sort_by: Optional[List[str]] = None,
        fill: Optional[str] = None,
        *,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        input_timezone: Optional[str] = None,
        output_timezone: Optional[str] = None,
    ) -> pd.DataFrame:
        """Query data from the table.

        Args:
            filter: A list of filter conditions as triplets in the following format:
                `[['function', 'column name', 'parameter'], ... ]`
                See all filter operators here:
                https://code.kx.com/insights/1.6/api/database/query/get-data.html#supported-filter-functions
            group_by: A list of column names to use for group by.
            aggs: Either a list of column names to select or a list of aggregations to perform as a
                list of triplers in the following form:
                `[['output_column', 'agg_function', 'input_column'], ... ]`
                See all aggregation functions here:
                https://code.kx.com/insights/1.6/api/database/query/get-data.html#supported-aggregations
            sort_by: List of column names to sort on.
            fill: This defines how to handle null values. This should be either `'forward'` or `'zero'` or `None`.
            start_time: Start of the time interval to query as an ISO 8601 formatted string
                (`start_time` included in the time range).
                `kdbai_client.MIN_DATETIME` corresponds to the minimum datetime supported.
            end_time: End of the time interval to query as an ISO 8601 formatted string
                (`end_time` excluded in the time range).
                `kdbai_client.MAX_DATETIME` corresponds to the maximum datetime supported
            input_timezone: The timezones of start_time and end_time, default is UTC if not
                specified.
            output_timezone: The timezone of output timestamp columns, default is UTC if not
                specified.

        Examples:
            ```python
            table.query(group_by = ['sensorID', 'qual'])
            table.query(filter = [['within', 'qual', [0, 2]]])
            table.query(start_time='2000-05-26', end_time='2000-05-27')
            ```

        Raises:
            KDBAIException: Raised when an error occurs during query.

        Returns:
            Pandas dataframe with the query results.
        """
        params: Dict[str, Any] = {"table": self.name}

        if start_time is not None and isinstance(start_time, datetime):
            start_time = start_time.isoformat()
        if end_time is not None and isinstance(end_time, datetime):
            end_time = end_time.isoformat()

        optional_params_map = (
            ("startTS", start_time),
            ("endTS", end_time),
            ("inputTZ", input_timezone),
            ("outputTZ", output_timezone),
            ("filter", filter),
            ("groupBy", group_by),
            ("agg", aggs),
            ("fill", fill),
            ("sortCols", sort_by),
        )
        for key, value in optional_params_map:
            if value is not None:
                params[key] = value

        try:
            out = self.session._rest_post_json_to_qipc(Session.QUERY_PATH, params)
            if not self._use_time_sym_columns:
                if self._use_time_sym_columns is None:
                    if not out[['time', 'sym']].dropna().empty:
                        self._use_time_sym_columns = True
                        return out
                out.drop(['time', 'sym'], axis=1, inplace=True)
            return out
        except urllib.error.HTTPError as e:
            raise KDBAIException(
                f'Failed to process the query {params} on table named: {self.name}.', e=e)
        except Exception:
            raise KDBAIException(
                f'Failed to process the query {params} on table named: {self.name}.')

    def search(
        self,
        vectors: List[List],
        n: int = 1,
        distances: Optional[str] = None,
        filter: Optional[List[list]] = None,
        group_by: Optional[str] = None,
        aggs: Optional[List[list]] = None,
        sort_by: Optional[List[str]] = None,
        *,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        input_timezone: Optional[str] = None,
        output_timezone: Optional[str] = None,
    ) -> List[pd.DataFrame]:
        """Perform similarity search on the table.

        Args:
            vectors (list of lists): Query vectors for the search.
            n (int): Number of neighbours to return.
            distances (str): Optional name of a column to output the distances.
                If not specified, __nn_distance
                will be added as an extra column to the result table.
            filter: A list of filter conditions as triplets in the following format:
                `[['function', 'column name', 'parameter'], ... ]`
                See all filter operators here:
                https://code.kx.com/insights/1.6/api/database/query/get-data.html#supported-filter-functions
            group_by: A list of column names to use for group by.
            aggs: Either a list of column names to select or a list of aggregations to perform as a
                list of triplers in the following form:
                `[['output_column', 'agg_function', 'input_column'], ... ]`
                See all aggregation functions here:
                https://code.kx.com/insights/1.6/api/database/query/get-data.html#supported-aggregations
            sort_by: List of column names to sort on.
            start_time: Start of the time interval to query as an ISO 8601 formatted string
                (`start_time` included in the time range).
                `kdbai_client.MIN_DATETIME` corresponds to the minimum datetime supported.
            end_time: End of the time interval to query as an ISO 8601 formatted string
                (`end_time` excluded in the time range).
                `kdbai_client.MAX_DATETIME` corresponds to the maximum datetime supported
            input_timezone: The timezones of start_time and end_time, default is UTC if not
                specified.
            output_timezone: The timezone of output timestamp columns, default is UTC if not
                specified.

        Examples:
            ```python
            #Find the closest neighbour of a single query vector
            table.search(vectors=[[0,0,0,0,0,0,0,0,0,0]], n=1)

            #Find the 3 closest neighbours of 2 query vectors
            table.search(vectors=[[0,0,0,0,0,0,0,0,0,0], [1,1,1,1,1,1,1,1,1,1]], n=3)
            ```

        Raises:
            KDBAIException: Raised when an error occurs during search.

        Returns:
            List of Pandas dataframes with one dataframe of matching neighbors for each query vector.
        """
        params: Dict[str, Any] = {"table": self.name}

        if start_time is not None and isinstance(start_time, datetime):
            start_time = start_time.isoformat()
        if end_time is not None and isinstance(end_time, datetime):
            end_time = end_time.isoformat()

        params['vectors'] = vectors
        params['n'] = n

        optional_params_map = (
            ("distances", distances),
            ("startTS", start_time),
            ("endTS", end_time),
            ("inputTZ", input_timezone),
            ("outputTZ", output_timezone),
            ("filter", filter),
            ("groupBy", group_by),
            ("agg", aggs),
            ("sortCols", sort_by),
        )
        for key, value in optional_params_map:
            if value is not None:
                params[key] = value # type: ignore

        try:
            out = self.session._rest_post_json_to_qipc(Session.SEARCH_PATH, params)
            if not self._use_time_sym_columns:
                if self._use_time_sym_columns is None:
                    for df in out:
                        if not df[['time', 'sym']].dropna().empty:
                            self._use_time_sym_columns = True
                            return out
                for df in out:
                    df.drop(['time', 'sym'], axis=1, inplace=True)
            return out
        except urllib.error.HTTPError as e:
            raise KDBAIException(
                f'Failed to process the query {params} on table named: {self.name}.', e=e)
        except Exception:
            raise KDBAIException(
                f'Failed to process the query {params} on table named: {self.name}.')

    def drop(self):
        """Drop the table.

        Raises:
            KDBAIException: Raised when an error occurs during the table deletion.
        """
        try:
            body = self.session._rest_delete(Session.DROP_PATH % self.name)
            return self._drop_status(body)
        except urllib.error.HTTPError as e:
            raise KDBAIException(
                f'Failed to drop the table named: {self.name}.', e=e)
        except KDBAIException as e:
            raise e
        except Exception:
            raise KDBAIException(
                f'Failed to drop the table named: {self.name}.')

    def _drop_status(self, body):
        if 'message' in body and body['message'] == 'success':
            return True
        else:
            raise KDBAIException(body)

class KDBAIException(Exception):
    """KDB.AI exception."""

    def __init__(self, msg, e = None, *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
        self.e = e
        if self.e is not None:
            reason = None
            try:
                if (self.e.getcode() == 400
                    and self.e.headers.get('Content-type') == 'application/octet-stream'):
                    reason = \
                        kx._wrappers.deserialize(self.e.fp.read()).py()[0]['ai'].decode('utf-8')
                else:
                    reason = json.loads(self.e.fp.read().decode('utf-8'))
            except Exception:
                reason = self.e.fp.read().decode('utf-8')
            self.code = self.e.code
            if reason is not None:
                self.text = f'{msg[:-1]}, because of: {reason}.'
            self.args = (self.text,)
