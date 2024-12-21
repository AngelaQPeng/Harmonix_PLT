import ast

class MusicPatternOptimizer(ast.NodeTransformer):
    def __init__(self):
        super().__init__()
        self.cached_calls = {}
        self.pending_cache_assignments = []

    def optimize_loop(self, node):
        if (len(node.body) == 1 and 
            isinstance(node.body[0], ast.Expr) and 
            isinstance(node.body[0].value, ast.Call) and 
            isinstance(node.body[0].value.func, ast.Attribute) and 
            node.body[0].value.func.attr == "extend"):

            target_variable = node.body[0].value.func.value.id
            extend_arg = node.body[0].value.args[0]
            if isinstance(extend_arg, ast.Call):
                func_name = extend_arg.func.id
                print(func_name)
                if func_name in self.cached_calls:
                    loop_count = node.iter.args[0].value
                    if loop_count == 1:
                        return ast.Expr(
                            value=ast.Call(
                                func=ast.Attribute(
                                    value=ast.Name(id=target_variable, ctx=ast.Load()),
                                    attr="extend",
                                    ctx=ast.Load()
                                ),
                                args=[
                                    ast.Name(id=self.cached_calls[func_name], ctx=ast.Load())
                                ],
                                keywords=[]
                            )
                        ), True
                    else:
                        return ast.Expr(
                            value=ast.Call(
                                func=ast.Attribute(
                                    value=ast.Name(id=target_variable, ctx=ast.Load()),
                                    attr="extend",
                                    ctx=ast.Load()
                                ),
                                args=[
                                    ast.BinOp(
                                        left=ast.Name(id=self.cached_calls[func_name], ctx=ast.Load()),
                                        op=ast.Mult(),
                                        right=ast.Constant(value=loop_count)
                                    )
                                ],
                                keywords=[]
                            )
                        ), True
        
        return node, False

    def visit_For(self, node):
        if (isinstance(node.iter, ast.Call) and 
            isinstance(node.iter.func, ast.Name) and 
            node.iter.func.id == "range" and 
            len(node.iter.args) == 1):
            
            optimized_node, was_optimized = self.optimize_loop(node)
            if was_optimized:
                return optimized_node
        
        return self.generic_visit(node)

    def visit_FunctionDef(self, node):
        optimized_body = []
        append_buffer = []
        
        def flush_buffer():
            if len(append_buffer) > 1:
                repeated_note = append_buffer[0].value.args[0]
                repetition_count = len(append_buffer)
                optimized_body.append(
                    ast.Expr(
                        value=ast.Call(
                            func=ast.Attribute(
                                value=ast.Name(id="pattern", ctx=ast.Load()),
                                attr="extend",
                                ctx=ast.Load(),
                            ),
                            args=[
                                ast.BinOp(
                                    left=ast.List(elts=[repeated_note], ctx=ast.Load()),
                                    op=ast.Mult(),
                                    right=ast.Constant(value=repetition_count),
                                )
                            ],
                            keywords=[],
                        )
                    )
                )
            elif len(append_buffer) == 1:
                optimized_body.append(append_buffer[0])
            append_buffer.clear()
        
        for stmt in node.body:
            if (isinstance(stmt, ast.For) and 
                isinstance(stmt.iter, ast.Call) and 
                isinstance(stmt.iter.func, ast.Name) and 
                stmt.iter.func.id == "range"):
                flush_buffer()
                optimized_stmt, was_optimized = self.optimize_loop(stmt)
                optimized_body.append(optimized_stmt)
            elif (isinstance(stmt, ast.Expr) and 
                  isinstance(stmt.value, ast.Call) and 
                  isinstance(stmt.value.func, ast.Attribute) and 
                  stmt.value.func.attr == "append" and 
                  stmt.value.func.value.id == "pattern"):
                if (len(append_buffer) > 0 and 
                    not ast.dump(stmt.value.args[0]) == ast.dump(append_buffer[0].value.args[0])):
                    flush_buffer()
                append_buffer.append(stmt)
            elif (isinstance(stmt, ast.Assign) and 
                  isinstance(stmt.targets[0], ast.Name) and 
                  stmt.targets[0].id.startswith("repeat_result")):
                if len(node.body) > node.body.index(stmt) + 1:
                    next_stmt = node.body[node.body.index(stmt) + 1]
                    if (isinstance(next_stmt, ast.Expr) and 
                        isinstance(next_stmt.value, ast.Call) and 
                        isinstance(next_stmt.value.func, ast.Attribute) and 
                        next_stmt.value.func.attr == "extend" and 
                        isinstance(next_stmt.value.args[0], ast.Name) and 
                        next_stmt.value.args[0].id == stmt.targets[0].id):
                        continue
                optimized_body.append(stmt)
            else:
                flush_buffer()
                optimized_body.append(stmt)
        
        flush_buffer()
        node.body = optimized_body
        
        cached_var = f"cached_{node.name}"
        self.cached_calls[node.name] = cached_var
        cache_assignment = ast.Assign(
            targets=[ast.Name(id=cached_var, ctx=ast.Store())],
            value=ast.Call(func=ast.Name(id=node.name, ctx=ast.Load()), args=[], keywords=[]),
        )
        self.pending_cache_assignments.append(cache_assignment)
        
        return node

    def visit_Call(self, node):
        self.generic_visit(node)
        
        if isinstance(node.func, ast.Name):
            function_name = node.func.id
            if function_name in self.cached_calls:
                cached_var = self.cached_calls[function_name]
                return ast.Name(id=cached_var, ctx=ast.Load())
        
        return node

    def optimize(self, code):
        tree = ast.parse(code)
        
        optimized_tree = self.visit(tree)
        
        new_body = []
        for node in optimized_tree.body:
            new_body.append(node)
            if isinstance(node, ast.FunctionDef):
                cache_assignments = [assign for assign in self.pending_cache_assignments 
                                  if assign.targets[0].id == f"cached_{node.name}"]
                new_body.extend(cache_assignments)
        
        optimized_tree.body = new_body
        ast.fix_missing_locations(optimized_tree)
        return ast.unparse(optimized_tree)