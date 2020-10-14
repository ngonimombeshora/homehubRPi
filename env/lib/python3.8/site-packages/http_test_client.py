from collections import namedtuple
import json
import logging
import re
import requests
import urllib
import six
import six.moves


class ClientError(Exception):
    def __init__(self, status_code, text):
        if not text:
            message = 'Status code %d' % status_code
        else:
            message = '%s (status code %d)' % (text, status_code)
        super(ClientError, self).__init__(message)
        self.status_code = status_code
        self.text = text


Response = namedtuple('Response', ['status_code', 'headers', 'text'])


PARAM_RE = re.compile(r'^/(?:[^{]+/)*\{(.+)\}$')


class ApiNamespace(object):
    def __init__(self, path, klass):
        self.path = path
        m = PARAM_RE.match(path)
        self.param = m.group(1) if m else None
        self.klass = klass

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.param:
            raise AttributeError()
        return self.klass(obj._client, obj._url + self.path)


class DummyTransport(object):
    '''
    Transport that just prints executed requests
    '''
    def request(self, url, method=None, headers=None, data=None, **kwargs):
        if data is not None:
            print '%s %s data=%s' % (method, url, json.dumps(data))
        else:
            print '%s %s' % (method, url)

        return Response(200, {}, '')


class HttpTransport(object):
    '''
    HTTP transport. Use base_url to specifying URL prefix (e.g. host/port)
    '''
    def __init__(self, base_url):
        super(HttpTransport, self).__init__()
        self._base_url = base_url
        self._session = requests.Session()

    def request(self, url, method=None, headers=None, data=None, **kwargs):
        request = requests.Request(
            url=self._base_url + url, method=method or 'GET',
            headers=headers or {},
            data=data,
            **kwargs
        )

        return self._session.send(self._session.prepare_request(request))


class Client(object):
    '''
    Top level API client object. Holds reference to transport and base url.
    Has cleanup API to allow resources to register cleanup callbacks.
    '''
    logger = logging.getLogger(__module__ + '.Client')

    def __init__(self, transport, url=''):
        """
        Args:
            transport  Instance HttpSession
            url        API URL to access a specific resource
        """
        self._transport = transport
        self._url = url
        self._cleanup = []

        self._client = self

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self._url)

    def add_cleanup(self, url, func):
        '''Add cleanup callback associated with given URL'''
        self._cleanup.append((url, func))

    def remove_cleanup(self, url):
        '''Remove cleanup callbacks associated with given URL'''
        self._cleanup = [(url1, func) for (url1, func) in self._cleanup
                         if url1 != url and not url1.startswith(url + '/')]

    def cleanup(self):
        '''Execute all cleanup callbacks'''
        for _, func in self._cleanup:
            func()
        self._cleanup = []

    def raw_request(self, url, method=None, headers=None, data=None, **kwargs):
        '''
        Send HTTP request through configured transport and return Response object
        '''
        if method is None:
            method = 'GET' if data is None else 'POST'

        url = self._url + url
        if data is not None:
            data = json.dumps(data)

        if headers is None:
            headers = {}

        headers['Content-Type'] = 'application/json'

        self._log_request(url, method=method, headers=headers, data=data)

        response = self._transport.request(
            url=url, method=method, headers=headers, data=data, **kwargs
        )

        self._log_response(response)

        return response

    def request(self, url, method=None, headers=None, data=None, **kwargs):
        '''Send HTTP request and return JSON response data'''
        response = self.raw_request(
            url, method=method, headers=headers, data=data, **kwargs
        )

        if response.status_code not in six.moves.range(200, 299):
            raise ClientError(response.status_code, response.text)

        return json.loads(response.text) if len(response.text) > 0 else None

    # compatibility with Api
    def _raw_request(self, *args, **kwargs):
        return super(Client, self).raw_request(*args, **kwargs)

    def _request(self, *args, **kwargs):
        return super(Client, self).request(*args, **kwargs)

    def _log_request(self, url, method, headers, data):
        """Log request"""
        s = '%s request to %s' % (method, url)
        if headers:
            s += ' headers=%s' % repr(headers)
        if data:
            s += ' body=%s' % data

        self.logger.debug('Sending %s', s)

    def _log_response(self, response):
        """Log response"""
        s = 'code=%d' % response.status_code
        if response.headers:
            s += ' headers=%s' % repr(response.headers)
        if response.text:
            s += ' body=%s' % response.text

        self.logger.debug('Got response %s', s)


