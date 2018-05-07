function instance = load_instance(file)
text = fileread(file);
instance = jsondecode(text);