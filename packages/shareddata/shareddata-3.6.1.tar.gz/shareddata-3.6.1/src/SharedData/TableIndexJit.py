from numba.typed import List
import numpy as np
from numba import njit


###################### DATE_SYMBOL ########################
@njit(cache=True)
def create_pkey_date_symbol_jit(records, count, pkey, dateiniidx, dateendidx, dateunit, start):
    n = pkey.size-1
    for i in range(start, count):
        intdt = np.int32(np.int64(records['date'][i])/dateunit)
        if dateiniidx[intdt] == -1:
            dateiniidx[intdt] = i
        if dateendidx[intdt] < i:
            dateendidx[intdt] = i
        h0 = hash(records['date'][i])
        h1 = hash(records['symbol'][i])
        h = (h0 ^ h1) % n
        if pkey[h] == -1:
            pkey[h] = i
        else:
            duplicatedkey = True
            j = 1
            while (
                    (records[pkey[h]]['date'] != records[i]['date']) |
                    (records[pkey[h]]['symbol'] != records[i]['symbol'])
            ):
                h = (h + j**2) % n
                if pkey[h] == -1:
                    pkey[h] = i
                    duplicatedkey = False
                    break
                j += 1
            if duplicatedkey:
                raise Exception('error duplicated index')


@njit(cache=True)
def get_loc_date_symbol_jit(records, pkey, keys):
    n = pkey.size-1
    loc = np.empty((keys.size, ))
    for i in range(keys.size):
        h0 = hash(keys['date'][i])
        h1 = hash(keys['symbol'][i])
        h = (h0 ^ h1) % n
        if pkey[h] == -1:
            loc[i] = pkey[h]
        else:
            j = 1
            while (
                    (records[pkey[h]]['date'] != keys[i]['date']) |
                    (records[pkey[h]]['symbol'] != keys[i]['symbol'])
            ):
                h = (h + j**2) % n
                if pkey[h] == -1:
                    break
                j += 1
            loc[i] = pkey[h]
    return loc


@njit(cache=True)
def upsert_date_symbol_jit(records, count, new_records, pkey, dateiniidx, dateendidx, dateunit):
    minchgid = count
    maxsize = records.size
    nrec = new_records.size
    n = pkey.size - 1

    for i in range(nrec):
        h0 = hash(new_records['date'][i])
        h1 = hash(new_records['symbol'][i])
        h = (h0 ^ h1) % n
        found = False

        if pkey[h] != -1:  # hash already exists
            j = 1
            while True:  # check for collision & find a free bucket
                if (records[pkey[h]]['date'] == new_records[i]['date'] and
                   records[pkey[h]]['symbol'] == new_records[i]['symbol']):
                    # record exists update it
                    records[pkey[h]] = new_records[i]
                    minchgid = min(minchgid, pkey[h])
                    found = True
                    break
                # collision confirmed jump hash
                h = (h + j ** 2) % n
                if pkey[h] == -1:
                    break
                j += 1

        if not found:
            # Check space and append new record
            if count >= maxsize:
                break  # max size reached
            else:
                # append new record
                records[count] = new_records[i]
                intdt = np.int32(np.int64(new_records['date'][i]) / dateunit)
                if dateiniidx[intdt] == -1:
                    dateiniidx[intdt] = count
                if dateendidx[intdt] < count:
                    dateendidx[intdt] = count
                pkey[h] = count
                count += 1
                minchgid = min(minchgid, count)

    return count, minchgid

###################### DATE_SYMBOL_SYMBOL2 ########################


