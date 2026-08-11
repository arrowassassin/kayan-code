# Simplify Path

You are given an absolute Unix-style file path `path` (it always starts with `/`). Convert it to its **canonical** form, applying the usual Unix rules:

- `.` means "stay in the current directory" and disappears.
- `..` means "go up one directory"; going up from the root `/` stays at the root.
- Any run of consecutive slashes (`//`, `///`, ...) acts as a single separator.
- Anything else between slashes is a real directory name — including names made of dots such as `...` or `.hidden`, which have **no** special meaning.

The canonical path must start with a single `/`, contain single slashes between names, and must not end with a trailing `/` (unless it is just the root `/`).

## Example 1

```
Input: path = "/home//foo/"
Output: "/home/foo"
```

The double slash collapses; the trailing slash goes.

## Example 2

```
Input: path = "/a/./b/../../c/"
Output: "/c"
```

`.` vanishes; each `..` cancels the most recent real directory: `/a/b` → `/a` → `/`, then `c` enters.

## Example 3

```
Input: path = "/../"
Output: "/"
```

You cannot go above the root.

## Constraints

- `1 <= len(path) <= 3000`
- `path` consists of English letters, digits, `.`, `/` and `_`
- `path` always begins with `/`
