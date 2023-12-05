import os
import glob
import markdown2
import argparse
from jinja2 import Environment, FileSystemLoader


def prepare_gallery(directory):
    print(f"Prepping directory: {directory}")
    # Get all image files in the directory
    files = os.listdir(directory)
    image_files = [f for f in files if f.endswith((".png", ".jpg", ".jpeg"))]

    for image_file in image_files:
        # Generate .txt file for each image file
        txt_file = os.path.splitext(image_file)[0] + ".txt"
        if not os.path.exists(txt_file):
            print(f"\tCreating {txt_file}")
            with open(txt_file, "w") as f:
                f.write("")

    # Generate descriptions.txt, title.txt, footnote.txt
    for txt in ["description.txt", "title.txt", "footnote.txt"]:
        txt_file = os.path.join(args.directory, txt)
        if not os.path.exists(txt_file):
            print(f"\tCreating {txt_file}")
            with open(txt_file, "w") as f:
                f.write("")

    print("Done")


def generate_gallery(directory, template, debug):
    template_dir = os.path.dirname(template)
    env = Environment(loader=FileSystemLoader(template_dir))
    tmpl = env.get_template(os.path.basename(template))
    # Read all the files in the given directory
    files = os.listdir(directory)
    print(f"Generating gallery for {directory}")
    # Filter out image files
    image_files = [f for f in files if f.endswith((".png", ".jpg", ".jpeg"))]
    image_files = sorted(image_files)
    # read manifest.txt from the directory and use that list over this autogenerated
    # list of image files
    if os.path.exists(os.path.join(directory, "manifest.txt")):
        with open(os.path.join(directory, "manifest.txt"), "r") as f:
            image_files = [f.strip() for f in f.readlines()]

    # Read the image description from the <filename>.txt file
    # corresponding to the image file and write it below the image tag using markdown rendering
    # set the image's alt tag  the plain text read from the .txt file.
    images = []
    for image_file in image_files:
        print(f"Processing {image_file}")
        txt_file = os.path.splitext(image_file)[0] + ".txt"
        with open(os.path.join(directory, txt_file), "r") as f:
            alt_text = f.read()
            if debug:
                alt_text = f"DEBUG: **{image_file}** {alt_text}"
        images.append(
            {"src": image_file, "desc": markdown2.markdown(alt_text), "alt": alt_text}
        )

    # Use the template.html as jinja2 template to render the contents
    # The title of the page should be read from the title.txt file in the directory
    with open(os.path.join(directory, "title.txt"), "r") as f:
        title = f.read()

    # The description of the page should be read from the description.txt file in the directory and rendered using markdown
    with open(os.path.join(directory, "description.txt"), "r") as f:
        description = markdown2.markdown(f.read())

    # The footnote of the page should be read from the footnote.txt file in the directory and rendered using markdown
    with open(os.path.join(directory, "footnote.txt"), "r") as f:
        footnote = markdown2.markdown(f.read())

    # The generated index.html should be written to the directory
    with open(os.path.join(directory, "gallery.html"), "w") as f:
        f.write(
            tmpl.render(
                title=title,
                description=description,
                images=images,
                footnote=footnote,
            )
        )
        print(f"Generated {os.path.join(directory, 'gallery.html')}")


def main():
    parser = argparse.ArgumentParser("Jallery - A simple static gallery generator")
    subparsers = parser.add_subparsers(dest="command")

    prep_parser = subparsers.add_parser("prepare")
    generate_parser = subparsers.add_parser("generate")
    prep_parser.add_argument("directory", help="Directory to preare")
    generate_parser.add_argument("directory", help="Directory to generate gallery for")
    generate_parser.add_argument(
        "-t",
        "--template",
        help="Jinja2 template",
        default=os.path.join(os.getcwd(), "template.html"),
    )
    generate_parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable debug mode", default=False
    )

    args = parser.parse_args()
    if args.command == "prep":
        prepare_gallery(args.directory)
    elif args.command == "generate":
        generate_gallery(args.directory, args.template, args.debug)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