@njit(cache=True)
def create_pkey_date_symbol_symbol1_jit(records, count, pkey, dateiniidx, dateendidx, dateunit, start):
    n = pkey.size-1
    for i in range(start, count):
        intdt = np.int32(np.int64(records['date'][i])/dateunit)
        if dateiniidx[intdt] == -1:
            dateiniidx[intdt] = i
        if dateendidx[intdt] < i:
            dateendidx[intdt] = i
        if records['symbol'][i] != records['symbol1'][i]:
            h0 = hash(records['date'][i])
            h1 = hash(records['symbol'][i])
            h2 = hash(records['symbol1'][i])
            h = (h0 ^ h1 ^ h2) % n
        else:
            h0 = hash(records['date'][i])
            h1 = hash(records['symbol'][i])
            h = (h0 ^ h1) % n
        if pkey[h] == -1:
            pkey[h] = i
        else:
            duplicatedkey = True
            j = 1
            while (
                    (records[pkey[h]]['date'] != records[i]['date']) |
                    (records[pkey[h]]['symbol'] != records[i]['symbol']) |
                    (records[pkey[h]]['symbol1'] != records[i]['symbol1'])
            ):
                h = (h + j**2) % n
                if pkey[h] == -1:
                    pkey[h] = i
                    duplicatedkey = False
                    break
                j += 1
            if duplicatedkey:
                raise Exception('error duplicated index')


@njit(cache=True)
def get_loc_date_symbol_symbol1_jit(records, pkey, keys):
    n = pkey.size-1
    loc = np.empty((keys.size, ))
    for i in range(keys.size):
        if keys['symbol'][i] != keys['symbol1'][i]:
            h0 = hash(keys['date'][i])
            h1 = hash(keys['symbol'][i])
            h2 = hash(keys['symbol1'][i])
            h = (h0 ^ h1 ^ h2) % n
        else:
            h0 = hash(keys['date'][i])
            h1 = hash(keys['symbol'][i])
            h = (h0 ^ h1) % n
        if pkey[h] == -1:
            loc[i] = pkey[h]
        else:
            j = 1
            while (
                    (records[pkey[h]]['date'] != keys[i]['date']) |
                    (records[pkey[h]]['symbol'] != keys[i]['symbol']) |
                    (records[pkey[h]]['symbol1'] != keys[i]['symbol1'])
            ):
                h = (h + j**2) % n
                if pkey[h] == -1:
                    break
                j += 1
            loc[i] = pkey[h]
    return loc


@njit(cache=True)
def upsert_date_symbol_symbol1_jit(records, count, new_records, pkey, dateiniidx, dateendidx, dateunit):
    minchgid = count
    maxsize = records.size
    nrec = new_records.size
    n = pkey.size - 1

    for i in range(nrec):
        if new_records['symbol'][i] != new_records['symbol1'][i]:
            h0 = hash(new_records['date'][i])
            h1 = hash(new_records['symbol'][i])
            h2 = hash(new_records['symbol1'][i])
            h = (h0 ^ h1 ^ h2) % n
        else:
            h0 = hash(new_records['date'][i])
            h1 = hash(new_records['symbol'][i])
            h = (h0 ^ h1) % n
        found = False

        if pkey[h] != -1:  # hash already exists
            j = 1
            while True:  # check for collision & find a free bucket
                if (records[pkey[h]]['date'] == new_records[i]['date'] and
                   records[pkey[h]]['symbol'] == new_records[i]['symbol'] and
                        records[pkey[h]]['symbol1'] == new_records[i]['symbol1']):
                    # record exists update it
                    records[pkey[h]] = new_records[i]
                    minchgid = min(minchgid, pkey[h])
                    found = True
                    break
                # collision confirmed jump hash
                h = (h + j ** 2) % n
                if pkey[h] == -1:
                    break
                j += 1

        if not found:
            # Check space and append new record
            if count >= maxsize:
                break  # max size reached
            else:
                # append new record
                records[count] = new_records[i]
                intdt = np.int32(np.int64(new_records['date'][i]) / dateunit)
                if dateiniidx[intdt] == -1:
                    dateiniidx[intdt] = count
                if dateendidx[intdt] < count:
                    dateendidx[intdt] = count
                pkey[h] = count
                count += 1
                minchgid = min(minchgid, count)

    return count, minchgid

