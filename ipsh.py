"""Python debugger using a nested iPython interactive shell"""
import inspect

# First import the embed function
from IPython.terminal.embed import InteractiveShellEmbed

# Messages displayed when I drop into and exit the shell.
banner_msg = """
**Nested Interpreter:
Hit Ctrl-D to exit interpreter and continue program.
Note that if you use %kill_embedded, you can fully deactivate
This embedded instance so it will never turn on again
"""
exit_msg = '**Leaving Nested interpreter'


# Wrap it in a function that gives me more context:
def ipsh():
    """
    Generates an interactive Python shell for debugging purposes. At the point 
    where you want a codebreak, insert:

    from ipsh import ipsh; ipsh()

    and run your code as you normally would (from the command line only?).
    """
    ipshell = InteractiveShellEmbed(banner1=banner_msg, exit_msg=exit_msg)

    frame = inspect.currentframe().f_back
    msg = 'Stopped at {0.f_code.co_filename} at line {0.f_lineno}'.format(frame)

    # Go back one level!
    # This is needed because the call to ipshell is inside the function ipsh()
    ipshell(msg, stack_depth=2)
