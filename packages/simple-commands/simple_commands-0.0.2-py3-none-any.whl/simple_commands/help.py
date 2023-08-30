from colorama import Fore, Style
def help(language='en'):
    """
    Function to provide help and usage instructions for the available functions.
    """
    if language == 'th':
        print()
    else:
        print(f"""{Fore.LIGHTBLUE_EX}
    ===========================================================
    Available Functions and Their Usage:

    opens():
        Open a file and write texts into it.
        
        Usage:
            opens(path="", texts=[], text="")
        
        Parameters:
            path (str): Path to the file to be opened.
            texts (list of str): List of strings to be written into the file.
            text (str): A single string to be written into the file.

    data_model():
        Prepare data for a machine learning model.
        
        Usage:
            data_model(x_train=[], x_test=[], y_train=0, y_test=0)
        
        Parameters:
            x_train (list): Training data features.
            x_test (list): Testing data features.
            y_train (int): Training data labels.
            y_test (int): Testing data labels.

    main_folder():
        List files in the main folder based on their file type.
        
        Usage:
            main_folder(main_folder_path, file_type='NONE')
        
        Parameters:
            main_folder_path (str): Path to the main folder.
            file_type (str or tuple of str, optional): File type(s) to filter the files. Use 'NONE' to show all files or provide a list of file extensions.
            Example file_type values: '.jpg', ('.jpg', '.png'), '.img', 'NONE'
            Use '.img' to show all image files.

    folder_file():
        List files in a specific folder based on their file type.
        
        Usage:
            folder_file(path, file_type='NONE')
        
        Parameters:
            path (str): Path to the folder.
            file_type (str or tuple of str, optional): File type(s) to filter the files. Use 'NONE' to show all files or provide a list of file extensions.
            Example file_type values: '.jpg', ('.jpg', '.png'), '.img', 'NONE'
            Use '.img' to show all image files.
        
        Returns:
            list_file (list): List of file paths matching the specified file type.

    Note: For file_type, you can use specific file extensions (e.g., '.jpg'), a tuple of extensions (e.g., ('.jpg', '.png')), or 'NONE' to show all files.
    ===========================================================
    {Style.RESET_ALL}""")