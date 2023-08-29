#!/usr/bin/env python3
# Shamelessly stolen from https://github.com/ksons/jscodegen.py/blob/develop/jscodegen/__init__.py

import json
import pprint

from enum import IntEnum
from .syntax import Syntax, Statements

import logging

logger = logging.getLogger(__name__)


class Precedence(IntEnum):
    Sequence = 0
    Yield = 1
    Await = 1
    Assignment = 1
    Conditional = 2
    ArrowFunction = 2
    LogicalOR = 3
    LogicalAND = 4
    BitwiseOR = 5
    BitwiseXOR = 6
    BitwiseAND = 7
    Equality = 8
    Relational = 9
    BitwiseSHIFT = 10
    Additive = 11
    Multiplicative = 12
    Unary = 13
    Postfix = 14
    Call = 15
    New = 16
    TaggedTemplate = 17
    Member = 18
    Primary = 19


# fmt:off
BinaryPrecedence = {
    "||": Precedence.LogicalOR
    , "&&": Precedence.LogicalAND
    , "|": Precedence.BitwiseOR
    , "^": Precedence.BitwiseXOR
    , "&": Precedence.BitwiseAND
    , "==": Precedence.Equality
    , "!=": Precedence.Equality
    , "===": Precedence.Equality
    , "!==": Precedence.Equality
    , "is": Precedence.Equality
    , "isnt": Precedence.Equality
    , "<": Precedence.Relational
    , ">": Precedence.Relational
    , "<=": Precedence.Relational
    , ">=": Precedence.Relational
    , "in": Precedence.Relational
    , "instanceof": Precedence.Relational
    , "<<": Precedence.BitwiseSHIFT
    , ">>": Precedence.BitwiseSHIFT
    , ">>>": Precedence.BitwiseSHIFT
    , "+": Precedence.Additive
    , "-": Precedence.Additive
    , "*": Precedence.Multiplicative
    , "%": Precedence.Multiplicative
    , "/": Precedence.Multiplicative
    }
# fmt:on


def default_block(message):
    return {"default_block": message}


