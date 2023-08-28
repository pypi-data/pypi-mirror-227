"""
This module is used to:
  Auto-generate the test case list based on the .csv and corresponding .py files.

If you need to use a dataSet (currently only supporting CSV format), please define it as follows:
  1. Create a CSV file using a comma ("," or '\t') as the separator.
  2. In the same directory as the CSV file, create a .py file with the same name. This .py file must define a `run_test(self, param...)` method.

For example:
  1. testLogin.csv file content:
        username,password
        user1,password1
        user2,password2

  2. testLogin.py file content:
        from common.test_login import login  # Import the specific business logic handling method

        def run_my_test(self, username, password):  # Define the received parameters (parameters must be defined in the CSV columns)
            self.logger.info("start run_test()...")
            login(self, username, password)

  -----> If executed correctly, the framework will generate a file (testLogin_case_list_auto_generated_by_csv.py) that conforms to the framework's running standards based on testLogin.csv and testLogin.py.

  Note: Similar to the __init__.py file, each time the script is executed, it will generate the latest auto_generated_by_csv.py file based on the corresponding .csv and .py files.

  The content of testLogin_case_list_auto_generated_by_csv.py:

      from linktest.api_testcase import APITestCase
      from tests.api.csv_dataset import testLoginDataSet

      class testLoginDataSet_1(APITestCase):
          tag = "testLoginDataSet"

          def run_test(self):
              username = 'user1'
              password = 'password1'

              testLoginDataSet.run_test(self, username, password)

      class testLoginDataSet_2(APITestCase):
          tag = "testLoginDataSet"

          def run_test(self):
              username = 'user2'
              password = 'password2'

              testLoginDataSet.run_test(self, username, password)

@author: Wang Lin
"""

import os
import csv
import traceback

from . import get_project_info


PROJECT_INFO = get_project_info.get_project_info()
TESTS_PACKAGE_PATH = PROJECT_INFO.project_path + os.sep + PROJECT_INFO.testcase_package_name

try:
    import settings
except ImportError:
    traceback.print_exc()
import re

