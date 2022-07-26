import os
import sys

def run_charcut(human, mt, out_path):
    os.system(f'python charcut.py -o {out_path} {human},{mt}')

def main(input):
    in_dir = input
    out_dir = in_dir+'/formatted/'
    candidate_files = []
    mt_files = []

    # ensure output directory exists
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for filename in os.listdir(in_dir):
        f = os.path.join(in_dir, filename)

        # checking if it is a file
        if os.path.isfile(f):

            print(f'[INFO] processing file {f}')

            with open(f, 'r') as file:
                # remove file if it exists (e.g. from a previous run)
                out_file = out_dir+filename
                try:
                    os.remove(out_file)
                except OSError:
                    pass
                
                
                
                for line in file.readlines():
                    with open(out_file, 'w') as output:
                        for sentence in line.split('. '):
                            output.write(f'{sentence.lstrip()}\n')
                
                if filename == 'mt.txt':
                    mt_files.append(f)
                else:
                    candidate_files.append(f)

    # ensure output directory exists
    html_out = out_dir+'/out'
    if not os.path.exists(html_out):
        os.makedirs(html_out)
    for mt_file in mt_files:
        for candidate in candidate_files:
            out_path = f'{out_dir}out/{candidate.split(".")[0].replace(in_dir+"/", "")}_{mt_file.split(".")[0].replace(in_dir+"/", "")}.html'
            run_charcut(candidate, mt_file, out_path)

# run this script like: python run.py directoryname
if __name__ == '__main__':
    input = sys.argv[1]
    main(input)
