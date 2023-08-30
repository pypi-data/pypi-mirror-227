class DatasetFile:
    """
    Class to store necessary metadata for a Dataset file.

    Parameters
    ----------
    id : str
        Dataset File id

    name: str
        File name

    num_rows : long
        Number of rows in the file

    num_columns: int
        Number of columns in the file

    uploaded_timestamp: str
        Timestamp in UTC at which dataset was uploaded
    """
    def __init__(self, id: str, name: str, num_rows: int, num_columns: int):
        self.id = id
        self.name = name
        self.num_rows = num_rows
        self.num_columns = num_columns

    def describe(self):
        """Print file metadata - id, name, number of rows, number of columns
        """
        print("File: " + self.name + " [" + self.id + "]")
        print("Number of rows: " + self.num_rows)
        print("Number of columns: " + self.num_columns)
