# TODO Import modules from pattern and copy to working dir

import re, os
import shutil
import stat

import subprocess

pattern_import_all_r = re.compile('from\s+(.+?)\s+import')
core_from_wd_r = re.compile("\S+tku_patterns\\\CORE\\\\")


def walk_folder(folder_path):
    """
    Get all patterns situated in active folder

    :param folder_path: str
    :return:
    """
    folder_content = os.walk(folder_path)
    subdirs = next(folder_content)
    current_subdirs = subdirs[1]
    return current_subdirs


def list_folder(folder_path):
    """
    Get working_dir content to find all tplpre

    ['BMCRemedyARSystem.tplpre']
    ['D:\\Doc\\PerForce\\addm\\tkn_main\\tku_patterns\\CORE\\BMCRemedyARSystemBMCRemedyARSystem.tplpre']

    :param folder_path: str
    :return: list
    """
    all_tplre = []
    tplpre_path = []
    folder_content = os.listdir(folder_path)
    for file in folder_content:
        if file.endswith(".tplpre"):
            all_tplre.append(file)
            tplpre_path.append(folder_path + os.sep + file)
            # break
    return tplpre_path


def read_pattern(pattern_path_list):
    """
    Read pattern and store content
    Parse pattern obj and find imports section

    Example for Supporting files only
    ['module SupportingFiles.CDM_Mapping', 'module DiscoveryFunctions', 'module SearchFunctions', 'module SupportingFiles.Cluster.Support']

    Example for other imports:
    ['module SupportingFiles.CDM_Mapping', 'module DiscoveryFunctions', 'module SearchFunctions', 'module SupportingFiles.Cluster.Support',
    'module ApacheFoundation.Tomcat', 'module J2EE.InferredModel', 'module RDBMSFunctions']


    list of patterns where search for imports, list can have 1 pattern, but it should be
    formatted as list!

    :param pattern_path_list: list
    :return: list
    """

    imports = []

    for pattern in pattern_path_list:
        open_file = open(pattern)
        read_file = open_file.read(1024) # About 30+ lines from the beggining of pattern
        open_file.close()
        pattern_import = pattern_import_all_r.findall(read_file)
        if pattern_import:
            for module in pattern_import:
                imports_line = "module " + module
                imports.append(imports_line)

    # print("Patt imp: "+str(imports))

    return imports

'''
Old func - will delete after finish this research

# def read_pattern(pattern_path_list):
#     """
#     Read pattern and store content
#     Parse pattern obj and find imports section
#
#     Example for Supporting files only
#     ['module SupportingFiles.CDM_Mapping', 'module DiscoveryFunctions', 'module SearchFunctions', 'module SupportingFiles.Cluster.Support']
#
#     Example for other imports:
#     ['module SupportingFiles.CDM_Mapping', 'module DiscoveryFunctions', 'module SearchFunctions', 'module SupportingFiles.Cluster.Support',
#     'module ApacheFoundation.Tomcat', 'module J2EE.InferredModel', 'module RDBMSFunctions']
#
#
#     list of patterns where search for imports, list can have 1 pattern, but it should be
#     formatted as list!
#
#     :param pattern_path_list: list
#     :return: list
#     """
#     imports = []
#     pattern_data = ''
#     for pattern in pattern_path_list:
#         try:
#             with open(pattern, 'r', encoding='utf-8') as pattern_file:
#                 pattern_data = pattern_file.readlines()
#                 pattern_file.close()
#         except UnicodeDecodeError:
#             print("Unicode error for pattern!")
#             pass
#
#         for line in pattern_data:
#             pattern_import = pattern_import_all_r.match(line)
#             if pattern_import:
#                 imports_line = "module " + pattern_import.group(1)
#                 imports.append(imports_line)
#     # print(imports)
#     return imports

 '''

