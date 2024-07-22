# SteamSurveyExplorer

## Compilando no Linux

### Usando GNOME Builder

Na tela inicial, clique em clonar repositório.

Use o endereço: https://github.com/jspast/SteamSurveyExplorer.git

Para compilar, clique o botão de play.

## Compilando no Windows

### Python

Primeiro, instale o [Python](https://www.python.org/downloads/windows/).

### Meson

Depois de instalar o Python, baixe o Meson, que é o sistema de compilação utilizado:

```PowerShell
pip install meson
```

### GTK

É preciso ter as bibliotecas GTK instaladas e configuradas.

A forma mais fácil é por meio do [gvsbuild](https://github.com/wingtk/gvsbuild/releases), que disponibiliza os arquivos necessários pré-compilados.

Baixe a última versão e extraia o arquivo `GTK4_Gvsbuild_VERSION_x64.zip` para `C:\gtk`.

Depois, defina as variáveis de ambiente necessárias executando os comandos abaixo no PowerShell:

```PowerShell
$currentPath = [System.Environment]::GetEnvironmentVariable("Path", "User")
$newPath = $currentPath + ";C:\gtk\bin"
[System.Environment]::SetEnvironmentVariable("Path", $newPath, "User")

$currentLIB = [System.Environment]::GetEnvironmentVariable("LIB", "User")
$newLIB = $currentLIB + ";C:\gtk\lib"
[System.Environment]::SetEnvironmentVariable("LIB", $newLIB, "User")

$currentINCLUDE = [System.Environment]::GetEnvironmentVariable("INCLUDE", "User")
$newINCLUDE = $currentINCLUDE + ";C:\gtk\include;C:\gtk\include\cairo;C:\gtk\include\glib-2.0;C:\gtk\include\gobject-introspection-1.0;C:\gtk\lib\glib-2.0\include"
[System.Environment]::SetEnvironmentVariable("INCLUDE", $newINCLUDE, "User")

$currentXDG_DATA_HOME = [System.Environment]::GetEnvironmentVariable("XDG_DATA_HOME", "User")
$newXDG_DATA_HOME = $currentXDG_DATA_HOME + ";$HOME\.local\share"
[System.Environment]::SetEnvironmentVariable("XDG_DATA_HOME", $newXDG_DATA_HOME, "User")
```

Também é possível alterar as variáveis de ambiente nas Configurações avançadas do sistema.

### PyGObject e pycairo

Essas dependências devem ser instaladas pelo pip, com correções feitas pelo gvsbuild:

```PowerShell
pip install --force-reinstall (Resolve-Path C:\gtk\wheels\PyGObject*.whl)
pip install --force-reinstall (Resolve-Path C:\gtk\wheels\pycairo*.whl)
```

### Matplotlib

Biblioteca usada para gerar gráficos, também deve ser instalada pelo pip:

```PowerShell
pip install matplotlib
```

### Compilando

No diretório que deseja colocar o programa, clone o repositório com [git](https://gitforwindows.org/):

```PowerShell
git clone https://github.com/jspast/SteamSurveyExplorer.git
cd SteamSurveyExplorer
```

#### Configuração

Inicialize a pasta de compilação:

```PowerShell
meson setup builddir
```

Configure para instalar na pasta:

```PowerShell
meson configure builddir --prefix $PWD\builddir\output\
```

#### Comandos principais

Compile o programa:

```PowerShell
meson compile -C builddir
```

Instale o programa, removendo instalação antiga se existir:

```PowerShell
Remove-Item -Path builddir\output\bin\steam-survey-explorer -Force ; meson install -C builddir
```

Execute o programa:

```PowerShell
py builddir\output\bin\steam-survey-explorer
```
