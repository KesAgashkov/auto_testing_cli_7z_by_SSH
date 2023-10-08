import random
import string
import yaml
import pytest as pytest
from checks import ssh_checkout, ssh_getout
from datetime import datetime


# Задание 1.
#
# Условие:
# Дополнить проект фикстурой, которая после каждого шага теста дописывает в заранее созданный файл stat.txt строку вида:
# время, кол-во файлов из конфига, размер файла из конфига, статистика загрузки процессора из файла /proc/loadavg
# (можно писать просто всё содержимое этого файла).
#
# Задание 2. (дополнительное задание)
#
# Дополнить все тесты ключом команды 7z -t (тип архива). Вынести этот параметр в конфиг.

with open('config.yaml') as fy:
    data = yaml.safe_load(fy)


@pytest.fixture()
def make_folder():
    return ssh_checkout(data["host"], data["user"], data["passwd"],
        f'mkdir -p {data["folder_in"]} {data["folder_out"]} {data["folder_ext"]} {data["folder_ext3"]} {data["folder_bad"]}',
        "")


@pytest.fixture()
def clear_folder():
    return ssh_checkout(data["host"], data["user"], data["passwd"],
        f'rm -rf {data["folder_in"]}/* {data["folder_out"]}/* {data["folder_ext"]}/* {data["folder_ext3"]}/* {data["folder_bad"]}/*',
        "")


@pytest.fixture()
def make_files():
    list_files = []
    for i in range(data['count']):
        file_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        ssh_checkout(data["host"], data["user"], data["passwd"],f'cd {data["folder_in"]};'
                        f'dd if=/dev/urandom of={file_name} bs={data["bs"]} count=1 iflag=fullblock', '')
        list_files.append(file_name)

    return list_files


@pytest.fixture()
def make_subfolder():
    subfolder_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfile_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    if not ssh_checkout(data["host"], data["user"], data["passwd"], f'cd {data["folder_in"]}; mkdir {subfolder_name}', ''):
        return None, None
    if not  ssh_checkout(data["host"], data["user"], data["passwd"], f'cd {data["folder_in"]}/{subfolder_name}; '
                    f'dd if=/dev/urandom of={subfile_name} bs={data["bs"]} count=1 iflag=fullblock', ''):
        return subfolder_name, None

    return subfolder_name, subfile_name


@pytest.fixture()
def create_bad_archive():
    ssh_checkout(data["host"], data["user"], data["passwd"], f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx2.{data["exten"]}', "Everything is Ok")
    ssh_checkout(data["host"], data["user"], data["passwd"], f'cp {data["folder_out"]}/arx2.{data["exten"]} {data["folder_bad"]}/arx2.{data["exten"]}', '')
    ssh_checkout(data["host"], data["user"], data["passwd"], f'truncate -s 1 {data["folder_bad"]}/arx2.{data["exten"]}', '')  # сделали битым



@pytest.fixture(autouse=True)
def add_log_info():
    d = f"time = {datetime.now().strftime('%H:%M:%S.%f')} count = {data['count']} size = {data['bs']}" \
        f" host:port = {data['host']}:22, user = {data['user']}\n"
    with open("stat.txt", "a") as file_name:
        file_name.write(d)

