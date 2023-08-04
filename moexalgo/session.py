from __future__ import annotations
import typing as t
import httpx

from moexalgo.utils import json

BASE_URL = 'https://iss.moex.com/iss'
AUTH_URL = 'https://passport.moex.com/authenticate'
AUTH_CERT = None
USE_HTTPS = True


class Client:
    """ API клиент """

    def __init__(self, sync: bool = True, **options):
        base_url = options.get('base_url', BASE_URL)
        if base_url.startswith('http:') and USE_HTTPS:
            options['base_url'] = base_url.replace('http:', 'https:')
        elif base_url.startswith('https:') and not USE_HTTPS:
            options['base_url'] = base_url.replace('https:', 'http:')
        self.httpx_cli = httpx.Client(**options) if sync else httpx.AsyncClient(**options)
        self.options = options

    @property
    def sync(self):
        return isinstance(self.httpx_cli, httpx.Client)

    def authorize(self, username: str, password: str) -> str | None | t.Coroutine[t.Any, t.Any, str | None]:

        async def _async_authorize():
            resp = await self.httpx_cli.get(AUTH_URL, auth=(username, password))
            return resp.cookies.get('MicexPassportCert')

        def _sync_authorize():
            resp = self.httpx_cli.get(AUTH_URL, auth=(username, password))
            return resp.cookies.get('MicexPassportCert')

        self.options['MicexPassportCert'] = _sync_authorize() if self.sync else _async_authorize()
        return self.options['MicexPassportCert']

    def get_objects(self, path: str, source: str, deserializer: t.Callable[[dict], dict | list], **params):
        path = [item for item in path.split('/') if item.strip()]
        path += [(source.split('.')[0] if '.' in source else source) + '.json']
        url = '/'.join(path)

        def _parse_response(resp: httpx.Response):
            if not resp.is_success:
                resp.raise_for_status()
            if data := json.loads(resp.text):
                return deserializer(data)
            raise ValueError('Received wrong data')

        async def _async_get_objects():
            return _parse_response(await self.httpx_cli.get(url, params=params))

        def _sync_get_objects():
            return _parse_response(self.httpx_cli.get(url, params=params))

        return _sync_get_objects() if self.sync else _async_get_objects()


class Session:
    """ API клиент сессия """

    def __init__(self, client: Client | None = None, /, auth_cert: str = None, base_url: str = None, timeout=300):
        self.options = dict(base_url=base_url or BASE_URL, timeout=timeout,
                            cookies={'MicexPassportCert': auth_cert} if auth_cert else {})
        if client is not None:
            self.options.update(client.options)
        self._client = None

    @property
    def client(self) -> Client:
        return self._client or Client(True, **self.options)

    def __enter__(self) -> Client:
        self._client = Client(True, **self.options)
        self._client.httpx_cli.__enter__()
        return self._client

    def __exit__(self, *exc_info):
        return self._client.httpx_cli.__exit__(*exc_info)

    async def __aenter__(self) -> Client:
        self._client = Client(False, **self.options)
        await self._client.httpx_cli.__aenter__()
        return self._client

    async def __aexit__(self, *exc_info):
        return await self._client.httpx_cli.__aexit__(*exc_info)


def authorize(username: str, password: str) -> bool:
    """ Авторизация сессии по умолчанию """
    global AUTH_CERT
    with Session(auth_cert=AUTH_CERT) as client:
        if auth_cert := client.authorize(username, password):
            AUTH_CERT = auth_cert
            return True
        return False


def __getattr__(name):
    if name == 'default':
        return Session(auth_cert=AUTH_CERT)
