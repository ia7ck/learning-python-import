ディレクトリ構造は以下で、依存関係は `main.py <- aaa.py <- bbb.py` となっている。

```
./ok001
|-- main.py
`-- pkg
 |-- __init__.py
 |-- aaa.py
 `-- bbb.py
```

`cd ok001 && python main.py` をしたときエラーにならないでほしい。

## 用語の整理

### モジュール

用語集によると [module](https://docs.python.org/ja/3.8/glossary.html#term-module) は

> Python コードの組織単位としてはたらくオブジェクト

とのこと。???

Python コードが書かれているファイルと考えていい?

### パッケージ

regular package と namespace package があるが、ここでは regular package のみを扱う。

ふたたび用語集によると [package](https://docs.python.org/ja/3.8/glossary.html#term-package) は

> サブモジュールや再帰的にサブパッケージを含むことの出来る module のこと

で、[regular package](https://docs.python.org/ja/3.8/glossary.html#term-regular-package) は

> `__init__.py` ファイルを含むディレクトリとしての package

とのこと。package はよく分からないけど、regular package は「`__init__.py` ファイルを含むディレクトリ」と考えてよさそう。

## 検証

### ng

`aaa.py` の 1 行目 `import bbb` で `ModuleNotFoundError: No module named 'bbb'` となる。

### ok001

`pkg/__init__.py` に `sys.path.append(os.path.dirname(__file__))` と書くことで 、`pkg` をモジュール検索パスに追加する ([参考](https://docs.python.org/ja/3/library/sys.html?highlight=sys%20path#sys.path)) と上手くいく。`__init__.py` はパッケージが import されるときに実行される ([参考](https://docs.python.org/ja/3.8/reference/import.html#regular-packages)) ため、おそらく `pkg/aaa.py` の `import bbb` より早く上の処理が行われて期待する動作になる。

### ok002

`pkg001`, `pkg002`, ... のように複数のパッケージがある場合 `__init__.py` をいくつも作る必要がある。これを避けるには `main.py` の先頭に

```python
for p in pathlib.Path(".").iterdir():
    if p.is_dir():
        sys.path.append(str(p.resolve()))
```

を書けばいい。内容は、`main.py` があるディレクトリ直下のパッケージ (のパス) をモジュール検索リストに追加する、というもの。[pathlib](https://docs.python.org/ja/3/library/pathlib.html) などを参考にする。

### ok003

`pkg/aaa.py` で `from . import bbb` と書くと `python main.py` は上手くいく。[relative import](https://docs.python.org/ja/3/reference/import.html#package-relative-imports) を参考にする。ただ、`python pkg/aaa.py` や `cd pkg && python aaa.py` は `ImportError: cannot import name 'bbb' from '__main__'` となり失敗する。???
