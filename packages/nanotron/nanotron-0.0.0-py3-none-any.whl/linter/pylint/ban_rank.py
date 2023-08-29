from typing import TYPE_CHECKING

from astroid import nodes
from pylint.checkers import BaseChecker

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class GroupRankChecker(BaseChecker):

    name = "no_group_rank_used"
    msgs = {
        "E5001": (
            "Remove the use of `group.rank()`, instead use `dist.get_rank(group)`",
            "group_rank_used",
            "Remove the use of `group.rank()`, instead use `dist.get_rank(group)`",
        )
    }

    def visit_call(self, node: nodes.Call) -> None:
        if not isinstance(node.func, nodes.Attribute):
            return

        if node.func.attrname != "rank":
            return

        if len(node.args) != 0:
            return

        if len(node.keywords) != 0:
            return

        # TODO @thomasw21: Maybe be more specific
        #  - specify that the input should be a node
        self.add_message("group_rank_used", node=node)


def register(linter: "PyLinter") -> None:
    linter.register_checker(GroupRankChecker(linter))
