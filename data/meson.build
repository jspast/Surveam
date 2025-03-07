desktop_file = i18n.merge_file(
        input: 'io.github.jspast.Surveam.desktop.in',
       output: 'io.github.jspast.Surveam.desktop',
         type: 'desktop',
       po_dir: '../po',
      install: true,
  install_dir: get_option('datadir') / 'applications'
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils, args: [desktop_file])
endif

appstream_file = i18n.merge_file(
        input: 'io.github.jspast.Surveam.metainfo.xml.in',
       output: 'io.github.jspast.Surveam.metainfo.xml',
       po_dir: '../po',
      install: true,
  install_dir: get_option('datadir') / 'metainfo'
)

appstreamcli = find_program('appstreamcli', required: false, disabler: true)
test('Validate appstream file', appstreamcli,
     args: ['validate', '--no-net', '--explain', appstream_file])

install_data('io.github.jspast.Surveam.gschema.xml',
  install_dir: get_option('datadir') / 'glib-2.0' / 'schemas'
)

compile_schemas = find_program('glib-compile-schemas', required: false, disabler: true)
test('Validate schema file',
     compile_schemas,
     args: ['--strict', '--dry-run', meson.current_source_dir()])


service_conf = configuration_data()
service_conf.set('bindir', get_option('prefix') / get_option('bindir'))
configure_file(
  input: 'io.github.jspast.Surveam.service.in',
  output: 'io.github.jspast.Surveam.service',
  configuration: service_conf,
  install_dir: get_option('datadir') / 'dbus-1' / 'services'
)

styles = files(
  'styles/adwaita.mplstyle',
  'styles/adwaita-dark.mplstyle',
)

install_data(styles, install_dir: moduledir / 'styles')

csvs = files('shs.csv', 'shs_platform.csv', 'mapping.csv')

install_data(csvs, install_dir: moduledir / 'data')

subdir('icons')
