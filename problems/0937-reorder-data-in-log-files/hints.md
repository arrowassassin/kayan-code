## Hint 1

Don't write a sorting algorithm — write a **sort key**. The three rules (letter-logs first, letter-logs by content then identifier, digit-logs untouched) can all be encoded in what each log maps to under `key=`.

## Hint 2

Split each log just once: `ident, rest = log.split(' ', 1)`, and classify by whether `rest` starts with a digit. A tuple key sorts lexicographically field by field — so make letter-logs `(0, content, identifier)` and give every digit-log the *same* key starting with `1`.

## Hint 3

If all digit-logs share one identical key, what keeps them in original order? Python's `sorted` is guaranteed **stable** — equal keys preserve input order. That single library guarantee replaces the whole "partition, sort one half, concatenate" dance. (That two-list version is also fine — say why you'd pick one or the other.)