def pattern_imports(folder_path, import_modules):
    """
    Collect import modules, find them

    INPUT:
    import_modules = ['module SupportingFiles.CDM_Mapping',
                      'module DiscoveryFunctions',
                      'module SearchFunctions',
                      'module SupportingFiles.Cluster.Support',
                      'module ApacheFoundation.Tomcat',
                      'module J2EE.InferredModel',
                      'module RDBMSFunctions']

    folder_path = 'D:\Doc\PerForce\addm\tkn_main\tku_patterns\CORE\BMCRemedyARSystem'


    OUTPUT:
    [{'module_name': 'module SupportingFiles.CDM_Mapping', 'pattern_file': 'd:\\Doc\\PerForce\\addm\\tkn_main\\tku_patterns\\CORE\\SupportingFiles\\CDM_Mapping.tplpre'},
     {'module_name': 'module SupportingFiles.Cluster.Support', 'pattern_file': 'd:\\Doc\\PerForce\\addm\\tkn_main\\tku_patterns\\CORE\\SupportingFiles\\Cluster_Support.tplpre'},
     {'module_name': 'module DiscoveryFunctions', 'pattern_file': 'd:\\Doc\\PerForce\\addm\\tkn_main\\tku_patterns\\CORE\\SupportingFiles\\DiscoveryFunctions.tplpre'},
     {'module_name': 'module J2EE.InferredModel', 'pattern_file': 'd:\\Doc\\PerForce\\addm\\tkn_main\\tku_patterns\\CORE\\SupportingFiles\\J2EEInferredModel.tplpre'},
     {'module_name': 'module RDBMSFunctions', 'pattern_file': 'd:\\Doc\\PerForce\\addm\\tkn_main\\tku_patterns\\CORE\\SupportingFiles\\RDBMSFunctions.tplpre'},
     {'module_name': 'module SearchFunctions', 'pattern_file': 'd:\\Doc\\PerForce\\addm\\tkn_main\\tku_patterns\\CORE\\SupportingFiles\\SearchFunctions.tplpre'}]

    :type folder_path: str
    :param import_modules: list
    :return: list
    """
    import_modules_patterns = []
    tkn_core = os.environ.get("TKN_CORE")
    supporting_files_path = ""
    tku_patterns = ""
    core = ""


    # Setting TKN_CORE from system variable or parse working directory for it
    if tkn_core:
        supporting_files_path = tkn_core + "SupportingFiles"
        tku_patterns = os.path.abspath(os.path.join(tkn_core, os.pardir))
        core = tku_patterns + os.sep + "CORE"

    elif not tkn_core:
        tkn_core = core_from_wd_r.match(folder_path).group(0)
        supporting_files_path = tkn_core + "SupportingFiles"
        tku_patterns = os.path.abspath(os.path.join(tkn_core, os.pardir))
        core = tku_patterns + os.sep + "CORE"

    # Find all founded imports for current pattern
    # print(import_modules)
    if supporting_files_path:
        import_modules_patterns, modules_left = _search_in_pattern(search_path=supporting_files_path, import_modules_list=import_modules)
        # If there any modules which was not found in Supp files - function will return list with them:

    if import_modules_patterns:
        imports = read_pattern(import_modules_patterns)
        import_modules_patterns_add, modules_left = _search_in_pattern(search_path=supporting_files_path, import_modules_list=imports)
        for additional_imports in import_modules_patterns_add:
            if additional_imports not in import_modules_patterns:
                import_modules_patterns.append(additional_imports)

    # print(import_modules_patterns)
    return import_modules_patterns




def import_tkn(patterns_path, working_dir):
    """
    Copy patterns to "imorts" folder

    Create folder 'imports'
    Copy imported patterns in folder imports
    Then - syntax check will be started

    INPUT: [{'pattern_file': 'd:\\Doc\\PerForce\\addm\\tkn_main\\tku_patterns\\CORE\\SupportingFiles\\CDM_Mapping.tplpre', 'module_name': 'module SupportingFiles.CDM_Mapping'},]

    :param patterns_path: list
    :return:
    """

    imports_folder = working_dir + os.sep + "imports"

    _del_old_imports(imports_folder)
    if not os.path.exists(imports_folder):
        os.mkdir(imports_folder)
        for pattern in patterns_path:
            shutil.copy2(pattern, imports_folder)

    return


def import_modules(working_dir):
    """
    Summarize all imports

    :param working_dir: str
    :return:
    """
    messages = []

    pattern_path_list = list_folder(working_dir)
    module_imports = read_pattern(pattern_path_list)
    import_list = pattern_imports(import_modules=module_imports, folder_path=working_dir)
    # if import_list:
    #     messages.append({"log":"debug", "msg":"DEBUG: Importing patterns:"+" "*25+str(import_list)})
    # else:
    #     messages.append({"log":"debug", "msg":"DEBUG: Import modules not found in pattern file"})
    import_tkn(import_list, working_dir)


    return True, messages


