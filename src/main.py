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
    


def main():
    copy_process()
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()