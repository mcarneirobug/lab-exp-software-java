import requests
import time
import constant
from datetime import datetime
from dateutil import relativedelta
import os
import os.path

import shutil
from python_loc_counter import LOCCounter
from git import Repo


def run_github_query(query):
    request = requests.post(f'{constant.URL}', json=query, headers=constant.HEADERS)
    while request.status_code != 200:
        print("Error calling the API, processing again...")
        print(f'The query failed: {request.status_code}. {json["query"]}, {json["variables"]}')
        time.sleep(2)
        request = requests.post(f'{constant.URL}', json=query, headers=constant.HEADERS)
    return request.json()


def csv_header():
    path = os.getcwd() + "\\" + constant.PATH_CSV
    with open(path, 'w+') as csv_final:
        csv_final.write("Name" + ";"
                        + "URL" + ";"
                        + "Primary Language" + ";"
                        + "Created At" + ";"
                        + "Repository Age" + ";"
                        + "Amount of stars" + ";"
                        + "Total amount of release(s)" + ";"
                        + "Total Source LOC" + ";"
                        + "Total Line LOC" + ";"
                        + "Total Comments LOC" + ";"
                        + "Total Blank LOC" + "\n")


def export_to_csv(data):
    path = os.getcwd() + "\\" + constant.PATH_CSV
    urls = ""
    for node in data:
        if node['primaryLanguage'] is None:
            primary_language = "None"
        else:
            primary_language = str(node['primaryLanguage']['name'])

        date_pattern = "%Y-%m-%dT%H:%M:%SZ"
        datetime_now = datetime.now()
        datetime_created_at = datetime.strptime(node['createdAt'], date_pattern)
        datetime_updated_at = datetime.strptime(node['updatedAt'], date_pattern)
        repository_age = relativedelta.relativedelta(datetime_now, datetime_created_at).years

        urls += node['url']

        with open(path, 'a+') as csv_final:
            csv_final.write(node['nameWithOwner'] + ";" +
                            node['url'] + ";" +
                            datetime_created_at.strftime('%d/%m/%y %H:%M:%S') + ";" +
                            str(repository_age) + ";" +
                            datetime_updated_at.strftime('%d/%m/%y %H:%M:%S') + ";" +
                            str(node['stargazers']['totalCount']) + ";" +
                            str(node['pullRequests']['totalCount']) + ";" +
                            str(node['releases']['totalCount']) + ";" +
                            primary_language + "\n")
    export_urls_to_txt(urls)


def export_urls_to_txt(list_urls):
    path = os.getcwd() + r"\urls_repos.txt"
    file = open(path, "w+")
    file.write(list_urls)
    file.close()


# The function delete an entire directory tree
def clean_repository(path_folder):
    shutil.rmtree(path_folder, ignore_errors=True)


def clone_repository(git_path, directory_path):
    print("\n" + f'Starting the git clone: {git_path}')
    try:
        success = os.system("git clone --depth 1 %s %s" % (git_path, directory_path))
        if success != 0:
            raise Exception("Error when cloning...")
        print(f'Finished git clone!\n')
    except Exception:
        print(f'Trying again...')
        clone_success = retry_clone_repository(git_path, directory_path)
        number_retries = 1
        while not clone_success and number_retries <= 5:
            clone_success = retry_clone_repository(git_path, directory_path)
            number_retries += 1


def retry_clone_repository(git_path, directory_path):
    try:
        success = os.system("git clone --depth 1 %s %s" % (git_path, directory_path))
        return success == 0
    except Exception:
        return False


# The flag is responsible for replacing the cursor on the next page
finalQuery = constant.QUERY.replace("{AFTER}", "")

json = {
    "query": finalQuery, "variables": {}
}

# Run application first time
total_pages = 1
print(f'Page -> {total_pages}')
response = run_github_query(json)

current_final_cursor = response["data"]["search"]["pageInfo"]["endCursor"]
has_next_page = response["data"]["search"]["pageInfo"]["hasNextPage"]
nodes = response["data"]["search"]["nodes"]

# 5 repositories * 200 pages = 1000 repositories
while total_pages < 200 and has_next_page:
    total_pages += 1
    print(f'Page -> {total_pages}')
    next_query = constant.QUERY.replace("{AFTER}", ', after: "%s"' % current_final_cursor)
    json["query"] = next_query
    response = run_github_query(json)
    # Increase the output
    nodes += response["data"]["search"]["nodes"]
    # Changes to the next page
    has_next_page = response["data"]["search"]["pageInfo"]["hasNextPage"]
    # Changes the cursor to the current
    current_final_cursor = response["data"]["search"]["pageInfo"]["endCursor"]

if __name__ == "__main__":
    csv_header()
    export_to_csv(nodes)
    print('#' * 100)
    print('\nSuccessfully generated csv file...')
