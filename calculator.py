"""Command-line calculator program.

This module exposes a ``calculate`` function that safely evaluates
arithmetic expressions and a small CLI for evaluating a single
expression passed via the command line.
"""

from __future__ import annotations

import argparse
import ast
import operator
from typing import Any, Callable, Dict


AllowedBinaryOps = Dict[type, Callable[[Any, Any], Any]]


class EvaluationError(Exception):
    """Raised when an expression cannot be evaluated."""


_BINARY_OPERATORS: AllowedBinaryOps = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.FloorDiv: operator.floordiv,
}

_UNARY_OPERATORS: Dict[type, Callable[[Any], Any]] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def calculate(expression: str) -> Any:
    """Evaluate an arithmetic expression safely.

    Parameters
    ----------
    expression:
        String containing an arithmetic expression (e.g. ``"2 + 2"``).

    Returns
    -------
    Any
        Result of the evaluated expression. Most expressions produce
        ``int`` or ``float`` values.

    Raises
    ------
    EvaluationError
        If the expression contains unsupported syntax or cannot be
        evaluated.
    """

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:  # pragma: no cover - simple pass-through
        raise EvaluationError("Invalid expression") from exc

    return _evaluate_node(tree.body)


def _evaluate_node(node: ast.AST) -> Any:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _BINARY_OPERATORS:
            raise EvaluationError(f"Unsupported operator: {op_type.__name__}")

        left = _evaluate_node(node.left)
        right = _evaluate_node(node.right)
        try:
            return _BINARY_OPERATORS[op_type](left, right)
        except ZeroDivisionError as exc:
            raise EvaluationError("Division by zero") from exc

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _UNARY_OPERATORS:
            raise EvaluationError(f"Unsupported unary operator: {op_type.__name__}")

        operand = _evaluate_node(node.operand)
        return _UNARY_OPERATORS[op_type](operand)

    if isinstance(node, ast.Expression):
        return _evaluate_node(node.body)

    raise EvaluationError(f"Unsupported expression component: {type(node).__name__}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Evaluate arithmetic expressions.")
    parser.add_argument(
        "expression",
        help="Arithmetic expression to evaluate. Surround with quotes to avoid shell parsing.",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)
    result = calculate(args.expression)
    print(result)


if __name__ == "__main__":
    main()
