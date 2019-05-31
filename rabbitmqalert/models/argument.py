import ConfigParser
import os

CONFIG_FILE_PATH = "/etc/rabbitmq-alert/config.ini"


class Argument:

    def __init__(self, logger, arguments):
        self.log = logger
        self.arguments = arguments

        self.defaults = self.load_defaults()
        self.file = self.load_file()

    def load_defaults(self):
        file_defaults = ConfigParser.ConfigParser()

        path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        defaults_file_path = os.path.join(path, "../config/defaults.ini")

        if os.path.isfile(defaults_file_path):
            file_defaults.read(defaults_file_path)
            self.log.info("Using defaults configuration file \"{0}\"".format(defaults_file_path))
        else:
            self.log.error("Defaults configuration file \"{0}\" not found".format(defaults_file_path))
            exit(1)

        return file_defaults

    def load_file(self):
        file = ConfigParser.ConfigParser()

        if os.path.isfile(CONFIG_FILE_PATH) and not self.arguments["config_file"]:
            file.read(CONFIG_FILE_PATH)
            self.log.info("Using configuration file \"{0}\"".format(CONFIG_FILE_PATH))
        elif self.arguments["config_file"]:
            self.log.info("Using configuration file \"{0}\"".format(self.arguments["config_file"]))
            if not os.path.isfile(self.arguments["config_file"]):
                self.log.error("The provided configuration file \"{0}\" does not exist".format(self.arguments["config_file"]))
                exit(1)

            file.read(self.arguments["config_file"])

        return file

    def get_type(self, argument):
        if argument.type is None and argument.const in [True, False]:
            return bool
        return argument.type

    def files_have_group(self, group):
        return self.file.has_section(group) or self.defaults.has_section(group)

    def create_argument_object(self, dest, object_type, const):
        group_argument = type('lamdbaobject', (object,), {})()
        group_argument.dest = dest
        group_argument.type = object_type
        group_argument.const = const
        return group_argument

    def get_value_from_file(self, file, group, argument):
        name = "_".join(argument.dest.split("_")[1:])
        value = None

        if file.has_option(group, name):
            if self.get_type(argument) == str:
                value = file.get(group, name)
            elif self.get_type(argument) == int:
                value = file.getint(group, name)
            elif self.get_type(argument) == bool:
                value = file.getboolean(group, name)

        return value

    def get_value(self, group, argument):

        def foo():
            # get value from cli arguments
            yield (self.arguments[argument.dest] if argument.dest in self.arguments else None)
            # get value from configuration file (given or global configuration file)
            yield self.get_value_from_file(self.file, group, argument)
            # get value from the defaults file
            yield self.get_value_from_file(self.defaults, group, argument)

        value = None
        try:
            # get the first not-None returned value of the above functions
            value = next(result for result in foo() if result is not None)
        except StopIteration:
            pass
        return value
