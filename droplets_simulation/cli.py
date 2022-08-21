import sys

sys.path.append('../')
from lib.setting_reader import read_setting

print("please write your case directory name")
CaseDir = input()
read_setting(CaseDir)