def mf(media_disciplina: float | int, exame) -> tuple:
    """
    Calcula a média final de uma disciplina.

    :param media_disciplina: Média da disciplina
    :param exame: Nota do exame
    :return: Média final e conclusão (float, bool)
    """
    media_final = (media_disciplina + exame) / 2

    if 4.75 <= media_final < 5:
        media_final = 5

    conclusao = True if media_final >= 5.0 else False

    return media_final, conclusao
