[![shuncommand Actions](https://github.com/mypaceshun/shuncommands/actions/workflows/main.yml/badge.svg)](https://github.com/mypaceshun/shuncommands/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/mypaceshun/shuncommands/branch/main/graph/badge.svg?token=6Z6O1J3K0E)](https://codecov.io/gh/mypaceshun/shuncommands)
[![PyPI](https://img.shields.io/pypi/v/shuncommands?style=plastic)](https://pypi.org/project/shuncommands/)
[![Downloads](https://static.pepy.tech/badge/shuncommands)](https://pepy.tech/project/shuncommands)
# shuncommands

my usefull commands


# install

```
$ pip install shuncommands
```

# install with pdftool

```
$ pip install shuncommands[pdf]
```

# install commands

  * rmtmp
  * pdftool (Require install with pdf)

# rmtmp Usage

```
Usage: rmtmp [OPTIONS] TARGETDIR

  tmpディレクトリの中身お掃除君

  <TARGETDIR>で指定されたディレクトリの中身をせっせとお掃除してくれるかわいいやつ。
  自分がよく ~/document/tmp/ とか雑にディレクトリ作ってしまうので、それのお掃除用に生まれた

  <TARGETDIR>/.rmtmpignore のファイルに gitignore と同様の書式でファイルを指定することで、
  削除対象から明示的に外すことができる。

Options:
  -q, --quiet              quiet output
  --dry-run
  -d, --day INTEGER RANGE  削除対象となる期日  [default: 3; x>=0]
  --help                   Show this message and exit.
```

# pdftool usage

```
Usage: pdftool [OPTIONS] COMMAND [ARGS]...

  PDF file をあれやこれやしたいがためのコマンド

Options:
  -v, --version  Show the version and exit.
  -h, --help     Show this message and exit.

Commands:
  text    PDFファイルを、テキストファイルに変換する
  unlock  パスワード付きPDFファイルを、パスワードなしPDFファイルにコピーする
```
