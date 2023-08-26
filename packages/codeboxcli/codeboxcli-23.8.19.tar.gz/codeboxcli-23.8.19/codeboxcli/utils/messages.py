# -*- coding: utf-8 -*-
def help_default():
    return """
    Usage: codebox COMMAND [ARGS]

    Commands:
      add       Add an item.
      list      List items.
      delete    Delete an item.
      edit      Edit an item.
      share     Share an item
    """


def help_add():
    return """
    Usage: codebox add [ARGS]
    
    Arguments:
      --help                 Show this help message and exit.
      --name TEXT            Specify a name for the snippet. (Required)
      --description TEXT     Specify the content for the snippet.
      --tags TEXT            Add tags to categorize this snippet. Separate multiple tags with space.
    """


def help_delete():
    return """
    Usage: codebox delete [ARGS] SNIPPET_ID, ...
    
    Arguments:
      --help          Show this help message and exit.
    """


def help_edit():
    return """
    Usage: codebox edit [ARGS] SNIPPET_ID
    
    Arguments:
      --help          Show this help message and exit.
    """


def help_share():
    return """
    Usage: codebox share SNIPPET_ID [ARGS]
    
    Arguments:
      --help          Show this help message and exit.
      --expire-date   Specify the expire day.
      --dev-key       Specify the developer key.
    """


def error_invalid_subcommand():
    return """
    Error: Invalid subcommand.
    """


def error_missing_value(value):
    return f"""
    Error: Missing value after {value}.
    """


def error_missing_argument(value):
    return f"""
    Error: Missing {value} argument.
    """


def error_unknown_argument(value):
    return f"""
    Error: Unknown argument {value}.
    """


def error_saving():
    return f"""
    Error: Snippet not saved.
    """


def error_not_found(value):
    return f"""
    Error: Snippet with ID {value} not found.
    """


def share_url(value):
    return f"""
    The snippet has been successfully shared.
    {value}.
    """


def share_error(value):
    return f"""
    Error: Unable to share the snippet.
           {value}.
    """
