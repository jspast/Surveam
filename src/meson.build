moduledir = python_dir / 'steam_survey_explorer'

blueprints = custom_target('blueprints',
  input: files(
    'ui/main_window.blp',
    'ui/about.blp',
    'ui/category_window.blp'
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

gnome.compile_resources('steam-survey-explorer',
  configure_file(
    input: 'steam_survey_explorer.gresource.xml.in',
    output: 'steam_survey_explorer.gresource.xml',
    configuration: conf,
  ),
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  dependencies: blueprints,
)

configure_file(
  input: 'steam-survey-explorer.in',
  output: 'steam-survey-explorer',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
)

steam_survey_explorer_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'category_window.py',
]

install_data(steam_survey_explorer_sources, install_dir: moduledir)
