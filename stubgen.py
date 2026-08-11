"""Deterministic per-language starter stubs, generated from starter.py.

Parses the Python starter with ast and emits an idiomatic stub for each
supported language. No AI involved: the AI transpiler receives the Python
contract at submit time, so the stub only needs matching class/method names
and honest parameter types.
"""
import ast

HEADER = {
    "java": "// Judged via AI translation to Python — keep class/method names.",
    "cpp": "// Judged via AI translation to Python — keep class/method names.",
    "javascript": "// Judged via AI translation to Python — keep class/method names.",
    "typescript": "// Judged via AI translation to Python — keep class/method names.",
    "go": "// Judged via AI translation to Python — keep the function names.",
    "rust": "// Judged via AI translation to Python — keep the method names.",
}


def parse_starter(source):
    """-> [{name, methods: [{name, params: [(pname, ptype)], ret: ptype}]}]"""
    tree = ast.parse(source)
    classes = []
    for node in tree.body:
        if not isinstance(node, ast.ClassDef):
            continue
        methods = []
        for item in node.body:
            if not isinstance(item, ast.FunctionDef):
                continue
            params = []
            for arg in item.args.args:
                if arg.arg == "self":
                    continue
                params.append((arg.arg, _ann(arg.annotation)))
            methods.append({
                "name": item.name,
                "params": params,
                "ret": _ann(item.returns),
            })
        classes.append({"name": node.name, "methods": methods})
    return classes


def _ann(node):
    if node is None:
        return "any"
    return ast.unparse(node).replace("Optional[", "").rstrip("]") \
        if isinstance(node, ast.Subscript) and getattr(node.value, "id", "") == "Optional" \
        else ast.unparse(node)


# type maps: python annotation -> (java, cpp, ts, go, rust)
TYPES = {
    "int": ("int", "int", "number", "int", "i64"),
    "float": ("double", "double", "number", "float64", "f64"),
    "bool": ("boolean", "bool", "boolean", "bool", "bool"),
    "str": ("String", "string", "string", "string", "String"),
    "list[int]": ("int[]", "vector<int>&", "number[]", "[]int", "Vec<i64>"),
    "list[float]": ("double[]", "vector<double>&", "number[]", "[]float64", "Vec<f64>"),
    "list[str]": ("String[]", "vector<string>&", "string[]", "[]string", "Vec<String>"),
    "list[list[int]]": ("int[][]", "vector<vector<int>>&", "number[][]", "[][]int", "Vec<Vec<i64>>"),
    "list[list[str]]": ("String[][]", "vector<vector<string>>&", "string[][]", "[][]string", "Vec<Vec<String>>"),
    "list[bool]": ("boolean[]", "vector<bool>&", "boolean[]", "[]bool", "Vec<bool>"),
    "TreeNode": ("TreeNode", "TreeNode*", "TreeNode | null", "*TreeNode", "Option<Rc<RefCell<TreeNode>>>"),
    "ListNode": ("ListNode", "ListNode*", "ListNode | null", "*ListNode", "Option<Box<ListNode>>"),
    "list[ListNode]": ("ListNode[]", "vector<ListNode*>&", "(ListNode | null)[]", "[]*ListNode", "Vec<Option<Box<ListNode>>>"),
    "Node": ("Node", "Node*", "_Node | null", "*Node", "Option<Rc<RefCell<Node>>>"),
    "None": ("void", "void", "void", "", "()"),
    "any": ("Object", "auto", "any", "interface{}", "()"),
}
DEFAULTS = {  # return-statement placeholder per java/cpp/ts family type
    "int": "0", "double": "0.0", "boolean": "false", "String": '""',
    "void": "", "bool": "false", "number": "0", "string": '""',
}
_IDX = {"java": 0, "cpp": 1, "typescript": 2, "go": 3, "rust": 4}


def _t(pytype, lang):
    pytype = (pytype or "any").replace("List[", "list[").replace(" ", "")
    base = TYPES.get(pytype) or TYPES["any"]
    return base[_IDX[lang]]


def generate(source, language):
    classes = parse_starter(source)
    if not classes:
        return None
    gen = {
        "java": _java, "cpp": _cpp, "javascript": _js,
        "typescript": _ts, "go": _go, "rust": _rust,
    }.get(language)
    if gen is None:
        return None
    return HEADER[language] + "\n\n" + "\n\n".join(gen(c) for c in classes) + "\n"


def _java(cls):
    lines = [f"class {cls['name']} {{"]
    for m in cls["methods"]:
        if m["name"] == "__init__":
            args = ", ".join(f"{_t(t, 'java')} {n}" for n, t in m["params"])
            lines += [f"    public {cls['name']}({args}) {{", "        ", "    }", ""]
            continue
        ret = _t(m["ret"], "java")
        args = ", ".join(f"{_t(t, 'java')} {n}" for n, t in m["params"])
        lines.append(f"    public {ret} {m['name']}({args}) {{")
        d = DEFAULTS.get(ret, "null")
        lines.append(f"        return {d};" if ret != "void" else "        ")
        lines += ["    }", ""]
    if lines[-1] == "":
        lines.pop()
    lines.append("}")
    return "\n".join(lines)


