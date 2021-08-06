# 日本語病名正規化
日本語の病名を[標準病名マスター](http://www.byomei.org/)の標準病名に紐づけるライブラリです。  
[万病辞書](https://sociocom.naist.jp/manbyou-dic/)に名寄せすることで紐付けします。  
略語辞書による略語の展開にも対応しています。 

## インストール
```bash
pip install git+https://github.com/ujiuji1259/disease_normalizer.git
```

## 手法
- Exact Match  
万病辞書との完全一致で標準病名に紐付けます。  
- Fuzzy Match  
[simstring](http://www.chokkan.org/software/simstring/index.html.ja)による曖昧一致を行います。文字単位の2-gramによるコサイン類似度により類似度を計算します。
- DNorm  
古典的な病名正規化手法である[DNorm](http://dx.doi.org/10.1093/bioinformatics/btt474)を用いて病名を名寄せします。Tf-idfベースのランキング学習手法です。

## 使用例
```python
from japanese_disease_normalizer.normalizer import Normalizer

normalizer = Normalizer("abbr", "fuzzy")

input_disease = "AML"
normalized_term = normalizer.normalize(input_disease)
```

## Spacy extension
spacyのパイプラインに加えることで，固有表現（ここでは病名）に正規化結果の`DictEntry`を付与することができます．  
日本語モデル（`spacy.lang.ja.Japanese`）を元にした病名認識パイプラインを公開していますので，そちらもご利用ください．
### 使用例
```python
import spacy
from japanese_disease_normalizer.spacy_extension import ManbyoNormalizer

nlp = spacy.load("/path/to/model_for_disease_recognition")
nlp.add_pipe("manbyo_normalizer")

text = "急性骨髄性白血病により緊急入院"
doc = nlp(text)
for ent in doc.ents:
  print(ent._.norm)
```

### 結果
`DictEntry(name="急性骨髄性白血病", icd="C920", norm="急性骨髄性白血病", level="S")`

## 略語展開例

`>>> normalizer.normalize("高K血症")`  
`DictEntry(name='高カリウム血症', icd='E875', norm='高カリウム血症', level='S')`  
`>>> normalizer.normalize("AML")`  
`DictEntry(name='急性骨髄性白血病特', icd='C920', norm='急性骨髄性白血病', level='C')`
