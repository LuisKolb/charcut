import os
import sys

#
# This script automatically formats the input files and runs charcut on them.
# Mainly used for convenient batch processing.
#

# cand  refers to   machine translation
# ref   refers to   human translation


def run_charcut(cand, ref, out_path):
    os.system(f"python charcut.py -o {out_path} {cand},{ref} -n")


def main(input, format):
    in_dir = input
    out_dir = os.path.join(in_dir, "formatted")
    human_files = []
    mt_files = []

    # ensure output directory exists
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for filename in os.listdir(in_dir):
        f = os.path.join(in_dir, filename)

        # checking if it is a file
        if os.path.isfile(f):
            out_file = os.path.join(out_dir, filename)
            if format == "format" or format == "onlyformat":
                print(f"[INFO] processing file {f} with formatting")
                with open(f, "r") as file:
                    # remove file if it exists (e.g. from a previous run)
                    try:
                        os.remove(out_file)
                    except OSError:
                        pass

                    lines = ""
                    for line in file.readlines():
                        lines = lines + line

                    text = " ".join(lines.replace("\n", " ").split())

                    with open(out_file, "w") as output:
                        for sentence in text.split("."):
                            if sentence.lstrip() == "":
                                pass
                            else:
                                output.write(f"{sentence.lstrip()}.\n")
            else:
                print(f"[INFO] copying file {f} without formatting")
                with open(f, "r") as file:
                    # remove file if it exists (e.g. from a previous run)
                    try:
                        os.remove(out_file)
                    except OSError:
                        pass

                    lines = ""
                    for line in file.readlines():
                        lines = lines + line
                    with open(out_file, "w") as output:
                        output.write(lines)

            if filename == "mt.txt":
                mt_files.append(out_file)
            else:
                human_files.append(out_file)

    if format == "onlyformat":
        return

    # ensure output directory exists
    out_dir = os.path.join(in_dir, "formatted")
    html_out = os.path.join(out_dir, "out")
    if not os.path.exists(html_out):
        os.makedirs(html_out)
    for mt_file in mt_files:
        for human_file in human_files:
            human_filename = os.path.splitext(os.path.basename(human_file))[0]
            mt_filename = os.path.splitext(os.path.basename(mt_file))[0]
            out_path = os.path.join(html_out, f"{human_filename}_{mt_filename}.html")
            run_charcut(mt_file, human_file, out_path)


# run this script like: python main.py directoryname format|noformat|onlyformat
if __name__ == "__main__":
    # if help is requested, print usage
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
        print("Usage: python main.py directoryname format|noformat|onlyformat")
        print("directoryname: Directory containing the input files.")
        print("format: Format the input files before processing.")
        print("noformat: Do not format the input files, just copy them.")
        print("onlyformat: Only format the input files, do not run charcut.")
        sys.exit(0)
    # check if arguments are provided
    # if not, print error message and usage
    if len(sys.argv) < 3:
        print("Error: Not enough arguments provided.")
        print("Usage: python main.py directoryname format|noformat|onlyformat")
        sys.exit(1)
    input = sys.argv[1]
    format = sys.argv[2]
    if format not in ["format", "noformat", "onlyformat"]:
        print("Error: Invalid format argument. Use format, noformat, or onlyformat.")
        sys.exit(1)
    # run the main function with the provided input and format

    main(input, format)
