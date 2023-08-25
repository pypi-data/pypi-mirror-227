from astropy.io import fits
from astropy.time import Time

import numpy as np
import os

from compPy.util.util import find_files, get_save_dir
from compPy.util import config

from typing import List

__all__ = ['cp_save_fits']


def cp_save_fits(fits_dict: dict, date: str, file_dir: str = None,
                 name_addon: str = 'comp.1074.dynamics.3'):
    """
    Save CoMP I, V, W cubes as multi-extension fits.

    Parameters
    -----------
    date - str
           date of observations
    """
    print("Saving data as fits")
    if not file_dir:
        file_dir = config.proc_dir
    save_dir = get_save_dir(date)
    file_path = '{0}{1}'.format(save_dir, file_dir)

    if not os.path.isdir(file_path):
        os.mkdir(file_path)

    cubes = fits_dict['data']
    heads = fits_dict['headers']
    primary_heads = fits_dict['primary_header']

    keys = ['cube_i', 'cube_v', 'cube_w']

    for j, prim_head in enumerate(primary_heads):

        hdul = fits.HDUList()
        hdul.append(fits.PrimaryHDU(header=prim_head))

        for key in keys:
            hdul.append(fits.CompImageHDU(data=cubes[key][j],
                                          header=heads[key + '_head'][j])
                        )
        time = prim_head['TIME-OBS'].replace(':', '')
        date_file = prim_head['DATE-OBS'].replace('-', '')

        path_comps = [file_path, date_file, time, name_addon]
        save_to = '{0}/{1}.{2}.{3}.fits'.format(*path_comps)
        hdul.writeto(save_to, overwrite=True)


def cp_save_fits_u(fits_dict: dict, date: str, file_dir: str = None,
                   name_addon: str = 'ucomp.1074.dynamics.3'):
    """
    Save CoMP I, V, W cubes as multi-extension fits.

    Parameters
    -----------
    date - str
           date of observations
    """
    print("Saving data as fits")
    if not file_dir:
        file_dir = config.proc_dir
    save_dir = get_save_dir(date)
    file_path = '{0}{1}'.format(save_dir, file_dir)

    if not os.path.isdir(file_path):
        os.mkdir(file_path)

    cubes = fits_dict['data']
    heads = fits_dict['headers']
    primary_heads = fits_dict['primary_header']

    keys = ['cube_i', 'cube_v', 'cube_w']

    for j, prim_head in enumerate(primary_heads):

        hdul = fits.HDUList()
        hdul.append(fits.PrimaryHDU(header=prim_head))

        for key in keys:
            hdul.append(fits.CompImageHDU(data=cubes[key][j],
                                          header=heads[key + '_head'][j])
                        )
        times = Time(prim_head['DATE-OBS'], format='isot')
        time = str(times.datetime.time())
        date_file = str(times.datetime.date()).replace('-', '')

        path_comps = [file_path, date_file, time, name_addon]
        save_to = '{0}/{1}.{2}.{3}.fits'.format(*path_comps)
        hdul.writeto(save_to, overwrite=True)


def cp_load_fits(date: str, keys: List[str] = ['i'], file_dir: str = None):
    """
    Load comp fits files from processed directory.

    Parameters
    -----------
    date - str
           date of observations
    keys - keys for which observable, i,v, w
    file_dir - alternative directory for saved files
    """
    if not file_dir:
        file_dir = config.proc_dir
    save_dir = get_save_dir(date)
    file_path = '{0}{1}'.format(save_dir, file_dir)

    files = find_files('*.fits', file_path)
    if len(files) == 0:
        print('No files found')
        return

    with fits.open(files[0]) as hdul:
        nx = hdul[1].header['NAXIS1']
        ny = hdul[1].header['NAXIS2']
        instrument = hdul[0].header['INSTRUME']
    nt = len(files)

    obs_keys = []
    if 'i' in keys:
        obs_keys.append('INTENSITY')
    if 'v' in keys:

        if instrument == 'UCoMP':
            obs_keys.append('LOS VELOCITY')
        else:
            obs_keys.append('CORRECTED LOS VELOCITY')
    if 'w' in keys:
        obs_keys.append('LINE WIDTH')

    cubes = {}
    headers = {}
    prim_head = []
    for key in keys:
        cubes['cube_' + key] = np.zeros([nt, ny, nx])
        headers['cube_' + key + '_head'] = []

    for i, file in enumerate(files):
        with fits.open(file) as hdul:
            prim_head.append(hdul[0].header)
            for key, obs_key in zip(keys, obs_keys):
                cubes['cube_' + key][i] = hdul[obs_key].data
                headers['cube_' + key + '_head'].append(hdul[obs_key].header)

    return {'data': cubes, 'headers': headers, 'primary_header': prim_head}


