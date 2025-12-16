# `Literal`が必要な理由

## 問題：`bool`型では型チェッカーが区別できない

### ❌ `bool`を使った場合（動作しない）

```python
@overload
def get_document_list(
    self, date: datetime.datetime, withdocs: bool = False
) -> GetDocumentResponse: ...

@overload
def get_document_list(
    self, date: datetime.datetime, withdocs: bool = True
) -> GetDocumentResponseWithDocs: ...
```

**問題点：**

- `bool`型は`True`と`False`の**両方**を含む型
- 型チェッカーは「`withdocs`が`True`か`False`か」を**実行時まで判断できない**
- そのため、どちらのオーバーロードを使うべきか判断できず、`Union[GetDocumentResponse, GetDocumentResponseWithDocs]`として推論される

### ✅ `Literal`を使った場合（正しく動作）

```python
@overload
def get_document_list(
    self, date: datetime.datetime, withdocs: Literal[False] = False
) -> GetDocumentResponse: ...

@overload
def get_document_list(
    self, date: datetime.datetime, withdocs: Literal[True]
) -> GetDocumentResponseWithDocs: ...
```

**利点：**

- `Literal[False]`は「`False`という**具体的な値**」を表す型
- `Literal[True]`は「`True`という**具体的な値**」を表す型
- 型チェッカーは、呼び出し時に渡された値（またはデフォルト値）を見て、**正しいオーバーロードを選択できる**

## 具体例

### ケース 1: デフォルト値を使用（`withdocs`を省略）

```python
# 呼び出し
document_list = target.get_document_list(datetime_obj)
# withdocsのデフォルト値はFalse

# Literal[False]を使っている場合
# → 型チェッカーは「withdocs=False」と判断
# → 最初のオーバーロードを選択
# → 戻り値型: GetDocumentResponse ✅

# boolを使っている場合
# → 型チェッカーは「withdocsはbool型」としか判断できない
# → どちらのオーバーロードか判断できない
# → 戻り値型: GetDocumentResponse | GetDocumentResponseWithDocs ❌
```

### ケース 2: 明示的に`False`を指定

```python
# 呼び出し
document_list = target.get_document_list(datetime_obj, withdocs=False)

# Literal[False]を使っている場合
# → 型チェッカーは「withdocs=Literal[False]」と判断
# → 最初のオーバーロードを選択
# → 戻り値型: GetDocumentResponse ✅

# boolを使っている場合
# → 型チェッカーは「withdocs=bool型のFalse」と判断
# → でもbool型はTrueもFalseも含むので、どちらか判断できない
# → 戻り値型: GetDocumentResponse | GetDocumentResponseWithDocs ❌
```

### ケース 3: 明示的に`True`を指定

```python
# 呼び出し
document_list = target.get_document_list(datetime_obj, withdocs=True)

# Literal[True]を使っている場合
# → 型チェッカーは「withdocs=Literal[True]」と判断
# → 2番目のオーバーロードを選択
# → 戻り値型: GetDocumentResponseWithDocs ✅

# boolを使っている場合
# → 型チェッカーは「withdocs=bool型のTrue」と判断
# → でもbool型はTrueもFalseも含むので、どちらか判断できない
# → 戻り値型: GetDocumentResponse | GetDocumentResponseWithDocs ❌
```

## まとめ

| 方法                               | 型チェッカーの判断                                | 戻り値型の推論                                                   |
| ---------------------------------- | ------------------------------------------------- | ---------------------------------------------------------------- |
| `bool`                             | 「`withdocs`は`bool`型（`True`か`False`か不明）」 | `GetDocumentResponse \| GetDocumentResponseWithDocs`（曖昧）     |
| `Literal[False]` / `Literal[True]` | 「`withdocs`は具体的な値（`False`または`True`）」 | `GetDocumentResponse`または`GetDocumentResponseWithDocs`（正確） |

**結論：** `Literal`を使うことで、型チェッカーが**実行前に**正しい戻り値型を推論できるようになります。これにより、IDE の補完や型チェックが正確に動作します。
