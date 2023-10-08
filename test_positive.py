import yaml
from checks import ssh_checkout,  ssh_getout

with open('config.yaml') as fy:
    data = yaml.safe_load(fy)

class TestPositive:

    def test_add_archive(self, make_folder, clear_folder, make_files):  # a создали архив
        res_add = ssh_checkout(data["host"], data["user"], data["passwd"],
                               f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx2.{data["exten"]}',
                               "Everything is Ok")
        res_ls = ssh_checkout(data["host"], data["user"], data["passwd"], f'ls {data["folder_out"]}', f"arx2.{data['exten']}")
        assert res_add and res_ls
        

    def test_check_e_extract(self, clear_folder, make_files):  #
        res = list()
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"], f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx2.{data["exten"]}', "Everything is Ok"))
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"],f'cd {data["folder_out"]}; 7z e arx2.{data["exten"]} -o{data["folder_ext"]} -y', "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(data["host"], data["user"], data["passwd"], f'ls {data["folder_ext"]}', item))
        assert all(res)
        

    def test_check_e_extract_subfolder(self, clear_folder, make_files, make_subfolder):
        res = list()
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"], f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx2.{data["exten"]}', "Everything is Ok"))
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"], f'cd {data["folder_out"]}; 7z e arx2.{data["exten"]} -o{data["folder_ext"]} -y', "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(data["host"], data["user"], data["passwd"], f'ls {data["folder_ext"]}', item))
        for item in make_subfolder:
            res.append(ssh_checkout(data["host"], data["user"], data["passwd"], f'ls {data["folder_ext"]}', item))
        assert all(res)
        

    def test_check_x_extract_subfolder(self, clear_folder, make_files, make_subfolder):
        # files, subflder and files in subfolder
        res = list()
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"], f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx2.{data["exten"]}', "Everything is Ok"))
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"], f'cd {data["folder_out"]}; 7z x arx2.{data["exten"]} -o{data["folder_ext"]} -y', "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(data["host"], data["user"], data["passwd"], f'ls {data["folder_ext"]}', item))
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"], f'ls {data["folder_ext"]}', make_subfolder[0]))
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"], f'ls {data["folder_ext"]}/{make_subfolder[0]}', make_subfolder[1]))
        assert all(res)
        

    def test_check_x_files(self, clear_folder, make_files):  # only files
        res = list()
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"], f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx2.{data["exten"]}', "Everything is Ok"))
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"], f'cd {data["folder_out"]}; 7z x arx2.{data["exten"]} -o{data["folder_ext"]} -y', "Everything is Ok"))
        for item in make_files:
            res.append(ssh_checkout(data["host"], data["user"], data["passwd"], f'ls {data["folder_ext"]}', item))
        assert all(res)
        

    def test_totality(self, clear_folder, make_files):  # t проверка целостности архива
        res = list()
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"], f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx2.{data["exten"]}', "Everything is Ok"))
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"], f'cd {data["folder_out"]}; 7z t arx2.{data["exten"]}', "Everything is Ok"))
        assert all(res)
        

    def test_delete(self, clear_folder, make_files, make_subfolder):  # d удаление из архива
        res = list()
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"], f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx2.{data["exten"]}', "Everything is Ok"))
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"], f'cd {data["folder_out"]}; 7z d arx2.{data["exten"]}', "Everything is Ok"))
        assert all(res)
        

    def test_update(self):  # u - обновление архива
        assert ssh_checkout(data["host"], data["user"], data["passwd"], f'cd {data["folder_in"]}; 7z u {data["folder_out"]}/arx2.{data["exten"]}', "Everything is Ok"), 'NO update'


    def test_nonempty_archive(self, clear_folder, make_files):
        res = list()
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"], f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx2.{data["exten"]}', "Everything is Ok"))
        res.append(ssh_checkout(data["host"], data["user"], data["passwd"], f'cd {data["folder_out"]}; 7z l arx2.{data["exten"]}', f'{len(make_files)} files'))


    def test_check_hash(self):
        hash_crc32 = ssh_getout(data["host"], data["user"], data["passwd"], f'cd {data["folder_out"]}; crc32 arx2.{data["exten"]}')
        res_upper = ssh_checkout(data["host"], data["user"], data["passwd"], f'cd {data["folder_out"]}; 7z h arx2.{data["exten"]}', hash_crc32.upper())
        res_lower = ssh_checkout(data["host"], data["user"], data["passwd"], f'cd {data["folder_out"]}; 7z h arx2.{data["exten"]}', hash_crc32.lower())
        with open("stat.txt", "a") as file_name:
            file_name.write("\n")
        assert res_lower or res_upper, 'NO equal hash'