def _cpp(cls):
    lines = [f"class {cls['name']} {{", "public:"]
    for m in cls["methods"]:
        if m["name"] == "__init__":
            args = ", ".join(f"{_t(t, 'cpp')} {n}" for n, t in m["params"])
            lines += [f"    {cls['name']}({args}) {{", "        ", "    }", ""]
            continue
        ret = _t(m["ret"], "cpp").rstrip("&")
        args = ", ".join(f"{_t(t, 'cpp')} {n}" for n, t in m["params"])
        lines.append(f"    {ret} {m['name']}({args}) {{")
        d = DEFAULTS.get(ret, "{}")
        lines.append(f"        return {d};" if ret != "void" else "        ")
        lines += ["    }", ""]
    if lines[-1] == "":
        lines.pop()
    lines.append("};")
    return "\n".join(lines)


def _js(cls):
    lines = [f"class {cls['name']} {{"]
    for m in cls["methods"]:
        doc = ["    /**"]
        for n, t in m["params"]:
            doc.append(f"     * @param {{{_t(t, 'typescript')}}} {n}")
        if m["name"] != "__init__" and m["ret"] not in ("None", None):
            doc.append(f"     * @return {{{_t(m['ret'], 'typescript')}}}")
        doc.append("     */")
        name = "constructor" if m["name"] == "__init__" else m["name"]
        args = ", ".join(n for n, _ in m["params"])
        lines += doc + [f"    {name}({args}) {{", "        ", "    }", ""]
    if lines[-1] == "":
        lines.pop()
    lines.append("}")
    return "\n".join(lines)


def _ts(cls):
    lines = [f"class {cls['name']} {{"]
    for m in cls["methods"]:
        args = ", ".join(f"{n}: {_t(t, 'typescript')}" for n, t in m["params"])
        if m["name"] == "__init__":
            lines += [f"    constructor({args}) {{", "        ", "    }", ""]
            continue
        ret = _t(m["ret"], "typescript")
        lines.append(f"    {m['name']}({args}): {ret} {{")
        d = DEFAULTS.get(ret, "null as any")
        lines.append(f"        return {d};" if ret != "void" else "        ")
        lines += ["    }", ""]
    if lines[-1] == "":
        lines.pop()
    lines.append("}")
    return "\n".join(lines)


def _go(cls):
    lines = []
    ctor = next((m for m in cls["methods"] if m["name"] == "__init__"), None)
    plain = [m for m in cls["methods"] if m["name"] != "__init__"]
    if ctor is not None:  # design class -> struct + constructor + methods
        lines += [f"type {cls['name']} struct {{", "    ", "}", ""]
        args = ", ".join(f"{n} {_t(t, 'go')}" for n, t in ctor["params"])
        lines += [f"func New{cls['name']}({args}) {cls['name']} {{",
                  f"    return {cls['name']}{{}}", "}", ""]
        recv = cls["name"][0].lower()
        for m in plain:
            margs = ", ".join(f"{n} {_t(t, 'go')}" for n, t in m["params"])
            ret = _t(m["ret"], "go")
            sig = f"func ({recv} *{cls['name']}) {m['name']}({margs})"
            lines += [f"{sig} {ret} {{".rstrip() + ("" if ret else ""), "    ", "}", ""]
    else:
        for m in plain:
            margs = ", ".join(f"{n} {_t(t, 'go')}" for n, t in m["params"])
            ret = _t(m["ret"], "go")
            lines += [f"func {m['name']}({margs}) {ret} {{".replace("  {", " {"),
                      "    ", "}", ""]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines)


def _rust(cls):
    lines = ["#[allow(non_snake_case)]", f"struct {cls['name']};", "",
             "#[allow(non_snake_case)]", f"impl {cls['name']} {{"]
    for m in cls["methods"]:
        if m["name"] == "__init__":
            args = ", ".join(f"{n}: {_t(t, 'rust')}" for n, t in m["params"])
            lines += [f"    pub fn new({args}) -> Self {{",
                      f"        {cls['name']}", "    }", ""]
            continue
        args = ", ".join(f"{n}: {_t(t, 'rust')}" for n, t in m["params"])
        ret = _t(m["ret"], "rust")
        head = f"    pub fn {m['name']}(&mut self, {args})" if args else \
               f"    pub fn {m['name']}(&mut self)"
        if ret and ret != "()":
            head += f" -> {ret}"
        lines += [head + " {", "        todo!()", "    }", ""]
    if lines[-1] == "":
        lines.pop()
    lines.append("}")
    return "\n".join(lines)
