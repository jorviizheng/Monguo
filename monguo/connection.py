# -*- coding: utf-8 -*-

import motor
from error import *

class Connection(object):

    DEFAULT_CONNECTION_NAME = 'default'

    _connections        = {}
    _default_connection = None
    _default_db         = None

    @classmethod
    def connect(
            cls, db_name=None, 
            connection_name=None, 
            replica_set=False, *args, **kwargs):

        if connection_name is None:
            connection_name = Connection.DEFAULT_CONNECTION_NAME

        Connection.disconnect(connection_name)

        client_class = (motor.MotorReplicaSetClient if replica_set else 
                        motor.MotorClient)
        try:
            connection = client_class(*args, **kwargs).open_sync()
        except Exception, e:
            raise ConnectionErroe('Cant\'t connect to mongdb.')

        Connection._connections[connection_name] = connection

        Connection._default_connection = connection_name
        Connection._default_db = db_name

    @classmethod
    def disconnect(cls, connection_name=None):
        if connection_name is None:
            connection_name = Connection._default_connection
            Connection._default_connection = None

        if connection_name in Connection._connections:
            Connection._connections[connection_name].close()
            del Connection._connections[connection_name]
            del Connection._connection_setting[connection_name]

    @classmethod
    def get_connection(cls, connection_name=None):
        if connection_name is None:
            connection_name = Connection._default_connection

        return (None if connection_name not in Connection._connections else 
                Connection._connections[connection_name])

    @classmethod
    def get_db(cls, connection_name=None, db_name=None):
        connection = Connection.get_connection(connection_name)
        if connection is None:
            raise ConnectionError('mongdb has not been connected!')

        if db_name is None:
            db_name = Connection._default_db
        if db_name is None:
            raise ConnectionError('please set a database first!')

        return connection[db_name]

    @classmethod
    def switch_connection(cls, connection_name):
        if connection_name not in Connection._connections:
            return False

        Connection._default_connection = connection_name
        return True

    @classmethod
    def switch_db(cls, db_name):
        Connection._default_db = db_name
