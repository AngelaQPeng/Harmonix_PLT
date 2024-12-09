class PythonCodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.generated_code = []
        self.repeat_counter = 0

    def generate(self):
        self.process_statements(self.ast["statements"])
        return "\n".join(self.generated_code)

    def process_statements(self, statements):
        for stmt in statements:
            if stmt["type"] == "title_statement":
                self.generated_code.append(f"Title = '{stmt['title']}'")
            elif stmt["type"] == "composer_statement":
                self.generated_code.append(f"Composer = '{stmt['composer']}'")
            elif stmt["type"] == "staff_statement":
                self.generated_code.append(f"staff = '{stmt['staff']}'")
            elif stmt["type"] == "clef_statement":
                self.generated_code.append(f"clef = '{stmt['clef']}'")
            elif stmt["type"] == "time_sig_statement":
                self.generated_code.append(f"time_signature = '{stmt['timeSig']}'")
            elif stmt["type"] == "key_sig_statement":
                self.generated_code.append(f"key_signature = '{stmt['keySig']}'")
            elif stmt["type"] == "pattern_definition":
                self.process_pattern_definition(stmt)
            elif stmt["type"] == "repeat_statement":
                self.process_top_level_repeat(stmt)
            elif stmt["type"] == "assignment_statement":
                self.process_assignment_statement(stmt)
            else:
                raise ValueError(f"Unknown statement type: {stmt['type']}")

    def process_pattern_definition(self, stmt):
        self.generated_code.append(f"def {stmt['name']}():")
        self.generated_code.append("    pattern = []")
        for body_stmt in stmt["body"]:
            if body_stmt["type"] == "note_statement":
                note = body_stmt.get("note")
                duration = body_stmt.get("duration")
                if note and duration:
                    self.generated_code.append(f"    pattern.append({{'note': '{note}', 'duration': '{duration}'}})")
                else:
                    raise ValueError(f"Invalid note statement: {body_stmt}")
            elif body_stmt["type"] == "repeat_statement":
                self.process_inline_repeat(body_stmt, indent=4)
            elif body_stmt["type"] == "pattern_reference":
                self.generated_code.append(f"    pattern.extend({body_stmt['name']}())")
        self.generated_code.append("    return pattern")

    def process_inline_repeat(self, stmt, indent=4):
        count = stmt.get("count")
        body = stmt.get("body")
        if count is None or body is None:
            raise ValueError(f"Invalid repeat statement: {stmt}")

        indent_space = " " * indent
        repeat_var = f"repeat_result_{self.repeat_counter}"
        self.repeat_counter += 1

        self.generated_code.append(f"{indent_space}{repeat_var} = []")
        self.generated_code.append(f"{indent_space}for _ in range({count}):")
        for body_stmt in body:
            if body_stmt["type"] == "pattern_reference":
                pattern_name = body_stmt["name"]
                self.generated_code.append(f"{indent_space}    {repeat_var}.extend({pattern_name}())")
            elif body_stmt["type"] == "note_statement":
                note = body_stmt.get("note")
                duration = body_stmt.get("duration")
                if note and duration:
                    self.generated_code.append(
                        f"{indent_space}    {repeat_var}.append({{'note': '{note}', 'duration': '{duration}'}})"
                    )
                else:
                    raise ValueError(f"Invalid note statement: {body_stmt}")
        self.generated_code.append(f"{indent_space}pattern.extend({repeat_var})")

    def process_top_level_repeat(self, stmt):
        count = stmt.get("count")
        body = stmt.get("body")
        if count is None or body is None:
            raise ValueError(f"Invalid repeat statement: {stmt}")

        repeat_var = f"repeat_result_{self.repeat_counter}"
        self.repeat_counter += 1

        self.generated_code.append(f"{repeat_var} = []")
        self.generated_code.append(f"for _ in range({count}):")
        for body_stmt in body:
            if body_stmt["type"] == "pattern_reference":
                pattern_name = body_stmt["name"]
                self.generated_code.append(f"    {repeat_var}.extend({pattern_name}())")
            elif body_stmt["type"] == "note_statement":
                note = body_stmt.get("note")
                duration = body_stmt.get("duration")
                if note and duration:
                    self.generated_code.append(
                        f"    {repeat_var}.append({{'note': '{note}', 'duration': '{duration}'}})"
                    )
        self.generated_code.append(f"final_pattern = {repeat_var}")

    def process_assignment_statement(self, stmt):
        name = stmt["name"]
        expression_code = self.generate_expression(stmt["expression"])
        self.generated_code.append(f"{name} = {expression_code}")

    def generate_expression(self, expr):
        if expr["type"] == "identifier":
            return f"{expr['name']}()"
        elif expr["type"] == "addition_expression":
            left = self.generate_expression(expr["left"])
            right = self.generate_expression(expr["right"])
            return f"({left} + {right})"
        elif expr["type"] == "repeat_statement":
            return self.generate_repeat_expression(expr)
        else:
            raise ValueError(f"Unknown expression type: {expr['type']}")

    def generate_repeat_expression(self, expr):
        count = expr.get("count")
        body = expr.get("body")
        if count is None or body is None:
            raise ValueError(f"Invalid repeat expression: {expr}")

        repeat_var = f"repeat_result_{self.repeat_counter}"
        self.repeat_counter += 1

        self.generated_code.append(f"{repeat_var} = []")
        self.generated_code.append(f"for _ in range({count}):")
        for body_stmt in body:
            if body_stmt["type"] == "pattern_reference":
                pattern_name = body_stmt["name"]
                self.generated_code.append(f"    {repeat_var}.extend({pattern_name}())")
            elif body_stmt["type"] == "note_statement":
                note = body_stmt.get("note")
                duration = body_stmt.get("duration")
                if note and duration:
                    self.generated_code.append(
                        f"    {repeat_var}.append({{'note': '{note}', 'duration': '{duration}'}})"
                    )
        return repeat_var

