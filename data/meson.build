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
  install_mode: 'rwxr-xr-x'
)

if host_machine.system() == 'windows'
  desktop_file = configure_file(
    input: app_id + '.desktop.in',
    output: app_id + '.desktop.in',
    configuration: conf,
    install: true,
    install_dir: get_option('datadir') / 'applications'
  )
else
  desktop_file = i18n.merge_file(
    input: configure_file(
      input: app_id + '.desktop.in',
      output: app_id + '.desktop.in',
      configuration: conf,
    ),
    output: app_id + '.desktop',
    type: 'desktop',
    po_dir: '../po',
    install: true,
    install_dir: get_option('datadir') / 'applications',
  )
endif

if host_machine.system() != 'windows'
  desktop_utils = find_program('desktop-file-validate', required: false)
  if desktop_utils.found()
    test('Validate desktop file', desktop_utils, args: [desktop_file])
  endif
endif

if host_machine.system() == 'windows'
  appstream_file = configure_file(
    input: app_id + '.metainfo.xml.in',
    output: app_id + '.metainfo.xml',
    configuration: conf,
    install: true,
    install_dir: get_option('datadir') / 'metainfo',
  )
else
  appstream_file = i18n.merge_file(
    input: configure_file(
      input: app_id + '.metainfo.xml.in',
      output: app_id + '.metainfo.xml.in',
      configuration: conf,
    ),
    output: app_id + '.metainfo.xml',
    po_dir: '../po',
    install: true,
    install_dir: get_option('datadir') / 'metainfo',
  )
endif

if host_machine.system() != 'windows'
  appstreamcli = find_program('appstreamcli', required: false)
  if appstreamcli.found()
    test(
      'Validate appstream file',
      appstreamcli,
      args: ['validate', '--no-net', '--explain', appstream_file],
      workdir: meson.current_build_dir(),
    )
  endif
endif

install_data(
  configure_file(
    input: app_id + '.gschema.xml.in',
    output: app_id + '.gschema.xml',
    configuration: conf,
  ),
  install_dir: get_option('datadir') / 'glib-2.0' / 'schemas',
)

compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test(
    'Validate schema file',
    compile_schemas,
    args: ['--strict', '--dry-run', meson.current_source_dir()],
  )
endif

subdir('icons')