def _del_old_imports(path):
    if os.path.exists(path):
        shutil.rmtree(path, onerror=_del_rw)
        # print("Folder exist!")


def _del_rw(action, name, exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)


def _search_in_pattern(import_modules_list, search_path):
    """
    Search import modules by parsing each pattern in selected folder to find it.s module name

    OUTPUT: [{'module_name': 'module SupportingFiles.CDM_Mapping', 'pattern_file': 'd:\\Doc\\PerForce\\addm\\tkn_main\\tku_patterns\\CORE\\SupportingFiles\\CDM_Mapping.tplpre'},
             {'module_name': 'module SupportingFiles.Cluster.Support', 'pattern_file': 'd:\\Doc\\PerForce\\addm\\tkn_main\\tku_patterns\\CORE\\SupportingFiles\\Cluster_Support.tplpre'},
             {'module_name': 'module DiscoveryFunctions', 'pattern_file': 'd:\\Doc\\PerForce\\addm\\tkn_main\\tku_patterns\\CORE\\SupportingFiles\\DiscoveryFunctions.tplpre'},
             {'module_name': 'module J2EE.InferredModel', 'pattern_file': 'd:\\Doc\\PerForce\\addm\\tkn_main\\tku_patterns\\CORE\\SupportingFiles\\J2EEInferredModel.tplpre'},
             {'module_name': 'module RDBMSFunctions', 'pattern_file': 'd:\\Doc\\PerForce\\addm\\tkn_main\\tku_patterns\\CORE\\SupportingFiles\\RDBMSFunctions.tplpre'},
             {'module_name': 'module SearchFunctions', 'pattern_file': 'd:\\Doc\\PerForce\\addm\\tkn_main\\tku_patterns\\CORE\\SupportingFiles\\SearchFunctions.tplpre'}]


    :type import_modules_list: list
    :type supporting_files_path: str
    :return: list
    """
    import_modules_patterns = []
    modules_to_import = []

    # TODO: Return modules which was not found to run another search in next place.


    folder_content = os.listdir(search_path)
    for file in folder_content:
        if file.endswith(".tplpre"):
            open_file = open(search_path + os.sep + file, "r")
            read_file = open_file.read(1024) # About 30+ lines from the beggining of pattern
            open_file.close()
            for module in import_modules_list:
                module_r = re.compile(module)
                check_modules = module_r.findall(read_file)
                if check_modules:
                    pattern_file = search_path + os.sep + file
                    if pattern_file not in import_modules_patterns:
                        import_modules_patterns.append(pattern_file)
                        # Remove module which was found from list, then return list with left modules.
                        import_modules_list.remove(module)

    return import_modules_patterns, import_modules_list


def _search_findstr(import_modules_list, search_path):
    """

    :param import_modules_list:
    :param search_path:
    :return:
    """
    import_modules_patterns_left = []

    # D:\Doc\PerForce\addm\tkn_main\tku_patterns\CORE\SupportingFiles>findstr /M /C:"module SupportingFiles.CDM_Mapping" *.tplpre
    # D:\Doc\PerForce\addm\tkn_main\tku_patterns\CORE>findstr /S /M /C:"module ApacheFoundation.Tomcat" *.tplpre

    for module in import_modules_list:
        # find_str = subprocess.Popen('findstr /S /M /D:"D:\\Doc\\PerForce\\addm\\tkn_main\\tku_patterns\\CORE\\" /C:"'+module+'" *.tplpre', cwd=search_path, stdout=subprocess.PIPE)
        # find_str = subprocess.Popen('findstr /S /M /C:"'+module+'" *.tplpre', cwd="D:\\Doc\\PerForce\\addm\\tkn_main\\tku_patterns\\CORE", stdout=subprocess.PIPE)
        find_str = subprocess.Popen('findstr /S /M /C:"'+module+'" *.tplpre', cwd=search_path, stdout=subprocess.PIPE)
        result = find_str.stdout.read().decode()
        if result:
            print("Find for: "+module)
            print("Found in:\n "+result)
            break

    return import_modules_patterns_left