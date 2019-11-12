import os
import shutil
import json

from glob import glob

def read_context():
    with open('_context.json', 'r') as f:
        cxt = json.load(f)
    return cxt

def read_json_file(json_file):
    with open(json_file, 'r') as f:
        file_cxt = json.load(f)
    return file_cxt

def get_location_from_ds(ds_file):
    """
    Get GeoJSON polygon of union of IFGs.
    :param ds_file: .dataset.json file, which have the 'location' key
    :return: geojson of merged bbox
    """
    f = open(ds_file)
    ds = json.load(f)
    geojson = ds['location']
    return geojson

def get_dataset_met_json_files(cxt, pwd):
    """
    returns 2 lists: file paths for dataset.json files and met.json files
    :param cxt: json from _context.json
    :param pwd: path of work directory
    :return: str, str
    """
    if cxt['localize_urls'] != []:
        localize_url = cxt['localize_urls'][0]
        local_path = localize_url['url']
        coreg_slc_id = local_path.split('/')[-1]
        slc_path = os.path.join(pwd, coreg_slc_id, coreg_slc_id)
        ds_file = slc_path + '.dataset.json'
        met_file = slc_path + '.met.json'
    return ds_file, met_file

def get_insar_dir(pwd):
    '''
    get INSAR directory full path
    :param pwd: path of work directory
    :return: str
    '''
    insar_dir = []
    insar_dir_wildcard = pwd + "/INSAR_*"
    for dir in glob(insar_dir_wildcard):
        insar_dir.append(dir)
    insar_dir = insar_dir[0]
    return insar_dir

def remove_slcs_from_insar_dir(insar_dir):
    '''
    remove SLCs from INSAR directory
    :param insar_dir: str of INSAR directory full path
    '''
    date_wildcard = insar_dir + '/[0-9]*'
    for dir in glob(date_wildcard):
        shutil.rmtree(dir)
    return None

def get_min_max_timestamps(cxt, pwd):
    """
    returns the min timestamp and max timestamp of the stack
    :param cxt: json from _context.json
    :param pwd: path of work directory
    :return: (str, str) 2 timestamp strings, ex. 20190518T161611
    """
    localize_urls = cxt['localize_urls'][0]
    local_path = localize_urls['url']
    coreg_slc_id = local_path.split('/')[-1]
    parsed = coreg_slc_id.split('-')
    min_timestamp = parsed[-2]
    max_timestamp = parsed[-1]

    return min_timestamp, max_timestamp

def create_list_from_keys_json_file(json_file, *args):
    """
    gets all key values in each .json file and returns a sorted array of values
    :param json_file: str
    :return: list[]
    """
    values = set()
    f = open(json_file)
    data = json.load(f)
    for arg in args:
        value = data[arg]
        values.add(value)

    return sorted(list(values))

def generate_dataset_json_data(dataset_json_file, version):
    """
    :param cxt: _context.json file
    :param dataset_json_file: list[str] all file paths of SLC's .dataset.json files
    :param version: str: version, ex. v1.0
    :return: dict
    """
    dataset_json_data = dict()
    dataset_json_data['version'] = version
    sensing_timestamps = create_list_from_keys_json_file(dataset_json_file, 'starttime', 'endtime')
    dataset_json_data['starttime'] = min(sensing_timestamps)
    dataset_json_data['endtime'] = max(sensing_timestamps)
    dataset_json_data['location'] = get_location_from_ds(dataset_json_file)

    return dataset_json_data


def generate_met_json_data(cxt, met_json_file, dataset_json_file, version):
    """
    :param cxt: _context.json file
    :param met_json_file: stack met.json file
    :param dataset_json_file: stack dataset.json file
    :param version: version of dataset
    :return: dict
    """
    # load _job.json data to met.json
    job_json = read_json_file('_job.json')
    met_json_data = dict()
    met_json_data['job_params'] = job_json['params']['job_specification']['params']
    met_json_data['processing_start'] = job_json['job_info']['cmd_start']
    met_json_data['processing_end'] = job_json['job_info']['cmd_end']
    met_json_data['processing_duration'] = job_json['job_info']['cmd_duration']

    #load stack met.json to ps-timeseries met.json
    stack_met_json = read_json_file(met_json_file)
    met_json_data['direction'] = stack_met_json['direction']
    met_json_data['orbit_number'] = stack_met_json['orbit_number']
    met_json_data['track_number'] = stack_met_json['track_number']
    met_json_data['sensor'] = stack_met_json['sensor']
    met_json_data['platform'] = stack_met_json['platform']
    met_json_data['scene_count'] = stack_met_json['scene_count']

    # load stack dataset.json to ps-timeseries met.json
    stack_dataset_json = read_json_file(dataset_json_file)
    met_json_data['stack_id'] = stack_dataset_json['label']
    met_json_data['location'] = get_location_from_ds(dataset_json_file)

    # additional information
    met_json_data['version'] = version
    met_json_data['dataset_type'] = 'ps-time-series'

    return met_json_data
