#   AUTHOR: Krishnendu Marathe
#  PROGRAM: Simple Directory Explorer
#
# *********O
# |  BUGS  |
# *********O
# 1) Terminal Resize Support Is Rough
# 2) Character Height Allocation Needs Pre-calculation To Include Test Wraps for Directory Display
# 3) Screen Refresh Implementation is Slow (Microsoft Windows)
#
"""
                        Simple Directory Explorer
                        -------------------------
    Simple Directory Explorer is a CLI File Explore written in Python
    with support for Linux and Microsoft Windows

                                License
                                -------

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""
import os
import platform
import subprocess as launch
from time import sleep
from sys import stdout as std

_VERSION = '0.01'


def handle_terminate():
    """A Simple function to handle program exit"""
    if _which_platform == 'Linux':
        exit(1)
    else:
        input('')
        exit(1)


def clear_screen():
    """Clear Terminal Screen Handler"""
    os.system(_clear_string)


# System Specific Implementations
_which_platform = platform.system()
if _which_platform in ['Linux', 'Darwin']:
    _clear_string = 'clear'
elif _which_platform == 'Windows':
    _clear_string = 'cls'
else:
    print("\033[31;1m" + "ERROR :: ONLY WINDOWS, MAC AND LINUX SUPPORTED" + "\033[0m")
    handle_terminate()


# Terminal Interface Class Object
class TerminalFunctions:
    """
    Class that encompasses all the functions of this program under a single object
    It is necessary to use the get_updates command to initialise and update variables in a program loop
    """
    fileList = []
    fileName = []
    dirList = []
    dirName = []

    command_list = []
    the_height = 0
    allowed_height = 0
    allowed_characters = 0
    allowed_width = 0

    reload = False  # default value
    no_function_output = False  # default value

    # Help message for functions
    __help_quit = "q/quit -  Quit Program"
    __help_help = "help   -  Display This Message"
    __help_clear = "clear  -  Clear Screen"
    __help_change_dir = "chdir  -  Change Directory"
    __help_terminal = "sh     -  Run shell command"

    current_directory = ''
    # commands list
    commands_msg = " q/quit || help || clear || chdir || sh "
    commands_msg_len = len(commands_msg)

    # First Launch Welcome
    def splash_screen(self):
        """Display a splash screen at launch and exit"""
        reset_color = '\033[0m'
        background = '\033[42;1m'
        welcome = ['Simple Directory Explorer V' + _VERSION,
                   '@ Krishnendu Marathe']

        start_height = (self.the_height // 2) - 1
        start_width_one = (self.allowed_width // 2) - (len(welcome[0]) // 2)
        start_width_two = (self.allowed_width // 2) - (len(welcome[1]) // 2)
        all_characters = self.allowed_width * self.the_height
        count = 0
        print(background, end='')
        while count <= all_characters + 1:
            count += 1

            if count == (self.allowed_width * (start_height - 1)) + start_width_one:
                print(welcome[0], end='')
                count += len(welcome[0])
            elif count == (self.allowed_width * start_height) + start_width_two:
                print(welcome[1], end='')
                count += len(welcome[1])
            else:
                print(' ', end='')

        print(reset_color, end='')
        std.flush()
        # Sleep 2 seconds
        sleep(2)
        clear_screen()

    # Get Update for Terminal Variables
    def get_updates(self, command=''):
        """
        Initiation and Update Method for class TerminalFunctions

        Parameters:
            command (string): User input command to the program
        """

        try:
            self.current_directory = os.getcwd()
            term_size = os.get_terminal_size()

            th = 3
            tz = 0
            self.allowed_width = term_size[0]
            self.the_height = term_size[1]
            if self.commands_msg_len > self.allowed_width:
                num = self.commands_msg_len // self.allowed_width
                num_res = self.commands_msg_len - (num * self.allowed_width)
                tz += num - 1  # 1 for preexisting space count
                if num_res != 0:
                    tz += 1

            th += tz
            self.allowed_height = term_size[1] - th
            self.allowed_characters = self.allowed_height * self.allowed_width
            if command != '':
                self.command_list = command.split(" ")

        except OSError:
            self.error_msg("Inappropriate ioctl for device")
            handle_terminate()

    # Command Handler
    def function_call(self):
        """Method to handle commands for class TerminalFunctions"""

        if self.command_list[0] in self.__command_dictionary:
            self.__command_dictionary[self.command_list[0]](self)
        else:
            self.error_msg("Unknown Command " + self.command_list[0])

    # Error Message Display
    def error_msg(self, text):
        """
        Method for class TerminalFunctions to display error messages

        Parameters:
            text (string): Error Message
        """

        print("\033[31;1m" + f"ERROR :: {text}" + "\033[0m")
        for i in range(1, self.allowed_height):
            print("")

    # Display Help Function
    def __help_function(self):
        """Method for class TerminalFunctions to display help on available user commands"""
        print("")
        help_list = [self.__help_quit, self.__help_help, self.__help_clear, self.__help_change_dir,
                     self.__help_terminal]

        # implement print with individual and height adjustments
        help_list_len = len(help_list)
        for i in range(0, self.allowed_height - 1):
            if i < help_list_len:
                ln = len(help_list[i])
                if ln > self.allowed_width:
                    for j in range(0, self.allowed_width - 3):
                        print(help_list[i][j], end='')

                    print(" ..")
                else:
                    print(help_list[i])

            else:
                print("")

        if help_list_len > (self.allowed_height - 1):
            self.error_msg("...")

    # Run a Shell Command
    def __sys_command(self):
        """Method for class TerminalFunctions to run shell commands"""
        try:
            if _which_platform == 'Windows':
                output = launch.run(self.command_list[1:], stdout=launch.PIPE, shell=True).stdout.decode('utf-8')
            else:
                output = launch.run(self.command_list[1:], stdout=launch.PIPE).stdout.decode('utf-8')

            min_cnt = 0
            max_cnt = 0
            output_list = output.split('\n')
            for out_line in output_list:
                max_cnt += 1
                if len(output_list) > self.allowed_height and max_cnt > (self.allowed_height - 1 - min_cnt):
                    _display_dir_name('...', False)
                    print('')
                    break

                line_len = len(out_line)
                if (self.allowed_width * 2) >= line_len >= self.allowed_width:
                    min_cnt += 1
                    print(out_line)
                elif line_len > (self.allowed_width * 2):
                    min_cnt += 1
                    for i in range(0, (self.allowed_width * 2) - 3):
                        print(out_line[i], end='')

                    print(' ', end='')
                    _display_file_name('..', False)
                    print('')
                else:
                    print(out_line)

            if len(output_list) <= self.allowed_height:
                for i in range(0, (self.allowed_height - len(output_list) - min_cnt)):
                    print('')

        except launch.CalledProcessError:
            self.error_msg("CalledProcessError Detected. Aborting...")
        except IndexError:
            self.error_msg("IndexError Detected. Aborting...")
        except FileNotFoundError:
            self.error_msg("Command Not Found")

    # Change Directory
    def __change_directory(self):
        """"Method for class TerminalFunctions to change working directory"""

        if len(self.command_list) > 2:
            self.error_msg("Only 1 Argument Accepted")
        else:
            try:
                if len(self.command_list) == 1 or self.command_list[1] == '~':
                    change_dir = os.path.expanduser("~")
                else:
                    change_dir = self.command_list[1]

                os.chdir(change_dir)
                self.no_function_output = True
                self.reload = True
            except FileNotFoundError:
                self.error_msg("No such Directory")
            except OSError:
                self.error_msg("Cannot Change Directory")

    # Command to Function mapping
    __command_dictionary = {
        "help": __help_function,
        "chdir": __change_directory,
        "sh": __sys_command
    }

    # Display Directory Structure
    def display_directory_structure(self, sorted_directory, sorted_file):
        """
        Method for class TerminalFunctions to display directories anf files in the working directory

        Parameters:
            sorted_directory (list): List of directory names in the working directory sorted in Ascending Order
                                     Empty if new instance or reload in case of no directory change
            sorted_file (list): List of file names in the working directory sorted in Ascending Order
                                Empty if new instance or reload in case of no directory change

        Returns:
            sorted_directory (list): List of directory names in the working directory sorted in Ascending Order
            sorted_file (list): List of file names in the working directory sorted in Ascending Order
        """

        if self.reload:
            self.fileList = []
            self.fileName = []
            self.dirList = []
            self.dirName = []

            for fl in os.listdir(self.current_directory):
                if os.path.isfile(fl):
                    self.fileList.append(os.path.join(self.current_directory, fl))
                    self.fileName.append(fl)

                if os.path.isdir(fl):
                    self.dirList.append(os.path.join(self.current_directory, fl))
                    self.dirName.append(fl)

            sorted_file = self.fileName
            sorted_file.sort()
            sorted_directory = self.dirName
            sorted_directory.sort()

            sorted_directory.insert(0, '..')

        else:
            if sorted_directory == [] and sorted_file == []:
                self.error_msg("No Reload Directory Display Malfunctions")
                handle_terminate()

        # Count max character width for names
        max_char_count_file = 0
        max_char_count_directory = 0

        for each in sorted_directory:
            max_char_count_directory += len(each) + 1

        for each in sorted_file:
            max_char_count_file += len(each) + 1

        _dir_break = False
        _file_break = False
        if max_char_count_directory >= self.allowed_characters:
            _dir_break = True

        if (max_char_count_directory + max_char_count_file) > self.allowed_characters:
            _file_break = True

        len_sorted_dir = len(sorted_directory)
        len_sorted_file = len(sorted_file)
        count_char = 0
        count_width = 0
        count_height = 1

        # Display Files and Directories
        for each in range(0, (len_sorted_dir + len_sorted_file)):
            if each <= (len_sorted_dir - 1):
                if _dir_break:
                    if count_char >= (self.allowed_characters - (self.allowed_width * 2)):
                        count_height += 1
                        _display_dir_name('...', False)
                        print('')
                        _display_file_name('...', False)
                        break

                if (count_width + len(sorted_directory[each]) + 1) >= self.allowed_width:
                    if (count_width + len(sorted_directory[each])) <= self.allowed_width:
                        count_height += 1
                        _display_dir_name(sorted_directory[each], False)
                        count_char += len(sorted_directory[each])
                        count_width = 0
                        print("")
                    else:
                        print('')
                        count_height += 1
                        _display_dir_name(sorted_directory[each])
                        count_char += len(sorted_directory[each]) + 1
                        count_width = len(sorted_directory[each]) + 1
                else:
                    _display_dir_name(sorted_directory[each])
                    count_char += len(sorted_directory[each]) + 1
                    count_width += len(sorted_directory[each]) + 1

            else:
                if each == len_sorted_dir:
                    count_height += 2
                    print('\n')

                index = each - len_sorted_dir
                if _file_break:
                    if count_char >= (self.allowed_characters - (self.allowed_width * 1)):
                        _display_file_name('...', False)
                        break

                if (count_width + len(sorted_file[index]) + 1) >= self.allowed_width:
                    if (count_width + len(sorted_file[index])) <= self.allowed_width:
                        _display_file_name(sorted_file[index], False)
                        count_char += len(sorted_file[index])
                        count_width = 0
                        count_height += 1
                        print("")
                    else:
                        print('')
                        count_height += 1
                        _display_file_name(sorted_file[index])
                        count_char += len(sorted_file[index]) + 1
                        count_width = len(sorted_file[index]) + 1
                else:
                    _display_file_name(sorted_file[index])
                    count_char += len(sorted_file[index]) + 1
                    count_width += len(sorted_file[index]) + 1

        for i in range(count_height, self.allowed_height):
            print('')

        return sorted_directory, sorted_file


