from socketio import AsyncNamespace
from orbit_component_base.src.orbit_nql import NQL
from orbit_component_base.src.orbit_auth import OrbitAuth
from orbit_component_base.src.orbit_decorators import Sentry, check_own_hostid, check_permission
from orbit_component_base.schema.OrbitSessions import SessionsCollection
from orbit_component_base.schema.OrbitSessions import SessionsTable
from loguru import logger as log
from orbit_component_base.src.orbit_shared import world


class PluginBase (AsyncNamespace):

    NAMESPACE = ''
    COLLECTIONS = []

    @property
    def ns (self):
        return f'/{self.NAMESPACE}'

    def __init__(self, *args, **kwargs):
        # log.debug(f'Initialise namespace: {self.ns}')
        kwargs['namespace'] = self.ns
        self._odb = kwargs.pop('odb')
        self._nql = None
        self._collections = []
        super().__init__(*args, **kwargs)

    def open (self, nql=True):
        if world.conf.debug:
            log.success(f'Open namespace: {self.ns}')
        if nql:
            self._nql = NQL(self.emit, self.ns).open()
        for cls in self.COLLECTIONS:
            cls().open(self._odb, self._nql)
        if nql:
            SessionsCollection().flush(self.ns)
        return self
    
    def register (self, sio):
        sio.register_namespace(self)
        return self
    
    async def on_connect(self, sid, environ):
        await self.save_session(sid, {
            'sid': sid,
            'address': environ['aiohttp.request'].transport.get_extra_info('peername')[0]
        })
        self._nql.connect(sid)

    async def on_disconnect(self, sid):
        self._nql.disconnect(sid)
        SessionsTable().from_sid(sid).delete()

    async def on_auth_hello(self, sid, auth):
        return await OrbitAuth(sid, self.ns).hello(auth, self.get_session, self.save_session)

    async def on_auth_validate(self, sid, auth):
        log.info(f'Validated access for session={sid} to namespace={self.NAMESPACE}')
        return await OrbitAuth(sid, self.ns).validate(auth, self.get_session, self.save_session)

    async def on_auth_confirm(self, sid, auth):
        return await OrbitAuth(sid, self.ns).confirm(auth, self.get_session, self.save_session)

    @Sentry(check_own_hostid)
    async def on_call_nql(self, sid, params):
        return self._nql.call(sid, params)

    @Sentry()
    async def on_drop_nql(self, sid, params):
        return self._nql.drop(sid, params)

    @Sentry()
    async def on_dump_nql(self, sid):
        return self._nql.dump ()
    

class ArgsBase:

    def __init__ (self, parser=None, args=None):
        self._parser = parser

    def setup (self):
        return self

    def open (self, odb=None, args=None):
        self._odb = odb
        self._args = args
        return self

    def process (self):
        return self