###################### DATE_PORTFOLIO ########################


@njit(cache=True)
def create_pkey_date_portfolio_jit(records, count, pkey, dateiniidx, dateendidx, dateunit, start):
    n = pkey.size-1
    for i in range(start, count):
        intdt = np.int32(np.int64(records['date'][i])/dateunit)
        if dateiniidx[intdt] == -1:
            dateiniidx[intdt] = i
        if dateendidx[intdt] < i:
            dateendidx[intdt] = i
        h0 = hash(records['date'][i])
        h1 = hash(records['portfolio'][i])
        h = (h0 ^ h1) % n
        if pkey[h] == -1:
            pkey[h] = i
        else:
            duplicatedkey = True
            j = 1
            while (
                    (records[pkey[h]]['date'] != records[i]['date']) |
                    (records[pkey[h]]['portfolio'] != records[i]['portfolio'])
            ):
                h = (h + j**2) % n
                if pkey[h] == -1:
                    pkey[h] = i
                    duplicatedkey = False
                    break
                j += 1
            if duplicatedkey:
                raise Exception('error duplicated index')


@njit(cache=True)
def get_loc_date_portfolio_jit(records, pkey, keys):
    n = pkey.size-1
    loc = np.empty((keys.size, ))
    for i in range(keys.size):
        h0 = hash(keys['date'][i])
        h1 = hash(keys['portfolio'][i])
        h = (h0 ^ h1) % n
        if pkey[h] == -1:
            loc[i] = pkey[h]
        else:
            j = 1
            while (
                    (records[pkey[h]]['date'] != keys[i]['date']) |
                    (records[pkey[h]]['portfolio'] != keys[i]['portfolio'])
            ):
                h = (h + j**2) % n
                if pkey[h] == -1:
                    break
                j += 1
            loc[i] = pkey[h]
    return loc


@njit(cache=True)
def upsert_date_portfolio_jit(records, count, new_records, pkey, dateiniidx, dateendidx, dateunit):
    minchgid = count
    maxsize = records.size
    nrec = new_records.size
    n = pkey.size - 1

    for i in range(nrec):
        h0 = hash(new_records['date'][i])
        h1 = hash(new_records['portfolio'][i])
        h = (h0 ^ h1) % n
        found = False

        if pkey[h] != -1:  # hash already exists
            j = 1
            while True:  # check for collision & find a free bucket
                if (records[pkey[h]]['date'] == new_records[i]['date'] and
                   records[pkey[h]]['portfolio'] == new_records[i]['portfolio']):
                    # record exists update it
                    records[pkey[h]] = new_records[i]
                    minchgid = min(minchgid, pkey[h])
                    found = True
                    break
                # collision confirmed jump hash
                h = (h + j ** 2) % n
                if pkey[h] == -1:
                    break
                j += 1

        if not found:
            # Check space and append new record
            if count >= maxsize:
                break  # max size reached
            else:
                # append new record
                records[count] = new_records[i]
                intdt = np.int32(np.int64(new_records['date'][i]) / dateunit)
                if dateiniidx[intdt] == -1:
                    dateiniidx[intdt] = count
                if dateendidx[intdt] < count:
                    dateendidx[intdt] = count
                pkey[h] = count
                count += 1
                minchgid = min(minchgid, count)

    return count, minchgid

###################### DATE_PORTFOLIO_SYMBOL ########################


