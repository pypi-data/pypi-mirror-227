# using Click implementation
import datetime
import re
import subprocess
from functools import wraps

from pathlib import Path
from typing import List, Optional, Tuple

import click  # CLI magic
from git import Repo

from todotree.Addons import Addons
from todotree.ConsolePrefixes import ConsolePrefixes
from todotree.Errors.TodoFileNotFound import TodoFileNotFound
from todotree.Errors.DoneFileNotFound import DoneFileNotFound
from todotree.Errors.ConfigFileNotFound import ConfigFileNotFound
from todotree.Taskmanager import Taskmanager, task_to_done
from todotree.config import Config


# Click Replaces:
# Argparse
#
# NOTE: this file cannot be in a class. See: https://github.com/pallets/click/issues/601
# But context and variable ferrying can be done using the context option.
# We just call the context 'self' and hope the issue does resolve itself.
# https://click.palletsprojects.com/en/8.1.x/commands/#nested-handling-and-contexts

def common_options(function):
    """
    Wrapper that defines common functions.

    It should be used as a decorator: `@common_options`

    This function will be needed when we want to support both
    `todotree cd --verbose` and `todotree --verbose cd`
    """

    @wraps(function)
    @click.option('--config-path', default=None, help="Path to the configuration file.")
    @click.option('--todo-file', default=None, help="Path to the todo.txt file, overrides --config.")
    @click.option('--done-file', default=None, help="Path to the done.txt file, overrides --config.")
    @click.option('--verbose', is_flag=True, help="Increases verbosity in messages.", is_eager=True)
    @click.option('--quiet', is_flag=True, help="Do not print messages, only output. Useful in scripts.", is_eager=True)
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)

    return wrapper


@click.group()
@common_options
@click.pass_context
def root(self: click.Context, config_path: Optional[Path], todo_file: Optional[Path], done_file: Optional[Path],
         verbose: bool, quiet: bool):
    """todotree help text."""
    # ^ This text also shows up in the help command.
    # Root click group. This manages all the command line interactions.
    # ensure that ctx.obj exists and is a dict
    self.ensure_object(dict)
    initialize(config_path, done_file, quiet, self, todo_file, verbose)
    # Pass to another command.
    pass


def initialize(config_path: Optional[Path], done_file: Optional[Path], quiet: bool, self: click.Context,
               todo_file: Optional[Path], verbose: bool):
    """
    Initializes the application and loads the configuration.
    :param config_path: Path to the configuration file from the command line.
    :param done_file: Path to the configuration file from the command line.
    :param quiet: --quiet value
    :param self: Context.
    :param todo_file: Path to the configuration file from the command line.
    :param verbose: --verbose value.
    """
    # parsing arguments.
    config = Config()
    try:
        config.read(config_path)
    except ConfigFileNotFound as e:
        handle_config_file_not_found(e, verbose, config_path)

    if todo_file is not None:
        config.todo_file = todo_file
    if done_file is not None:
        config.done_file = done_file
    if verbose:
        config.verbose = True
    if quiet:
        config.quiet = True
        config.verbose = False
    # Logging
    if config.verbose:
        config.console.info(f"Read configuration from {config.config_file}")
        config.console.info(f"The todo file is supposed to be at {config.todo_file}")
        config.console.info(f"The done file is supposed to be at {config.done_file}")
    # creating variables a la __init__.
    self.obj["config"] = config
    self.obj["task_manager"] = Taskmanager(configuration=config)


def handle_config_file_not_found(e: BaseException, verbose: bool, config_path):
    """Handle when the configuration file is not found.

    :param config_path: The path where the file was not found.
    :param verbose: Additional verbosity.
    :param e: The exception raised.
    """
    # Gentoo style prefixes.
    cp = ConsolePrefixes(True, " * ", " * ", " * ")
    cp.warning("The config.yaml file could not be found.")
    if verbose:
        cp.warning(f"The config file should be located at {config_path}")
        cp.warning(str(e))
    cp.warning("The default options are now used.")


