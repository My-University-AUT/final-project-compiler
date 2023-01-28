

def variable_list_to_c_code(variable_list: dict):
    if len(variable_list['int']) != 0:
        int_def = "int "+ ", ".join([variable for variable in variable_list['int']])
    else:
        int_def = ""
    if len(variable_list['float']) != 0:
        float_def = "float "+ ", ".join([variable for variable in variable_list['float']])
    else:
        float_def = ""
    return int_def + ";\n" + float_def + ";\n"

def temp_variables_to_c_code(temp_count):
    if temp_count > 0:
        return "float T_" + ", T_".join([str(i+1) for i in range(temp_count)]) + ";\n"
    return ""

def quad_to_c_code(q):
    if q.op == "+":
        return f"\t{q.result} = {q.left} + {q.right};\n"
    if q.op == "-":
        if q.right == None:
            return f"\t{q.result} = -{q.left};\n"
        return f"\t{q.result} = {q.left} - {q.right};\n"
    if q.op == "*":
        return f"\t{q.result} = {q.left} * {q.right};\n"
    if q.op == "/":
        return f"\t{q.result} = {q.left} / {q.right};\n"
    if q.op == "=":
        return f"\t{q.result} = {q.left};\n"
    if q.op == "print":
        return f"\tprintf(\"%f\\n\", (float){q.result});\n"
    if q.op == ">":
        return f"\t{q.result} = {q.left} > {q.right};\n"
    if q.op == "<":
        return f"\t{q.result} = {q.left} < {q.right};\n"
    if q.op == ">=":
        return f"\t{q.result} = {q.left} >= {q.right};\n"
    if q.op == "<=":
        return f"\t{q.result} = {q.left} <= {q.right};\n"
    if q.op == "==":
        return f"\t{q.result} = {q.left} == {q.right};\n"
    if q.op == "<>":
        return f"\t{q.result} = {q.left} != {q.right};\n"
    if q.op == "and":
        return f"\t{q.result} = {q.left} && {q.right};\n"
    if q.op == "or":
        return f"\t{q.result} = {q.left} || {q.right};\n"
    if q.op == "not":
        return f"\t{q.result} = !{q.left};\n"
    if q.op == "GOTO":
        return f"\tgoto L_{q.result};\n"
    if q.op == "if GOTO":
        return f"\tif ({q.left}) goto L_{q.result};\n"


def quads_to_c_code(quads: list):
    return "".join([f" L_{i+1}:"+quad_to_c_code(quads[i]) for i in range(len(quads))])

def compile_to_c_code(quads: list, variable_list: dict, temp_count):
    return "#include <stdio.h>\n"+\
        variable_list_to_c_code(variable_list) +\
        temp_variables_to_c_code(temp_count) +\
        "int main() {\n"+\
        quads_to_c_code(quads)+\
        f" L_{len(quads)+1}:"+"\treturn 0;\n"+\
        "}\n"
