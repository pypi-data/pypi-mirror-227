from typing import IO
from ..classes.httpclient import HttpClient
from ..classes.datasetfile import DatasetFile

import json

def upload(file_name: str, file_bytes: IO[bytes], client: HttpClient) -> DatasetFile:    
    payload = dict()
    files = {
        'document': (None, json.dumps({"fileName": file_name, "csvConfig":{}}), 'application/json'),
        'file': file_bytes
    }
    file = client.http_post("/api/datasetfiles/upload_local_file", files=files)
    #numRows is null when a file is first uploaded
    return DatasetFile(file["fileId"], file["fileName"], file.get("numRows"), file["numColumns"])