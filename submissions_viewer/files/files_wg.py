import webbrowser

from IPython import display
from ipywidgets import widgets

import submissions_viewer.files.utils


class Widgets:
    def __init__(self, out: widgets.Output, get_filtered_db):
        self.wg = dict()
        self.files = []
        self.scores = []
        self._selected_index = 0
        self._get_filtered_db = get_filtered_db
        self._create()
        self._add_functionality()
        self._display(out)
        self.update_files_and_scores()

    def _create(self):
        default_layout = widgets.Layout(width='auto', height='auto')
        self.wg['organization'] = widgets.Text(
            value='TestOrgJustAymeric',
            description='Organization',
            layout=default_layout
        )
        self.wg['repository_prefix'] = widgets.Text(
            placeholder='Repository name prefix',
            description='Filter',
            layout=default_layout
        )
        self.wg['filename'] = widgets.Text(
            value='exercice.py',
            description='Filename',
            layout=default_layout
        )
        self.wg['request_url'] = widgets.Text(
            description='Request',
            value=f'https://raw.githubusercontent.com/{self.wg["organization"].value}/%RepositoryName%/master/{self.wg["filename"].value}',
            layout=default_layout,
            disabled=True
        )
        self.wg['get_files'] = widgets.Button(description='Fetch submissions')
        self.wg['get_files_status'] = widgets.Valid(layout=default_layout)
        self.wg['previous_button'] = widgets.Button(description='Previous')
        self.wg['next_button'] = widgets.Button(description='Next')
        self.wg['open_in_browser'] = widgets.Button(description='Open in GitHub', layout=default_layout)
        self.wg['open_file'] = widgets.Checkbox(description='File only', layout=default_layout)
        self.wg['repository_select'] = widgets.Dropdown(
            description='Select',
            # options=[''],
            layout=widgets.Layout(width='600px'))
        self.wg['max_preview_lines'] = widgets.IntText(
            value=100,
            disabled=False,
            layout=widgets.Layout(width='50px')
        )
        self.wg['preview_lines_range'] = widgets.IntRangeSlider(
            value=[0, 20],
            min=0,
            max=self.wg['max_preview_lines'].value,
            step=1,
            description='Lines range:',
            continuous_update=True,
            orientation='horizontal',
            readout=True,
            readout_format='d',
            layout=widgets.Layout(width='500px')
        )
        self.wg['repository_grading'] = widgets.HTML(
            layout=widgets.Layout(
                width='auto',
                height='auto',
                border='solid 1px',
                padding='2px 10px 2px 10px'
            )
        )
        html_layout = widgets.Layout(width='auto', height='auto', padding='20px 100px 0px 20px')
        self.wg['file_preview_stats'] = widgets.HTML(layout=html_layout)
        self.wg['file_preview'] = widgets.HTML(layout=html_layout)
        self.wg['file_view_stats'] = widgets.HTML(layout=html_layout)
        self.wg['file_view'] = widgets.HTML(layout=html_layout)
        file_preview_box = widgets.HBox((self.wg['file_preview'], self.wg['file_preview_stats']))
        file_view_box = widgets.HBox((self.wg['file_view'], self.wg['file_view_stats']))
        lines_range_box = widgets.HBox((self.wg['preview_lines_range'], self.wg['max_preview_lines']))
        self.wg['accordion'] = widgets.Accordion(
            children=[
                widgets.VBox((lines_range_box, file_preview_box)),
                file_view_box
            ]
        )
        self.wg['accordion'].set_title(0, 'Preview')
        self.wg['accordion'].set_title(1, 'File')

    def _add_functionality(self):
        self.wg['organization'].observe(lambda _: self._update_request_url())
        self.wg['filename'].observe(lambda _: self._update_request_url())
        self.wg['repository_prefix'].observe(lambda _: self._update_request_url())
        self.wg['max_preview_lines'].observe(lambda _: self._update_max_preview_lines())
        self.wg['get_files'].on_click(lambda _: self.update_files_and_scores())
        self.wg['previous_button'].on_click(lambda _: self._select_previous())
        self.wg['next_button'].on_click(lambda _: self._select_next())
        self.wg['open_in_browser'].on_click(lambda _: self._open_browser())
        self.wg['repository_select'].observe(lambda _: self._apply_select())
        self.wg['preview_lines_range'].observe(lambda _: self._update_file_preview())

    def _display(self, out: widgets.Output):
        @out.capture()
        def _display():
            display.display(self.wg['organization'])
            display.display(self.wg['filename'])
            display.display(self.wg['repository_prefix'])
            display.display(self.wg['request_url'])
            display.display(widgets.HBox((self.wg['get_files'], self.wg['get_files_status'])))
            display.display(
                widgets.HBox((self.wg['repository_select'], self.wg['open_in_browser'], self.wg['open_file'])))
            display.display(widgets.HBox((self.wg['previous_button'], self.wg['next_button'])))
            display.display(self.wg['repository_grading'])
            display.display(self.wg['accordion'])

        _display()

    def _update_max_preview_lines(self):
        self.wg['preview_lines_range'].max = self.wg['max_preview_lines'].value

    def _open_browser(self):
        org = self.wg['organization'].value
        repo = self.wg['repository_select'].value
        filename = self.wg['filename'].value
        if self.wg['open_file'].value == True:
            webbrowser.open(f'https://github.com//{org}/{repo}/blob/master/{filename}')
        else:
            webbrowser.open(f'https://github.com//{org}/{repo}')

    def _update_request_url(self):
        org = self.wg['organization'].value
        filename = self.wg['filename'].value
        repository_prefix = self.wg['repository_prefix'].value
        self.wg[
            'request_url'].value = f'https://raw.githubusercontent.com/{org}/%Repository name containing: {repository_prefix}%/master/{filename}'

    def _update_file_view(self, selected_index=None):
        if selected_index is not None:
            self._selected_index = selected_index
        try:
            file = self.files[self._selected_index]
            line_scores = self.scores[self._selected_index]
            self.wg['file_view_stats'].value = '<pre><code>' + ''.join(line_scores) + '</code></pre>'
            self.wg['file_view'].value = '<pre><code>' + file + '</code></pre>'
        except IndexError as e:
            self.wg['file_view_stats'].value = '<p>Couldn\'t get stats</p>'
            self.wg['file_view'].value = '<p>Couldn\'t get file</p>'

    def _update_file_preview(self, selected_index=None):
        if selected_index is not None:
            self._selected_index = selected_index
        try:
            file = self.files[self._selected_index]
            line_scores = self.scores[self._selected_index]
            lines_range = self.wg['preview_lines_range']
            file_lines = [line + '\n' for line in file.split('\n')]
            selected_lines = file_lines[lines_range.lower: min(lines_range.upper, len(file_lines))]
            selected_scores = line_scores[lines_range.lower: min(lines_range.upper, len(line_scores))]
            self.wg['file_preview_stats'].value = '<pre><code>' + ''.join(selected_scores) + '</code></pre>'
            self.wg['file_preview'].value = '<pre><code>' + ''.join(selected_lines) + '</code></pre>'
        except IndexError as e:
            self.wg['file_preview_stats'].value = '<p>Couldn\'t get stats</p>'
            self.wg['file_preview'].value = '<p>Couldn\'t get file</p>'

    def update_files_and_scores(self):
        org = self.wg['organization'].value
        filename = self.wg['filename'].value
        repository_names = self._get_repository_names()
        urls = list(map(
            lambda
                repo: f'https://raw.githubusercontent.com/{org}/{repo}/master/{filename}',
            repository_names
        ))
        self.files = []
        self.wg['get_files_status'].value = True
        self.wg['get_files_status'].description = f'Success'
        for url in urls:
            try:
                file = submissions_viewer.files.utils.get_file(url)
                self.files.append(file)
            except Exception as e:
                self.files.append('Couldn\'t get file')
                self.wg['get_files_status'].value = False
                self.wg['get_files_status'].description = f'{e}'
        files_scores = submissions_viewer.files.utils.get_scores(self.files)
        formated_scores = []
        for scores in files_scores:
            formated_scores.append(
                list(map(
                    lambda score: f'{100 * score / len(files_scores):.2f}% ({score}/{len(files_scores)})\n',
                    scores
                ))
            )
        self.scores = formated_scores
        self.wg['repository_select'].options = repository_names
        self._update_file_preview()
        self._update_file_view()
        self._update_repository_grading()

    def _select_previous(self):
        self._selected_index = max(0, self._selected_index - 1)
        self.wg['repository_select'].value = list(self.wg['repository_select'].options)[self._selected_index]

    def _select_next(self):
        self._selected_index = min(len(self.files) - 1, self._selected_index + 1)
        self.wg['repository_select'].value = list(self.wg['repository_select'].options)[self._selected_index]

    def _apply_select(self):
        try:
            selected = self.wg['repository_select'].value
            self._selected_index = list(self.wg['repository_select'].options).index(selected)
        except ValueError:
            self._selected_index = 0
        self._update_file_preview()
        self._update_file_view()
        self._update_repository_grading()

    def _update_repository_grading(self):
        filter_value = self.wg['repository_prefix'].value
        filtered_db = self._get_filtered_db(filter_value)
        try:
            test_dict = filtered_db[self.wg['repository_select'].value]
            grading_html = 'Test results:<br>'
            for test_name, test_result in test_dict.items():
                result = "ok" if test_result["passing"] else "fail"
                grading_html += f'- {test_name}: {result}<br>'
            self.wg['repository_grading'].value = grading_html
        except:
            self.wg['repository_grading'].value = '<p>Couldn\'t apply grading</p>'

    def _get_repository_names(self):
        filter_value = self.wg['repository_prefix'].value
        filtered_db = self._get_filtered_db(filter_value)
        return list(filtered_db.keys())
