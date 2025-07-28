# CharCut

Character-based MT evaluation and difference highlighting

CharCut compares outputs of MT systems with reference translations. It can compare multiple file pairs simultaneously and produce HTML outputs showing character-based differences along with scores that are directly inferred from the lengths of those differences, thus making the link between evaluation and visualisation straightforward.

The matching algorithm is based on an iterative search for longest common substrings, combined with a length-based threshold that limits short and noisy character matches. As a similarity metric this is not new, but to the best of our knowledge it was never applied to highlighting and scoring of MT outputs. It has the neat effect of keeping character-based differences readable by humans.

Accidentally, the scores inferred from those differences correlate very well with human judgments, similarly to other great character-based metrics like [chrF(++)](https://github.com/m-popovic/chrF) or [CharacTER](https://github.com/rwth-i6/CharacTER). It was evaluated here:

> Adrien Lardilleux and Yves Lepage: "CharCut: Human-Targeted Character-Based MT Evaluation with Loose Differences". In [Proceedings of IWSLT 2017](http://workshop2017.iwslt.org/64.php).

It is intended to be lightweight and easy to use, so the HTML outputs are, and will be kept, slick on purpose.

## Usage

CharCut is written in Python 3. It only relies on the standard library.

Basic usage:

```bash
python3 charcut.py cand.txt,ref.txt
```

where `cand.txt` and `ref.txt` contain corresponding candidate (MT) and reference (human) segments, 1 per line. Multiple file pairs can be specified on the command line: candidates with references, candidates with other candidates, etc.
By default, only document-level scores are displayed on standard output. To produce a HTML output file, use the `-o` option:

```bash
python3 charcut.py cand.txt,ref.txt -o mydiff.html
```

A few more options are available; call

```bash
python3 charcut.py -h
```

to list them.

Consider lowering the `-m` option value (minimum match size) for non-alphabetical writing systems such as Chinese or Japanese. The default value (3 characters) should be acceptable for most European languages, but depending on the language and data, larger values might produce better looking results.

## WebApp by LuisKolb

This repo contains, in addition to the previous CharCut code, a script to process text files in bulk (see `main.py`) and a Flask service to make it accessible on the web at [charcut.vercel.app](https://charcut.vercel.app/). The WebApp provides some quality-of-life features. Deploying on Vercel means some prerequisites, on which there is unfortunately little info available online:

- `index.py` entry point
- npm build script starting the flask server
- `requirements.txt` as the env definition
- `vercel dev` from the Vercel CLI can be used to test deployments locally

## Changes

28/07/2025

- Updated the WebApp for better usability
- Love you, mom

11/02/2022

- added a Flask app to use charcut in the browser - includes modifications to charcut.py to be able to output strings instead of only dumping to files
- deployed to Vercel at [charcut.vercel.app](https://charcut.vercel.app/)

27/07/2022

- forked by [Luis Kolb](https://github.com/LuisKolb) to include a directory crawler+formatting+execution script (`run.py`)
- execute the script like `python run.py sample-data/ format`

09/07/2019

- ported code to Python3
- added support for comparing multiple file pairs simultaneously
- removed "-c" and "-r" command line arguments, replaced with a space-separated list of (comma-separated) file pairs
