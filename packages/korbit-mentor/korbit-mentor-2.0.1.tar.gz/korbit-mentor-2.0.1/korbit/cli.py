import getpass
import logging
import os
import sys

import click
import requests

from korbit.constant import (
    KORBIT_COMMAND_EXIT_CODE_AUTH_FAILED,
    KORBIT_COMMAND_EXIT_CODE_CHECK_FAILED,
    KORBIT_COMMAND_EXIT_CODE_ISSUES_FOUND_WITHIN_THRESHOLD,
    KORBIT_COMMAND_EXIT_CODE_UNKNOWN_ERROR,
    KORBIT_LOCAL_FOLDER,
)
from korbit.interface import (
    INTERFACE_AUTH_COMMAND_HELP,
    INTERFACE_AUTH_INPUT_SECRET_ID,
    INTERFACE_AUTH_INPUT_SECRET_ID_HELP,
    INTERFACE_AUTH_INPUT_SECRET_KEY,
    INTERFACE_AUTH_INPUT_SECRET_KEY_HELP,
    INTERFACE_AUTH_UNAUTHORIZED_CREDENTIALS_MSG,
    INTERFACE_CHECK_FAILED_MSG,
    INTERFACE_SCAN_COMMAND_HELP,
    INTERFACE_SCAN_FINAL_REPORT_FOR_HEADLESS_MSG,
    INTERFACE_SCAN_FINAL_REPORT_PATH_MSG,
    INTERFACE_SCAN_HEADLESS_HELP,
    INTERFACE_SCAN_PREPARING_FOLDER_SCAN_MSG,
    INTERFACE_SCAN_REQUESTING_A_SCAN_MSG,
    INTERFACE_SCAN_THRESHOLD_CONFIDENCE_HELP,
    INTERFACE_SCAN_THRESHOLD_PRIORITY_HELP,
    INTERFACE_SOMETHING_WENT_WRONG_MSG,
)
from korbit.local_file import clean_output_file, get_output_file, upload_file, zip_folder
from korbit.login import store_credentials
from korbit.models.issue import IssueFilterThresholds
from korbit.models.report import Report
from korbit.scan import display_report, display_scan_status, download_report, filter_issues_by_threshold

old_stdout, old_stderr = sys.stdout, sys.stderr


@click.group()
def cli():
    pass


@cli.command("login", help=INTERFACE_AUTH_COMMAND_HELP)
@click.option("--secret_id", default=None, help=INTERFACE_AUTH_INPUT_SECRET_ID_HELP)
@click.option("--secret_key", default=None, help=INTERFACE_AUTH_INPUT_SECRET_KEY_HELP)
@click.argument("client_secret_id", required=False, type=click.STRING)
@click.argument("client_secret_key", required=False, type=click.STRING)
def login(client_secret_id, client_secret_key, secret_id, secret_key):
    if not secret_id:
        if not client_secret_id:
            secret_id = input(INTERFACE_AUTH_INPUT_SECRET_ID)
        else:
            secret_id = client_secret_id
    if not secret_key:
        if not client_secret_key:
            secret_key = getpass.getpass(INTERFACE_AUTH_INPUT_SECRET_KEY)
        else:
            secret_key = client_secret_key
    store_credentials(secret_id, secret_key)


@cli.command("scan", help=INTERFACE_SCAN_COMMAND_HELP)
@click.option(
    "--threshold-priority", type=int, default=0, required=False, help=INTERFACE_SCAN_THRESHOLD_CONFIDENCE_HELP
)
@click.option(
    "--threshold-confidence", default=0, type=int, required=False, help=INTERFACE_SCAN_THRESHOLD_PRIORITY_HELP
)
@click.option("--headless", is_flag=True, default=None, required=False, help=INTERFACE_SCAN_HEADLESS_HELP)
@click.argument("path", type=click.Path(exists=True))
def main(path, threshold_priority, threshold_confidence, headless):
    global old_stdout, old_stderr
    clean_output_file()
    if headless:
        output_file = get_output_file()
        sys.stdout = output_file
        sys.stderr = output_file

    os.makedirs(KORBIT_LOCAL_FOLDER, exist_ok=True)
    click.echo(f"Preparing to scan: {path}")
    click.echo(INTERFACE_SCAN_PREPARING_FOLDER_SCAN_MSG.format(path=path))
    zip_file_path = zip_folder(path)

    try:
        click.echo(INTERFACE_SCAN_REQUESTING_A_SCAN_MSG.format(path=zip_file_path))
        scan_id = upload_file(zip_file_path)
        if not scan_id:
            click.echo(INTERFACE_CHECK_FAILED_MSG)
            if not headless:
                return
            sys.exit(KORBIT_COMMAND_EXIT_CODE_CHECK_FAILED)

        display_scan_status(scan_id, headless)
        issues = download_report(scan_id)
        report = Report.from_json(issues)

        issue_thresholds = IssueFilterThresholds(priority=threshold_priority, confidence=threshold_confidence)
        report = filter_issues_by_threshold(report, issue_thresholds)
        display_report(report, headless=headless)

        if not report.is_successful() and headless:
            click.echo(INTERFACE_SCAN_FINAL_REPORT_FOR_HEADLESS_MSG.format(path=report.report_path))
            sys.exit(KORBIT_COMMAND_EXIT_CODE_ISSUES_FOUND_WITHIN_THRESHOLD)

        click.echo(INTERFACE_SCAN_FINAL_REPORT_PATH_MSG.format(path=report.report_path))

    except requests.exceptions.HTTPError as e:
        if e.response.status_code in [401, 403]:
            click.echo(INTERFACE_AUTH_UNAUTHORIZED_CREDENTIALS_MSG)
            if headless:
                sys.exit(KORBIT_COMMAND_EXIT_CODE_AUTH_FAILED)
        logging.exception(INTERFACE_SOMETHING_WENT_WRONG_MSG)
        if headless:
            sys.exit(KORBIT_COMMAND_EXIT_CODE_UNKNOWN_ERROR)
    except Exception:
        logging.exception(INTERFACE_SOMETHING_WENT_WRONG_MSG)
        if headless:
            sys.exit(KORBIT_COMMAND_EXIT_CODE_UNKNOWN_ERROR)
    finally:
        sys.stdout, sys.stderr = old_stdout, old_stderr


if __name__ == "__main__":
    cli()