@njit(cache=True)
def create_pkey_date_portfolio_symbol_jit(records, count, pkey, dateiniidx, dateendidx, dateunit,
                                          portiniidx, portendidx, portlist, portlistcount, start):
    n = pkey.size-1
    for i in range(start, count):
        intdt = np.int32(np.int64(records['date'][i])/dateunit)
        if dateiniidx[intdt] == -1:
            dateiniidx[intdt] = i
        if dateendidx[intdt] < i:
            dateendidx[intdt] = i
        h0 = hash(records['date'][i])
        h1 = hash(records['portfolio'][i])
        h2 = hash(records['symbol'][i])
        h = (h0 ^ h1 ^ h2) % n
        if pkey[h] == -1:
            pkey[h] = i
        else:
            duplicatedkey = True
            j = 1
            while (
                    (records[pkey[h]]['date'] != records[i]['date']) |
                    (records[pkey[h]]['portfolio'] != records[i]['portfolio']) |
                    (records[pkey[h]]['symbol'] != records[i]['symbol'])
            ):
                h = (h + j**2) % n
                if pkey[h] == -1:
                    pkey[h] = i
                    duplicatedkey = False
                    break
                j += 1
            if duplicatedkey:
                raise Exception('error duplicated index')

        hport = (h0 ^ h1) % n
        if portiniidx[hport] == -1:
            newid = int(portlistcount*2)
            portiniidx[hport] = newid
            portendidx[hport] = newid
            portlist[newid] = i
            portlistcount += 1
        else:
            j = 1
            fid = portlist[portiniidx[hport]]
            newindex = False
            while (
                    (records[fid]['date'] != records[i]['date']) |
                    (records[fid]['portfolio'] != records[i]['portfolio'])
            ):
                hport = (hport + j**2) % n
                if portiniidx[hport] == -1:
                    newid = int(portlistcount*2)
                    portiniidx[hport] = newid
                    portendidx[hport] = newid
                    portlist[newid] = i
                    portlistcount += 1
                    newindex = True
                    break
                fid = portlist[portiniidx[hport]]
                j += 1
            if not newindex:
                curid = portendidx[hport]
                newid = int(portlistcount*2)
                portlist[curid+1] = newid
                portlist[newid] = i
                portendidx[hport] = newid
                portlistcount += 1


@njit(cache=True)
def get_loc_date_portfolio_symbol_jit(records, pkey, keys):
    n = pkey.size-1
    loc = np.empty((keys.size, ))
    for i in range(keys.size):
        h0 = hash(keys['date'][i])
        h1 = hash(keys['portfolio'][i])
        h2 = hash(keys['symbol'][i])
        h = (h0 ^ h1 ^ h2) % n
        if pkey[h] == -1:
            loc[i] = pkey[h]
        else:
            j = 1
            while (
                    (records[pkey[h]]['date'] != keys[i]['date']) |
                    (records[pkey[h]]['portfolio'] != keys[i]['portfolio']) |
                    (records[pkey[h]]['symbol'] != keys[i]['symbol'])
            ):
                h = (h + j**2) % n
                if pkey[h] == -1:
                    break
                j += 1
            loc[i] = pkey[h]
    return loc