def generate_testcase_list_by_csv_old(file_name, row, index, is_ui_testcase, tag_name=''):
    py_file_name = file_name.split(".")[0] + ".py"

    # 先 解析 py 文件,检测 文件中是否包含 def run_test(self, param1, param2 ...) 方法定义， 否则提示用户必须按照这种规范来写 dataSet（csv)的testcase
    with open(py_file_name, "r", encoding='utf-8') as py_file_obj:
        has_run_test_func_flag = False

        for line in py_file_obj.readlines():
            if line.startswith("def ") and line.__contains__("run_test") and line.__contains__("(") and \
                    line.__contains__(")") and line.__contains__(":") and not line.strip().startswith("#") \
                    and line.replace(" ", "").startswith("defrun_test(self,"):
                has_run_test_func_flag = True
                break

        if not has_run_test_func_flag:
            errInfo = """
            %s 文件 不符合如下规范！ 请检查更新后重新运行！
            如果需要使用 dataSet(目前只支持CSV格式）,请按照如下方式定义：
            1. 定义一个 csv文件, 并且必须以","作为分隔符
            2. 在csv文件的同级目录下定义一个 和csv文件同名的.py文件，py文件中必须定义一个 run_test(self, param...)方法
            参考如下：
               1. testLogin.csv 文件如下：
                   channel,username,password
                    web,"admin1","admin1"
                    web,admin2,"admin2"
                    web,user1,user2
                    app,admin1,admin1
                    app,admin2,admin2
                    
               2. testLogin.py文件内容如下：
                    from common.test_login import login # 引入的具体业务逻辑处理方法
        
                    def run_my_test(self, username, password, channel): # 定义接受的参数（此处接收的参数都必须定义在csv中--列名）
                        self.logger.info("start run_test()...") 
                        login(self, username, password, channel)
                        
              -----> 如果正确运行后，框架会根据 testLogin.csv & testLogin.py 自动生成符合框架运行标准的 auto_generated_by_csv.py文件（testLogin_case_list_auto_generated_by_csv.py）
                注意：和__init__.py文件类似，每次执行，都会根据相应的 .csv & .py文件自动生成最新的 auto_generated_by_csv.py文件
              testLogin_case_list_auto_generated_by_csv.py 内容如下：
              
                from linktest.api_testcase import APITestCase
                from tests.api.csv_dataset import testLoginDataSet
                
                
                class testLoginDataSet_1(APITestCase):
                    tag = "testLoginDataSet"
                
                    def run_test(self):
                        username = 'admin1'
                        password = 'admin1'
                
                        testLoginDataSet.run_test(self, username, password)
                
                
                class testLoginDataSet_2(APITestCase):
                    tag = "testLoginDataSet"
                
                    def run_test(self):
                        username = 'admin2'
                        password = 'admin2'
                
                        testLoginDataSet.run_test(self, username, password)
                
                
                class testLoginDataSet_3(APITestCase):
                    tag = "testLoginDataSet"
                
                    def run_test(self):
                        username = 'user1'
                        password = 'user2'
                
                        testLoginDataSet.run_test(self, username, password)
                
                
                class testLoginDataSet_4(APITestCase):
                    tag = "testLoginDataSet"
                
                    def run_test(self):
                        username = 'admin1'
                        password = 'admin1'
                
                        testLoginDataSet.run_test(self, username, password)
                
                
                class testLoginDataSet_5(APITestCase):
                    tag = "testLoginDataSet"
                
                    def run_test(self):
                        username = 'admin2'
                        password = 'admin2'
                
                        testLoginDataSet.run_test(self, username, password)
                              
            """ % py_file_name
            raise NotImplementedError(errInfo)

    with open(py_file_name, "r", encoding='utf-8') as py_file_obj:
        contents = py_file_obj.readlines()
        new_file_lines = []
        i = 0

        while i < len(contents):
            line = contents[i]

            if line.startswith("def ") and line.__contains__("(") and line.__contains__(":") and \
                    line.__contains__("run_test") and not line.strip().startswith("#"):
                class_name = py_file_name.split(".")[0].split(os.sep)[-1]
                # class_name = "".join(class_name[:1].upper() + class_name[1:]) # todo: 讨论是否需要把clasName首字母转成大写？
                if is_ui_testcase:
                    new_file_lines.append("\n\n\nclass %s_%s(UITestCase):\n" % (class_name, index))
                else:
                    new_file_lines.append("\n\n\nclass %s_%s(APITestCase):\n" % (class_name, index))
                new_file_lines.append('    tag = "%s, %s"\n\n' % (class_name, tag_name))
                param_list = line.replace(" ", "").split("self,")[1].split(")")[0].split(",")
                line = "    def run_test(self):"
                new_file_lines.append(line)

                temp_params_str = ""
                for param in param_list:
                    new_file_lines.append("\n        %s = '%s'" % (param, row[param]))
                    temp_params_str += ", " + param

                new_file_lines.append(
                    "\n\n        %s.run_test(self%s)" % (py_file_name.split(".")[0].split(os.sep)[-1], temp_params_str))
                break

            i += 1

    with open(file_name.split(".")[0] + "_case_list_auto_generated_by_csv.py", "a") as f:
        f.writelines(new_file_lines)

def process_csv_file(csv_file_full_path, is_ui_testcase, tag_name=''):
    with open(csv_file_full_path) as f:
        f_csv = csv.DictReader(f, delimiter=getattr(settings, 'delimiter_in_csv', ","))
        reversed_f_csv = [row for row in f_csv][::-1]
        generate_testcase_list_by_csv(csv_file_full_path, reversed_f_csv, is_ui_testcase, tag_name=tag_name)


def generate_testcase_list_by_csv(file_name, rows, is_ui_testcase, tag_name=''):
    # Define regex pattern for function validation
    run_test_pattern = re.compile(r'^def run_test\(self,.*\):')

    py_file_name = file_name.split(".")[0] + ".py"
    contents = open(py_file_name, "r", encoding='utf-8').readlines()
    if not any(run_test_pattern.match(line) for line in contents):
        raise NotImplementedError(f"{py_file_name} does not contain a valid 'run_test' function.")

    class_name = py_file_name.split(".")[0].split(os.sep)[-1]
    new_file_lines = []
    for index, row in enumerate(rows, 1):
        # Generate a class for each row
        if is_ui_testcase:
            new_file_lines.append(f"\n\nclass {class_name}_{index}(UITestCase):\n")
        else:
            new_file_lines.append(f"\n\nclass {class_name}_{index}(APITestCase):\n")
        new_file_lines.append(f'    tag = "{class_name}, {tag_name}"\n\n')

        # Generate a run_test function for each row
        new_file_lines.append("    def run_test(self):\n")
        for param, value in row.items():
            new_file_lines.append(f"        {param} = '{value}'\n")

        new_file_lines.append(f"\n        {class_name}.run_test(self, {', '.join(row.keys())})")

    # Write all lines to the output Python file
    with open(file_name.split(".")[0] + "_case_list_auto_generated_by_csv.py", "a") as f:
        f.writelines(new_file_lines)

