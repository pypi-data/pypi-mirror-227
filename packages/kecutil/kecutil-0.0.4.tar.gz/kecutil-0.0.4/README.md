## KEC ITP: Python Util Functions

### Functions

> kecutil.reduce(cb(cur, val), list, default)
> Reduce is used to *reduce* a list to one value.
> This is commonly useful when finding the longest string for example
>
> ```python
> from kecutil import reduce
>
>
> strings = ["ab", "acb", "abcdef", "abd"]
> longestString = reduce(lambda x, y: x if len(x) > len(y) else y, strings, "")
>
> print(longestString) # "abcdef"
> ```
