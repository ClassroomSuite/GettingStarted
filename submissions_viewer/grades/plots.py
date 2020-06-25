import itertools

import matplotlib.pyplot as plt


class Plots:
    def __init__(self):
        self.counter = itertools.count()

    def plot_barh(self, title, y, width):
        plt.ion()
        plt.clf()
        plt.style.use('ggplot')
        fig = plt.figure()
        plt.barh(y=y, width=width)
        plt.title(title)
        plt.show()
        return fig

    def num_passing_per_test(self, filtered_db):
        group_results = dict()
        for repo_name, test_dict in filtered_db.items():
            for test_name, test_result in test_dict.items():
                group_results.setdefault(test_name, 0)
                if test_result['passing']:
                    group_results[test_name] += 1
        fig = self.plot_barh(
            title=f'Réussite en fonction des critères no{next(self.counter)} (n={len(filtered_db.keys())})',
            y=list(group_results.keys()),
            width=group_results.values()
        )
        return fig