def cp_save_mask(mask: np.ndarray, date: str, name_addon: str = ''):
    """
    Save mask as a numpy save.

    Parameters
    -----------
    date - str
           date of observations
    """
    file_path = get_save_dir(date)
    file_name = '{0}/{1}_mask{2}.npy'.format(file_path, date, name_addon)

    np.save(file_name, mask)
    return True


def cp_load_mask(date: str, name_addon: str = ''):
    """
    Load the mask from a numpy save.

    Parameters
    -----------
    date - str
           date of observations
    """
    file_path = get_save_dir(date)
    file_name = '{0}/{1}_mask{2}.npy'.format(file_path, date, name_addon)

    if not os.path.isfile(file_name):
        print('Mask npy file not in path {0}'.format(file_name))

    return np.load(file_name)


def cp_save_angles(date: str, wave_angle: np.ndarray, name_addon: str = ''):
    """
    Save the wave angle map as a numpy save.

    Parameters
    -----------
    date - str
           date of observations
    """
    file_path = get_save_dir(date)
    file_name = '{0}/{1}_wave_angle{2}.npy'.format(file_path, date, name_addon)

    np.save(file_name, wave_angle)
    return True


def cp_load_angles(date: str, name_addon: str = ''):
    """
    Load the wave angles from a numpy save.

    parameters
    date - str
           date of observations
    """
    file_path = get_save_dir(date)
    file_name = '{0}/{1}_wave_angle{2}.npy'.format(file_path, date, name_addon)

    if not os.path.isfile(file_name):
        print('Wave angle npy file not in path {0}'.format(file_name))

    return np.load(file_name)


def cp_save_coh(date: str, coh: np.ndarray, name_addon: str = ''):
    """
    Save the coherence map as a numpy save.

    Parameters
    -----------
    date - str
           date of observations
    """
    file_path = get_save_dir(date)
    file_name = '{0}/{1}_coherence{2}.npy'.format(file_path, date, name_addon)

    np.save(file_name, coh)
    return True


def cp_load_coh(date: str, name_addon: str = ''):
    """
    Load the coherence map from a numpy save.

    Parameters
    -----------
    date - str
           date of observations
    """
    file_path = get_save_dir(date)
    file_name = '{0}/{1}_coherence{2}.npy'.format(file_path, date, name_addon)

    if not os.path.isfile(file_name):
        print('Coherence npy file not in path {0}'.format(file_name))

    return np.load(file_name)


def cp_save_cadence(cadence: int, date: str):
    """
    Save the cadence value as a numpy save.

    parameters
    cadence - float
              single value for cadence of observations
    date - str
           date of observations
    """
    file_path = get_save_dir(date)
    file_name = '{0}/{1}_cadence_value.npy'.format(file_path, date)

    np.save(file_name, cadence)
    return True


def cp_load_cadence(date: str):
    """
    Load the cadence value from a numpy save.

    parameters
    date - str
           date of observations
    """
    file_path = get_save_dir(date)
    file_name = '{0}/{1}_cadence_value.npy'.format(file_path, date)

    if not os.path.isfile(file_name):
        print('Cadence npy file not in path {0}'.format(file_name))

    return np.load(file_name)


def cp_save_filler_fits(fits_dict: dict, file_path: str, file_dir: str = None,
                        name_addon: str = 'comp.1074.dynamics.3'):
    """
    Save CoMP I, V, W cubes as multi-extension fits.

    """
    cubes = fits_dict['data']
    heads = fits_dict['headers']
    primary_heads = fits_dict['primary_header']

    keys = ['cube_i', 'cube_v', 'cube_w']

    for j, prim_head in enumerate(primary_heads):

        hdul = fits.HDUList()
        hdul.append(fits.PrimaryHDU(header=prim_head))

        for key in keys:
            hdul.append(fits.CompImageHDU(data=cubes[key][j],
                                          header=heads[key + '_head'][j])
                        )
        time = prim_head['TIME-OBS'].replace(':', '')
        date_file = prim_head['DATE-OBS'].replace('-', '')

        path_comps = [file_path, date_file, time, name_addon]
        save_to = '{0}/{1}.{2}.{3}.fts.gz'.format(*path_comps)
        hdul.writeto(save_to, overwrite=True)


def cp_save_pro_ret(date: str, prograde: np.ndarray,
                    retrograde: np.ndarray, name_addon: str = ''):
    """
    Save the filtered data as a numpy save.

    Parameters
    -----------
    date - str
           date of observations
    """
    file_path = get_save_dir(date)
    file_name = '{0}/{1}_pro_ret_cubes_{2}.npz'.format(file_path, date,
                                                       name_addon)

    np.savez(file_name, prograde=prograde, retrograde=retrograde)
    return True


