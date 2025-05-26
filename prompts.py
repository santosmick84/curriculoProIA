# templates de prompt para análise OpenAI

def build_prompt(texto_cv: str, tipo_analise: str) -> str:
    """
    Monta o prompt para chamar a OpenAI,
    diferenciando análise gratuita vs premium.
    """
    header = (
        "Você é um avaliador de currículos experiente. "
        f"Faça uma análise {tipo_analise} do seguinte conteúdo de currículo:\n\n"
    )
    instructions = (
        "Responda em JSON com os campos:"
        " nota_geral (float), pontos_fortes (lista de strings),"
        " oportunidades_melhoria (lista de strings),"
        " correcoes_portugues (lista de strings),"
        " resumo_profissional (string)."
    )
    return header + texto_cv + "\n\n" + instructions
