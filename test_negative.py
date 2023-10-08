import pytest

from checks import ssh_checkout_negative
import yaml

# folder_in = '/home/user/tst'
# folder_out = '/home/user/out'
# folder_ext = '/home/user/folder1'
# folder_bad = '/home/user/folder2'

with open('config.yaml') as fy:
    data = yaml.safe_load(fy)


class TestNegative:
    def test_negative1(self, make_folder, clear_folder, make_files, create_bad_archive):  # e извлекли из архива

        assert ssh_checkout_negative(data["host"], data["user"], data["passwd"], f'cd {data["folder_bad"]}; 7z e arx2.{data["exten"]} -o{data["folder_ext"]} -y', "ERROR")

    def test_negative2(self, make_folder, clear_folder, make_files,
                       create_bad_archive):  # t проверка целостности архива
        assert ssh_checkout_negative(data["host"], data["user"], data["passwd"], f'cd {data["folder_bad"]}; 7z t arx2.{data["exten"]}', "ERROR")



if __name__ == '__main__':
    pytest.main(['-vv'])