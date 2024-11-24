import pathlib
import shutil

from md_to_html.textblock import BlockList


def main():
    recursive_copy("static", "public")
    generate_folder("content", "templates/template.html", "public")


def generate_folder(
    source: str | pathlib.Path,
    template: str | pathlib.Path,
    destination: str | pathlib.Path,
) -> None:
    source_path = pathlib.Path(source)
    destination_path = pathlib.Path(destination)

    markdown_files = source_path.glob("*.md")
    dirs = [path for path in source_path.glob("*") if path.is_dir()]

    for file in markdown_files:
        relative_file = file.relative_to(source)
        print(f"generating file {file.absolute()}")
        generate_page(
            file,
            template,
            str(destination_path / relative_file).rsplit(".", 1)[0] + ".html",
        )

    for dir in dirs:
        relative_dir = dir.relative_to(source)
        (destination_path / relative_dir).mkdir(exist_ok=True)
        generate_folder(dir, template, destination_path / relative_dir)


def recursive_copy(source: str | pathlib.Path, destination: str | pathlib.Path) -> None:
    source_path = pathlib.Path(source)
    destination_path = pathlib.Path(destination)

    if destination_path.exists():
        print(f"removing path: {destination_path.absolute()}")
        shutil.rmtree(destination_path)

    print(f"creating directory: {destination_path.absolute()}")
    destination_path.mkdir()

    files = [file for file in source_path.glob("*") if file.is_file()]
    dirs = [path for path in source_path.glob("*") if path.is_dir()]

    for file in files:
        relative_file = file.relative_to(source_path)
        print(
            f"copying file {file.absolute()} to {(destination / relative_file).absolute()}"
        )
        shutil.copy(file, destination / relative_file)

    for dir in dirs:
        relative_dir = dir.relative_to(source)
        recursive_copy(dir, destination / relative_dir)


def generate_page(
    from_path: str | pathlib.Path, template_path: str | pathlib.Path, dest_path: str
) -> None:
    with open(from_path) as f:
        markdown = f.read()

    with open(template_path) as f:
        template = f.read()

    title = BlockList.get_title(markdown)
    content = BlockList.from_text(markdown).to_html_node().to_html()

    with open(dest_path, "w") as f:
        f.write(
            template.replace("{{ Title }}", title).replace("{{ Content }}", content)
        )


if __name__ == "__main__":
    main()
