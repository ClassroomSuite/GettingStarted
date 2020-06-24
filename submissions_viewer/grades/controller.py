import threading

import ipywidgets as widgets
from IPython import display

import submissions_viewer.grades.gradesDB
import submissions_viewer.grades.grades_wg
import submissions_viewer.grades.plots


class Controller:
    def __init__(self, out):
        self.out = out
        self.wg = submissions_viewer.grades.grades_wg.Widgets()
        self.db = submissions_viewer.grades.gradesDB.GradesDB()
        self.interrupt_refresh_plots = threading.Event()

        self.wg['update_url'].on_click(
            lambda _: self.apply_url(),
        )
        self.wg['search_filter'].observe(
            handler=lambda _: self.apply_filter(),
            names=['value']
        )
        self.wg['interrupt_button'].on_click(lambda _: self.interrupt_refresh_plots.set())
        self.wg['resume_button'].on_click(lambda _: self.start())
        self.wg._display(out[0])

    def apply_filter(self):
        filter_value = self.wg['search_filter'].value
        filtered_db = self.db.filter_db(filter_value)
        choices = list(filtered_db.keys())
        self.wg.update_dropdown(choices)

    def apply_url(self):
        try:
            self.db.pull_db(self.wg['url'].value)
            self.wg['request_status'].value = True
            self.wg['request_status'].description = f'Success'
        except Exception as e:
            self.wg['request_status'].value = False
            self.wg['request_status'].description = f'{e}'
        finally:
            self.apply_filter()

    def pull_and_filter_db(self):
        self.db.pull_db(self.wg['url'].value)
        filter_value = ""
        if self.wg['dropdown'].value == 'All':
            filter_value = self.wg['search_filter'].value
        else:
            filter_value = self.wg['dropdown'].value
        filtered_db = self.db.filter_db(filter_value)
        return filtered_db

    def refresh_plots(self):
        filtered_db = self.pull_and_filter_db()
        # self.plots_out.clear_output(wait=True)
        plots = submissions_viewer.grades.plots.Plots(filtered_db)
        self._display(self.out[1], plots.figs[0])
        # plt.Text(str=f'Timestamp: {datetime.datetime.now().strftime("%H:%M:%S")}')
        # plt.show()
        # display.display(f'Timestamp: {datetime.datetime.now().strftime("%H:%M:%S")}')
        # print(f'Timestamp: {datetime.datetime.now().strftime("%H:%M:%S")}')
        # for out, fig in zip(list(self.out.values())[1:], plots.figs):
        # out.clear_output(wait=True)
        #    self.display_out(out, fig)
        # for fig in plots.figs:
        #    plt.close(fig)
        # fig.show()
        # display.display(fig)
        # images = plots.to_png()
        # for i, img in enumerate(images):
        # self.wg.update_image(i, img)
        # self.wg.add_image(i, img)
        # plt.imshow(img)
        # display.display(img)

    def _display(self, out: widgets.Output, content):

        @out.capture()
        def _display_out():
            display.clear_output(True)
            display.display(content)

        _display_out()

    def start(self):
        for thread in threading.enumerate():
            if thread.getName() == 'refresh_plots':
                thread.join(timeout=0)
        threading.Thread(name='refresh_plots', target=self.run, daemon=True).start()

    def run(self):
        interval_timeout = threading.Event()
        self.interrupt_refresh_plots.clear()
        threading.Timer(3600, lambda _: self.interrupt_refresh_plots.set).start()
        while not self.interrupt_refresh_plots.is_set():
            interval_timeout.clear()
            threading.Timer(self.wg['update_interval'].value, interval_timeout.set).start()
            self.refresh_plots()
            # display.display(widgets.Label(f'Timestamp: {datetime.datetime.now().strftime("%H:%M:%S")}'))
            while True:
                if interval_timeout.wait(timeout=1):
                    break
                if self.interrupt_refresh_plots.wait(timeout=1):
                    break
        self.refresh_plots()
        # plt.Text(str='Interrupted')
        # plt.show()
        # display.display(widgets.Label('Interrupted'))