def cp_load_pro_ret(date: str, name_addon: str = ''):
    """
    Load the cadence value from a numpy save.

    parameters
    date - str
           date of observations
    """
    file_path = get_save_dir(date)
    file_name = '{0}/{1}_pro_ret_cubes_{2}.npz'.format(file_path, date,
                                                       name_addon)

    if not os.path.isfile(file_name):
        print('Prograde/retrograde npz file not in path {0}'.format(file_name))
    data = np.load(file_name)
    prograde = data['prograde']
    retrograde = data['retrograde']
    return prograde, retrograde


def cp_save_speeds(date: str, speeds: dict, name_addon: str = ''):
    """
    Save the speed data as a numpy save.

    Parameters
    -----------
    date - str
           date of observations
    """
    file_path = get_save_dir(date)
    file_name = '{0}/{1}_wave_speeds_{2}.npz'.format(file_path, date,
                                                     name_addon)

    np.savez(file_name, **speeds)

    return True


def cp_load_speeds(date: str, name_addon: str = ''):
    """
    Load the cadence value from a numpy save.

    parameters
    date - str
           date of observations
    """
    file_path = get_save_dir(date)
    file_name = '{0}/{1}_wave_speeds_{2}.npz'.format(file_path, date,
                                                     name_addon)

    if not os.path.isfile(file_name):
        print('Wave speeds npz file not in path {0}'.format(file_name))
    data = np.load(file_name)

    speeds = {}
    for key in data.keys():
        speeds[key] = data[key]

    return speeds

# def cp_save(cubes, name_addon='', compress=False):
#     """
#     Saves CoMP I, V, W cubes as multi-extension fits and index,
#     mask as numpy arrays

#     """
#     gz = '' if not compress else '.gz'

#     outpath = cubes['index']['outpath']
#     date = cubes['index']['date']

#     for key in cubes:

#         # Saving index
#         if key == 'index' or key == 'mask':
#             save_to = '{0}{1}_{2}{3}.npy'.format(outpath, key, date,
#                                                  name_addon)
#             np.save(save_to, cubes[key])

#         else:
#             # Saving data files
#             dat = cubes[key]
#             hdul = fits.HDUList()
#             hdul.append(fits.PrimaryHDU())

#             for img in dat:
#                 hdul.append(fits.ImageHDU(data=img))

#             save_to = '{0}{1}_{2}{3}.fits{4}'.format(outpath, key, date,
#                                                      name_addon, gz)
#             hdul.writeto(save_to, overwrite=True)
#     return


# def cp_load(date,  name_addon='', compress=False, **kwargs):
#     """
#     Loads CoMP cubes (e.g. I, V, W) 
#     Always restores index and mask

#     @params
#     keys: string list of data products to read in, default is ['cube_i','cube_v','cube_w']
#           empty list will just read in associated index and mask
#     name_addon: If your file has a non-standard name (string)
#     compress: required if you want to read in fits.gz files, set equal to 1 for compressed
#     """
#     print('Loading in data')

#     keys = kwargs.pop('keys', ['cube_i', 'cube_v', 'cube_w'])
#     gz = '' if not compress else '.gz'

#     home = os.path.expanduser("~")
#     inpath = '{1}/analysis/CoMP/wave_tracking_output/{0}/'.format(date, home)

#     cubes = {}

#     # read in data files
#     for key in keys:
#         fname = '{0}{1}_{2}{3}.fits{4}'.format(inpath, key, date,
#                                                name_addon, gz)

#         if not os.path.isfile(fname):
#             #message =
#             print('Skipping {0}. File not in path {1}'.format(key, fname))
#             continue

#         with fits.open(fname) as hdul:

#             number_files = len(hdul)-1
#             for vals, hdu in enumerate(hdul):
#                 if vals == 0:
#                     continue  # Skip primary header

#                 hdu_data = hdu.data

#                 # Set up zero array to fill on first loop through
#                 if vals == 1:
#                     ny, nx = hdu_data.shape
#                     temp = np.zeros((number_files, ny, nx))

#                 temp[vals-1, :, :] = hdu_data

#                 del hdu_data
#                 del hdu.data

#         cubes[key] = temp

#     # read in extra files
#     for key in ['index', 'mask']:
#         fname = '{0}{1}_{2}{3}.npy'.format(inpath, key, date, name_addon)
#         if not os.path.isfile(fname):
#             print('Skipping {0}. File not in path {1}'.format(key, fname))
#             continue

#         if key == 'index':
#             # loads in dictionary
#             cubes[key] = np.load(fname, allow_pickle=True)[()]
#         else:
#             # loads in an array
#             cubes[key] = np.load(fname)

#     return cubes
