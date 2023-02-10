import os
import sys

# cand  refers to   machine translation
# ref   refers to   human translation

def run_charcut(cand, ref, out_path):
    os.system(f'python charcut.py -o {out_path} {cand},{ref} -n')

def main(input, format):
    in_dir = input
    out_dir = in_dir+'formatted/'
    human_files = []
    mt_files = []

    # ensure output directory exists
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for filename in os.listdir(in_dir):
        f = os.path.join(in_dir, filename)

        # checking if it is a file
        if os.path.isfile(f):
            if format == 'format' or format == 'onlyformat':
                print(f'[INFO] processing file {f} with formatting')
                with open(f, 'r') as file:
                    # remove file if it exists (e.g. from a previous run)
                    out_file = out_dir+filename
                    try:
                        os.remove(out_file)
                    except OSError:
                        pass

                    lines = ''
                    for line in file.readlines():
                        lines = lines + line

                    text = ' '.join(lines.replace('\n', ' ').split())

                    with open(out_file, 'w') as output:
                        for sentence in text.split('.'):
                            if sentence.lstrip() == '':
                                pass
                            else:
                                output.write(f'{sentence.lstrip()}.\n')
            else:
                print(f'[INFO] copying file {f} without formatting')
                with open(f, 'r') as file:
                    # remove file if it exists (e.g. from a previous run)
                    out_file = out_dir+filename
                    try:
                        os.remove(out_file)
                    except OSError:
                        pass

                    lines = ''
                    for line in file.readlines():
                        lines = lines + line
                    with open(out_file, 'w') as output:
                        output.write(lines)


            if filename == 'mt.txt':
                mt_files.append(out_file)
            else:
                human_files.append(out_file)
    
    if format == 'onlyformat': 
        return

    # ensure output directory exists
    html_out = out_dir+'out/'
    if not os.path.exists(html_out):
        os.makedirs(html_out)
    for mt_file in mt_files:
        for human_file in human_files:
            human_filename = human_file.split(".")[0].split("/")[-1]
            mt_filename = mt_file.split(".")[0].split("/")[-1]
            out_path = f'{html_out}{human_filename}_{mt_filename}.html'
            run_charcut(mt_file, human_file, out_path)

# run this script like: python run.py directoryname/ format|noformat|onlyformat
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('[ERROR] missing arguments: python run.py directoryname/ format|noformat|onlyformat')
    input = sys.argv[1]
    format = sys.argv[2]
    main(input, format)
