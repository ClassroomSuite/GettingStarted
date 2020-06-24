import requests


def get_file(url):
    try:
        res = requests.get(url)
        if res.ok:
            return res.content.decode('utf-8')
        else:
            raise Exception(f'Bad request: {res.text}')
    except:
        raise Exception(f'Bad url')


def get_line_counts(files):
    line_counts = dict()
    for f in files:
        lines = f.split('\n')
        unique_lines = set(lines)
        scores_per_file = []
        for line in unique_lines:
            line_counts.setdefault(line, 0)
            line_counts[line] += 1
    return line_counts


def score_lines(file, line_counts):
    lines = file.split('\n')
    scores = list(map(lambda line: line_counts[line], lines))
    return scores


def get_scores(files):
    line_counts = get_line_counts(files)
    files_scores = list(map(lambda file: score_lines(file, line_counts), files))
    return files_scores
