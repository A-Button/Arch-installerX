"""

Make Arch Linux Great AGAIN !!!
MAKE OPEN SOURCE GREAT AGAIN !!!!!!

"""

import os, time, json
import logging

# Configure logging
log_filename = str(int(time.time())) + ".log"
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


### functions


# Basic ability
class BasicAbility:
    # Execute commands
    @staticmethod
    def execute(command, is_have_result=1):
        logging.info("Executed " + command)
        if is_have_result:
            return os.popen(command).readlines()
        else:
            return os.system(command)

    # Change y/n to bools
    @staticmethod
    def yn_to_bools(text):
        if text == "y":
            logging.info("Chose y")
            return True
        elif text == "n":
            logging.info("Chose n")
            return False
        else:
            logging.info("Invalid input", 1)
            print("[WARNING]:Invalid input")
            return None

    # Choose an option
    @staticmethod
    def choose_or_quit(start, end, message, function_list):
        choice = input(message)
        temp_list = [str(i) for i in range(start, end + 1)].append("q")
        if choice in temp_list:
            if choice == "q":
                logging.warning("User quit")
                quit()
            else:
                logging.info("User choose " + choice)
                return function_list[int(choice) - 1]()
        else:
            logging.warning("Invalid input")
            print("[WARNING]:Invalid input")
            return BasicAbility.choose_or_quit(start, end, message, function_list)


############################################################################################


## Functional modules
class FunctionalModules(BasicAbility):
    def choose_mirror(self):
        mirrors = [
            "https://mirrors.ustc.edu.cn/archlinux/$repo/os/$arch",
            "https://mirrors.tuna.tsinghua.edu.cn/archlinux/$repo/os/$arch",
            "https://repo.huaweicloud.com/archlinux/$repo/os/$arch",
        ]
        m = input("""Please choose a mirror or type a url for a new mirror or type d to do not make any changes
        (1) USTC Mirror
        (2) TUNA Mirror
        (3) HUAWEI Cloud
        (q) Quit
        Choose a mirror(123dq or a url for a new mirror):""")
        if m in "123":
            chosen_mirror = mirrors[int(m) - 1]
            logging.info("Choose mirror " + chosen_mirror)
            return chosen_mirror
        elif "http" in m:
            logging.info("Choose mirror " + m)
            return m
        elif m == "d":
            logging.info("Did not choose any mirror")
            return False
        elif m == "q":
            logging.warning("User quit")
            quit()
        else:
            logging.warning("Invalid input")
            print("[WARNING]:Invalid input")
            return self.choose_mirror()

    @staticmethod
    def welcome():
        print("Welcome to Arch Linux InstallerX !")
        print(
            "You need to hava a Internet connection to use this script or you hava a locale host to get packages."
        )

    @staticmethod
    def choose_mode():
        FunctionalModules.welcome()
        return input(
            """(1)Basic (2)Import a json (3)QuickStart (q)Quit\nChoose a mode(123q):"""
        )


############################################################################################


## init funcs
class InitFunctions:
    def __init__(self, locale_set, with_windows):
        self.locale_set = locale_set
        self.with_windows = with_windows

    # Basic
    def basic_install(self):
        self.locale_set = input("Locale(example:us,en_US.UTF-8):")
        self.with_windows = input("Do you want to use Arch Linux with Windows?(y/n):")

    def json_install(self):  # Coming soon...
        pass

    def quick_start(self):  # Coming soon...
        pass


class Main(BasicAbility, FunctionalModules, InitFunctions):
    def main(self):
        # Welcome
        super().welcome()
        # choose a mirror
        super().choose_mirror()

        # init
        t = super().choose_mode()
        if t == "1":
            super().basic_install()
        elif t == "2":
            super().json_install()
        elif t == "3":
            super().quick_start()
        elif t == "q":
            logging.warning("Quit")
            quit()
        else:
            logging.error("Invalid input in Main.main")
            print("[ERROR]:Invalid input")
            self.main()

        # Tips
        print("Tips: You can directly use Enter to us default value")
        logging.info("Exit Main.main")


############################################################################################
