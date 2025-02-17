project(
  'steam-survey-explorer',
  version: '0.1.0',
  meson_version: '>= 0.62.0',
  default_options: [
    'warning_level=2',
    'werror=false',
  ],
)

# Translations are broken on Windows for multiple reasons
# gresources don't work and MSYS2 seems to have also broken the gettext package
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

py_installation = python.find_installation('python3')

python_dir = join_paths(get_option('prefix'), py_installation.get_install_dir())
pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
libexecdir = join_paths(get_option('prefix'), get_option('libexecdir'))
app_id = 'io.github.jspast.SteamSurveyExplorer'
prefix = '/io/github/jspast/SteamSurveyExplorer'

conf = configuration_data()
conf.set('PYTHON', py_installation.full_path())
conf.set('PYTHON_VERSION', py_installation.language_version())
conf.set('APP_ID', app_id)
conf.set('PREFIX', prefix)
conf.set('VERSION', meson.project_version())
conf.set('BIN', join_paths(get_option('prefix'), get_option('bindir'), meson.project_name()))
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)
conf.set('libexecdir', libexecdir)

subdir('src')
subdir('data')

if host_machine.system() != 'windows'
  subdir('po')

  gnome.post_install(
    glib_compile_schemas: true,
    gtk_update_icon_cache: true,
    update_desktop_database: true,
  )
else
  gnome.post_install(
    glib_compile_schemas: true,
    gtk_update_icon_cache: true,
    update_desktop_database: false,
  )
endif