@njit(cache=True)
def upsert_date_portfolio_symbol_jit(records, count, new_records, pkey, dateiniidx, dateendidx, dateunit,
                                     portiniidx, portendidx, portlist, portlistcount):

    minchgid = count
    maxsize = records.size
    nrec = new_records.size
    n = pkey.size - 1

    for i in range(nrec):
        h0 = hash(new_records['date'][i])
        h1 = hash(new_records['portfolio'][i])
        h2 = hash(new_records['symbol'][i])
        h = (h0 ^ h1 ^ h2) % n
        found = False

        if pkey[h] != -1:  # hash already exists
            j = 1
            while True:  # check for collision & find a free bucket
                if (records[pkey[h]]['date'] == new_records[i]['date'] and
                   records[pkey[h]]['portfolio'] == new_records[i]['portfolio'] and
                   records[pkey[h]]['symbol'] == new_records[i]['symbol']):
                    # record exists, update it
                    records[pkey[h]] = new_records[i]
                    minchgid = min(minchgid, pkey[h])
                    found = True
                    break
                # collision confirmed, jump hash
                h = (h + j ** 2) % n
                if pkey[h] == -1:
                    break
                j += 1

        if not found:
            # Check space and append new record
            if count >= maxsize:
                break  # max size reached
            else:
                # append new record
                records[count] = new_records[i]
                intdt = np.int32(np.int64(new_records['date'][i]) / dateunit)
                if dateiniidx[intdt] == -1:
                    dateiniidx[intdt] = count
                if dateendidx[intdt] < count:
                    dateendidx[intdt] = count
                pkey[h] = count

                # inlined logic for updating portlist
                hport = (h0 ^ h1) % n
                if portiniidx[hport] == -1:
                    newid = int(portlistcount * 2)
                    portiniidx[hport] = newid
                    portendidx[hport] = newid
                    portlist[newid] = count
                    portlistcount += 1
                else:
                    j = 1
                    fid = portlist[portiniidx[hport]]
                    newindex = False
                    while (records[fid]['date'] != records[count]['date'] or
                           records[fid]['portfolio'] != records[count]['portfolio']):
                        hport = (hport + j ** 2) % n
                        if portiniidx[hport] == -1:
                            newid = int(portlistcount * 2)
                            portiniidx[hport] = newid
                            portendidx[hport] = newid
                            portlist[newid] = count
                            portlistcount += 1
                            newindex = True
                            break
                        fid = portlist[portiniidx[hport]]
                        j += 1

                    if not newindex:
                        curid = portendidx[hport]
                        newid = int(portlistcount * 2)
                        portlist[curid + 1] = newid
                        portlist[newid] = count
                        portendidx[hport] = newid
                        portlistcount += 1

                count += 1
                minchgid = min(minchgid, count)

    return count, minchgid

###################### DATE_PORTFOLIO_SYMBOL_CLORDID ########################


@njit(cache=True)
def create_pkey_date_portfolio_symbol_clordid_jit(records, count, pkey, dateiniidx, dateendidx, dateunit, portiniidx, portendidx, portlist, portlistcount, start):
    n = pkey.size-1
    for i in range(start, count):
        intdt = np.int32(np.int64(records['date'][i])/dateunit)
        if dateiniidx[intdt] == -1:
            dateiniidx[intdt] = i
        if dateendidx[intdt] < i:
            dateendidx[intdt] = i
        h0 = hash(records['date'][i])
        h1 = hash(records['portfolio'][i])
        h2 = hash(records['symbol'][i])
        h3 = hash(records['clordid'][i])
        h = (h0 ^ h1 ^ h2 ^ h3) % n
        if pkey[h] == -1:
            pkey[h] = i
        else:
            duplicatedkey = True
            j = 1
            while (
                    (records[pkey[h]]['date'] != records[i]['date']) |
                    (records[pkey[h]]['portfolio'] != records[i]['portfolio']) |
                    (records[pkey[h]]['symbol'] != records[i]['symbol']) |
                    (records[pkey[h]]['clordid'] != records[i]['clordid'])
            ):
                h = (h + j**2) % n
                if pkey[h] == -1:
                    pkey[h] = i
                    duplicatedkey = False
                    break
                j += 1
            if duplicatedkey:
                raise Exception('error duplicated index')

        hport = (h0 ^ h1) % n
        if portiniidx[hport] == -1:
            newid = int(portlistcount*2)
            portiniidx[hport] = newid
            portendidx[hport] = newid
            portlist[newid] = i
            portlistcount += 1
        else:
            j = 1
            fid = portlist[portiniidx[hport]]
            newindex = False
            while (
                    (records[fid]['date'] != records[i]['date']) |
                    (records[fid]['portfolio'] != records[i]['portfolio'])
            ):
                hport = (hport + j**2) % n
                if portiniidx[hport] == -1:
                    newid = int(portlistcount*2)
                    portiniidx[hport] = newid
                    portendidx[hport] = newid
                    portlist[newid] = i
                    portlistcount += 1
                    newindex = True
                    break
                fid = portlist[portiniidx[hport]]
                j += 1
            if not newindex:
                curid = portendidx[hport]
                newid = int(portlistcount*2)
                portlist[curid+1] = newid
                portlist[newid] = i
                portendidx[hport] = newid
                portlistcount += 1


