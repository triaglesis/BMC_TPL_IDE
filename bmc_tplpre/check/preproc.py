import os
import subprocess

'''
1. If syntax_passed = True after Notepad_IDE/Sublime/check/syntax_checker.py run TPLPreprocessor (input)
2. Run TPLPreprocessor with passed args - "with imports/without", "tpl ver"  (input)
3. Check if TPLPreprocessor finished its work, check results update - tpl_preproc = False\True
4. Return Tplpreproc result (tpl_preproc = False/True) and folder path (output)
'''


def tpl_preprocessor(sublime_working_dir, working_dir, dir_label, full_curr_path, file_path):
    """
    1. If preproc has an argument full_curr_path - the path to edited pattern:
        RUN only on this pattern and include imports from it.

    2. If preproc has NO full_curr_path - RUN on the active folder, where edited pattern situated, no imots included.

    :param curr_work_dir: Working dir where sublime plugin and this module lies
    :param working_dir:  WD where pattern lies
    :param dir_label: Name of WD
    :param full_curr_path: full path to edited pattern
    :param file_path: result folder after TPLPreproc run
    :return:
    """

    messages = []
    python_v = "C:\\Python27\\python.exe"
    if full_curr_path:
        messages.append({"log": "info", "msg": "INFO: TPLPreprocessor run on one file:" + " " * 26 + full_curr_path})
        try:
            run_preproc = subprocess.Popen('cmd /c ' + python_v + ' "'
                                           + sublime_working_dir + '\\TPLPreprocessor.py" -q -o "'
                                           + working_dir + '" -f "' + full_curr_path + '"', stdout=subprocess.PIPE)
            run_preproc.wait()  # wait until command finished
            tpl_preproc = os.path.exists(file_path)  # True
            if tpl_preproc:
                messages.append({"log": "debug", "msg": "DEBUG: TPLPreprocessor success:" + " " * 26 + file_path})
        except:
            messages.append({"log": "error", "msg": "ERROR: TPL_Preprocessor won't run!"})
    # NO IMPORTS - run on folder
    else:
        messages.append({"log": "debug",
                         "msg": "DEBUG: TPLPreprocessor run all on all files in directory:" + " " * 7 + dir_label})
        try:
            run_preproc = subprocess.Popen('cmd /c ' + python_v + ' "'
                                           + sublime_working_dir + '\\TPLPreprocessor.py" -q -o "'
                                           + working_dir + '" -d "' + working_dir + '"', stdout=subprocess.PIPE)
            run_preproc.wait()  # wait until command finished
            tpl_preproc = os.path.exists(file_path)  # True
            if tpl_preproc:
                messages.append({"log": "debug", "msg": "DEBUG: TPLPreprocessor success:" + " " * 26 + file_path})
        except:
            messages.append({"log": "error", "msg": "ERROR: TPL_Preprocessor won't run!"})

    return tpl_preproc, messages