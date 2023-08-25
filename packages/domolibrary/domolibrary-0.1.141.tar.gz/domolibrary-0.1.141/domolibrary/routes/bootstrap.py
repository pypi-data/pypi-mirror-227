# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/routes/bootstrap.ipynb.

# %% auto 0
__all__ = ['get_bootstrap', 'get_bootstrap_features', 'get_bootstrap_pages']

# %% ../../nbs/routes/bootstrap.ipynb 3
import httpx

import domolibrary.client.get_data as gd
import domolibrary.client.ResponseGetData as rgd
import domolibrary.client.DomoAuth as dmda

# %% ../../nbs/routes/bootstrap.ipynb 4
async def get_bootstrap(
    auth: dmda.DomoFullAuth, ## only works with DomoFullAuth authentication, do not use TokenAuth
    debug_api: bool = False, 
    session: httpx.AsyncClient = None,
    return_raw: bool = False
) -> rgd.ResponseGetData:
    """get bootstrap data"""

    if auth.__class__.__name__ != 'DomoFullAuth':
        raise dmda.InvalidAuthTypeError(function_name='get_bootstrap',
                                        domo_instance=auth.domo_instance, 
                                        required_auth_type =  dmda.DomoFullAuth )

    # url = f"https://{auth.domo_instance}.domo.com/api/domoweb/bootstrap?v2Navigation=false"
    url = f"https://{auth.domo_instance}.domo.com/api/domoweb/bootstrap?v2Navigation=true"

    res = await gd.get_data(
        url=url, method="GET", auth=auth, debug_api=debug_api, session=session, is_follow_redirects = True
    )

    if res.response == '' and not return_raw:
        raise Exception('BSR_Features:  no features returned - is there a VPN?')

    return res


# %% ../../nbs/routes/bootstrap.ipynb 8
async def get_bootstrap_features(
    auth: dmda.DomoAuth, session: httpx.AsyncClient = None,
    debug_api: bool = False,
    return_raw: bool = False
) -> rgd.ResponseGetData:

    res = await get_bootstrap(auth=auth, session=session, debug_api=debug_api, return_raw=return_raw)

    if return_raw:
        return res

    if not res.is_success:
        return None

    res.response = res.response.get("data").get("features")
    return res


# %% ../../nbs/routes/bootstrap.ipynb 11
async def get_bootstrap_pages(
    auth: dmda.DomoAuth, session: httpx.AsyncClient = None, debug_api: bool = False, return_raw: bool = False
) -> rgd.ResponseGetData:
    res = await get_bootstrap(auth=auth, session=session, debug_api=debug_api)

    if return_raw:
        return res
        
    if not res.is_success:
        return None

    res.response = res.response.get("data").get("pages")
    return res