def auto_generate_testcase_list_from_csv(call_by_doctor=False):
    print("start to auto_generate_testcase_list_from_csv")

    # fetch all the test cases which in tests package and organize test cases
    for directory_path, directory_names, file_names in os.walk(TESTS_PACKAGE_PATH, topdown=True):
        csv_files = []

        directory_path = directory_path.replace(PROJECT_INFO.project_path + os.sep, "")

        for file_name in file_names:
            file_full_name = os.path.join(directory_path, file_name)
            if file_full_name.startswith(PROJECT_INFO.testcase_package_name + os.sep + "android" + os.sep):
                continue

            if file_full_name.split(".")[-1] == "csv":
                csv_files.append(file_full_name.split(".csv")[0].split(os.sep)[-1])

        # 如果存在csv文件 才有必要继续判断是否有对应的python文件
        if len(csv_files) > 0:
            for file_name in file_names:
                if file_name.split(".")[-1] == "py" and file_name != "__init__.py" and\
                        file_name.split(".")[0] in csv_files:
                    has_run_test_flag = False

                    with open(PROJECT_INFO.project_path + os.sep + directory_path + os.sep + file_name.split(".")[
                        0] + ".py", "r", encoding='utf-8') as py_file_obj:

                        for line in py_file_obj.readlines():
                            if line.startswith("def run_test(self,"):
                                has_run_test_flag = True
                                break

                    if not has_run_test_flag:
                        print("py文件:%s 格式不符合要求! --- 不会自动生成对应的testcase文件" % file_name)
                        print("""
如果需要使用 dataSet(目前只支持CSV格式）,请按照如下方式定义：
    1. 定义一个 csv文件，支持以 ’,‘ 或者 ’\t‘ 作为分隔符 (二选一，可以在setting/__init__.py中显示指定 delimiter_in_csv = '\t',默认值为 ‘,’)
    2. 在csv文件的同级目录下定义一个和csv文件同名的.py文件, py文件中必须定义一个 run_test(self, param...)方法
    参考如下：
       1. testLogin.csv 文件如下(该csv文件以英文逗号作为分隔符)：
           channel,username,password
            web,"admin1","admin1"
            web,admin2,"admin2"
            web,user1,user2
            app,admin1,admin1
            app,admin2,admin2

       2. testLogin.py文件内容如下：
            from common.test_login import login # 引入的具体业务逻辑处理方法

            def run_my_test(self, username, password, channel): # 定义接受的参数（此处接收的参数都必须定义在csv中--列名）
                self.logger.info("start run_test()...")
                login(self, username, password, channel)

      -----> 如果正确运行后，框架会根据 testLogin.csv & testLogin.py 自动生成符合框架运行标准的 auto_generated_by_csv.py文件（testLogin_case_list_auto_generated_by_csv.py）
        注意：和__init__.py文件类似，每次执行，都会根据相应的 .csv & .py文件自动生成最新的 auto_generated_by_csv.py文件
      testLogin_case_list_auto_generated_by_csv.py 内容如下：

        from linktest.api_testcase import APITestCase
        from tests.api.csv_dataset import testLoginDataSet


        class testLoginDataSet_1(APITestCase):
            tag = "testLoginDataSet"

            def run_test(self):
                username = 'admin1'
                password = 'admin1'

                testLoginDataSet.run_test(self, username, password)


        class testLoginDataSet_2(APITestCase):
            tag = "testLoginDataSet"

            def run_test(self):
                username = 'admin2'
                password = 'admin2'

                testLoginDataSet.run_test(self, username, password)


        class testLoginDataSet_3(APITestCase):
            tag = "testLoginDataSet"

            def run_test(self):
                username = 'user1'
                password = 'user2'

                testLoginDataSet.run_test(self, username, password)


        class testLoginDataSet_4(APITestCase):
            tag = "testLoginDataSet"

            def run_test(self):
                username = 'admin1'
                password = 'admin1'

                testLoginDataSet.run_test(self, username, password)


        class testLoginDataSet_5(APITestCase):
            tag = "testLoginDataSet"

            def run_test(self):
                username = 'admin2'
                password = 'admin2'

                testLoginDataSet.run_test(self, username, password)                      
                        """)
                        break

                    # print(file_name + "存在对应的csv文件")
                    try:
                        os.remove(PROJECT_INFO.project_path + os.sep + directory_path + os.sep + file_name.split(".")[
                            0] + "_case_list_auto_generated_by_csv.py")
                    except BaseException:
                        pass

                    with open(PROJECT_INFO.project_path + os.sep + directory_path + os.sep + file_name.split(".")[
                        0] + "_case_list_auto_generated_by_csv.py", "w") as f:
                        f.write("from %s import %s\n" % (directory_path.replace(os.sep, "."), file_name.split(".")[0]))

                    is_ui_testcase = False
                    # 先 解析 py 文件, 判断文件中是否有 self.browser 有则说明需要导入UITestCase
                    with open(PROJECT_INFO.project_path + os.sep + directory_path + os.sep + file_name.split(".")[
                        0] + ".py", "r", encoding='utf-8') as py_file_obj:
                        for line in py_file_obj.readlines():
                            if line.replace(" ", "").startswith("self.browser."):
                                is_ui_testcase = True
                                # 导入 UTTestCase
                                with open(PROJECT_INFO.project_path + os.sep + directory_path + os.sep +
                                          file_name.split(".")[
                                              0] + "_case_list_auto_generated_by_csv.py", "a") as f:
                                    f.write("from linktest.ui_testcase import UITestCase")
                                break

                    if not is_ui_testcase:
                        # 导入 UTTestCase
                        with open(PROJECT_INFO.project_path + os.sep + directory_path + os.sep +
                                  file_name.split(".")[
                                      0] + "_case_list_auto_generated_by_csv.py", "a") as f:
                            f.write("from linktest.api_testcase import APITestCase")

                    csv_file_full_path = PROJECT_INFO.project_path + os.sep + directory_path + os.sep + \
                                         file_name.split('.')[0] + ".csv"


                    # 解析 py 文件, 判断文件中是否有 tag = "tagName" 有则说明需要 为自动生成的testcase 同时设置用户自定义的 tagName
                    tag_name = ''
                    with open(PROJECT_INFO.project_path + os.sep + directory_path + os.sep + file_name.split(".")[
                        0] + ".py", "r", encoding='utf-8') as py_file_obj:
                        for line in py_file_obj.readlines():
                            if line.replace(" ", "").startswith("tag="):
                                tag_name = line.replace(" ", "").split("=")[1].replace('"', "").replace("'", "").replace("\n", "")
                                break

                    print("======================== start generate testcase list from csv: ", csv_file_full_path)


                    process_csv_file(csv_file_full_path, is_ui_testcase, tag_name=tag_name)

                    # with open(csv_file_full_path) as f:
                    #     # f_csv = csv.DictReader(f)
                    #     f_csv = csv.DictReader(f, delimiter=getattr(settings, 'delimiter_in_csv', ","))
                    #     # todo: 此处应该自动兼容多种分隔符？ e.g：, \t 等
                    #
                    #     reversed_f_csv = []
                    #     for r in f_csv:
                    #         reversed_f_csv.append(r)
                    #
                    #     index = len(reversed_f_csv)
                    #
                    #     for row in reversed_f_csv[::-1]:
                    #         py_file_name = file_name.split(".")[0] + ".py"
                    #         print("csv_file_full_path: ", csv_file_full_path)
                    #         print("row: ", row)
                    #         print("index: ", index)
                    #         generate_testcase_list_by_csv_old(csv_file_full_path, row, index, is_ui_testcase, tag_name=tag_name)
                    #         index -= 1


if __name__ == "__main__":
    auto_generate_testcase_list_from_csv()
