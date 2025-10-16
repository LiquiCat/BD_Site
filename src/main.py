import os
from shutil import rmtree, copy
from block import extract_title, markdown_to_html_node

def copy_process():
    working = os.getcwd()
    public_dir = os.path.join(working, "public")
    static_dir = os.path.join(working, "static")

    if os.path.exists(public_dir):
        rmtree(public_dir)
    os.mkdir(public_dir)

    copy_to_public(static_dir, public_dir, "")

def copy_to_public(static_dir, public_dir, folder_relative):
    cur_dir_s = os.path.join(static_dir, folder_relative)
    cur_dir_p = os.path.join(public_dir, folder_relative)

    for item in os.listdir(cur_dir_s):
        path_in_static = os.path.join(cur_dir_s, item)
        if os.path.isfile(path_in_static):
            copy(path_in_static, cur_dir_p)
        else:
            path_in_public = os.path.join(cur_dir_p, item)
            os.mkdir(path_in_public)
            extended_path = os.path.join(folder_relative, item)
            copy_to_public(static_dir, public_dir, extended_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()
    
    with open(template_path, "r") as f:
        template = f.read()

    title = extract_title(markdown)
    html_page = markdown_to_html_node(markdown).to_html()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_page)

    with open(dest_path, "w+") as f:
        f.write(template)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    
    for item in os.listdir(dir_path_content):
        path_in_content = os.path.join(dir_path_content, item)
        if os.path.isfile(path_in_content):
            name, ext = os.path.splitext(item)
            if ext == ".md":
                new_name = f"{name}.html"
                path_in_pubclic = os.path.join(dest_dir_path, new_name)
                generate_page(path_in_content, template_path, path_in_pubclic)
        else:
            path_in_public = os.path.join(dest_dir_path, item)
            os.mkdir(path_in_public)
            generate_pages_recursive(path_in_content, template_path, path_in_public)



def main():
    copy_process()

    working_dir = os.getcwd()

    generate_pages_recursive(os.path.join(working_dir, "content"), 
                             os.path.join(working_dir, "template.html"), 
                             os.path.join(working_dir, "public")
                             )

if __name__ == "__main__":
    main()