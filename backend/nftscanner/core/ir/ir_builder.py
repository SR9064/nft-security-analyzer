# =========================================================
# NORMALIZED IR BUILDER
# =========================================================

def build_ir(ast):

    ir = {
        "contracts": []
    }

    # -----------------------------------------------------
    # SOURCE UNIT
    # -----------------------------------------------------
    children = ast.get("children", [])

    for child in children:

        if child.get("type") != "ContractDefinition":
            continue

        contract_ir = {
            "name": child.get("name"),
            "functions": []
        }

        # -------------------------------------------------
        # STATE VARIABLES
        # -------------------------------------------------
        state_variables = set()

        # -------------------------------------------------
        # VARIABLE → CONTRACT MAP
        # -------------------------------------------------
        variable_map = {}

        for sub in child.get("subNodes", []):

            # ---------------------------------------------
            # STATE VARIABLES
            # ---------------------------------------------
            if sub.get("type") == "StateVariableDeclaration":

                for var in sub.get("variables", []):

                    state_variables.add(
                        var.get("name")
                    )

                    type_name = var.get(
                        "typeName",
                        {}
                    )

                    # -------------------------------------
                    # CONTRACT REFERENCE MAP
                    # -------------------------------------
                    if (
                        type_name.get("type")
                        == "UserDefinedTypeName"
                    ):

                        variable_map[
                            var.get("name")
                        ] = type_name.get(
                            "namePath"
                        )

        # -------------------------------------------------
        # FUNCTIONS
        # -------------------------------------------------
        for sub in child.get("subNodes", []):

            if sub.get("type") != "FunctionDefinition":
                continue

            fn_ir = {
                "name": sub.get("name"),
                "body": []
            }

            body = (
                sub.get("body", {})
                .get("statements", [])
            )

            for stmt in body:

                # =========================================
                # EXPRESSION STATEMENT
                # =========================================
                if stmt.get("type") == "ExpressionStatement":

                    expr = stmt.get(
                        "expression",
                        {}
                    )

                    # -------------------------------------
                    # ASSIGNMENT
                    # -------------------------------------
                    if expr.get("type") == "BinaryOperation":

                        left = expr.get(
                            "left",
                            {}
                        )

                        right = expr.get(
                            "right",
                            {}
                        )

                        symbolic_value = "updated"

                        # ---------------------------------
                        # IDENTIFIER VALUE
                        # ---------------------------------
                        if (
                            right.get("type")
                            == "Identifier"
                        ):

                            symbolic_value = right.get(
                                "name",
                                "symbolic"
                            )

                        # ---------------------------------
                        # LITERAL VALUE
                        # ---------------------------------
                        elif (
                            right.get("type")
                            == "NumberLiteral"
                        ):

                            symbolic_value = right.get(
                                "number",
                                "0"
                            )

                        # ---------------------------------
                        # FUNCTION CALL VALUE
                        # ---------------------------------
                        elif (
                            right.get("type")
                            == "FunctionCall"
                        ):

                            symbolic_value = "call_result"

                        # ---------------------------------
                        # STATE VARIABLE WRITE
                        # ---------------------------------
                        if (
                            left.get("type")
                            == "Identifier"
                            and left.get("name")
                            in state_variables
                        ):

                            fn_ir["body"].append({
                                "type": "SSTORE",
                                "key": left.get(
                                    "name"
                                ),
                                "value": symbolic_value
                            })

                        # ---------------------------------
                        # MAPPING WRITE
                        # ---------------------------------
                        elif (
                            left.get("type")
                            == "IndexAccess"
                        ):

                            base = left.get(
                                "base",
                                {}
                            )

                            index = left.get(
                                "index",
                                {}
                            )

                            index_name = "idx"

                            if (
                                index.get("type")
                                == "Identifier"
                            ):

                                index_name = index.get(
                                    "name",
                                    "idx"
                                )

                            if (
                                base.get("type")
                                == "Identifier"
                                and base.get("name")
                                in state_variables
                            ):

                                storage_key = (
                                    f"{base.get('name')}[{index_name}]"
                                )

                                fn_ir["body"].append({
                                    "type": "SSTORE",
                                    "key": storage_key,
                                    "value": symbolic_value
                                })

                            else:

                                fn_ir["body"].append({
                                    "type": "MSTORE",
                                    "key": "memory",
                                    "value": symbolic_value
                                })

                        # ---------------------------------
                        # LOCAL VARIABLE WRITE
                        # ---------------------------------
                        else:

                            fn_ir["body"].append({
                                "type": "MSTORE",
                                "key": "memory",
                                "value": symbolic_value
                            })

                    # -------------------------------------
                    # FUNCTION CALL
                    # -------------------------------------
                    elif expr.get("type") == "FunctionCall":

                        call_expr = expr.get(
                            "expression",
                            {}
                        )

                        target = "UNKNOWN"

                        # ---------------------------------
                        # REQUIRE DETECTION
                        # ---------------------------------
                        if (
                            call_expr.get("type")
                            == "Identifier"
                            and call_expr.get("name")
                            == "require"
                        ):

                            args = expr.get(
                                "arguments",
                                []
                            )

                            if args:

                                arg = args[0]

                                # -------------------------
                                # IDENTIFIER
                                # -------------------------
                                if (
                                    arg.get("type")
                                    == "Identifier"
                                ):

                                    condition = arg.get(
                                        "name",
                                        "unknown"
                                    )

                                # -------------------------
                                # BINARY OPERATION
                                # -------------------------
                                elif (
                                    arg.get("type")
                                    == "BinaryOperation"
                                ):

                                    left = arg.get(
                                        "left",
                                        {}
                                    )

                                    right = arg.get(
                                        "right",
                                        {}
                                    )

                                    op = arg.get(
                                        "operator",
                                        "=="
                                    )

                                    # -----------------
                                    # LEFT OPERAND
                                    # -----------------
                                    if (
                                        left.get("type")
                                        == "Identifier"
                                    ):

                                        left_name = left.get(
                                            "name",
                                            "left"
                                        )

                                    elif (
                                        left.get("type")
                                        == "MemberAccess"
                                    ):

                                        left_name = (
                                            f"{left.get('expression', {}).get('name', '')}."
                                            f"{left.get('memberName', '')}"
                                        )

                                    else:

                                        left_name = "left"

                                    # -----------------
                                    # RIGHT OPERAND
                                    # -----------------
                                    if (
                                        right.get("type")
                                        == "Identifier"
                                    ):

                                        right_name = right.get(
                                            "name",
                                            "right"
                                        )

                                    elif (
                                        right.get("type")
                                        == "MemberAccess"
                                    ):

                                        right_name = (
                                            f"{right.get('expression', {}).get('name', '')}."
                                            f"{right.get('memberName', '')}"
                                        )

                                    else:

                                        right_name = "right"

                                    condition = (
                                        f"{left_name} "
                                        f"{op} "
                                        f"{right_name}"
                                    )

                                else:

                                    condition = "True"

                                fn_ir["body"].append({
                                    "type": "REQUIRE",
                                    "condition": condition
                                })

                            continue

                        # ---------------------------------
                        # MEMBER ACCESS
                        # ---------------------------------
                        if (
                            call_expr.get("type")
                            == "MemberAccess"
                        ):

                            base = call_expr.get(
                                "expression",
                                {}
                            )

                            member = call_expr.get(
                                "memberName"
                            )

                            if (
                                base.get("type")
                                == "Identifier"
                            ):

                                var_name = base.get(
                                    "name"
                                )

                                contract_name = (
                                    variable_map.get(
                                        var_name,
                                        var_name
                                    )
                                )

                                target = (
                                    f"{contract_name}.{member}"
                                )

                        # ---------------------------------
                        # DIRECT CALL
                        # ---------------------------------
                        elif (
                            call_expr.get("type")
                            == "Identifier"
                        ):

                            target = call_expr.get(
                                "name",
                                "UNKNOWN"
                            )

                        fn_ir["body"].append({
                            "type": "CALL",
                            "target": target
                        })

                # =========================================
                # VARIABLE DECLARATION
                # =========================================
                elif (
                    stmt.get("type")
                    == "VariableDeclarationStatement"
                ):

                    fn_ir["body"].append({
                        "type": "MSTORE",
                        "key": "memory",
                        "value": "local_variable"
                    })

            contract_ir["functions"].append(
                fn_ir
            )

        ir["contracts"].append(
            contract_ir
        )

    return ir