def handle_todo_file_not_found(e: Exception, self):
    """Inform the user that the todo.txt was not found."""
    self.obj['config'].console.error("The todo.txt could not be found.")
    self.obj['config'].console.error(f"It searched at the following location: {self.obj['config'].todo_file}")
    if self.obj["config"].verbose:
        self.obj['config'].console.error(str(e))


def handle_done_file_not_found(e, self):
    """Inform the user that the done.txt was not found."""
    self.obj['config'].console.error("The done.txt could not be found.")
    self.obj['config'].console.error(f"It searched at the following location: {self.obj['config'].done_file}")
    if self.obj["config"].verbose:
        click.echo(e)


def commit_exit(action: str, config: Config):
    """
    Commit the files with git before exiting.

    :param config: The configuration parameters.
    :param action: The name of the action, such as list or add.
    """
    if config.git_mode not in ["Local", "Full"]:
        exit()
    repo = Repo(config.todo_folder)

    # Git add.
    repo.index.add('*')

    # Git commit.
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_commit = repo.index.commit(message=time + " " + action)
    config.console.info(f"Commit added: [{new_commit.hexsha[0:7]}] {new_commit.message} ")
    config.console.info(f"{new_commit.stats.total['files']} file(s) changed, "
                        f"{new_commit.stats.total['insertions']} insertions(+) "
                        f"{new_commit.stats.total['deletions']} deletions(-).")

    if config.git_mode == "Full":
        # Git push.
        result = repo.remote().push()[0].summary
        config.console.info(f"Push successful: {result}")


@root.command('add', short_help='Add a task to the task list')
@click.argument('task', type=str, nargs=-1)  # , short_help = 'Task To Add')
@click.pass_context
def add(self, task: Tuple):
    # Convert tuple to string
    task: str = " ".join(map(str, task))
    try:
        # Disable fancy imports, because they are not needed.
        self.obj['config'].enable_project_folder = False
        # Import tasks.
        self.obj["task_manager"].import_tasks()
        # Add task
        new_number = self.obj["task_manager"].add_task_to_file(task.strip() + "\n")
        self.obj['config'].console.info("Task added:")
        click.echo(f"{new_number} {task}")
        commit_exit("add", self.obj["config"])
    except TodoFileNotFound as e:
        handle_todo_file_not_found(e, self)
        exit(1)


@root.command('addx', short_help='Add a task and immediately mark it as done')
@click.argument('task', type=str)
@click.pass_context
def add_x(self, task):
    try:
        f = open(self.obj["config"].done_file, "a")
        done = task_to_done(
            task.strip())
        f.write(done)
        click.echo(done)
    except FileNotFoundError as e:
        handle_done_file_not_found(e, self)
        exit(1)


@root.command('append', short_help='append `append_string` to `task_nr`')
@click.argument('task_nr', type=int)
@click.argument('append_string', type=str, nargs=-1)
@click.pass_context
def append(self, task_nr: int, append_string: str):
    # Disable fancy imports, because they are not needed.
    self.obj['config'].enable_project_folder = False
    # Import tasks.
    try:
        self.obj["task_manager"].import_tasks()
    except TodoFileNotFound as e:
        handle_todo_file_not_found(e, self)
        exit(1)
    # Convert tuple to string.
    append_string = " ".join(append_string)
    self.obj['config'].console.info("The new task is: ")
    click.echo(self.obj["task_manager"].append_to_task(task_nr, append_string.strip()))
    commit_exit("append", self.obj["config"])


@root.command('context',
              short_help='list task in a tree, by context',
              help='list a tree, of which the first node is the context, the second nodes are the tasks')
@click.pass_context
def context(self):
    try:
        self.obj['task_manager'].import_tasks()
    except TodoFileNotFound as e:
        handle_todo_file_not_found(e, self)
        exit(1)
    # Print due tree.
    click.echo(self.obj['task_manager'].print_context_tree())
    exit()


@root.command('cd',
              short_help='print directory of the todo.txt directory',
              help='print directory of the todo.txt directory'
              )
