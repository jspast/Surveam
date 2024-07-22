pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'steam_survey_explorer'
gnome = import('gnome')

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
  'steam_survey_explorer.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  dependencies: blueprints,
)

python = import('python')

configure_file(
  input: 'steam-survey-explorer.in',
  output: 'steam-survey-explorer',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'rwxr-xr-x'
)

steam_survey_explorer_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'category_window.py',
]

install_data(steam_survey_explorer_sources, install_dir: moduledir)
