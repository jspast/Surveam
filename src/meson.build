moduledir = python_dir / 'steam_survey_explorer'

blueprints = custom_target('blueprints',
  input: files(
    'ui/main_window.blp',
    'ui/about_dialog.blp',
    'ui/category_window.blp',
    'ui/category_box.blp'
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

steam_survey_explorer_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'category_window.py',
  'db/database.py',
  'db/data.py',
  'db/trie.py',
]

install_data(steam_survey_explorer_sources, install_dir: moduledir)