@njit(cache=True)
def get_loc_date_portfolio_symbol_clordid_jit(records, pkey, keys):
    n = pkey.size-1
    loc = np.empty((keys.size, ))
    for i in range(keys.size):
        h0 = hash(keys['date'][i])
        h1 = hash(keys['portfolio'][i])
        h2 = hash(keys['symbol'][i])
        h3 = hash(keys['clordid'][i])
        h = (h0 ^ h1 ^ h2 ^ h3) % n
        if pkey[h] == -1:
            loc[i] = pkey[h]
        else:
            j = 1
            while (
                    (records[pkey[h]]['date'] != keys[i]['date']) |
                    (records[pkey[h]]['portfolio'] != keys[i]['portfolio']) |
                    (records[pkey[h]]['symbol'] != keys[i]['symbol']) |
                    (records[pkey[h]]['clordid'] != keys[i]['clordid'])
            ):
                h = (h + j**2) % n
                if pkey[h] == -1:
                    break
                j += 1
            loc[i] = pkey[h]
    return loc


@njit(cache=True)
def upsert_date_portfolio_symbol_clordid_jit(records, count, new_records, pkey, dateiniidx, dateendidx, dateunit,
                                             portiniidx, portendidx, portlist, portlistcount):

    minchgid = count
    maxsize = records.size
    nrec = new_records.size
    n = pkey.size - 1

    for i in range(nrec):
        h0 = hash(new_records['date'][i])
        h1 = hash(new_records['portfolio'][i])
        h2 = hash(new_records['symbol'][i])
        h3 = hash(new_records['clordid'][i])
        h = (h0 ^ h1 ^ h2 ^ h3) % n
        found = False

        if pkey[h] != -1:  # hash already exists
            j = 1
            while True:  # check for collision & find a free bucket
                if (records[pkey[h]]['date'] == new_records[i]['date'] and
                   records[pkey[h]]['portfolio'] == new_records[i]['portfolio'] and
                   records[pkey[h]]['symbol'] == new_records[i]['symbol'] and
                   records[pkey[h]]['clordid'] == new_records[i]['clordid']):
                    # record exists, update it
                    records[pkey[h]] = new_records[i]
                    minchgid = min(minchgid, pkey[h])
                    found = True
                    break
                # collision confirmed, jump hash using quadratic probing
                h = (h + j ** 2) % n
                if pkey[h] == -1:
                    break
                j += 1

        if not found:
            # Check space and append new record
            if count >= maxsize:
                break  # max size reached
            else:
                # append new record
                records[count] = new_records[i]
                intdt = np.int32(np.int64(new_records['date'][i]) / dateunit)
                if dateiniidx[intdt] == -1:
                    dateiniidx[intdt] = count
                if dateendidx[intdt] < count:
                    dateendidx[intdt] = count
                pkey[h] = count

                # inlined logic for updating portlist
                hport = (h0 ^ h1) % n
                if portiniidx[hport] == -1:
                    newid = int(portlistcount * 2)
                    portiniidx[hport] = newid
                    portendidx[hport] = newid
                    portlist[newid] = count
                    portlistcount += 1
                else:
                    j = 1
                    fid = portlist[portiniidx[hport]]
                    newindex = False
                    while (records[fid]['date'] != records[count]['date'] or
                           records[fid]['portfolio'] != records[count]['portfolio']):
                        hport = (hport + j ** 2) % n
                        if portiniidx[hport] == -1:
                            newid = int(portlistcount * 2)
                            portiniidx[hport] = newid
                            portendidx[hport] = newid
                            portlist[newid] = count
                            portlistcount += 1
                            newindex = True
                            break
                        fid = portlist[portiniidx[hport]]
                        j += 1

                    if not newindex:
                        curid = portendidx[hport]
                        newid = int(portlistcount * 2)
                        portlist[curid + 1] = newid
                        portlist[newid] = count
                        portendidx[hport] = newid
                        portlistcount += 1

                count += 1
                minchgid = min(minchgid, count)

    return count, minchgid

