---
title: "Comma format"
date: 2026-10-20
slug: comma-format
categories: [Python]
---

I discovered a shorthand I'm shocked I never knew before: f"{my_num:,}" will format 1234567 as 1,234,567.
I knew about several other fstring numerical formats (I wrote the fstring answer for [How to display a float with two decimal places?](https://stackoverflow.com/a/46495453/7942600)), but I never came across this one before. It looks odd at first, but it makes sense.

I also tried f"{1234567: } and which provides a leading space. Now, that would imply more than one space could work, but no, that's a ValueError. Apparently the feature is so you can align negatives:

```python
>>> print(f"{1234567: }\n{-1234567: }")
 1234567
-1234567
```

In addition to `,` `_` works too.

```python
>>> print(f"{1234567:_}\n{-1234567:_}")
 1_234_567
-1_234_567
```

Which I suppose makes sense given python accepts `_` in numbers for readability:

```python
>>> a = 1_234_567
>>> a
1234567
```
