import os
import shutil
from block_markdown import markdown_to_html_node, extract_title

def main():
        source = "/Users/jamie/workspace/github.com/Jam1-git/Static-Site-Gen/static"
        destination = "/Users/jamie/workspace/github.com/Jam1-git/Static-Site-Gen/public"
        template = "/Users/jamie/workspace/github.com/Jam1-git/Static-Site-Gen/template.html"
        content_dir = "/Users/jamie/workspace/github.com/Jam1-git/Static-Site-Gen/content"

        if os.path.exists(destination):
                shutil.rmtree(destination)
        os.mkdir(destination)
        
        copy(source, destination)
        generate_pages_recursive(content_dir, template, destination)



def copy(source_dir, dest_dir):
        if not os.path.exists(source_dir) or not os.path.exists(dest_dir):
                raise Exception("invalid directory path")
        
        source_files = os.listdir(source_dir)
        for item in source_files:
                if os.path.isfile(os.path.join(source_dir,item)):
                        shutil.copy(os.path.join(source_dir,item), dest_dir)
                else:
                        os.mkdir(os.path.join(dest_dir, item))
                        copy(os.path.join(source_dir, item), os.path.join(dest_dir, item))

def generate_page(from_path, template_path, dest_path):
        print(f"generating page from {from_path} to {dest_path} using {template_path}")
        with open(from_path, "r") as f:
                markdown = f.read()
        with open(template_path, "r") as f:
                template = f.read()
        content = markdown_to_html_node(markdown).to_html()
        title = extract_title(markdown)
        template = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
        with open(dest_path, "w") as f:
                f.write(template)  

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    with open(template_path, "r") as f:
        template = f.read()

    entries = sorted(os.listdir(dir_path_content))

    for entry in entries:
        content_path = os.path.join(dir_path_content, entry)
       
        if os.path.isfile(content_path) and entry.endswith(".md"):

            with open(content_path, "r") as f:
                markdown = f.read()

            content = markdown_to_html_node(markdown).to_html()
            title = extract_title(markdown)

            page = template.replace("{{ Title }}", title)
            page = page.replace("{{ Content }}", content)

            output_file = entry.replace(".md", ".html")
            output_path = os.path.join(dest_dir_path, output_file)

            with open(output_path, "w") as f:
                f.write(page)
 
        elif os.path.isdir(content_path):

            new_dest_dir_path = os.path.join(dest_dir_path, entry)

            os.makedirs(new_dest_dir_path, exist_ok=True)

            generate_pages_recursive(
                content_path,
                template_path,
                new_dest_dir_path
            )



if __name__ == "__main__":
        main()

        