class CodeGenerator:
    space = " "

    def __init__(self, indent):
        self.indentation = 0
        self.indent = indent

    def program(self, stmt):
        result = []
        for b in stmt.get("body"):
            result += self.generate_statement(b)
        return "".join(result)

    def expressionstatement(self, stmt):
        result = self.generate_expression(stmt.get("expression"), Precedence.Sequence)
        return result + ";\n"

    def forstatement(self, stmt):
        result = "for ("
        if stmt.get("init"):
            result += self.generate_expression(stmt.get("init"), Precedence.Sequence)
        result += ";"

        if stmt.get("test"):
            result += self.space + self.generate_expression(stmt.get("test"), Precedence.Sequence)
        result += ";"

        if stmt.get("update"):
            result += self.space + self.generate_expression(stmt.get("update"), Precedence.Sequence)
        result += ")"

        result += self.space + self.generate_statement(stmt.get("body"))
        return result

    def forinstatement(self, stmt):
        if stmt.get("left", default_block("forinstatement left 1")).get("type") == "VariableDeclaration":
            left = stmt.get("left", default_block("forinstatement left 2")).get("kind") + " " + self.generate_statement(stmt.get("left", default_block("forinstatement left 3")).get("declarations", [default_block("forinstatement left 4")])[0])
        else:
            left = self.generate_expression(stmt.get("left"), Precedence.Call)

        result = "for" + self.space + "(%s in %s)" % (left, self.generate_expression(stmt.get("right"), Precedence.Sequence))

        result += self.space + self.generate_statement(stmt.get("body"))
        return result

    def forofstatement(self, stmt):
        if stmt.get("left", default_block("forofstatement left 1")).get("type") == "VariableDeclaration":
            left = stmt.get("left", default_block("forofstatement left 2")).get("kind") + " " + self.generate_statement(stmt.get("left", default_block("forofstatement left 3")).get("declarations", [default_block("forofstatement left 4")])[0])
        else:
            left = self.generate_expression(stmt.get("left"), Precedence.Call)

        result = "for" + self.space + "(%s in %s)" % (left, self.generate_expression(stmt.get("right"), Precedence.Sequence))

        result += self.space + self.generate_statement(stmt.get("body"))
        return result

    def dowhilestatement(self, stmt):
        result = "do" + self.space + self.generate_statement(stmt.get("body"))
        result = result[:-1]
        result += " while (%s);" % self.generate_expression(stmt.get("test"), Precedence.Sequence)
        return result

    def switchstatement(self, stmt):
        cases = stmt.get("cases")
        fragments = []

        result = "switch" + self.space + "(%s)" % self.generate_expression(stmt.get("discriminant"), Precedence.Sequence)
        result += self.space + "{\n"
        self.indentation += self.indent
        for case in cases:
            fragments.append(self.generate_statement(case))
        self.indentation -= self.indent

        return result + "".join(fragments) + "}"

    def switchcase(self, stmt):
        result = self.indentation * self.space
        if stmt.get("test"):
            result += "case %s:\n" % self.generate_expression(stmt.get("test"), Precedence.Sequence)
        else:
            result += "default:\n"

        self.indentation += self.indent
        for consequent in stmt.get("consequent"):
            result += self.indentation * self.space
            result += self.generate_statement(consequent) + "\n"
        self.indentation -= self.indent
        return result

    def assignmentexpression(self, expr, precedence=Precedence.Sequence):
        left = self.generate_expression(expr.get("left"), Precedence.Call)
        right = self.generate_expression(expr.get("right"), Precedence.Assignment)
        return self.parenthesize(left + self.space + expr["operator"] + self.space + right, Precedence.Assignment, precedence)

    def sequenceexpression(self, expr, precedence=Precedence.Sequence):
        result = [self.generate_expression(e, Precedence.Assignment) for e in expr["expressions"]]
        return self.parenthesize(", ".join(result), Precedence.Sequence, precedence)

    def thisexpression(self, expr, precedence=Precedence.Sequence):
        return "this"

    def emptystatement(self, stmt):
        return ";"

    def binaryexpression(self, expr, precedence=Precedence.Sequence):
        operator = expr["operator"]
        current_precedence = BinaryPrecedence[operator]
        result = [self.generate_expression(expr["left"], current_precedence), self.space, operator, self.space, self.generate_expression(expr["right"], current_precedence)]
        return self.parenthesize("".join(result), current_precedence, precedence)

    def logicalexpression(self, expr, precedence=Precedence.Sequence):
        return self.binaryexpression(expr, precedence=Precedence.Sequence)

    def unaryexpression(self, expr, precedence=Precedence.Sequence):
        operator = expr["operator"]
        result = operator + (" " if len(operator) > 2 else "") + self.generate_expression(expr["argument"], Precedence.Unary)
        return self.parenthesize(result, Precedence.Unary, precedence)

    def updateexpression(self, expr, precedence=Precedence.Sequence):
        operator = expr["operator"]
        if expr["prefix"]:
            return self.parenthesize(operator + self.generate_expression(expr["argument"], Precedence.Unary), Precedence.Unary, precedence)
        else:
            return self.parenthesize(self.generate_expression(expr["argument"], Precedence.Postfix) + operator, Precedence.Postfix, precedence)

    def newexpression(self, expr, precedence=Precedence.Sequence):
        result = "new "
        result += self.generate_expression(expr["callee"], Precedence.New)
        result += "("
        result += ", ".join([self.generate_expression(x, Precedence.Assignment) for x in expr["arguments"]])
        return result + ")"

    def conditionalexpression(self, expr, precedence=Precedence.Sequence):
        result = self.generate_expression(expr["test"], Precedence.LogicalOR)
        result += self.space + "?" + self.space
        result += self.generate_expression(expr["consequent"], Precedence.Assignment)
        result += self.space + ":" + self.space
        result += self.generate_expression(expr["alternate"], Precedence.Assignment)
        return result

    def continuestatement(self, stmt):
        if stmt.get("label"):
            return "continue %s;" % stmt.get("label", default_block("continuestatement")).get("name")
        return "continue;"

    def breakstatement(self, stmt):
        if stmt.get("label"):
            return "break %s;" % stmt.get("label", "")
        else:
            return "break;"

    def returnstatement(self, stmt):
        if not stmt.get("argument"):
            return "return;\n"

        return "return %s;\n" % self.generate_expression(stmt.get("argument"), Precedence.Sequence)

    def ifstatement(self, stmt):
        result = "if" + self.space + "(%s)" % self.generate_expression(stmt.get("test"), Precedence.Sequence) + self.space
        result += self.generate_statement(stmt.get("consequent"))
        if "alternate" in stmt and stmt.get("alternate"):
            result = result[:-1]
            result += self.space + "else" + self.space
            result += self.generate_statement(stmt.get("alternate"))
        return result

    def whilestatement(self, stmt):
        result = "while" + self.space + "(%s)" % self.generate_expression(stmt.get("test"), Precedence.Sequence) + self.space
        result += self.generate_statement(stmt.get("body"))
        return result

    def arrayexpression(self, expr, precedence=Precedence.Sequence):
        elements = expr.get("elements")
        if not len(elements):
            return "[]"
        for el in elements:
            if None is el:
                logger.error(f"NONE EL: {pprint.pformat(el)} from {pprint.pformat(expr)} for {self.name}")
        elements = [self.generate_expression(e, Precedence.Assignment) for e in elements]
        return "[%s]" % ("," + self.space).join(elements)

    def objectpattern(self, expr, precedence=Precedence.Sequence):
        properties = expr["properties"]
        if not len(properties):
            return "{}"
        properties = [self.generate_expression(e, Precedence.Assignment) for e in properties]
        return "{%s}" % ("," + self.space).join(properties)

    def property(self, expr, precedence=Precedence.Sequence):
        key = self.generate_property_key(expr["key"], False) + ":" + self.space
        value = self.generate_expression(expr["value"], Precedence.Sequence)
        if expr["key"]["type"] == expr["value"]["type"] == "Identifier" and expr["key"]["name"] == expr["value"]["name"]:
            return value
        else:
            return key + value

    def spreadelement(self, expr, precedence=Precedence.Sequence):
        return "...%s" % self.generate_expression(expr["argument"], Precedence.Assignment)

    def objectexpression(self, expr, precedence=Precedence.Sequence):
        properties = expr["properties"]
        if not len(properties):
            return "{}"
        result = ["{"]
        self.indentation += self.indent
        fragments = [self.generate_expression(p, Precedence.Sequence) for p in properties]
        for i, fragment in enumerate(fragments):
            fragments[i] = f"{self.indentation * self.space}{fragment}"
        result.append("%s" % ",\n".join(fragments))
        self.indentation -= self.indent
        result.append("%s}" % (self.indentation * self.space))
        return "\n".join(result)

    def memberexpression(self, expr, precedence=Precedence.Sequence):
        result = [self.generate_expression(expr["object"], Precedence.Call)]
        if expr["computed"]:
            result += ["[", self.generate_expression(expr["property"], Precedence.Sequence), "]"]
        else:
            result += ["{}.".format("\n{}".format(self.indentation * self.space) if expr["property"]["name"] == "then" else ""), self.generate_expression(expr["property"], Precedence.Sequence)]

        return self.parenthesize("".join(result), Precedence.Member, precedence)

    def callexpression(self, expr, precedence=Precedence.Sequence):
        result = [self.generate_expression(expr["callee"], Precedence.Call), "("]
        args = []
        for arg in expr["arguments"]:
            args.append(self.generate_expression(arg, Precedence.Assignment))

        result.append(", ".join(args))
        if result and result[-1] and result[-1][-1] == "\n":
            result[-1] = result[-1][:-1]
        result.append(")")
        return "".join(result)

    def throwstatement(self, stmt):
        return "throw %s;\n" % self.generate_expression(stmt.get("argument"), Precedence.Sequence)

    def withstatement(self, stmt):
        result = "with" + self.space + "(%s)" % self.generate_expression(stmt.get("object"), Precedence.Sequence)
        result += self.generate_statement(stmt.get("body"))
        return result

    def identifier(self, expr, precedence=Precedence.Sequence):
        return self.generate_identifier(expr)

    def literal(self, expr, precedence=Precedence.Sequence):
        if "regex" in expr:
            return "/{}/{}".format(expr["regex"]["pattern"], expr["regex"]["flags"])
        if "value" not in expr:
            expr["value"] = None
        value = expr["value"]
        if isinstance(value, str):
            return "%s" % json.dumps(value)
        if isinstance(value, bool):
            return "true" if value else "false"
        if value == None:
            return "null"
        return str(value)

    def classexpression(self, stmt, precedence=Precedence.Sequence):
        return "CLASS_EXPRESSION"

    def arraypattern(self, stmt, precedence=Precedence.Sequence):
        return "ARRAY_PATTERN"

    def functiondeclaration(self, stmt):
        return "function %s%s" % (self.generate_identifier(stmt.get("id")), self.generate_function_body(stmt))

    def variabledeclaration(self, stmt, precedence=Precedence.Sequence):
        kind = stmt.get("kind")
        declarations = []
        for declaration in stmt.get("declarations"):
            declarations.append(self.generate_statement(declaration))
        result = kind + " " + ", ".join(declarations)
        if result[-1] == "\n":
            result = result[:-1]
        return result + ";\n"

    def variabledeclarator(self, stmt, precedence=Precedence.Sequence):
        result = self.generate_expression(stmt.get("id"), Precedence.Assignment)
        if stmt.get("init"):
            result += " = " + self.generate_expression(stmt.get("init"), Precedence.Assignment)
        return result

    def functionexpression(self, expr, precedence=Precedence.Sequence):
        result = ["function"]
        if "id" in expr and expr["id"]:
            result.append(self.generate_identifier(expr["id"]))

        result.append(self.generate_function_body(expr))
        return "".join(result)

    def arrowfunctionexpression(self, expr, precedence=Precedence.Sequence):
        result = []
        if "id" in expr and expr["id"]:
            result.append(self.generate_identifier(expr["id"]))

        result.append(self.generate_arrow_function_body(expr))
        return "".join(result)

    def blockstatement(self, stmt):
        result = ["{\n"]
        body = stmt.get("body")
        self.indentation += self.indent
        for bstmt in body:
            result.append("{}{}".format(self.indentation * self.space, self.generate_statement(bstmt)))
        self.indentation -= self.indent
        if result and result[-1] and result[-1][-1] == "\n":
            result[-1] = result[-1][:-1]
        result.append("\n%s}" % (self.indentation * self.space))
        result = "".join(result)
        if self.indentation == 0:
            result += "\n"
        return result

    def trystatement(self, stmt):
        result = "try" + self.space
        result += self.generate_statement(stmt.get("block"))
        result = result[:-1]
        result += "\n".join([self.generate_statement(s) for s in stmt.get("handlers", [])])
        return result

    def templateliteral(self, stmt, precedence=Precedence.Sequence):
        expressions = stmt.get("expressions", [])
        quasis = stmt.get("quasis", [])
        result = "`"
        for quasi, expression in zip(quasis, expressions):
            result += self.generate_statement(quasi)
            result += "${" + self.generate_statement(expression) + "}"
        result += self.generate_statement(quasis[-1])
        result += "`"
        return result

    def templateelement(self, stmt):
        result = stmt.get("value", default_block("templateelement value")).get("raw", "NO_TEMPLATE_ELEMENT_VALUE")
        return result

    def catchclause(self, stmt):
        result = self.space + "catch" + self.space + "(%s)" % self.generate_expression(stmt.get("param"), Precedence.Sequence)
        result += self.generate_statement(stmt.get("body"))
        return result

    def labeledstatement(self, stmt):
        return "%s: %s" % (stmt.get("label", default_block("labeledstatement label")).get("name"), self.generate_statement(stmt.get("body")))

    def debuggerstatement(self, stmt):
        return "debugger;"

    def parenthesize(self, text, current, should):
        if current < should:
            return "(" + text + ")"
        return text

    def is_statement(self, node):
        node_type = node.get("type", "")
        if not node_type:
            logger.error(f"Unknown type for node {pprint.pformat(node)}")
            # raise Exception(f"Unknown type for node {pprint.pformat(node)}")
            return False
        return Syntax(node_type) in Statements

    def generate_property_key(self, expr, computed):
        if computed:
            return "[%s]" % self.generate_expression(expr, Precedence.Sequence)
        return self.generate_expression(expr, Precedence.Sequence)

    def generate_function_params(self, node):
        params = []
        for param in node["params"]:
            params.append(self.generate_identifier(param))
        return "(" + ", ".join(params) + ")"

    def generate_function_body(self, node):
        result = [self.generate_function_params(node), self.space, self.generate_statement(node["body"])]
        return "".join(result)

    def generate_arrow_function_body(self, node):
        result = [self.generate_function_params(node), self.space, "=>", self.space, self.generate_statement(node["body"])]
        return "".join(result)

    def generate_expression(self, expr, precedence=Precedence.Sequence):
        if None is expr:
            raise Exception("NONE EXPRESSION")
        node_type = expr.get("type", "")
        attr = getattr(self, node_type.lower())
        return attr(expr, precedence)

    def generate_statement(self, stmt):
        node_type = stmt.get("type")
        if node_type.lower().endswith("expression"):
            return self.generate_expression(stmt, Precedence.Sequence)
        attr = getattr(self, node_type.lower())
        # print(attr)
        return attr(stmt)

    def generate_identifier(self, node):
        return str(node.get("name", "UN_NAMED_IDENTIFIER"))

    def generate(self, node, name=""):
        self.name = name
        if self.is_statement(node):
            return self.generate_statement(node)
        else:
            logger.error(f"Invalid top level node type {node.get('type')}")
            return ""


def generate(node, indent=2, name=""):
    g = CodeGenerator(indent)
    return g.generate(node, name)
