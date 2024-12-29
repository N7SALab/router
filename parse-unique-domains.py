import os
import json
import automon

HAR_PATH_FOLDER = '/Users/eric/Downloads'
HAR_PATH_FILES = []
HAR_PATH_FILES_LOADED = []
HAR_PATH_EXTENSION = 'har'

HAR_DATA_URLS = []
HAR_DATA_DOMAINS = []

for this_path, this_path_folders, this_path_files in os.walk(HAR_PATH_FOLDER):
    for selected_file in this_path_files:
        if HAR_PATH_EXTENSION == selected_file[-3:].lower():
            HAR_PATH_FILES.append(os.path.join(HAR_PATH_FOLDER, selected_file))

for har_file in HAR_PATH_FILES:
    HAR_PATH_FILES_LOADED.append(dict(
        har_file=har_file,
        har_data=json.load(open(har_file, 'r'))
    ))


def parsed_har_request_url(entry: dict) -> str:
    return entry['request']['url']


def parsed_har_entries(har_data: dict) -> list:
    return har_data['log']['entries']


for har_file_loaded in HAR_PATH_FILES_LOADED:

    har_file = har_file_loaded['har_file']
    har_data = har_file_loaded['har_data']

    for har_entry in parsed_har_entries(har_data=har_data):
        HAR_DATA_URLS.append(dict(
            har_file=har_file,
            request_url=parsed_har_request_url(har_entry)
        ))

for har_data_url in HAR_DATA_URLS:
    har_file = har_data_url['har_file']
    request_url = har_data_url['request_url']

    har_hostname = automon.Networking.urlparse(request_url).hostname
    har_domain = '.'.join(har_hostname.split('.')[-2:])

    if har_hostname not in [x['har_hostname'] for x in HAR_DATA_DOMAINS]:
        HAR_DATA_DOMAINS.append(dict(
            har_file=har_file,
            har_hostname=har_hostname,
            har_domain=har_domain
        ))

pass
