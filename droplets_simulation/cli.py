from lib.setting_reader import read_setting

def main():
    print("please write your case directory name")
    CaseDir = input()
    read_setting(CaseDir)

if __name__ == '__main__':
    main()