class ApiMeta(type):
    def __new__(mcs, name, bases, attrs):
        params = {attr_name: attr_value
                  for attr_name, attr_value in attrs.iteritems()
                  if isinstance(attr_value, ApiNamespace) and attr_value.param}

        if len(params) > 1:
            raise ValueError('Multiple param APIs are not supported')
        elif len(params) == 1:
            param_api = params.values()[0]

            def getitem(self, param_value):
                return param_api.klass(
                    self._client, self._url + '/' + urllib.quote(param_value),
                )

            attrs['__getitem__'] = getitem

        return super(ApiMeta, mcs).__new__(mcs, name, bases, attrs)


class Api(object):
    '''
    Base class for all HTTP APIs. Maintains a client and base url.
    '''
    __metaclass__ = ApiMeta

    def __init__(self, client, url, **kwargs):
        """
        Args:
            session  Instance HttpSession
            url      API URL to access a specific resource
            kwargs   Additional properties to store
        """
        self._client = client
        self._url = url
        for k, v in six.iteritems(kwargs):
            setattr(self, k, v)

    def _raw_request(self, url=None, *args, **kwargs):
        return self._client.raw_request(self._url + (url or ''), *args, **kwargs)

    def _request(self, url=None, *args, **kwargs):
        return self._client.request(self._url + (url or ''), *args, **kwargs)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self._url)


def api(path, klass=None):
    '''
    Returns property that instantiates and returns specified Api class instance
    passing it client and suburl, derived from self url and given path.

    :param path: (string) URI path relative to parent resource
    :param klass: (Api) Api class to instantiate
    :return: Property descriptor
    '''
    def wrapper(klass):
        if not issubclass(klass, Api):
            klass = type(klass.__name__, (klass, Api), {})
        return ApiNamespace(path, klass)

    if klass:
        return wrapper(klass)

    return wrapper


class RestResource(Api):
    def get(self, **kwargs):
        try:
            return self._request(method='GET', **kwargs)
        except ClientError as ce:
            if ce.status_code != 404:
                raise ce
            return None

    def update(self, data, **kwargs):
        return self._request(method='PUT', data=data, **kwargs)

    def delete(self, **kwargs):
        try:
            response = self._request(method='DELETE', **kwargs)
        except ClientError as ce:
            if ce.status_code != 404:
                raise ce

        self._client.remove_cleanup(self._url)


class RestResources(Api):
    '''
    REST resources API implementing access to collection of resources.
    Inner class "Resource" defines API for accessing particular resource.

    Example:

        users = RestResources(client, '/users')
        users.list() # => [{'id': '1', 'name': 'John'}, ... ]
        users.create({'name': 'Jane'}) # => {'id': '2'}

        users['2'].get() # => {'id': '2', 'name': 'Jane'}
        users['2'].update({'name': 'Jane Doe'})
        users['2'].delete()

    Uses Client's Cleanup API to register created resources for cleanup.
    '''
    def list(self, **kwargs):
        return self._request(method='GET', **kwargs)

    def create(self, data, **kwargs):
        result = self._request(method='POST', data=data, **kwargs)
        if isinstance(result, dict) and 'id' in result:
            resource_api = self[result['id']]
            self._client.add_cleanup(resource_api._url, resource_api.delete)
        return result

    @api('/{resource_id}')
    class Resource(RestResource):
        pass


def resources(path, klass=RestResources):
    '''Convenience shortcut for defining REST resources API

    Example:

        class Client(http_test_client.Client):
            users = resources('/users')

    '''
    return api(path, RestResources)
