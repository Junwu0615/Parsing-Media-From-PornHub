# -*- coding: utf-8 -*-
"""
@author: PC
Update Time: 2024-12-18
"""
from tqdm import tqdm
import os, requests, subprocess
from subprocess import PIPE, STDOUT
from concurrent.futures import ThreadPoolExecutor, wait

class ParsingMediaLogic:
    def __init__(self, obj):
        self.url = obj.url
        self.base_url = self.url.split('.mp4')[0] + '.mp4'
        self.path = os.getcwd() + '\\' + obj.path

        self.todo_dict = {}
        self.headers = ParsingMediaLogic.update_headers()
        self.session = requests.Session()
        self.timeout = 20

    @staticmethod
    def check_folder(path: str):
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)

    @staticmethod
    def update_headers() -> dict:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
            }
        return headers

    @staticmethod
    def progress_bar(task: str, symbol: str= '━'):
        if task == 'Args':
            print(f'Get Parameter... {symbol * 46} 100%')
        elif task == 'Get_Downloads_List':
            print(f'Get Downloads List... {symbol * 41} 100%')
        elif task == 'Finish_Task':
            print('Finish Task ! Exit Program ...')

    def remove_temp_file(self):
        for file in [i for i in os.listdir(self.path) if i.split('.')[-1] in ['ts', 'm3u8', 'txt']]:
            os.remove(self.path + '\\' + file)

    def use_executor(self, function_obj):
        get_inpt = str(input('是否使用 [非同步多執行緒] ?\n1: 使用 2: 不使用\n'))
        if get_inpt == '1':
            self.create_executor(function_obj)
        else:
            for target_name, file_name in tqdm(self.todo_dict.items(), position=0, desc='Downloads Schedule: '):
                ret = function_obj(target_name, file_name)
                if ret == -1:
                    check_list = list(self.todo_dict.keys())
                    print(f'下載過程有檔案未載成功: index[{check_list.index(target_name)}/{len(check_list)}]')
                    break

    def m3u8_processing(self):
        res = self.session.get(self.url, headers=self.headers, timeout=self.timeout)
        create_folder = len(os.listdir(self.path)) + 1
        self.path += f'\\Secret_{create_folder}'
        if not os.path.exists(self.path):
            ParsingMediaLogic.check_folder(self.path)

        # FIXME m3u8 串流媒體
        for i in [i for i in res.text.split('\n') if '#EXT' not in i and i != '']:
            if i not in self.todo_dict:
                self.todo_dict[i] = str(len(self.todo_dict) + 1) + '.ts'

        ParsingMediaLogic.progress_bar('Get_Downloads_List')
        self.use_executor(self.create_ts_media)
        self.combine_ts_to_mp4() # 合併 ts 檔並轉為 mp4
        self.remove_temp_file() # 是否刪除暫存檔

    def create_ts_media(self, target_name: str, file_name: str) -> int:
        ret = -1
        try:
            url = self.base_url + '/' + target_name
            res = self.session.get(url, headers=self.headers, timeout=self.timeout)
            if res.status_code == 200:
                with open(self.path + '\\' + file_name, 'wb') as f:
                    f.write(res.content)
                ret = 0
        except IOError as e:
            print(e)
        finally:
            return ret

    def combine_ts_to_mp4(self):
        with open(self.path + '\\media.txt', 'w') as f:
            for target_name, file_name in self.todo_dict.items():
                f.write(f"file '{file_name}'\n")

        cmdline = 'ffmpeg -f concat -i media.txt -c copy media.mp4'
        pop = subprocess.Popen(cmdline,
                               stdout=PIPE,
                               stderr=STDOUT,
                               cwd=self.path.lower(),
                               shell=True)

        while pop.poll() is None:
            line = pop.stdout.readline()
            try:
                line = line.decode('utf8')
                # print(line)

            except UnicodeDecodeError as e:
                pass
            except IOError as e:
                print(e)

    def create_executor(self, function_obj, max_workers: int=5):
        # FIXME 建立非同步的多執行緒的啟動器 -> 非同步下載檔案
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            new_task = {}
            task = {executor.submit(function_obj, target_name, file_name):
                        (target_name, file_name) for target_name, file_name in self.todo_dict.items()}

            schedule = tqdm(total=len(task), desc='Downloads Schedule: ')
            while len(task) > 0:
                callback, _ = wait(task, timeout=self.timeout, return_when='FIRST_COMPLETED')
                if callback != set():
                    for future in callback:
                        job = task[future]
                        ret = future.result()
                        del task[future]
                        if ret in [0]:
                            schedule.update(1)
                        elif ret in [-1]:
                            if future not in new_task:
                                new_task[future] = job  # 先儲存[需再 submit 的需求]
                        else:
                            pass

                        schedule.display()

                if len(task) == 0:
                    for future, job in new_task.items():
                        task[executor.submit(function_obj, job[0], job[1])] = job
                    new_task = {}

    def main(self):
        ParsingMediaLogic.check_folder(self.path)
        ParsingMediaLogic.progress_bar('Args')
        self.m3u8_processing()
        ParsingMediaLogic.progress_bar('Finish_Task')