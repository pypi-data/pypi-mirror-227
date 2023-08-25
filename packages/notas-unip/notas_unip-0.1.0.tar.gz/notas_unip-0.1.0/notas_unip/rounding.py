def rounding_md(md: float | int) -> tuple:
    """
    Arredonda a média da disciplina
    e retorna uma tupla com a média e a conclusão.

    :param md: Média da disciplina
    :return: Média da disciplina e conclusão (float, bool)
    """
    if 5.7 <= md < 6:
        md = 6
        conclusion = True
    else:
        conclusion = False

    return float(md), conclusion
