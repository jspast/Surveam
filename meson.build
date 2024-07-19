project(
  'steam-survey-explorer',
  version: '0.1.0',
  meson_version: '>= 0.62.0',
  default_options: [
    'warning_level=2',
    'werror=false',
  ],
)

platform = build_machine.system()

i18n = import('i18n')
gnome = import('gnome')
python = import('python')

dependency('glib-2.0', version: '>= 2.76.0')
dependency('gio-2.0', version: '>= 2.76.0')
dependency('gtk4', version: '>= 4.13.0')

libadwaita = dependency(
  'libadwaita-1',
  version: '>= 1.5.0',
  fallback: ['libadwaita', 'libadwaita_dep'],
  default_options: [
    'examples=false',
    'introspection=disabled',
    'tests=false',
    'vapi=false',
  ]
)

pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())

conf = configuration_data()
conf.set('PYTHON', python.find_installation().full_path())
conf.set('VERSION', meson.project_version())
conf.set('BIN', join_paths(get_option('prefix'), get_option('bindir'), meson.project_name()))
conf.set('pkgdatadir', join_paths(get_option('prefix'), get_option('datadir'), meson.project_name()))
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))

subdir('src')
subdir('data')
subdir('po')

if platform == 'windows'
	gnome.post_install(
	  glib_compile_schemas: true,
	  gtk_update_icon_cache: true,
	  update_desktop_database: false,
	)
else
	gnome.post_install(
	  glib_compile_schemas: true,
	  gtk_update_icon_cache: true,
	  update_desktop_database: true,
	)
endif