# olunicodenormalizer
ᱚᱞ-ᱪᱦᱤᱠᱤ Unicode Normalization for word normalization
# install
```python
pip install olunicodenormalizer
```
# useage
**initialization and cleaning**
```python
# import
from olunicodenormalizer import Normalizer 
from pprint import pprint
# initialize
bnorm=Normalizer()
# normalize
word = 'ᱡᱚᱦᱟᱨ'
result=bnorm(word)
print(f"Non-norm:{word}; Norm:{result['normalized']}")
print("--------------------------------------------------")
pprint(result)
```
> output 

```
Non-norm:ᱡᱚᱦᱟᱨ; Norm:ᱡᱚᱦᱟᱨ
--------------------------------------------------
{'given': 'ᱡᱚᱦᱟᱨ', 'normalized': 'ᱡᱚᱦᱟᱨ', 'ops': []}
```



```python
# initialize without english (default)
norm=Normalizer()
print("without english:",norm("ASD123")["normalized"])
# --> returns None
norm=Normalizer(allow_english=True)
print("with english:",norm("ASD123")["normalized"])

```
> output

```
without english: None
with english: ASD123
```

 
