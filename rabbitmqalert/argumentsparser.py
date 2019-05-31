import ConfigParser
import os.path

import apiclient
from models import argument

REQUIRED_ARGUMENTS = [
    "server_host",
    "server_port",
    "server_username",
    "server_password",
    "server_vhost",
    "server_check_rate",
]

GENERIC_CONDITIONS = (
    "conditions_consumers_connected",
    "conditions_open_connections",
    "conditions_nodes_running",
    "conditions_node_memory_used"
)

QUEUE_CONDITIONS = (
    "conditions_ready_queue_size",
    "conditions_unack_queue_size",
    "conditions_total_queue_size",
    "conditions_queue_consumers_connected"
)


class ArgumentsParser:

    def __init__(self, logger):
        self.log = logger

    def parse(self, parser):
        arguments = vars(parser.parse_args())

        model = argument.Argument(self.log, arguments)

        # parse the standard arguments (created with argparse)
        for group in parser._action_groups:
            group_title = group.title
            for group_argument in group._group_actions:
                arguments[group_argument.dest] = model.get_value(group_title, group_argument)

        if arguments["server_queues_discovery"] == True:
            arguments["server_queues"] = apiclient.ApiClient(self.log, arguments).get_queues()
        else:
            arguments["server_queues"] = arguments["server_queues"].split(",")

        if arguments["email_to"] is not None:
            arguments["email_to"] = arguments["email_to"].split(",")

        # parse non standard arguments on files
        arguments["queue_conditions"] = dict()
        for queue in arguments["server_queues"]:
            group_title = "Conditions:" + queue
            if not model.files_have_group(group_title):
                continue

            arguments["queue_conditions"][queue] = dict()
            for condition in QUEUE_CONDITIONS:
                group_argument = model.create_argument_object(condition, int, None)
                arguments["queue_conditions"][queue][condition] = model.get_value(group_title, group_argument)

        self.validate(arguments)

        conditions = self.format_conditions(arguments)
        arguments = dict(arguments.items() + conditions.items())

        return arguments

    def validate(self, arguments):
        for argument in REQUIRED_ARGUMENTS:
            if argument in arguments and arguments[argument] is not None:
                continue

            name = "_".join(argument.split("_")[1:])
            self.log.error("Required argument not defined: " + name)
            exit(1)

    @staticmethod
    def format_conditions(arguments):
        conditions = dict()

        # get the generic condition values from the "[Conditions]" section
        generic_conditions = dict()
        for key in GENERIC_CONDITIONS:
            generic_conditions[key] = arguments[key]

        for queue in arguments["server_queues"]:
            conditions[queue] = dict()

            if not queue in arguments["queue_conditions"]:
                for key in QUEUE_CONDITIONS:
                    conditions[queue][key] = arguments[key]
            else:
                conditions[queue] = arguments["queue_conditions"][queue]

        return {"conditions": conditions, "generic_conditions": generic_conditions}
