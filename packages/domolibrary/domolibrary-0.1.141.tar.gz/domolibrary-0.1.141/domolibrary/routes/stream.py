# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/routes/stream.ipynb.

# %% auto 0
__all__ = ['get_stream_by_id', 'update_stream', 'create_stream', 'execute_stream']

# %% ../../nbs/routes/stream.ipynb 2
import httpx

import domolibrary.client.get_data as gd
import domolibrary.client.ResponseGetData as rgd
import domolibrary.client.DomoAuth as dmda

# %% ../../nbs/routes/stream.ipynb 3
async def get_stream_by_id(auth: dmda.DomoAuth, stream_id: str,
                                session: httpx.AsyncClient = None,
                                debug_api: bool = False) -> rgd.ResponseGetData:
    url = f'https://{auth.domo_instance}.domo.com/api/data/v1/streams/{stream_id}'

    if debug_api:
        print(url)

    res = await gd.get_data(
        auth=auth,
        url=url,
        method='GET',
        session=session,
        debug_api=debug_api,
    )
    return res


async def update_stream(auth: dmda.DomoAuth, stream_id: str,
                        body: dict,
                        session: httpx.AsyncClient = None,
                        debug_api: bool = False) -> rgd.ResponseGetData:
    url = f'https://{auth.domo_instance}.domo.com/api/data/v1/streams/{stream_id}'

    if debug_api:
        print(url)

    res = await gd.get_data(
        auth=auth,
        url=url,
        body=body,
        method='PUT',
        session=session,
        debug_api=debug_api,
    )
    return res


async def create_stream(auth: dmda.DomoAuth,
                        body: dict,
                        session: httpx.AsyncClient = None,
                        debug_api: bool = False) -> rgd.ResponseGetData:
    url = f'https://{auth.domo_instance}.domo.com/api/data/v1/streams'

    if debug_api:
        print(url)

    res = await gd.get_data(
        auth=auth,
        url=url,
        body=body,
        method='POST',
        session=session,
        debug_api=debug_api,
    )
    return res

async def execute_stream(auth: dmda.DomoAuth,
                        stream_id: str,
                        session: httpx.AsyncClient = None,
                        debug_api: bool = False) -> rgd.ResponseGetData:
    url = f'https://{auth.domo_instance}.domo.com/api/data/v1/streams/{stream_id}/executions'

    if debug_api:
        print(url)

    res = await gd.get_data(
        auth=auth,
        url=url,
        method='POST',
        session=session,
        debug_api=debug_api,
    )
    return res