###################### DATE_PORTFOLIO_SYMBOL_TRADEID ########################


@njit(cache=True)
def create_pkey_date_portfolio_symbol_tradeid_jit(records, count, pkey, dateiniidx, dateendidx, dateunit, portiniidx, portendidx, portlist, portlistcount, start):
    n = pkey.size-1
    for i in range(start, count):
        intdt = np.int32(np.int64(records['date'][i])/dateunit)
        if dateiniidx[intdt] == -1:
            dateiniidx[intdt] = i
        if dateendidx[intdt] < i:
            dateendidx[intdt] = i
        h0 = hash(records['date'][i])
        h1 = hash(records['portfolio'][i])
        h2 = hash(records['symbol'][i])
        h3 = hash(records['tradeid'][i])
        h = (h0 ^ h1 ^ h2 ^ h3) % n
        if pkey[h] == -1:
            pkey[h] = i
        else:
            duplicatedkey = True
            j = 1
            while (
                    (records[pkey[h]]['date'] != records[i]['date']) |
                    (records[pkey[h]]['portfolio'] != records[i]['portfolio']) |
                    (records[pkey[h]]['symbol'] != records[i]['symbol']) |
                    (records[pkey[h]]['tradeid'] != records[i]['tradeid'])
            ):
                h = (h + j**2) % n
                if pkey[h] == -1:
                    pkey[h] = i
                    duplicatedkey = False
                    break
                j += 1
            if duplicatedkey:
                raise Exception('error duplicated index')

        hport = (h0 ^ h1) % n
        if portiniidx[hport] == -1:
            newid = int(portlistcount*2)
            portiniidx[hport] = newid
            portendidx[hport] = newid
            portlist[newid] = i
            portlistcount += 1
        else:
            j = 1
            fid = portlist[portiniidx[hport]]
            newindex = False
            while (
                    (records[fid]['date'] != records[i]['date']) |
                    (records[fid]['portfolio'] != records[i]['portfolio'])
            ):
                hport = (hport + j**2) % n
                if portiniidx[hport] == -1:
                    newid = int(portlistcount*2)
                    portiniidx[hport] = newid
                    portendidx[hport] = newid
                    portlist[newid] = i
                    portlistcount += 1
                    newindex = True
                    break
                fid = portlist[portiniidx[hport]]
                j += 1
            if not newindex:
                curid = portendidx[hport]
                newid = int(portlistcount*2)
                portlist[curid+1] = newid
                portlist[newid] = i
                portendidx[hport] = newid
                portlistcount += 1


@njit(cache=True)
def get_loc_date_portfolio_symbol_tradeid_jit(records, pkey, keys):
    n = pkey.size-1
    loc = np.empty((keys.size, ))
    for i in range(keys.size):
        h0 = hash(keys['date'][i])
        h1 = hash(keys['portfolio'][i])
        h2 = hash(keys['symbol'][i])
        h3 = hash(keys['tradeid'][i])
        h = (h0 ^ h1 ^ h2 ^ h3) % n
        if pkey[h] == -1:
            loc[i] = pkey[h]
        else:
            j = 1
            while (
                    (records[pkey[h]]['date'] != keys[i]['date']) |
                    (records[pkey[h]]['portfolio'] != keys[i]['portfolio']) |
                    (records[pkey[h]]['symbol'] != keys[i]['symbol']) |
                    (records[pkey[h]]['tradeid'] != keys[i]['tradeid'])
            ):
                h = (h + j**2) % n
                if pkey[h] == -1:
                    break
                j += 1
            loc[i] = pkey[h]
    return loc


