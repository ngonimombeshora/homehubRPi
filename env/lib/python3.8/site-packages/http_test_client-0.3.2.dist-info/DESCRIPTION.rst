****************
http-test-client
****************

Library to simplify writing HTTP REST service integration tests.

Allows to build a HTTP REST client with automatic resource cleanup.

Example
=======

.. code:: python

    from http_test_client import Client, HttpTransport, RestResources, resources

    class ArticleResources(RestResources):
        def search(self, query):
            return self._request('/search', method='POST', data={'query': query})

        class Resource(RestResources.Resource):
            def publish(self):
                return self._request('/publish', method='POST')

            comments = resources('/comments')

    class MyClient(Client):
        users = resources('/users')
        articles = resources('/articles', ArticleResources)

    client = MyClient(HttpTransport('http://localhost:8888'))

    # managing resources
    client.users.list() # => [{'id': '1', 'name': 'John'}, ...]
    client.users.create({'name': 'Jane'}) # => {'id': '2'}
    client.users['1'].get() # => {'id': '1', 'name': 'John'}
    client.users['1'].delete()

    # delete all resources that were created during this client session
    client.cleanup()

    # custom action
    client.articles['123'].publish()

    # nested resources
    client.articles['123'].comments.list()


Installation
============
::

    $ pip install http-test-client


Requirements
============

- Python >= 2.7 and <= 3.6
- `requests <http://docs.python-requests.org/en/master/>`_ >= 2.14
- six >= 1.10

Project Links
=============

- PyPI: https://pypi.python.org/pypi/http-test-client
- Issues: https://github.com/maximkulkin/http-test-client/issues

License
=======

MIT licensed. See the bundled `LICENSE <https://github.com/maximkulkin/http-test-client/blob/master/LICENSE>`_ file for more details.


