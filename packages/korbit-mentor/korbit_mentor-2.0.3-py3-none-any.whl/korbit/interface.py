import os

from rich.console import Console
from rich.progress import Progress
from rich.table import Table
from rich.tree import Tree

from korbit.constant import KORBIT_LOCAL_OUTPUT_LOG_FILE
from korbit.models.issue import Issue

# SCAN
INTERFACE_SCAN_COMMAND_HELP = """
Request a scan on a given path of a local file or folder.\n
Example:\n\n
`korbit scan /path/to/folder`\n
`korbit scan path/to/folder`\n
`korbit scan .`\n
"""
INTERFACE_SCAN_PATH_HELP = "Put the absolute or relative path of a local folder or file to scan."
INTERFACE_SCAN_THRESHOLD_PRIORITY_HELP = (
    "When specified, this threshold will filter out issues only above this priority score (on a scale of 0-10)."
)
INTERFACE_SCAN_THRESHOLD_CONFIDENCE_HELP = (
    "When specified, this threshold will filter out issues only above this confidence score (on a scale of 0-10)."
)
INTERFACE_SCAN_HEADLESS_HELP = """Run scan in headless mode.
Output will be generated in the .korbit folder in the current working directory.\n
If anything goes wrong the following exit codes could be returned:\n
- 90: something went wrong (unknown problem, contact support)\n
- 91: Check found issues\n
- 92: Can not start the folder/file analysis\n
- 93: authentication failed\n
"""
INTERFACE_SCAN_REPORT_ISSUES_COUNT_MSG = (
    "Final report contains {selected_issues} issues We ignored {ignored_issues}/{total_issues}."
)
INTERFACE_SCAN_WAITING_START_MSG = "Analysis requested is in the queue, it will start shortly..."
INTERFACE_SCAN_WAITING_REPORT_MSG = "Analysis completed successfully! Report generation in progress..."
INTERFACE_SOMETHING_WENT_WRONG_MSG = (
    "Sorry about that, something went wrong. Please contact support@korbit.ai for help."
)
INTERFACE_CHECK_FAILED_MSG = (
    "Sorry we are not able to start the analysis the file(s). Please contact support@korbit.ai for more help."
)
INTERFACE_SCAN_FINAL_REPORT_FOR_HEADLESS_MSG = "We found some issue in the code, see final report {path}"
INTERFACE_SCAN_FINAL_REPORT_PATH_MSG = "You can access the report at {path}"
INTERFACE_SCAN_PREPARING_FOLDER_SCAN_MSG = "Preparing to scan: {path}"
INTERFACE_SCAN_REQUESTING_A_SCAN_MSG = "Requesting a scan for: {path}"
# AUTH
INTERFACE_AUTH_COMMAND_HELP = """Store user credentials for future usage of `korbit scan --help` command. 
If you don't provide any arguments to the command, you will be requested to input the values.\n
You can set the following environment variables to replace this command:\n
```sh\n
export KORBIT_SECRET_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx\n
export KORBIT_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n
```\n
"""
INTERFACE_AUTH_UNAUTHORIZED_CREDENTIALS_MSG = "Invalid user credentials, please login again with `korbit login`!"
INTERFACE_AUTH_MISSING_CREDENTIALS_MSG = "No user credentials found, please login first with `korbit login`!"
INTERFACE_AUTH_INPUT_SECRET_ID = "Please enter your secret ID: "
INTERFACE_AUTH_INPUT_SECRET_ID_HELP = "The secret_id value generated on Korbit app for you user."
INTERFACE_AUTH_INPUT_SECRET_KEY = "Please enter your secret key (hidden): "
INTERFACE_AUTH_INPUT_SECRET_KEY_HELP = "The secret_key key generated on Korbit app for you user."

INTERFACE_SLEEPING_REFRESH = 1
tick_rotation = False


def create_console(headless: bool):
    if headless:
        return Console(file=open(KORBIT_LOCAL_OUTPUT_LOG_FILE, "a+"), record=True)

    return Console(record=True)


def create_progress_bar(console: Console, message: str, curr_progress: int = 0):
    with Progress(console=console, auto_refresh=True) as progress_bar:
        task = progress_bar.add_task(message, total=100, spinner="⌛️")
        progress_bar.update(task, completed=curr_progress)
        return progress_bar


def console_print_message(console: Console, message: str, only_once: bool = False, **kwargs):
    if only_once and message in console.export_text(clear=False):
        return
    console.clear()
    console.print(message, **kwargs)


def construct_file_tree(title: str, file_list: list) -> Tree:
    file_tree = build_file_tree(file_list)
    top_tree_node = Tree(title)
    add_nodes_to_tree(top_tree_node, file_tree)
    return top_tree_node


def build_file_tree(file_list: list) -> dict:
    file_tree = {}
    for file_info in file_list:
        file_name = file_info["name"]
        file_status = file_info.get("status", "Unknown")

        # Extract directory and filename from the file path
        directory, filename = os.path.split(file_name)

        # Traverse the file_tree to the appropriate directory node
        current_node = file_tree
        for folder in directory.split(os.sep):
            if folder not in current_node:
                current_node[folder] = {}
            current_node = current_node[folder]

        current_node[filename] = file_status

    return file_tree


def create_tree_node(name, status):
    global tick_rotation
    if status == "PROGRESS":
        name_with_status = name + (" ⌛️" if tick_rotation else " ⏳")
    elif status == "FAILURE":
        name_with_status = name + " ❌"
    elif status == "SUCCESS":
        name_with_status = name + " ✅"
    else:
        name_with_status = name + " 👀"
    node = Tree(name_with_status)
    tick_rotation = not tick_rotation
    return node


def add_nodes_to_tree(tree_node, current_node):
    for name, value in current_node.items():
        if isinstance(value, dict):
            if name:
                node = tree_node.add(name)
            else:
                node = tree_node
            add_nodes_to_tree(node, value)
        else:
            tree_node.add(create_tree_node(name, value))


def generate_category_table(console: Console, category: str, issues: list[Issue]):
    table = Table(title=f"Category: {category}")
    # Define columns.
    table.add_column("Error Description", overflow="fold", width=50, max_width=80)
    table.add_column("File Path", overflow="ignore")
    table.add_column("Confidence")
    table.add_column("Priority")

    for issue in issues:
        for j, issue_file in enumerate(reversed(sorted(issue.issue_files, key=lambda i_file: i_file.priority))):
            description = issue.description if j == 0 else ""
            is_last_element = j == len(issue.issue_files) - 1
            table.add_row(
                description,
                f"{issue_file.path}:{issue_file.get_line_number()}",
                str(issue_file.confidence),
                str(issue_file.priority),
                end_section=is_last_element,
            )
    console.print(table)
