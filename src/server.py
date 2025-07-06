import http.server
import socketserver
import yaml
import os
from pyprojroot import here

with open(here("configs/app_config.yml")) as cfg:
    app_config = yaml.load(cfg, Loader=yaml.FullLoader)

PORT = app_config["server"]["port"]
DIRECTORY1 = app_config["directories"]["data_directory"]
DIRECTORY2 = app_config["directories"]["data_directory_2"]

class SingleDirectoryHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Custom HTTP request handler that serves files from a specific directory.

    This class extends SimpleHTTPRequestHandler to always serve files from DIRECTORY1.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the request handler to serve files from DIRECTORY1.

        Args:
            args: Extra positional arguments for the base class.
            kwargs: Extra keyword arguments for the base class.
        """
        super().__init__(*args, directory=DIRECTORY1, **kwargs)

class MultiDirectoryHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Custom HTTP request handler that serves files from two directories.

    This handler extends SimpleHTTPRequestHandler and allows serving files from DIRECTORY1 or DIRECTORY2,
    depending on the requested path.
    """

    def translate_path(self, path):
        """
        Converts the requested URL path to a real file system path.

        Args:
            path (str): The URL path requested by the client.

        Returns:
            str: The full file system path to serve the requested file.
        """
        parts = path.split('/', 2)
        if len(parts) > 1: 
            frist_directory = parts[1]

            # Check if the first directory matches any of your target directories
            if frist_directory == os.path.basename(DIRECTORY1):
                path = os.path.join(DIRECTORY1, *parts[2:]) 

            elif frist_directory == os.path.basename(DIRECTORY2):
                path = os.path.join(DIRECTORY2, *parts[2:]) 

            else:
                # If the first part of the path is not a directory, check both directories for the file
                file_path1 = os.path.join(DIRECTORY1, frist_directory)
                file_path2 = os.path.join(DIRECTORY2, frist_directory)

                if os.path.isfile(file_path1):
                    return file_path1
                elif os.path.isfile(file_path2):
                    return file_path2
                
        return super().translate_path(path)
    
if __name__ == "__main__":
    with socketserver.TCPServer(("",PORT), MultiDirectoryHTTPRequestHandler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()