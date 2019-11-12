from utils import *

if __name__ == '__main__':
    VERSION = 'v1.0'
    DATASET_NAMING_TEMPLATE = 'standard_product-ps-timeseries-{min_timestamp}-{max_timestamp}'
    PWD = os.getcwd()

    # creating list of all SLC stack .dataset.json and .met.json files
    context_json = read_context()
    dataset_json_file, met_json_file = get_dataset_met_json_files(context_json, PWD)

    # getting list of SLC scenes and extracting min max timestamp
    min_timestamp, max_timestamp = get_min_max_timestamps(context_json, PWD)

    # creating dataset directory
    dataset_name = DATASET_NAMING_TEMPLATE.format(min_timestamp=min_timestamp, max_timestamp=max_timestamp)
    if not os.path.exists(dataset_name):
        os.mkdir(dataset_name)

    # remove SLCs from INSAR directory and move INSAR directory to dataset directory
    insar_dir = get_insar_dir(PWD)
    remove_slcs_from_insar_dir(insar_dir)
    if os.path.exists(insar_dir):
        shutil.move(insar_dir, dataset_name)

    # move _stdout.txt log file to dataset
    shutil.copyfile('_stdout.txt', os.path.join(dataset_name, '_stdout.txt'))

    # generate .dataset.json data
    dataset_json_data = generate_dataset_json_data(dataset_json_file, VERSION)
    dataset_json_data['label'] = dataset_name
    print(json.dumps(dataset_json_data, indent=2))

    # generate .met.json data
    met_json_data = generate_met_json_data(context_json, met_json_file, dataset_json_file, VERSION)
    print(json.dumps(met_json_data, indent=2))

    # writing .dataset.json to file
    dataset_json_filename = os.path.join(PWD, dataset_name, dataset_name + '.dataset.json')
    with open(dataset_json_filename, 'w') as f:
        json.dump(dataset_json_data, f, indent=2)

    # writing .met.json to file
    met_json_filename = os.path.join(PWD, dataset_name, dataset_name + '.met.json')
    with open(met_json_filename, 'w') as f:
        json.dump(met_json_data, f, indent=2)