from .grammar import *
from .syntax import *
from . import cardinals, ordinals
from .lexeme import NumeralLexeme


def inflect(
    whole: str,
    numerator: str,
    denominator: str,
    form: InflectionForm,
    insert_ones=False,
    strict_range=False,
) -> str:
    root = DummySyntaxNode(form)
    obj = DummySyntaxNode({})

    build_tree(root, obj, whole, numerator, denominator, insert_ones, strict_range)
    root.agree()
    return str(root)


def build_tree(
    root: SyntaxNode,
    obj: SyntaxNode,
    whole: str,
    numerator: str,
    denominator: str,
    insert_ones=False,
    strict_range=False,
) -> None:
    # Add a dummy node for the virtual lexeme "частина" as in
    #  1/4 = одна четверта [частина]
    vroot = DummySyntaxNode(
        persistent_form=InflectionForm(gender="feminine", animacy="inanimate"),
    )
    root.add_child_node(vroot, Relation.amod)
    vroot.add_child_node(obj, Relation.nmod)
    ordinals.build_tree(vroot, denominator, insert_ones, strict_range)
    cardinals.build_tree(vroot, numerator, insert_ones, strict_range)
    # TODO: find the right solutino
    _fix_puacal(vroot)
    if whole:
        whole_adj = vroot.add_child(NumeralLexeme.misc("whole"), Relation.amod)
        cardinals.build_tree(vroot, whole, insert_ones, strict_range)


def _fix_puacal(root: SyntaxNode):
    for edge in root.edges:
        if edge.rel == Relation.nummod_govpc:
            edge.rel = Relation.nummod_govpl
