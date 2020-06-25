import threading
import time

import ipywidgets as widgets
from IPython import display

import submissions_viewer.grades.gradesDB
import submissions_viewer.grades.grades_wg
import submissions_viewer.grades.plots
#rgsrthjs

def _display(out: widgets.Output, content, clear_output=True):
    @out.capture(clear_output=clear_output, wait=True)
    def _display_out():
        display.display(content)
        time.sleep(1)

    _display_out()


class Runner:
    def __init__(self,
                 url,
                 filter_value,
                 update_interval,
                 interrupt_refresh_plots,
                 outs: widgets.Output
                 ):
        self.url = url
        self.filter_value = filter_value
        self.update_interval = update_interval
        self.interrupt_refresh_plots = interrupt_refresh_plots
        self.outs = outs
        self.db = submissions_viewer.grades.gradesDB.GradesDB()

    def __call__(self):
        self.interrupt_refresh_plots.clear()
        threading.Timer(3600, lambda _: self.interrupt_refresh_plots.set).start()
        interval_timeout = threading.Event()
        plots = submissions_viewer.grades.plots.Plots()
        while not self.interrupt_refresh_plots.is_set():
            interval_timeout.clear()
            threading.Timer(self.update_interval, interval_timeout.set).start()
            self.refresh_plots(plots)
            while True:
                if interval_timeout.wait(timeout=1):
                    break
                if self.interrupt_refresh_plots.wait(timeout=1):
                    break

    def _pull_and_filter_db(self):
        self.db.pull_db(self.url)
        if self.filter_value == 'All':
            return self.db.filter_db('')
        else:
            return self.db.filter_db(self.filter_value)

    def refresh_plots(self, plots):
        filtered_db = self._pull_and_filter_db()
        figs = []
        for i in range(4):
            time.sleep(1)
            _display(
                self.outs[i],
                plots.num_passing_per_test(filtered_db),
                clear_output=False
            )


class Controller:
    def __init__(self, ui_out, plots_out):
        self.ui_out = ui_out
        self.plots_out = plots_out
        self.wg = submissions_viewer.grades.grades_wg.Widgets()
        self.db = submissions_viewer.grades.gradesDB.GradesDB()
        self.interrupt_refresh_plots = threading.Event()
        self.wg['search_filter']
        self.wg['update_url'].on_click(
            lambda _: self.apply_url(),
        )
        self.wg['search_filter'].observe(
            handler=lambda _: self.apply_filter(),
            names=['value']
        )
        self.wg['interrupt_button'].on_click(lambda _: self.apply_interrupt())
        self.wg['resume_button'].on_click(lambda _: self.apply_resume())
        self.wg._display(self.ui_out)

    def apply_interrupt(self):
        self.interrupt_refresh_plots.set()
        self.set_widgets_interaction(disabled=False)

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
        if self.wg['dropdown'].value == 'All':
            return self.db.filter_db(self.wg['search_filter'].value)
        else:
            return self.db.filter_db(self.wg['dropdown'].value)

    def set_widgets_interaction(self, disabled: bool):
        self.wg['url'].disabled = disabled
        self.wg['update_url'].disabled = disabled
        self.wg['search_filter'].disabled = disabled
        self.wg['dropdown'].disabled = disabled
        self.wg['update_interval'].disabled = disabled
        self.wg['resume_button'].disabled = disabled
        self.wg['interrupt_button'].disabled = not disabled

    def apply_resume(self):
        for thread in threading.enumerate():
            if thread.getName() == 'refresh_plots':
                thread.join(timeout=0)
        self.set_widgets_interaction(disabled=True)
        filter_value = self.wg['search_filter'].value \
            if self.wg['dropdown'].value == 'All' \
            else self.wg['dropdown'].value
        runner = Runner(
            url=self.wg['url'].value,
            filter_value=filter_value,
            update_interval=self.wg['update_interval'].value,
            interrupt_refresh_plots=self.interrupt_refresh_plots,
            outs=self.plots_out
        )
        threading.Thread(name='refresh_plots', target=runner, daemon=True).start()
