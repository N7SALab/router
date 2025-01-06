import os
import json
import pandas
import automon

HAR_PATH_FOLDER = '/Users/eric/Downloads'
HAR_PATH_FILES = []
HAR_PATH_FILES_LOADED = []
HAR_PATH_EXTENSION = 'har'

HAR_DATA_URLS = []
HAR_DATA_DOMAINS = []


def find_har_files_in_current_dir(HAR_PATH_FOLDER: str) -> list:
    HAR_PATH_FILES = []

    for this_path, this_path_folders, this_path_files in os.walk(HAR_PATH_FOLDER):
        for selected_file in this_path_files:
            if HAR_PATH_EXTENSION == selected_file[-3:].lower():
                HAR_PATH_FILES.append(os.path.join(HAR_PATH_FOLDER, selected_file))

    return HAR_PATH_FILES


def load_har_files(HAR_PATH_FILES: list) -> list:
    HAR_PATH_FILES_LOADED = []

    for har_file in HAR_PATH_FILES:
        HAR_PATH_FILES_LOADED.append(dict(
            har_file=har_file,
            har_data=json.load(open(har_file, 'r'))
        ))

    return HAR_PATH_FILES_LOADED


def parsed_har_entries(har_data: dict) -> list:
    return har_data['log']['entries']


def parsed_har_request_url(entry: dict) -> str:
    return entry['request']['url']


def parsed_har_urls(HAR_PATH_FILES_LOADED: list) -> list:
    HAR_DATA_URLS = []

    for har_file_loaded in HAR_PATH_FILES_LOADED:

        har_file = har_file_loaded['har_file']
        har_data = har_file_loaded['har_data']

        for har_entry in parsed_har_entries(har_data=har_data):
            HAR_DATA_URLS.append(dict(
                har_file=har_file,
                request_url=parsed_har_request_url(har_entry)
            ))

    return HAR_DATA_URLS


def parsed_har_domains(HAR_DATA_URLS: list) -> list:
    HAR_DATA_DOMAINS = []

    for har_data_url in HAR_DATA_URLS:
        har_file = har_data_url['har_file']
        request_url = har_data_url['request_url']

        har_hostname = automon.Networking.urlparse(request_url).hostname
        try:
            har_domain = '.'.join(har_hostname.split('.')[-2:])
        except:
            pass

        if har_hostname not in [x['har_hostname'] for x in HAR_DATA_DOMAINS]:
            HAR_DATA_DOMAINS.append(dict(
                har_file=har_file,
                har_hostname=har_hostname,
                har_domain=har_domain
            ))

    return HAR_DATA_DOMAINS


def main():
    HAR_PATH_FILES = find_har_files_in_current_dir(HAR_PATH_FOLDER=HAR_PATH_FOLDER)
    HAR_PATH_FILES_LOADED = load_har_files(HAR_PATH_FILES=HAR_PATH_FILES)
    HAR_DATA_URLS = parsed_har_urls(HAR_PATH_FILES_LOADED=HAR_PATH_FILES_LOADED)
    HAR_DATA_DOMAINS = parsed_har_domains(HAR_DATA_URLS=HAR_DATA_URLS)
    HAR_DATA_DOMAINS_UNIQUE = sorted(set([x['har_domain'] for x in HAR_DATA_DOMAINS]))

    df = pandas.DataFrame(HAR_DATA_DOMAINS)
    df2 = pandas.DataFrame(HAR_PATH_FILES_LOADED)

    pass


if __name__ == '__main__':
    main()