@click.pass_context
def cd(self):
    config_path: Path = Path(self.obj['config'].todo_folder)
    if self.obj['config'].verbose:
        self.obj['config'].console.info("The location to the data folder is: ")

    if config_path.is_absolute():
        # Then the configured path is printed.
        click.echo(str(config_path))
        exit()
    # Then the relative path is resolved to be absolute.
    base_path: Path = Path.home()
    full_path: Path = base_path / config_path
    click.echo(str(full_path))
    exit()


@root.command('do',
              short_help='mark task as done and move it to the done.txt'
              )
@click.argument('task_numbers', type=list, nargs=-1)  # type=list[int]
@click.pass_context
def do(self, task_numbers: List[Tuple]):
    # Convert to ints. Task numbers is a list of tuples. Each tuple contains one digit of the number.
    new_numbers: List[int] = []
    for task_tuple in task_numbers:
        new_number: str = ""
        for task_digit in task_tuple:
            new_number += task_digit
        new_numbers.append(int(new_number))
    # Write back to old value.
    task_numbers = new_numbers
    # Marking something as Done cannot be done with fancy imports
    # So we disable them.
    self.obj['config'].enable_project_folder = False
    try:
        self.obj['task_manager'].import_tasks()
    except TodoFileNotFound as e:
        handle_todo_file_not_found(e, self)
        exit(1)
    try:
        completed_tasks = self.obj["task_manager"].mark_as_done(task_numbers)
    except DoneFileNotFound as e:
        handle_done_file_not_found(e, self)
        exit(1)
    # Print the results
    self.obj['config'].console.info("Tasks marked as done:")
    for task in completed_tasks:
        click.echo(task)
    commit_exit("do", self.obj["config"])


@root.command('due',
              short_help='List tasks by their due date'
              )
@click.pass_context
def due(self):
    # Disable fancy imports, because they do not have due dates.
    self.obj['config'].enable_project_folder = False
    # Import tasks.
    try:
        self.obj['task_manager'].import_tasks()
    except TodoFileNotFound as e:
        handle_todo_file_not_found(e, self)
        exit(1)
    # Print due tree.
    click.echo(self.obj['task_manager'].print_by_due())
    exit()


@root.command('edit',
              short_help='open the todo.txt in $EDITOR (or nano)'
              )
@click.pass_context
def edit(self):
    # Disable fancy imports.
    self.obj['config'].enable_project_folder = False
    click.edit(filename=self.obj["config"].todo_file)
    commit_exit("edit", self.obj["config"])


@root.command('filter',
              short_help='only show tasks containing the search term.'
              )
@click.argument('search_term')
@click.pass_context
def filter_list(self, search_term):
    try:
        self.obj["task_manager"].import_tasks()
    except TodoFileNotFound as e:
        handle_todo_file_not_found(e, self)
        exit(1)

    if self.obj["config"].verbose:
        self.obj["config"].console.info("The todo list is:")
    elif not self.obj["config"].quiet:
        self.obj["config"].console.info("Todos")

    self.obj["task_manager"].filter_by_string(search_term)
    click.echo(self.obj["task_manager"])


@root.command('list', short_help='List tasks')
@click.pass_context
def list_tasks(self):
    try:
        self.obj["task_manager"].import_tasks()
    except TodoFileNotFound as e:
        handle_todo_file_not_found(e, self)
        exit(1)

    if self.obj["config"].verbose:
        self.obj["config"].console.info("The todo list is:")
    elif not self.obj["config"].quiet:
        self.obj["config"].console.info("Todos")

    click.echo(self.obj["task_manager"])


@root.command('list_done', short_help='List tasks which are marked as done')
@click.pass_context
def list_done(self):
    try:
        self.obj["task_manager"].list_done()
    except DoneFileNotFound as e:
        handle_done_file_not_found(e, self)
        exit(1)


@root.command('print_raw', short_help='print todo.txt without any formatting or filtering')
@click.pass_context
def print_raw(self):
    try:
        with open(self.obj["task_manager"].config.todo_file, "r") as f:
            click.echo(f.read())
    except FileNotFoundError as e:
        handle_todo_file_not_found(e, self)


