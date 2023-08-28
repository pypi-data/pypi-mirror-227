import typing

from spdx_tools.spdx.model.document import Document
from spdx_tools.spdx.parser.parse_anything import parse_file


def file2doc(f: str) -> Document:
    return parse_file(f)


class RuleCheckFailException(RuntimeError):
    pass


class Rule(object):
    def key(self) -> str:
        raise NotImplementedError

    def apply(self, doc_a: Document, doc_b: Document) -> bool:
        raise NotImplementedError


class _Runner(object):
    def __init__(self):
        self._rules: typing.List[Rule] = []
        self._rule_results: typing.Dict[str, bool] = dict()

    def add_rule(self, new_rule: Rule):
        self._rules.append(new_rule)

    def run_with_file(self, doc_a_file: str, doc_b_file: str):
        return self.run(file2doc(doc_a_file), file2doc(doc_b_file))

    def run(self, doc_a: Document, doc_b: Document):
        for each_rule in self._rules:
            rule_result = each_rule.apply(doc_a, doc_b)
            self._rule_results[each_rule.key()] = rule_result
        self.post_run(self._rule_results)

    def post_run(self, results: typing.Dict[str, bool]):
        raise NotImplementedError


class DefaultRunner(_Runner):
    def post_run(self, results: typing.Dict[str, bool]):
        pass


class StrictRunner(_Runner):
    def post_run(self, results: typing.Dict[str, bool]):
        if not all(results.values()):
            raise RuleCheckFailException()
