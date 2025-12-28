
# cssselector

## Overview

![](https://img.shields.io/badge/Python-3.12-blue)
![](https://img.shields.io/badge/License-AGPLv3-blue)

任意のCSSセレクターが指定されたHTML階層と一致するかを検証する機能を提供します。

本パッケージは `html.parser.HTMLParser` を用いてHTML文書を編集するために開発されました。
単純にHTML文書を編集するだけならば、より高度な機能が使える `BeautifulSoup` の使用を推奨します。

## Usage

基本機能の実行例

```py
import cssselector

selector = cssselector.parse_selector("p > a.read-more")
selector.match([("html", {}), ("body", {}), ("p", {}), ("a", {"href": "...", "class": "read-more"}), ("b", {})]) #True
selector.match([("html", {}), ("body", {}), ("p", {}), ("a", {"href": "...", "class": "read-more"})]) #True
selector.match([("html", {}), ("body", {}), ("p", {})]) #False
```

`html.parser.HTMLParser` と組み合わせた実行例

```py
import cssselector
from html.parser import HTMLParser

class TextExtractor (HTMLParser):

  def __init__ (self, selector:cssselector.ISelector):
    super().__init__()
    self.selector = selector
    self.element_stack = []

  def handle_starttag (self, tag:str, attrs:list[tuple[str, str]]):
    self.element_stack.append((tag, dict(attrs)))

  def handle_endtag (self, tag:str):
    self.element_stack.pop()

  def handle_data (self, data:str):
    if self.selector.match(self.element_stack):
      print(data)

selector = cssselector.parse_selector("p > a[href]")
extractor = TextExtractor(selector)
extractor.feed("""
<html>
  <head></head>
  <body>
    <h1></h1>
    <p>
      <a>Never Extract...</a>
      <a href="">Should Extract!</a>
    </p>
  </body>
</html>
""") #Should Extract!
```

## 対応セレクター

[cssselector](https://github.com/tikubonn/cssselector)が対応しているセレクターは次のとおりです。

### 単純セレクター

| 名称 | コード | 説明 |
| --- | --- | --- | 
| 全称セレクター | `*` | あらゆる要素名に一致します。 |
| 要素型セレクター | `タグ名` | 指定された要素名に一致します。 |
| クラスセレクター | `.クラス名` | 指定されたクラス名をもつ要素に一致します。 |
| IDセレクター | `#ID名` | 指定されたID名をもつ要素に一致します。 |
| 属性セレクター | `[属性名="属性値"]` ... | 指定された属性をもつ要素に一致します。対応している属性セレクターは[#属性セレクター](#属性セレクター)を参照ください。 |

#### 属性セレクター

| コード | 説明 |
| --- | --- |
| `[属性名]` | 指定された属性値が存在するかを判定する。 |
| `[属性名="属性値"]` | 指定属性値が指定値と一致するかを判定する。 |
| `[属性名^="属性値"]` | 指定属性値の先頭が指定値と一致するかを判定する。 |
| `[属性名$="属性値"]` | 指定属性値の末尾が指定値と一致するかを判定する。 |
| `[属性名*="属性値"]` | 指定属性値に指定値が含まれるかを判定する。 |
| `[属性名~="属性値"]` | 空白文字で区切られた指定属性値に、指定値が含まれるかを判定する。 |

### 結合子

兄弟結合子などの複雑な結合子は非対応です。

| 名称 | コード | 説明 | 
| --- | --- | --- |
| 子結合子 | `A > B` | 指定要素が直下にあるならば一致します。 |
| 子孫結合子 | `A B` | 指定要素が子要素として存在するならば一致します。 |

### その他

| 名称 | コード | 説明 |
| --- | --- | --- |
| セレクターリスト | `A,B,C` | 複数セレクターのうちいずれかに一致すれば一致扱いになります。 |

## Install

```shell
pip install .
```

### Test

```shell
pip install .[test]
pytest .
```

### Document

```py
import cssselector

help(cssselector)
```

## Donation

<a href="https://buymeacoffee.com/tikubonn" target="_blank"><img src="doc/img/qr-code.png" width="3000px" height="3000px" style="width:150px;height:auto;"></a>

もし本パッケージがお役立ちになりましたら、少額の寄付で支援することができます。<br>
寄付していただいたお金は書籍の購入費用や日々の支払いに使わせていただきます。
ただし、これは寄付の多寡によって継続的な開発やサポートを保証するものではありません。ご留意ください。

If you found this package useful, you can support it with a small donation.
Donations will be used to cover book purchases and daily expenses.
However, please note that this does not guarantee ongoing development or support based on the amount donated.

## License

© 2025 tikubonn

cssselector licensed under the [AGPLv3](./LICENSE).