@root.command('priority', short_help='set new priority to task')
@click.argument('task_number', type=int)
@click.argument('new_priority', type=str)
@click.pass_context
def priority(self, task_number, new_priority):
    # Disable fancy imports.
    self.obj['config'].enable_project_folder = False
    # Run task.
    try:
        self.obj["task_manager"].import_tasks()
    except TodoFileNotFound as e:
        handle_todo_file_not_found(e, self)
        exit(1)
    self.obj["task_manager"].add_or_update_priority(
        priority=(new_priority.upper()), task_number=task_number)


@root.command('project', short_help='print tree by project')
@click.pass_context
def project(self):
    # Import tasks.
    try:
        self.obj["task_manager"].import_tasks()
    except TodoFileNotFound as e:
        handle_todo_file_not_found(e, self)
        exit(1)
    # Print due tree.
    click.echo(self.obj['task_manager'].print_project_tree())
    exit()


@root.command('revive', short_help='Revive a task that was accidentally marked as done.')
@click.argument('done_number', type=int)
@click.pass_context
def revive(self, done_number):
    try:
        click.echo(self.obj["task_manager"].revive_task(done_number))
    except TodoFileNotFound as e:
        handle_todo_file_not_found(e, self)
        exit(1)
    except DoneFileNotFound as e:
        handle_done_file_not_found(e, self)
        exit(1)
    commit_exit("revive", self.obj["config"])


@root.command('schedule', short_help='hide task until date.',
              help='hide the task until the date given. If new_date is not in ISO format (yyyy-mm-dd), '
                   'then it tries to figure out the date with the `date` program, which is only in linux.'
              )
@click.pass_context
@click.argument('task_number', type=int)
@click.argument('new_date', type=str, nargs=-1)
def schedule(self: click.Context, task_number: int, new_date: Tuple[str]):
    # Disable fancy imports, because they do not have t dates.
    self.obj['config'].enable_project_folder = False
    # Convert
    date = " ".join(new_date)
    date_pattern = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
    if not date_pattern.match(date):
        if self.obj['config'].verbose:
            self.obj['config'].console.info(f"Attempt to parse {date} with the `date` program.")
        # Try to use the `date` utility.
        dat = subprocess.run(
            ["date", "-d " + date, "+%F "],
            capture_output=True,
            encoding="utf-8"
        )
        if dat.returncode > 0:
            self.obj['config'].console.error(f"The date {new_date} could not be parsed.")
            exit(1)
        date = dat.stdout.strip()
    try:
        self.obj["task_manager"].import_tasks()
        self.obj['config'].console.info(f"Task {task_number} hidden until {date}")
        updated_task = self.obj["task_manager"].change_t_date(date, task_number)
        self.obj['config'].console.info(str(updated_task))
    except TodoFileNotFound as e:
        handle_todo_file_not_found(e, self)
        exit(1)

    commit_exit("schedule", self.obj["config"])


addons = Addons(Config())


@root.command('addons', short_help='Run an addon script',
              help=f'Run an addon script. The addons that are detected are: {addons.list()}'
              )
@click.pass_context
@click.argument('command', type=str)
def addons_command(self: click.Context, command: str):
    """
    Run an addon script.
    :param self: Context
    :param command: The script/command to run.
    """
    try:
        result = Addons(self.obj['config']).run(command)
    except FileNotFoundError:
        self.obj['config'].console.error(f"There is no script at {Path(self.obj['config'].addons_folder / command)}")
        exit(1)
    click.echo(result.stdout, nl=False)
    commit_exit(f"addons {command}", self.obj['config'])


#  End Region Command Definitions.
#  Setup Click

CONTEXT_SETTINGS: dict = dict(help_option_names=['-h', '--help'])
"""Click context settings. See https://click.palletsprojects.com/en/8.1.x/complex/ for more information."""
cli: click.CommandCollection = click.CommandCollection(
    sources=[root],
    context_settings=CONTEXT_SETTINGS
)
"""Command Collection defining defaults. https://click.palletsprojects.com/en/8.1.x/api/#click.CommandCollection ."""

if __name__ == '__main__':
    cli()