# Display Directory Name
def _display_dir_name(name, ending=True):
    """Format Directory Name"""
    if ending:
        print("\033[45;1m" + f"{name}" + "\033[0m", end=" ")
    else:
        print("\033[45;1m" + f"{name}" + "\033[0m", end="")


# Display File Names
def _display_file_name(name, ending=True):
    """Format File Name"""
    if ending:
        print("\033[44;1m" + f"{name}" + "\033[0m", end=" ")
    else:
        print("\033[44;1m" + f"{name}" + "\033[0m", end="")


# Initialising Global instance of the class TerminalFunctions
terminal_buffer = TerminalFunctions()


# Main Driver
def main():
    """
    The Main Driver of the Program with program loop

    Returns:
        0: No Errors
        1: Errors Detected
    """

    clear_screen()
    terminal_buffer.no_function_output = True
    terminal_buffer.reload = True
    _first_run = True
    _dont_display_path = False

    sorted_directory = []
    sorted_file = []

    # Program Loop
    while True:
        terminal_buffer.get_updates()
        if _first_run:
            clear_screen()
            terminal_buffer.splash_screen()

        if terminal_buffer.no_function_output:
            sorted_directory, sorted_file = terminal_buffer.display_directory_structure(sorted_directory, sorted_file)
            print('')  # Separate UI with Output buffer
            if terminal_buffer.reload:
                terminal_buffer.reload = False

        # Display path, command list and command prompt
        if len(terminal_buffer.current_directory) > (terminal_buffer.allowed_width - 7):
            path = "..."
            path_buffer = terminal_buffer.current_directory
            diff = len(terminal_buffer.current_directory) - terminal_buffer.allowed_width + 7 + 3

            i = 0
            try:
                while True:
                    if i >= diff and (path_buffer[i] == '\\' or path_buffer[i] == '/'):
                        break

                    i += 1

                for t in range(i, len(terminal_buffer.current_directory)):
                    path += path_buffer[t]

            except IndexError:
                clear_screen()
                terminal_buffer.error_msg("Unsupported Terminal Size")

        else:
            path = terminal_buffer.current_directory

        if not _dont_display_path:
            print("\033[41;1m" + f"PATH:: {path}", end='')
            path_size = len(path)
            for i in range(0, (terminal_buffer.allowed_width - path_size - 7)):
                print(" ", end="")

        print("")  # Separate path with  command list
        print("\033[43;1m" + "\033[37;1m" + terminal_buffer.commands_msg, end='')

        if terminal_buffer.commands_msg_len > terminal_buffer.allowed_width:
            diff = terminal_buffer.allowed_width - (terminal_buffer.commands_msg_len % terminal_buffer.allowed_width)
        else:
            diff = terminal_buffer.allowed_width - terminal_buffer.commands_msg_len

        for i in range(0, diff):
            print(" ", end='')

        print("\033[0m")  # Reset color and separate command list with command prompt
        command = input("\033[0m" + "\033[46;1m" + "COMMAND:" + "\033[0m" + " ")
        if command == '':
            command += 'clear'

        terminal_buffer.get_updates(command)
        if not terminal_buffer.no_function_output:
            terminal_buffer.no_function_output = True

        clear_screen()
        if _first_run:
            std.flush()
            _first_run = False
            terminal_buffer.reload = False

        if terminal_buffer.command_list[0] in ['q', 'Q', 'quit', 'Quit', 'QUIT']:
            clear_screen()
            terminal_buffer.splash_screen()
            clear_screen()
            break
        else:
            if terminal_buffer.command_list[0] == 'clear':
                terminal_buffer.reload = True
            else:
                terminal_buffer.no_function_output = False
                terminal_buffer.function_call()

    return 0


if __name__ == '__main__':
    main()
