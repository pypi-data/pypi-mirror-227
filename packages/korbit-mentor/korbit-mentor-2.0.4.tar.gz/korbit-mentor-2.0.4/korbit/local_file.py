import os
import shutil
import tempfile
import zipfile
from typing import IO, Optional

import requests

from korbit.constant import KORBIT_CODE_ANALYSIS_CHECK, KORBIT_LOCAL_OUTPUT_LOG_FILE
from korbit.login import authenticate_request


def generate_zip_file_name(folder_path: str) -> str:
    if folder_path in [".", "./"]:
        return "current_dir.zip"
    elif folder_path in ["..", "../"]:
        return "parent_dir.zip"
    folder_path = folder_path.replace("../", "").replace("./", "").replace("/", "-")
    return folder_path + ".zip"


def zip_folder(folder_path: str) -> str:
    folder_path = folder_path[:-1] if folder_path.endswith("/") else folder_path
    zip_file_path = generate_zip_file_name(folder_path)
    top_folder_name = os.path.basename(folder_path).replace(".", "-")
    temp_folder_path = tempfile.mkdtemp()

    try:
        temp_top_folder_path = os.path.join(temp_folder_path, top_folder_name)
        if os.path.isfile(folder_path):
            fil_parent_temp_folder = f"{temp_top_folder_path}/temp"
            os.makedirs(fil_parent_temp_folder, exist_ok=True)
            shutil.copy(folder_path, fil_parent_temp_folder)
        else:
            shutil.copytree(folder_path, temp_top_folder_path)

        with zipfile.ZipFile(zip_file_path, "w") as zipf:
            zipf.write(temp_top_folder_path, top_folder_name)
            for root, _, files in os.walk(temp_folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_folder_path)
                    zipf.write(file_path, arcname)
    finally:
        shutil.rmtree(temp_folder_path)

    return zip_file_path


def upload_file(zip_file_path: str) -> Optional[int]:
    with open(zip_file_path, "rb") as file:
        response = authenticate_request(requests.post, url=KORBIT_CODE_ANALYSIS_CHECK, files={"repository": file})
        if response.status_code == 200:
            return response.json()
        else:
            return None


def get_output_file(mode="a+") -> IO:
    return open(KORBIT_LOCAL_OUTPUT_LOG_FILE, mode)


def clean_output_file():
    if os.path.exists(KORBIT_LOCAL_OUTPUT_LOG_FILE):
        os.remove(KORBIT_LOCAL_OUTPUT_LOG_FILE)
