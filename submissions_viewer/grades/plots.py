import itertools

import matplotlib.pyplot as plt


class Plots:
    def __init__(self, filtered_db):
        self.counter = itertools.count()
        self.figs = []
        self.figs.append(self._num_passing_per_test(filtered_db))
        self.figs.append(self._num_passing_per_test(filtered_db))
        self.figs.append(self._num_passing_per_test(filtered_db))
        self.figs.append(self._num_passing_per_test(filtered_db))

    def plot_barh(self, title, y, width):
        plt.clf()
        plt.style.use('ggplot')
        fig = plt.figure()
        plt.barh(y=y, width=width)
        plt.title(title)
        plt.show()
        return fig

    def to_png(self):
        images = []
        for i, fig in enumerate(self.figs):
            fp = f'{i}.png'
            fig.savefig(fp)
            plt.close(fig)
            img = plt.imread(fp)
            plt.imshow(img)
            # with open(fp, 'rb') as f:
            #    images.append(f.read())
        return images

    def _num_passing_per_test(self, filtered_db):
        group_results = dict()
        for repo_name, test_dict in filtered_db.items():
            for test_name, test_result in test_dict.items():
                group_results.setdefault(test_name, 0)
                if test_result['passing']:
                    group_results[test_name] += 1
                    # group_results[test_name] = random.randint(0, 100) % 100
                # else:
                # group_results[test_name] = random.randint(0, 100) % 100
        fig = self.plot_barh(
            title=f'Réussite en fonction des critères no{next(self.counter)} (n={len(filtered_db.keys())})',
            y=list(group_results.keys()),
            width=group_results.values()
        )
        # fp = f'{fig.number}.png'
        # fig.savefig(fp)
        # plt.close(fig)
        # img = plt.imread(fp)
        # plt.imshow(img)
        return fig
