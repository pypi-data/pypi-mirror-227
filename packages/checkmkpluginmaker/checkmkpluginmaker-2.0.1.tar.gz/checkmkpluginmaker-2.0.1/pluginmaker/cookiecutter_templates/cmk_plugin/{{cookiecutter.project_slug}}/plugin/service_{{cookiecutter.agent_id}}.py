#!/usr/bin/env python3
from .agent_based_api.v1 import *
from .agent_based_api.v1 import (
    State, 
    Result,
    Service,
    register
)

# this from special agent
DEBUG = 'DEBUG'
OK = 'OK'
WARN = 'WARN'
WARNING = 'WARNING'
CRITICAL = 'CRITICAL'
ERROR = 'ERROR'
UNKNOWN = 'UNKNOWN'



def discover_handler(section):
    """Decide how many service will show on monitor page of host

    Args:
        section (List[List[str]]): data from agent response
            Example raw section: 
                <<<some_section_id>>>
                service1 - OK - message ok
                service2 - WARNING - message warning
                service3 - CRITICAL - message critical
            
                section = [
                    ['service1', '-', 'OK', '-', 'message', 'ok'],
                    ['service2', '-', 'WARNING', '-', 'message', 'warning'],
                    ['service3', '-', 'CRITICAL', '-', 'message', 'criticals'],
                ]

    Yields:
        _type_: _description_
    """
    for line in section:
        if (
            line                                    # check not None
            and isinstance(line, (list, tuple,))    # check is an instance of list
            and len(line) > 0                       # check list has values
            and line[0] != DEBUG                    # ignore debug 
        ):
            yield Service(item=line[0])


def check_handler(item, section):
    """_summary_

    Args:
        item (str): service name
        section (List[str]): is a list which contains many item type of string
            Example raw section: 
                <<<some_section_id>>>
                service1 - OK - message ok
                service2 - WARNING - message warning
                service3 - CRITICAL - message critical
            
                section = [
                    ['service1', '-', 'OK', '-', 'message', 'ok'],
                    ['service2', '-', 'WARNING', '-', 'message', 'warning'],
                    ['service3', '-', 'CRITICAL', '-', 'message', 'criticals'],
                ]
    """
    for line in section:
        if (
            line                                    # check not None
            and isinstance(line, (list, tuple,))    # check is an instance of list
            and len(line) > 0                       # check list has values
            and line[0] == item                     # check right message for service that display on monitoring page
            and line[0] != 'DEBUG'                  # DO NOT show debug
        ):
            service_name = line[0]
            service_status = line[2]
            service_msg = f"{' '.join(line[2:])}"

            if service_status in (CRITICAL, ERROR, ):
                status = State.CRIT
            elif service_status in (WARN, WARNING, ):
                status = State.WARN
            else:
                status = State.OK
            yield Result(
                state = status,
                summary = service_msg,
                # details = 'your details message'     # uncomment if you need
            )
            return  # DO NOT handle more line

    

def agent_section_parser(string_table):
    # modify if you need
    return string_table


register.check_plugin(
    name = "{{cookiecutter.agent_id}}",
    service_name = "{{cookiecutter.service_name}}",
    discovery_function = discover_handler,
    check_function = check_handler,
)


register.agent_section(
    name="{{cookiecutter.agent_id}}",
    parse_function=agent_section_parser,
)
