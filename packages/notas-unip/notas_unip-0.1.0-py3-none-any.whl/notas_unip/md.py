from rounding import rounding_md


def dp(nota_prova: float | int) -> tuple:
    """
    Calcula a média de uma disciplina para disciplinas de DP,
    exceto para disciplinas de cunho prático / prática docente (licenciaturas).

    :param nota_prova: Nota da prova
    :return: Média da disciplina (float, bool)
    """
    media_disciplina = rounding_md(nota_prova)

    return media_disciplina


def dp_pratica_licenciatura(
    relatorio: float | int, relatorio_final: float | int
) -> tuple:
    """
    Calcula a média de uma disciplina de
    cunho prático / prática docente (licenciaturas).

    :param relatorio: Nota do relatório
    :param relatorio_final: Nota do relatório final
    :return: Média da disciplina (float, bool)
    """
    media_disciplina = (3 * relatorio + 7 * relatorio_final) / 10
    media_disciplina = rounding_md(media_disciplina)

    return media_disciplina


def regular_teorica_bacharelado(prova: float | int, ava: float | int) -> tuple:
    """
    Calcula a média de uma disciplina regular teórica
    de bacharelados e licenciaturas.

    :param prova: Nota da prova
    :param ava: Nota do AVA
    :return: Média da disciplina (float, bool)
    """
    media_disciplina = (9 * prova + ava) / 10
    media_disciplina = rounding_md(media_disciplina)

    return media_disciplina


def regular_teorica_tecnologo(
    prova: float | int, pim: float | int, ava: float | int
) -> tuple:
    """
    Calcula a média de uma disciplina regular teórica de
    cursos tecnólogos.

    :param prova: Nota da prova
    :param pim: Nota do PIM
    :param ava: Nota do AVA
    :return: Média da disciplina (float, bool)
    """
    media_disciplina = 7 * prova + 2 * pim + ava
    media_disciplina = rounding_md(media_disciplina)

    return media_disciplina


def regular_pratica_licenciatura(
    relatorio: float | int, relatorio_final: float | int, chat: float | int
) -> tuple:
    """
    Calcular a média de uma disciplina regular de cunho prático /
    prática docente (licenciaturas).

    :param relatorio: Nota do relatório
    :param relatorio_final: Nota do relatório final
    :param chat: Nota do chat
    :return: Média da disciplina (float, bool)
    """
    media_disciplina = (2 * relatorio + 7 * relatorio_final + chat) / 10
    media_disciplina = rounding_md(media_disciplina)

    return media_disciplina


def regular_pratica(relatorio: float | int, ap: float | int) -> tuple:
    """
    Calcular a média de uma disciplina regular prática.
    Cursos de:

    - **Biomedicina**
    - **CST Estética e Cosmética**
    - **Educação Física**
    - **Enfermagem**
    - **Farmácia**
    - **Física**
    - **Fisioterapia**
    - **Nutrição**
    - **Química**

    :param relatorio: Nota do relatório
    :param ap: Nota da AP
    :return: Média da disciplina (float, bool)
    """
    media_disciplina = (3 * relatorio + 7 * ap) / 10
    media_disciplina = rounding_md(media_disciplina)

    return media_disciplina


def tcc(trabalho: float | int, banca: float | int) -> tuple:
    """
    Calcular a média da disciplina para trabalhos de
    curso / estágio CCTB, regular e DP/AP.

    :param trabalho: Nota do trabalho
    :param banca: Nota da banca
    :return: Média da disciplina (float, bool)
    """
    media_disciplina = (7 * trabalho + 3 * banca) / 10
    media_disciplina = rounding_md(media_disciplina)

    return media_disciplina