@njit(cache=True)
def upsert_date_portfolio_symbol_tradeid_jit(records, count, new_records, pkey, dateiniidx, dateendidx, dateunit,
                                             portiniidx, portendidx, portlist, portlistcount):

    minchgid = count
    maxsize = records.size
    nrec = new_records.size
    n = pkey.size - 1

    for i in range(nrec):
        h0 = hash(new_records['date'][i])
        h1 = hash(new_records['portfolio'][i])
        h2 = hash(new_records['symbol'][i])
        h3 = hash(new_records['tradeid'][i])
        h = (h0 ^ h1 ^ h2 ^ h3) % n
        found = False

        if pkey[h] != -1:  # hash already exists
            j = 1
            while True:  # check for collision & find a free bucket
                if (records[pkey[h]]['date'] == new_records[i]['date'] and
                   records[pkey[h]]['portfolio'] == new_records[i]['portfolio'] and
                   records[pkey[h]]['symbol'] == new_records[i]['symbol'] and
                   records[pkey[h]]['tradeid'] == new_records[i]['tradeid']):
                    # record exists, update it
                    records[pkey[h]] = new_records[i]
                    minchgid = min(minchgid, pkey[h])
                    found = True
                    break
                # collision confirmed, jump hash using quadratic probing
                h = (h + j ** 2) % n
                if pkey[h] == -1:
                    break
                j += 1

        if not found:
            # Check space and append new record
            if count >= maxsize:
                break  # max size reached
            else:
                # append new record
                records[count] = new_records[i]
                intdt = np.int32(np.int64(new_records['date'][i]) / dateunit)
                if dateiniidx[intdt] == -1:
                    dateiniidx[intdt] = count
                if dateendidx[intdt] < count:
                    dateendidx[intdt] = count
                pkey[h] = count

                # inlined logic for updating portlist
                hport = (h0 ^ h1) % n
                if portiniidx[hport] == -1:
                    newid = int(portlistcount * 2)
                    portiniidx[hport] = newid
                    portendidx[hport] = newid
                    portlist[newid] = count
                    portlistcount += 1
                else:
                    j = 1
                    fid = portlist[portiniidx[hport]]
                    newindex = False
                    while (records[fid]['date'] != records[count]['date'] or
                           records[fid]['portfolio'] != records[count]['portfolio']):
                        hport = (hport + j ** 2) % n
                        if portiniidx[hport] == -1:
                            newid = int(portlistcount * 2)
                            portiniidx[hport] = newid
                            portendidx[hport] = newid
                            portlist[newid] = count
                            portlistcount += 1
                            newindex = True
                            break
                        fid = portlist[portiniidx[hport]]
                        j += 1

                    if not newindex:
                        curid = portendidx[hport]
                        newid = int(portlistcount * 2)
                        portlist[curid + 1] = newid
                        portlist[newid] = count
                        portendidx[hport] = newid
                        portlistcount += 1

                count += 1
                minchgid = min(minchgid, count)

    return count, minchgid


####################### COMPOSITE INDEX ######################################


@njit(cache=True)
def get_index_date_portfolio_jit(records, keys, pkey, portiniidx, portlist):
    n = pkey.size-1
    loc = List()
    keyloc = List()
    for i in range(keys.size):
        h0 = hash(keys['date'][i])
        h1 = hash(keys['portfolio'][i])
        h = (h0 ^ h1) % n
        if portiniidx[h] == -1:
            pass
        else:
            j = 1
            portfound = True
            recid = portlist[portiniidx[h]]
            while (
                    (records[recid]['date'] != keys[i]['date']) |
                    (records[recid]['portfolio'] != keys[i]['portfolio'])
            ):
                h = (h + j**2) % n
                if portiniidx[h] == -1:
                    portfound = False
                    break
                recid = portlist[portiniidx[h]]
                j += 1
            if portfound:
                curid = portiniidx[h]
                fid = portlist[curid]
                loc.append(fid)
                keyloc.append(i)
                nextid = portlist[curid+1]
                while nextid != -1:
                    curid = nextid
                    loc.append(portlist[curid])
                    keyloc.append(i)
                    nextid = portlist[curid+1]
    return loc, keyloc
