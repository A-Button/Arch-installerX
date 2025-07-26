import os,time,json

logfile = open(str(int(time.time()))+".log",'w')

### functions

## Basic_ability
class BasicAbility:

    # Execute commands
    @staticmethod
    def execute(commands, is_have_result=1):
        if is_have_result:
            return os.popen(commands).readlines()
        else:
            return os.system(commands)

    # Change y/n to bools
    @staticmethod
    def yn_to_bools(text):
        if text=='y':
            return True
        elif text=='n':
            return False
        else:
            print('[ERROR]:Invalid input')
            return None

    # Write log
    @staticmethod
    def write_log(message, level=2):
        if level==0:
            message_prewrite="[ERROR] "+str(time.time)+' '+message
        elif level==1:
            message_prewrite="[WARNING] "+str(time.time)+' '+message
        elif level==2:
            message_prewrite="[INFO] "+str(time.time)+' '+message
        else:
            message_prewrite="unknow action"
        logfile.write(message_prewrite)
        return message_prewrite

############################################################################################

## Functional modules
class FunctionalModules(BasicAbility):

    def choose_mirror(self):
        mirrors=[
            "https://mirrors.ustc.edu.cn/archlinux/$repo/os/$arch",
            "https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch",
            "https://repo.huaweicloud.com/archlinux/$repo/os/$arch",
        ]
        m = input('''Please choose a mirror or type a url for a new mirror or type d to do not make any changes
        (1) USTC Mirror
        (2) TUNA Mirror
        (3) HUAWEI Cloud
        (q) Quit
        Choose a mirror(123dq or a url for a new mirror):''')
        if m in "123":
            return mirrors[int(m)-1]
        elif "http" in m:
            return m
        elif m == "d":
            return False
        elif m == "q":
            quit()
        else:
            return self.choose_mirror()

############################################################################################

## init funcs
class InitFunctions:
    def __init__(self,locale_set,with_windows):
        self.locale_set = locale_set
        self.with_windows = with_windows
    # Basic
    def basic_install(self):
        self.locale_set=input("Locale(example:us,en_US.UTF-8):")
        self.with_windows=input("Do you want to use Arch Linux with Windows?(y/n):")


    def json_install(self):# Coming soon...
        pass

    def quick_start(self):#Cooming soon...
        pass

def welcome():
    print("Welcome to Arch install bro mama!")
    print("You need to hava a Internet connection to use this script or you hava a locale host to get packages.")

def choose_mode():
    welcome()
    return input('''(1)Basic (2)Import a json (3)QuickStart (q)Quit\nChoose a mode(123q):''')


class Main(BasicAbility, FunctionalModules, InitFunctions):
    def main(self):
        # Welcome

        # choose a mirror
        super().choose_mirror()

        # init
        t=choose_mode()
        if t=='1':
            super().basic_install()
        elif t=='2':
            super().json_install()
        elif t=='3':
            super().quick_start()
        elif t=='q':
            quit()
        else:
            print('[ERROR]:Invalid input')
            self.main()

        # Tips
        print("Tips: You can directly use Enter to us default value")




############################################################################################

logfile.close()