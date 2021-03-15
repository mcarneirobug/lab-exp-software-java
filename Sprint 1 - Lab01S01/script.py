import requests
import time
import constant
from datetime import datetime
from dateutil import relativedelta
import os
import os.path

import shutil
import stat
from python_loc_counter import LOCCounter
import pandas as pd


# The function responsible for making requests in GitHub API
def run_github_query(json):
    request = requests.post(f'{constant.URL}', json=json, headers=constant.HEADERS)
    while request.status_code != 200:
        print("Error calling the API, processing again...")
        print(f'The query failed: {request.status_code}. {json["query"]}, {json["variables"]}')
        time.sleep(2)
        request = requests.post(f'{constant.URL}', json=json, headers=constant.HEADERS)
    return request.json()


# The function responsible for saving GitHub repository urls in .txt file
def export_urls_to_txt(urls_git_to_save_file):
    path = os.getcwd() + r"\urls_repos.txt"
    file = open(path, "w+")
    file.write(urls_git_to_save_file)
    file.close()


def on_rm_error(func, path, exc_info):
    # path contains the path of the file that couldn't be removed
    # let's just assume that it's read-only and unlink it.
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)


# The function delete an entire directory tree
def clean_repository(path_folder):
    try:
        shutil.rmtree(path_folder, onerror=on_rm_error)
    except Exception as e:
        print(e)
        print(f'\nThe directory {path_folder} cannot be deleted. Erase manually!')


def call_ck_metrics(project_dir):
    print(f'\nCalculating metrics using ck...')
    try:
        success = os.system("java -jar ck-0.6.4-SNAPSHOT-jar-with-dependencies.jar %s 1 0 0" % project_dir)
        if success != 0:
            raise Exception("Error when apply metrics...")
        return success == 0
    except Exception as e:
        print(e)


def calculate_age_repository(datetime_created_at):
    return relativedelta.relativedelta(datetime.now(), datetime_created_at).years


def clone_repository(git_path, directory_path):
    print(f'\nStarting the git clone: ({git_path})')
    try:
        success = os.system("git clone --depth 1 %s %s" % (git_path, directory_path))
        if success != 0:
            raise Exception("Error when cloning...")
        print(f'Finished git clone!\n')
    except Exception as e:
        print(e)
        print(f'\nTrying again...')
        clone_success = retry_clone_repository(git_path, directory_path)  # trying to clone again
        number_retries = 1
        retries = 5
        while not clone_success and number_retries <= retries:
            clone_success = retry_clone_repository(git_path, directory_path)
            number_retries += 1


def retry_clone_repository(git_path, directory_path):
    try:
        success = os.system("git clone --depth 1 %s %s" % (git_path, directory_path))
        return success == 0
    except Exception as e:
        print(f'An exception occurred in making the clone: {e}')
        return False


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
                        + "Total Blank LOC" + ";"
                        + "Total Comments LOC" + ";"
                        + "CBO" + ";"
                        + "DIT" + ";"
                        + "WMC" + ";"
                        + "LOC" +
                        "\n")


def isPrimaryLanguage(node):
    if node['primaryLanguage'] is None:
        return "None"
    else:
        return str(node['primaryLanguage']['name'])


def export_to_csv(data):
    path = os.getcwd() + "\\" + constant.PATH_CSV
    urls_git_to_save_file = ""
    num_repositories = 0
    result = {'source_loc': 0, 'single_comments_loc': 0, 'single_docstring_loc': 0,
              'double_docstring_loc': 0, 'total_comments_loc': 0, 'blank_loc': 0, 'total_line_count': 0,
              'cbo': 0, 'dit': 0, 'wmc': 0, 'loc': 0}
    for node in data:

        datetime_created_at = datetime.strptime(node['createdAt'], '%Y-%m-%dT%H:%M:%SZ')

        urls_git_to_save_file += node['url'] + '\n'  # to save urls at .txt file

        repo_path = f'repository\\java\\{str(num_repositories)}'
        if os.path.exists(repo_path):
            clean_repository(repo_path)

        num_repositories += 1  # incrementing to count next repository

        git_path = node['url'] + ".git"  # ex: https://github.com/mcarneirobug/lab-exp-software-java.git
        clone_repository(git_path, repo_path)

        call_ck_metrics(repo_path)
        metrics_df = pd.read_csv(os.path.abspath(os.getcwd()) + "/class.csv", usecols=['cbo', 'dit', 'wmc', 'loc'])
        medians = metrics_df.median(skipna=True)

        if os.path.exists(repo_path):
            for root, dirs, files in os.walk(repo_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    try:
                        counter = LOCCounter(full_path)
                        loc_data = counter.getLOC()
                        for key in loc_data:
                            if key in result:
                                result[key] += loc_data[key]
                            else:
                                result[key] += loc_data[key]
                    except Exception as e:
                        print(e)
                        print(f'Error to read file {full_path}. Trying read again...')
                        continue

                    result['cbo'] = medians['cbo']
                    result['dit'] = medians['dit']
                    result['wmc'] = medians['wmc']
                    result['loc'] = medians['loc']
                    print(loc_data)

        clean_repository(repo_path)

        with open(path, 'a+') as csv_final:
            csv_final.write(node['nameWithOwner'] + ";"
                            + node['url'] + ";"
                            + isPrimaryLanguage(node) + ";"
                            + datetime_created_at.strftime('%d/%m/%y %H:%M:%S') + ";"
                            + str(calculate_age_repository(datetime_created_at)) + ";"
                            + str(node['stargazers']['totalCount']) + ";"
                            + str(node['releases']['totalCount']) + ";"
                            + str(result['source_loc']) + ";"
                            + str(result['total_line_count']) + ";"
                            + str(result['blank_loc']) + ";"
                            + str(result['total_comments_loc']) + ";"
                            + str(result['cbo']) + ";"
                            + str(result['dit']) + ";"
                            + str(result['wmc']) + ";"
                            + str(result['loc'])
                            + "\n")
    export_urls_to_txt(urls_git_to_save_file)


def run():
    # The flag is responsible for replacing the cursor on the next page
    final_query = constant.QUERY.replace("{AFTER}", "Y3Vyc29yOjQwMA==")

    json = {
        "query": final_query, "variables": {}
    }

    # Run application first time
    total_pages = 1
    print(f'Page -> {total_pages}')
    response = run_github_query(json)

    current_final_cursor = response["data"]["search"]["pageInfo"]["endCursor"]
    has_next_page = response["data"]["search"]["pageInfo"]["hasNextPage"]
    nodes = response["data"]["search"]["nodes"]

    # 5 repositories * 200 pages = 1000 repositories
    while total_pages < 100 and has_next_page:
        total_pages += 1
        print(f'Page -> {total_pages}')
        next_query = constant.QUERY.replace("{AFTER}", "%s" % current_final_cursor)
        json["query"] = next_query
        response = run_github_query(json)
        # Increase the output
        nodes += response["data"]["search"]["nodes"]
        # Changes to the next page
        has_next_page = response["data"]["search"]["pageInfo"]["hasNextPage"]
        # Changes the cursor to the current
        current_final_cursor = response["data"]["search"]["pageInfo"]["endCursor"]
    csv_header()
    export_to_csv(nodes)


if __name__ == "__main__":
    run()
    print('#' * 100)
    print('\nSuccessfully generated csv file...')
