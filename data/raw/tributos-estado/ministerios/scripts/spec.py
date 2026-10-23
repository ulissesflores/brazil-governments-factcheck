# Especificacao curada, ano a ano (1/1/1995 ... 1/1/2026): norma vigente, lista de Ministerios, orgaos com status.
# Cada afirmacao carrega ancora (arquivo bruto + regex) que scripts/gerar.py CONFERE contra o texto baixado; ancora que
# nao casa derruba a geracao. Nada aqui e preenchido de memoria sem ancora; o que nao tem ancora fica em `nv` (nao verificado).
#
# Regra de contagem (a mesma em todos os anos):
#   n_ministerios = itens que a norma chama de "Ministerios" (artigo "Os Ministerios sao os seguintes"), na redacao vigente em 1/1.
#   Orgaos com status (fora dessa lista), tres classes, cada orgao conta uma vez:
#     A = a norma declara "Ministros de Estado" o titular (paragrafo "Sao Ministros de Estado ..." ou cargo "Ministro de Estado Chefe da ...")
#     B = cargo/gabinete de "Ministro de Estado Extraordinario ..." (Esportes, Politica Fundiaria, Projetos Especiais, Seguranca Alimentar)
#     C = titular com "prerrogativas, garantias, vantagens e direitos equivalentes aos de Ministro de Estado"
#   n_ministerios_mais_status = n_ministerios + A + B + C.  As tres classes saem tambem como indicadores separados.
B = "bruto/"

# ---- ancoras reutilizaveis -------------------------------------------------------------------------------------
PAR95 = r"Parágrafo único\. São Ministros de Estado os titulares dos Ministérios, da Casa Civil da Presidência da República e do Estado-Maior das Forças Armadas"
ART24_813 = r"Art\. 24\. Ficam criados os cargos de natureza especial de Chefe da Casa Militar da Presidência da República, de Secretário-Geral da Presidência da República, de Secretário de Comunicação Social da Presidência da República e de Secretário de Assuntos Estratégicos da Presidência da República\. Parágrafo único\. Os titulares dos cargos de que trata este artigo terão prerrogativas, garantias, vantagens e direitos equivalentes aos de Ministro de Estado"
ART23_1226 = r"Art\. 23\. Os titulares dos cargos de Natureza Especial de Chefe da Casa Militar da Presidência da República, de Secretário-Geral da Presidência da República, de Secretário de Comunicação Social da Presidência da República e de Secretário de Assuntos Estratégicos da Presidência da República e do cargo de que trata o art\. 26, terão prerrogativas, garantias, vantagens e direitos equivalentes aos de Ministro de Estado"
ART26_1226 = r"Art\. 26\. O titular do cargo de Natureza Especial de Secretário-Executivo da Câmara de Políticas Regionais do Conselho de Governo, a que se refere o § 3º do art\. 7º desta Medida Provisória será também o titular da Secretaria Especial do Ministério do Planejamento e Orçamento"
ESP = r"Fica criado o cargo de Ministro de Estado Extraordinário dos Esportes"
FUND_D1888 = r"Gabinete do Ministro de Estado Extraordinário de Política Fundiária"
FUND_D2321 = r"Gabinete do Ministro Extraordinário de Política Fundiária"
PAR99 = r"Parágrafo único\. São Ministros de Estado os titulares dos Ministérios, o Chefe da Casa Civil da Presidência da República e o Chefe do Estado-Maior das Forças Armadas"
PAR00 = r"Parágrafo único\. São Ministros de Estado os titulares dos Ministérios, o Chefe da Casa Civil, o Chefe do Gabinete de Segurança Institucional, o Chefe da Secretaria-Geral e o Chefe da Secretaria de Comunicação de Governo da Presidência da República"
PAR01 = r"Parágrafo único\. São Ministros de Estado os titulares dos Ministérios, o Chefe da Casa Civil, o Chefe do Gabinete de Segurança Institucional, o Chefe da Secretaria-Geral e o Chefe da Secretaria de Comunicação de Governo da Presidência da República e o Advogado-Geral da União"
PAR02 = r"§ 1o São Ministros de Estado os titulares dos Ministérios, o Chefe da Casa Civil, o Chefe do Gabinete de Segurança Institucional, o Chefe da Secretaria-Geral e o Chefe da Secretaria de Comunicação de Governo da Presidência da República, o Advogado-Geral da União e o Corregedor-Geral da União"
SEDU = r"§ 2o O titular do cargo de Secretário Especial de Desenvolvimento Urbano terá prerrogativas, garantias, vantagens e direitos equivalentes aos de Ministro de Estado"
ART38 = r"Art\. 38\. São criados os cargos de natureza especial de Secretário Especial do Conselho de Desenvolvimento Econômico e Social, de Secretário Especial de Aq.icultura e Pesca, de Secretário Especial dos Direitos Humanos e de Secretário Especial de Políticas para as Mulheres da Presidência da República\.(?: \(Vide[^)]*\))? § 1o Os cargos referidos no caput terão prerrogativas, garantias, vantagens e direitos equivalentes aos de Ministro de Estado"
SEPPIR_C = r"Parágrafo único\. O cargo de natureza especial referido no caput terá prerrogativas, garantias, vantagens e direitos equivalentes ao de Ministro de Estado"
PORTOS_C = r"O cargo de Secretário Especial de Portos terá prerrogativas, garantias, vantagens e direitos equivalentes aos de Ministro de Estado"
PAR_COMUM = r"Parágrafo único\. São Ministros de Estado os titulares dos Ministérios, o Chefe da Casa Civil"
ART1_12462 = r"Art\. 1º A Presidência da República é constituída, essencialmente: I - pela Casa Civil; II - pela Secretaria-Geral; III - pela Secretaria de Relações Institucionais; IV - pela Secretaria de Comunicação Social; V - pelo Gabinete Pessoal; VI - pelo Gabinete de Segurança Institucional; VII - pela Secretaria de Assuntos Estratégicos; VIII - pela Secretaria de Políticas para as Mulheres; IX - pela Secretaria de Direitos Humanos; X - pela Secretaria de Políticas de Promoção da Igualdade Racial; XI - pela Secretaria de Portos; e XII - pela Secretaria de Aviação Civil\."
PAR_12462 = r"Parágrafo único\. São Ministros de Estado: I - os titulares dos Ministérios; II - os titulares das Secretarias da Presidência da República; III - o Advogado-Geral da União; IV - o Chefe da Casa Civil da Presidência da República; V - o Chefe do Gabinete de Segurança Institucional da Presidência da República; VI - o Chefe da Controladoria-Geral da União; VII - o Presidente do Banco Central do Brasil"

# nomes de Ministerios que se repetem em varios anos (com artigo, sem o prefixo "Ministério ")
M03 = ["da Agricultura, Pecuária e Abastecimento", "da Assistência Social", "das Cidades", "da Ciência e Tecnologia", "das Comunicações", "da Cultura",
       "da Defesa", "do Desenvolvimento Agrário", "do Desenvolvimento, Indústria e Comércio Exterior", "da Educação", "do Esporte", "da Fazenda",
       "da Integração Nacional", "da Justiça", "do Meio Ambiente", "de Minas e Energia", "do Planejamento, Orçamento e Gestão", "da Previdência Social",
       "das Relações Exteriores", "da Saúde", "do Trabalho e Emprego", "dos Transportes", "do Turismo"]           # 23 (Lei 10.683, redacao original)
M05 = [("do Desenvolvimento Social e Combate à Fome" if x == "da Assistência Social" else x) for x in M03]   # 23 (MDS, MP 163/Lei 10.869)
M10 = M05 + ["da Pesca e Aquicultura"]                                                           # 24 (Lei 11.958)
M12 = [("da Ciência, Tecnologia e Inovação" if x == "da Ciência e Tecnologia" else x) for x in M10]   # 24 (MP 541/Lei 12.545)
M16 = [x for x in M12 if x not in ("da Previdência Social", "da Pesca e Aquicultura", "do Trabalho e Emprego")] + \
      ["do Trabalho e Previdência Social", "das Mulheres, da Igualdade Racial e dos Direitos Humanos"]   # 23 (MP 696)
M17 = ["da Agricultura, Pecuária e Abastecimento", "da Ciência, Tecnologia, Inovações e Comunicações", "da Defesa", "da Cultura", "da Fazenda",
       "da Indústria, Comércio Exterior e Serviços", "da Integração Nacional", "da Justiça e Cidadania", "da Saúde",
       "da Transparência, Fiscalização e Controladoria-Geral da União - CGU", "das Cidades", "das Relações Exteriores", "de Minas e Energia",
       "do Desenvolvimento Social e Agrário", "do Esporte", "do Meio Ambiente", "do Planejamento, Desenvolvimento e Gestão", "do Trabalho", "do Turismo",
       "dos Transportes, Portos e Aviação Civil", "da Educação"]                                   # 21 (Leis 13.341 e 13.345)
M18 = ["da Agricultura, Pecuária e Abastecimento", "das Cidades", "da Ciência, Tecnologia, Inovações e Comunicações", "da Cultura", "da Defesa",
       "do Desenvolvimento Social", "dos Direitos Humanos", "da Educação", "do Esporte", "da Fazenda", "da Indústria, Comércio Exterior e Serviços",
       "da Integração Nacional", "da Justiça e Segurança Pública", "do Meio Ambiente", "de Minas e Energia", "do Planejamento, Desenvolvimento e Gestão",
       "do Trabalho", "dos Transportes, Portos e Aviação Civil", "do Turismo", "das Relações Exteriores", "da Saúde", "da Transparência e Controladoria-Geral da União"]  # 22 (Lei 13.502)
M20 = ["Ministério da Agricultura, Pecuária e Abastecimento", "Ministério da Cidadania", "Ministério da Ciência, Tecnologia, Inovações e Comunicações",
       "Ministério da Defesa", "Ministério do Desenvolvimento Regional", "Ministério da Economia", "Ministério da Educação",
       "Ministério da Infraestrutura", "Ministério da Justiça e Segurança Pública", "Ministério do Meio Ambiente", "Ministério de Minas e Energia",
       "Ministério da Mulher, da Família e dos Direitos Humanos", "Ministério das Relações Exteriores", "Ministério da Saúde", "Ministério do Turismo",
       "Controladoria-Geral da União"]                                                              # 16 (MP 870 / Lei 13.844)
M21 = [x for x in M20 if "Ciência" not in x] + ["Ministério da Ciência, Tecnologia e Inovações", "Ministério das Comunicações"]   # 17 (Lei 14.074)
M22 = M21 + ["Ministério do Trabalho e Previdência"]                                             # 18 (Lei 14.261)

# ---- especificacao por ano ---------------------------------------------------------------------------------------
# lista: ("auto", arq, regex_ini, regex_fim)  -> le o artigo no proprio arquivo
#        ("man", [nomes sem prefixo], [arquivos onde cada nome deve aparecer], arq_trecho, regex_trecho, tamanho_trecho)
# status: lista de grupos (arq, regex_ancora, base, [(tipo, nome, chave)]) ; chave deve aparecer no texto casado pela ancora
SPEC = []
def Y(ano, norma, data, arq, lista, status, atos, verif, extra_arqs=None, nv=None):
    SPEC.append(dict(ano=ano, norma=norma, data=data, arq=arq, lista=lista, status=status, atos=atos, verif=verif,
                     extra_arqs=extra_arqs or [], nv=nv or ""))

RI = r"Art\. 13\. (São os seguintes os Ministérios|Os Ministérios são os seguintes):"
FIM13 = r"Parágrafo único|§ 1[oº]"

Y(1995, "Medida Provisória nº 813, de 1º/1/1995 (organização da Presidência da República e dos Ministérios; art. 13)", "1995-01-01",
  B+"mpv-0813.html", ("auto", B+"mpv-0813.html", RI, FIM13),
  [(B+"mpv-0813.html", PAR95, "art. 13, par. único", [("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Estado-Maior das Forças Armadas", "Estado-Maior")]),
   (B+"mpv-0813.html", ESP, "art. 26", [("B", "Ministro de Estado Extraordinário dos Esportes", "Esportes")]),
   (B+"mpv-0813.html", ART24_813, "art. 24 e par. único", [("C", "Chefe da Casa Militar da Presidência da República", "Casa Militar"), ("C", "Secretário-Geral da Presidência da República", "Secretário-Geral"),
        ("C", "Secretário de Comunicação Social da Presidência da República", "Comunicação Social"), ("C", "Secretário de Assuntos Estratégicos da Presidência da República", "Assuntos Estratégicos")])],
  "Início da série: sem lista anterior comparada nos arquivos baixados (o governo anterior está fora do recorte).",
  "Lista lida no art. 13 do arquivo bruto. Status: lidos o par. único do art. 13, o art. 24 (equivalência) e o art. 26 (Esportes). MP em vigor desde a publicação em 1/1/1995.")

Y(1996, "Medida Provisória nº 1.226, de 14/12/1995 (reedição mensal da MP 813; art. 13)", "1995-12-14",
  B+"mpv-1226.html", ("auto", B+"mpv-1226.html", RI, FIM13),
  [(B+"mpv-1226.html", PAR95, "art. 13, par. único", [("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Estado-Maior das Forças Armadas", "Estado-Maior")]),
   (B+"mpv-1226.html", r"Fica criado o cargo de Ministro de Estado Extraordinário dos Esportes", "art. 25", [("B", "Ministro de Estado Extraordinário dos Esportes", "Esportes")]),
   (B+"mpv-1226.html", ART23_1226, "art. 23", [("C", "Chefe da Casa Militar da Presidência da República", "Casa Militar"), ("C", "Secretário-Geral da Presidência da República", "Secretário-Geral"),
        ("C", "Secretário de Comunicação Social da Presidência da República", "Comunicação Social"), ("C", "Secretário de Assuntos Estratégicos da Presidência da República", "Assuntos Estratégicos")]),
   (B+"mpv-1226.html", ART26_1226, "art. 23 c/c art. 26 (equivalência do Secretário-Executivo da Câmara de Políticas Regionais)", [("C", "Secretário-Executivo da Câmara de Políticas Regionais do Conselho de Governo", "Câmara de Políticas Regionais")])],
  "AUTO", "Lista e status lidos no texto da MP 1.226 (a MP seguinte da série, 1.263, é de 12/1/1996). Reedição = MP 813 renovada a cada ~30 dias; DOU não conferido arquivo a arquivo.")

Y(1997, "Medida Provisória nº 1.549, de 18/12/1996 (reedição da série MP 813/1.498; art. 13)", "1996-12-18",
  B+"mpv-1549.html", ("auto", B+"mpv-1549.html", RI, FIM13),
  [(B+"mpv-1549.html", PAR95, "art. 13, par. único", [("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Estado-Maior das Forças Armadas", "Estado-Maior")]),
   (B+"mpv-1549.html", r"Fica criado o cargo de Ministro de Estado Extraordinário dos Esportes", "art. 25", [("B", "Ministro de Estado Extraordinário dos Esportes", "Esportes")]),
   (B+"d1888.html", FUND_D1888, "Decreto nº 1.888, de 29/4/1996 (existência do Gabinete; ato de criação NÃO localizado)", [("B", "Ministro de Estado Extraordinário de Política Fundiária", "Política Fundiária")]),
   (B+"mpv-1549.html", ART23_1226, "art. 23", [("C", "Chefe da Casa Militar da Presidência da República", "Casa Militar"), ("C", "Secretário-Geral da Presidência da República", "Secretário-Geral"),
        ("C", "Secretário de Comunicação Social da Presidência da República", "Comunicação Social"), ("C", "Secretário de Assuntos Estratégicos da Presidência da República", "Assuntos Estratégicos")]),
   (B+"mpv-1549.html", r"Art\. 26\. O titular do cargo de Natureza Especial de Secretário-Executivo da Câmara de Políticas Regionais", "art. 23 c/c art. 26", [("C", "Secretário-Executivo da Câmara de Políticas Regionais do Conselho de Governo", "Câmara de Políticas Regionais")])],
  "AUTO", "Lista e status lidos na MP 1.549. Política Fundiária: o Gabinete do Ministro Extraordinário aparece nos Decretos 1.888 e 1.918 (abril-maio/1996) e 2.321 (8/9/1997); a norma que o criou não foi encontrada; presença em 1/1/1997 inferida por continuidade entre duas datas confirmadas (marca de incerteza).",
  extra_arqs=[B+"d1918.html"], nv="Política Fundiária em 1/1/1997: ato de criação e texto de 1/1/1997 não localizados.")

Y(1998, "Medida Provisória nº 1.549-38, de 31/12/1997 (reedição; art. 13)", "1997-12-31",
  B+"mpv-1549-38.html", ("auto", B+"mpv-1549-38.html", RI, FIM13),
  [(B+"mpv-1549-38.html", PAR95, "art. 13, par. único", [("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Estado-Maior das Forças Armadas", "Estado-Maior")]),
   (B+"mpv-1549-38.html", r"Fica criado o cargo de Ministro de Estado Extraordinário dos Esportes", "art. 25", [("B", "Ministro de Estado Extraordinário dos Esportes", "Esportes")]),
   (B+"d2321.html", FUND_D2321, "Decreto nº 2.321, de 8/9/1997 (existência do Gabinete; ato de criação NÃO localizado)", [("B", "Ministro de Estado Extraordinário de Política Fundiária", "Política Fundiária")]),
   (B+"mpv-1549-38.html", ART23_1226, "art. 23", [("C", "Chefe da Casa Militar da Presidência da República", "Casa Militar"), ("C", "Secretário-Geral da Presidência da República", "Secretário-Geral"),
        ("C", "Secretário de Comunicação Social da Presidência da República", "Comunicação Social"), ("C", "Secretário de Assuntos Estratégicos da Presidência da República", "Assuntos Estratégicos")]),
   (B+"mpv-1549-38.html", r"Art\. 26\. O titular do cargo de Natureza Especial de Secretário-Executivo da Câmara de Políticas Regionais", "art. 23 c/c art. 26", [("C", "Secretário-Executivo da Câmara de Políticas Regionais do Conselho de Governo", "Câmara de Políticas Regionais")])],
  "AUTO", "Lista e status lidos na MP 1.549-38 (31/12/1997; a anterior, 1.549-37, é de 4/12/1997 e tem a mesma lista). No texto do Planalto o item XVI aparece como 'XIV' (erro de numeração, 20 itens). Se a 1.549-38 só foi publicada em 1-2/1/1998, vale a -37, de lista idêntica. DOU não conferido.",
  nv="Data exata de publicação no DOU da MP 1.549-38 (31/12/1997 vs. 1-2/1/1998) não conferida; lista idêntica à da -37.")

Y(1999, "Lei nº 9.649, de 27/5/1998, na redação da Medida Provisória nº 1.795, de 1º/1/1999 (art. 13)", "1999-01-01",
  B+"mpv-1795.html", ("auto", B+"mpv-1795.html", RI, FIM13),
  [(B+"mpv-1795.html", PAR99, "art. 13, par. único (MP 1.795)", [("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Estado-Maior das Forças Armadas", "Estado-Maior")]),
   (B+"mpv-1795.html", r"Gabinete do Ministro Extraordinário de Projetos Especiais as atribuições", "art. 6º (MP 1.795)", [("B", "Ministro de Estado Extraordinário de Projetos Especiais", "Projetos Especiais")]),
   (B+"d2321.html", FUND_D2321, "Decreto nº 2.321, de 8/9/1997 (existência do Gabinete; ato de criação NÃO localizado)", [("B", "Ministro de Estado Extraordinário de Política Fundiária", "Política Fundiária")]),
   (B+"l9649-compilada.html", r"Art\. 23\. Os titulares dos cargos de Natureza Especial de Chefe da Casa Militar da Presidência da República", "art. 23 da Lei 9.649/1998 (texto compilado; a lei original não foi baixada)", [("C", "Chefe da Casa Militar da Presidência da República", "Casa Militar")]),
   (B+"mpv-1795.html", r"Art\. 26\. O titular do cargo de Natureza Especial de Secretário-Executivo da Câmara de Políticas Regionais.{0,300}equivalentes aos de Ministro de Estado", "art. 26 e par. único (MP 1.795)", [("C", "Secretário-Executivo da Câmara de Políticas Regionais do Conselho de Governo", "Câmara de Políticas Regionais")]),
   (B+"mpv-1795.html", r"Art\. 22-A\. Ficam extintos os cargos de Secretário-Geral da Presidência da República, de Secretário de Assuntos Estratégicos da Presidência da República, Secretário de Comunicação Social da Presidência da República", "art. 22-A (MP 1.795): extingue Secretário-Geral, Assuntos Estratégicos e Comunicação Social (saem de C) e o Ministro Extraordinário dos Esportes (sai de B)", [])],
  "AUTO", "Lista e par. único lidos na MP 1.795 (altera a Lei 9.649/1998, cujo texto original de 27/5/1998 não foi baixado; só a versão compilada de 2001). Status C do Chefe da Casa Militar: art. 23 da Lei 9.649 aparece apenas no compilado (anotado 'Vide MP 1.795'); a MP 1.795 não o revoga (revogado só pela MP 2.216-37). Projetos Especiais e Política Fundiária: presença por continuidade, atos de criação não localizados.",
  extra_arqs=[B+"mpv-1549-40.html", B+"mpv-1651-43.html"],
  nv="Atos de criação dos cargos de Ministro Extraordinário de Projetos Especiais e de Política Fundiária não localizados; Lei 9.649 original (27/5/1998) não baixada.")

Y(2000, "Lei nº 9.649/1998, na redação da Medida Provisória nº 1.999-13, de 14/12/1999 (art. 13)", "1999-12-14",
  B+"mpv-1999-13.html", ("auto", B+"mpv-1999-13.html", RI, FIM13),
  [(B+"mpv-1999-13.html", PAR00, "art. 13, par. único", [("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Gabinete de Segurança Institucional da Presidência da República", "Gabinete de Segurança Institucional"),
        ("A", "Secretaria-Geral da Presidência da República", "Secretaria-Geral"), ("A", "Secretaria de Comunicação de Governo da Presidência da República", "Secretaria de Comunicação de Governo")]),
   (B+"mpv-1999-13.html", SEDU, "art. 24-A, § 2º", [("C", "Secretário Especial de Desenvolvimento Urbano", "Desenvolvimento Urbano")])],
  "AUTO", "Lista no art. 13 da MP 1.999-13; o Planalto traz erro de numeração (XVIII, IX, XX) mas há 20 itens (corrigido na reedição 1.999-15). Gabinete do Ministro Extraordinário de Política Fundiária virou Ministério da Política Fundiária e do Desenvolvimento Agrário (item da lista), então não entra em B. EMFA extinto (Defesa).")

Y(2001, "Lei nº 9.649/1998, na redação da Medida Provisória nº 2.049-26, de 21/12/2000 (art. 13)", "2000-12-21",
  B+"mpv-2049-26.html", ("auto", B+"mpv-2049-26.html", RI, FIM13),
  [(B+"mpv-2049-26.html", PAR01, "art. 13, par. único", [("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Gabinete de Segurança Institucional da Presidência da República", "Gabinete de Segurança Institucional"),
        ("A", "Secretaria-Geral da Presidência da República", "Secretaria-Geral"), ("A", "Secretaria de Comunicação de Governo da Presidência da República", "Secretaria de Comunicação de Governo"), ("A", "Advogado-Geral da União", "Advogado-Geral")]),
   (B+"mpv-2049-26.html", SEDU, "art. 24-A, § 2º", [("C", "Secretário Especial de Desenvolvimento Urbano", "Desenvolvimento Urbano")])],
  "AUTO", "Lista e par. único lidos na MP 2.049-26 (21/12/2000); a série 2.123/2.143 só começa em 26/1/2001.")

Y(2002, "Lei nº 9.649/1998, na redação da Medida Provisória nº 2.216-37, de 31/8/2001 (art. 13), com o Decreto nº 4.046, de 10/12/2001", "2001-08-31",
  B+"mpv-2216-37.html", ("auto", B+"mpv-2216-37.html", RI, r"§ 1o"),
  [(B+"mpv-2216-37.html", PAR02, "art. 13, § 1º (o texto lista também o Chefe da Secretaria de Comunicação de Governo, mas ver Decreto 4.046)", [("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Gabinete de Segurança Institucional da Presidência da República", "Gabinete de Segurança Institucional"),
        ("A", "Secretaria-Geral da Presidência da República", "Secretaria-Geral"), ("A", "Advogado-Geral da União", "Advogado-Geral"), ("A", "Corregedor-Geral da União", "Corregedor-Geral")]),
   (B+"d4046.html", r"Fica extinto o cargo de Ministro de Estado Chefe da Secretaria de Comunicação de Governo da Presidência da República", "Decreto 4.046, de 10/12/2001, art. 1º: extingue o cargo de Ministro Chefe da SECOM (não conta em A)", []),
   (B+"mpv-2216-37.html", SEDU, "art. 24-A, § 2º", [("C", "Secretário Especial de Desenvolvimento Urbano", "Desenvolvimento Urbano")])],
  "AUTO", "Lista e § 1º lidos na MP 2.216-37 (31/8/2001; passou a vigência indefinida com a EC 32/2001). O Decreto 4.046 extinguiu o cargo de Ministro Chefe da SECOM: contado como não-Ministro em 1/1/2002 (o texto do § 1º ainda o cita, com 'Vide Decreto 4.046' no compilado). Séries paralelas 2.123/2.143 examinadas: lista idêntica à da 2.216-37, salvo o nome da Agricultura.",
  extra_arqs=[B+"mpv-2143-35.html", B+"mpv-2123-30.html"])

Y(2003, "Medida Provisória nº 103, de 1º/1/2003 (organização da Presidência da República e dos Ministérios; art. 25; revoga a Lei 9.649/1998)", "2003-01-01",
  B+"mpv-0103.html", ("auto", B+"mpv-0103.html", r"Art\. 25\. Os Ministérios são os seguintes:", r"§ 1o"),
  [(B+"mpv-0103.html", r"§ 1o São Ministros de Estado os titulares dos Ministérios, o Chefe da Casa Civil, o Chefe do Gabinete de Segurança Institucional, o Chefe da Secretaria de Comunicação de Governo e Gestão Estratégica e o Chefe da Secretaria-Geral da Presidência da República, o Advogado-Geral da União e o Controlador-Geral da União", "art. 25, § 1º", [("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Gabinete de Segurança Institucional da Presidência da República", "Gabinete de Segurança Institucional"),
        ("A", "Secretaria de Comunicação de Governo e Gestão Estratégica", "Comunicação de Governo"), ("A", "Secretaria-Geral da Presidência da República", "Secretaria-Geral"), ("A", "Advogado-Geral da União", "Advogado-Geral"), ("A", "Controlador-Geral da União", "Controlador-Geral")]),
   (B+"mpv-0103.html", r"Art\. 37\. Fica criado o cargo de Ministro de Estado Extraordinário de Segurança Alimentar e Combate à Fome", "art. 37 (e Gabinete no art. 26: não é item da lista de Ministérios)", [("B", "Ministro de Estado Extraordinário de Segurança Alimentar e Combate à Fome", "Segurança Alimentar")]),
   (B+"mpv-0103.html", ART38, "art. 38 e § 1º", [("C", "Secretário Especial do Conselho de Desenvolvimento Econômico e Social", "Conselho de Desenvolvimento Econômico e Social"), ("C", "Secretário Especial de Aquicultura e Pesca", "Pesca"),
        ("C", "Secretário Especial dos Direitos Humanos", "Direitos Humanos"), ("C", "Secretário Especial de Políticas para as Mulheres", "Mulheres")])],
  "AUTO", "Lista no art. 25 da MP 103. A SEPPIR ainda não existia (MP 111, de 21/3/2003). Cargo de Secretário Especial de Desenvolvimento Urbano: extinto pelo art. 41 da lei de 2003 (não lido na MP; ver nota).",
  extra_arqs=[B+"mpv-0111.html"])

Y(2004, "Lei nº 10.683, de 28/5/2003 (texto original; conversão da MP 103/2003), art. 25", "2003-05-28",
  B+"l10683-original.html", ("man", M03, [B+"l10683-original.html"], B+"l10683-original.html", r"Art\. 25\. Os Ministérios são os seguintes: I - da Agricultura, Pecuária e Abastecimento; II - da Assistência Social;", 420),
  [(B+"l10683-original.html", r"Parágrafo único\. São Ministros de Estado os titulares dos Ministérios, o Chefe da Casa Civil, o Chefe do Gabinete de Segurança Institucional, o Chefe da Secretaria de Comunicação de Governo e Gestão Estratégica e o Chefe da Secretaria-Geral da Presidência da República, o Advogado-Geral da União e o Ministro de Estado do Controle e da Transparência", "art. 25, par. único (texto original, sem anotação no compilado)", [("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Gabinete de Segurança Institucional da Presidência da República", "Gabinete de Segurança Institucional"),
        ("A", "Secretaria de Comunicação de Governo e Gestão Estratégica", "Comunicação de Governo"), ("A", "Secretaria-Geral da Presidência da República", "Secretaria-Geral"), ("A", "Advogado-Geral da União", "Advogado-Geral"), ("A", "Ministro de Estado do Controle e da Transparência", "Controle e da Transparência")]),
   (B+"l10683-original.html", r"Art\. 37\. Fica criado o cargo de Ministro de Estado Extraordinário de Segurança Alimentar e Combate à Fome", "art. 37 (revogado só pela Lei 10.869/2004)", [("B", "Ministro de Estado Extraordinário de Segurança Alimentar e Combate à Fome", "Segurança Alimentar")]),
   (B+"l10683-original.html", ART38, "art. 38 e § 1º", [("C", "Secretário Especial do Conselho de Desenvolvimento Econômico e Social", "Conselho de Desenvolvimento Econômico e Social"), ("C", "Secretário Especial de Aquicultura e Pesca", "Pesca"),
        ("C", "Secretário Especial dos Direitos Humanos", "Direitos Humanos"), ("C", "Secretário Especial de Políticas para as Mulheres", "Mulheres")]),
   (B+"l10678.html", SEPPIR_C, "Lei 10.678/2003, art. 4º e par. único (SEPPIR)", [("C", "Secretário Especial de Políticas de Promoção da Igualdade Racial", "")])],
  "MP 103 (1/1/2003) convertida na Lei 10.683 (28/5/2003): art. 25, inciso II passa de 'da Assistência e Promoção Social' para 'da Assistência Social'; a MP 111 (21/3/2003), convertida na Lei 10.678 (23/5/2003), cria a Secretaria Especial de Políticas de Promoção da Igualdade Racial (C). Controlador-Geral da União passa a 'Ministro de Estado do Controle e da Transparência'.",
  "Texto original da Lei 10.683 não está em arquivo próprio no Planalto: lido no texto compilado, onde o trecho sem anotação 'Redação dada' é o original. Lista: 23 itens do art. 25 original conferidos no compilado.",
  extra_arqs=[B+"mpv-0103.html"])

Y(2005, "Lei nº 10.683/2003, art. 25, na redação das Leis nº 10.869 (13/5/2004; MP 163 de 23/1/2004) e nº 11.036 (22/12/2004; MP 207 de 13/8/2004)", "2004-12-22",
  B+"l11036.html", ("man", M05, [B+"l10683-original.html", B+"l10869.html"], B+"l10869.html", r"II - do Desenvolvimento Social e Combate à Fome", 140),
  [(B+"l11036.html", r"Parágrafo único\. São Ministros de Estado os titulares dos Ministérios, o Chefe da Casa Civil, o Chefe do Gabinete de Segurança Institucional, o Chefe da Secretaria de Comunicação de Governo e Gestão Estratégica, o Chefe da Secretaria-Geral da Presidência da República, o Chefe da Secretaria de Coordenação Política e Assuntos Institucionais da Presidência da República, o Advogado-Geral da União, o Ministro de Estado do Controle e da Transparência e o Presidente do Banco Central do Brasil", "art. 25, par. único (Lei 11.036)", [("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Gabinete de Segurança Institucional da Presidência da República", "Gabinete de Segurança Institucional"),
        ("A", "Secretaria de Comunicação de Governo e Gestão Estratégica", "Comunicação de Governo"), ("A", "Secretaria-Geral da Presidência da República", "Secretaria-Geral"), ("A", "Secretaria de Coordenação Política e Assuntos Institucionais", "Coordenação Política"),
        ("A", "Advogado-Geral da União", "Advogado-Geral"), ("A", "Ministro de Estado do Controle e da Transparência", "Controle e da Transparência"), ("A", "Presidente do Banco Central do Brasil", "Banco Central")]),
   (B+"l10869.html", r"Art\. 10\. Ficam extintos os cargos de Ministro de Estado Extraordinário de Segurança Alimentar e Combate à Fome", "Lei 10.869, art. 10: extingue o cargo de Ministro Extraordinário de Segurança Alimentar (sai de B)", []),
   (B+"l10683-original.html", ART38, "art. 38 e § 1º", [("C", "Secretário Especial do Conselho de Desenvolvimento Econômico e Social", "Conselho de Desenvolvimento Econômico e Social"), ("C", "Secretário Especial de Aquicultura e Pesca", "Pesca"),
        ("C", "Secretário Especial dos Direitos Humanos", "Direitos Humanos"), ("C", "Secretário Especial de Políticas para as Mulheres", "Mulheres")]),
   (B+"l10678.html", SEPPIR_C, "Lei 10.678/2003, art. 4º e par. único (SEPPIR)", [("C", "Secretário Especial de Políticas de Promoção da Igualdade Racial", "")])],
  "MP 163 (23/1/2004; Lei 10.869, 13/5/2004): inciso II vira 'do Desenvolvimento Social e Combate à Fome' (substitui Assistência Social), extingue o Ministro Extraordinário de Segurança Alimentar (arts. 6º e 10) e inclui a Secretaria de Coordenação Política e Assuntos Institucionais em A. MP 207 (13/8/2004; Lei 11.036, 22/12/2004) transforma o cargo de Presidente do Banco Central em cargo de Ministro de Estado (art. 2º) e o põe no par. único.",
  "Lista: texto original (compilado) + a alteração do inciso II (Lei 10.869). Par. único e extinção lidos nas leis citadas. Equivalências (art. 38, Lei 10.678) não revogadas até aqui, segundo as anotações do compilado.",
  extra_arqs=[B+"mpv-0163.html", B+"mpv-0207.html"])

Y(2006, "Lei nº 10.683/2003, art. 25, na redação da Lei nº 11.204, de 5/12/2005 (conversão da MP 259, de 21/7/2005)", "2005-12-05",
  B+"l11204.html", ("man", M05, [B+"l10683-original.html", B+"l10869.html"], B+"l10869.html", r"II - do Desenvolvimento Social e Combate à Fome", 140),
  [(B+"l11204.html", r"Parágrafo único\. São Ministros de Estado os titulares dos Ministérios, o Chefe da Casa Civil, o Chefe do Gabinete de Segurança Institucional, o Chefe da Secretaria-Geral da Presidência da República, o Chefe da Secretaria de Relações Institucionais da Presidência da República, o Advogado-Geral da União, o Ministro de Estado do Controle e da Transparência e o Presidente do Banco Central do Brasil", "art. 25, par. único (Lei 11.204)", [("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Gabinete de Segurança Institucional da Presidência da República", "Gabinete de Segurança Institucional"),
        ("A", "Secretaria-Geral da Presidência da República", "Secretaria-Geral"), ("A", "Secretaria de Relações Institucionais da Presidência da República", "Relações Institucionais"), ("A", "Advogado-Geral da União", "Advogado-Geral"),
        ("A", "Ministro de Estado do Controle e da Transparência", "Controle e da Transparência"), ("A", "Presidente do Banco Central do Brasil", "Banco Central")]),
   (B+"l11204.html", r"Art\. 4º Ficam extintos: I - o cargo de Ministro de Estado Chefe da Secretaria de Comunicação de Governo e Gestão Estratégica da Presidência da República; e II - o cargo de Natureza Especial de Secretário Especial do Conselho de Desenvolvimento Econômico e Social", "Lei 11.204, art. 4º: extingue o Ministro Chefe da SECOM e o Secretário Especial do CDES (saem de A e C)", []),
   (B+"l10683-original.html", ART38, "art. 38 e § 1º (CDES já extinto pela Lei 11.204)", [("C", "Secretário Especial de Aquicultura e Pesca", "Pesca"), ("C", "Secretário Especial dos Direitos Humanos", "Direitos Humanos"), ("C", "Secretário Especial de Políticas para as Mulheres", "Mulheres")]),
   (B+"l10678.html", SEPPIR_C, "Lei 10.678/2003, art. 4º e par. único (SEPPIR)", [("C", "Secretário Especial de Políticas de Promoção da Igualdade Racial", "")])],
  "MP 259 (21/7/2005; Lei 11.204, 5/12/2005): Secretaria de Coordenação Política vira Secretaria de Relações Institucionais; extingue o cargo de Ministro Chefe da SECOM (comunicação passa à Secretaria-Geral) e o de Secretário Especial do CDES.",
  "Par. único e extinções lidos na Lei 11.204; lista de Ministérios inalterada (anotações do compilado não mostram outra redação do art. 25, caput, entre 2004 e 2008).",
  extra_arqs=[B+"mpv-0259.html"])

Y(2007, "Lei nº 10.683/2003, art. 25, na redação da Lei nº 11.204, de 5/12/2005 (sem alteração de lista ou status em 2006)", "2005-12-05",
  B+"l11204.html", ("man", M05, [B+"l10683-original.html", B+"l10869.html"], B+"l10869.html", r"II - do Desenvolvimento Social e Combate à Fome", 140),
  [(B+"l11204.html", r"Parágrafo único\. São Ministros de Estado os titulares dos Ministérios, o Chefe da Casa Civil, o Chefe do Gabinete de Segurança Institucional, o Chefe da Secretaria-Geral da Presidência da República, o Chefe da Secretaria de Relações Institucionais da Presidência da República, o Advogado-Geral da União, o Ministro de Estado do Controle e da Transparência e o Presidente do Banco Central do Brasil", "art. 25, par. único (Lei 11.204)", [("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Gabinete de Segurança Institucional da Presidência da República", "Gabinete de Segurança Institucional"),
        ("A", "Secretaria-Geral da Presidência da República", "Secretaria-Geral"), ("A", "Secretaria de Relações Institucionais da Presidência da República", "Relações Institucionais"), ("A", "Advogado-Geral da União", "Advogado-Geral"),
        ("A", "Ministro de Estado do Controle e da Transparência", "Controle e da Transparência"), ("A", "Presidente do Banco Central do Brasil", "Banco Central")]),
   (B+"l10683-original.html", ART38, "art. 38 e § 1º (CDES já extinto pela Lei 11.204)", [("C", "Secretário Especial de Aquicultura e Pesca", "Pesca"), ("C", "Secretário Especial dos Direitos Humanos", "Direitos Humanos"), ("C", "Secretário Especial de Políticas para as Mulheres", "Mulheres")]),
   (B+"l10678.html", SEPPIR_C, "Lei 10.678/2003, art. 4º e par. único (SEPPIR)", [("C", "Secretário Especial de Políticas de Promoção da Igualdade Racial", "")])],
  "Nenhum ato que altere art. 25 (caput ou par. único) ou os arts. 37-38 foi achado entre 5/12/2005 e 1/1/2007 nas anotações do compilado da Lei 10.683 (leis de 2006 listadas ali mexem só no art. 29).",
  "Mesma redação do ano anterior. A varredura das anotações do compilado é por busca de texto (ver scripts/gerar.py, função varredura_anotacoes).")

Y(2008, "Lei nº 10.683/2003, art. 25, na redação da Lei nº 11.497, de 28/6/2007 (conversão da MP 360, de 28/3/2007) e Lei nº 11.518, de 5/9/2007 (Portos)", "2007-06-28",
  B+"l11497.html", ("man", M05, [B+"l10683-original.html", B+"l10869.html"], B+"l10869.html", r"II - do Desenvolvimento Social e Combate à Fome", 140),
  [(B+"l11497.html", r"Parágrafo único\. São Ministros de Estado os titulares dos Ministérios, o Chefe da Casa Civil da Presidência da República, o Chefe do Gabinete de Segurança Institucional da Presidência da República, o Chefe da Secretaria-Geral da Presidência da República, o Chefe da Secretaria de Relações Institucionais da Presidência da República, o Chefe da Secretaria de Comunicação Social da Presidência da República, o Advogado-Geral da União, o Ministro de Estado do Controle e da Transparência e o Presidente do Banco Central do Brasil", "art. 25, par. único (Lei 11.497)", [("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Gabinete de Segurança Institucional da Presidência da República", "Gabinete de Segurança Institucional"),
        ("A", "Secretaria-Geral da Presidência da República", "Secretaria-Geral"), ("A", "Secretaria de Relações Institucionais da Presidência da República", "Relações Institucionais"), ("A", "Secretaria de Comunicação Social da Presidência da República", "Comunicação Social"),
        ("A", "Advogado-Geral da União", "Advogado-Geral"), ("A", "Ministro de Estado do Controle e da Transparência", "Controle e da Transparência"), ("A", "Presidente do Banco Central do Brasil", "Banco Central")]),
   (B+"l10683-original.html", ART38, "art. 38 e § 1º (CDES já extinto)", [("C", "Secretário Especial de Aquicultura e Pesca", "Pesca"), ("C", "Secretário Especial dos Direitos Humanos", "Direitos Humanos"), ("C", "Secretário Especial de Políticas para as Mulheres", "Mulheres")]),
   (B+"l10678.html", SEPPIR_C, "Lei 10.678/2003, art. 4º e par. único (SEPPIR)", [("C", "Secretário Especial de Políticas de Promoção da Igualdade Racial", "")]),
   (B+"l11518.html", PORTOS_C, "Lei 11.518/2007, art. 7º, par. único (Portos; MP 369 de 7/5/2007)", [("C", "Secretário Especial de Portos", "")])],
  "MP 360 (28/3/2007; Lei 11.497, 28/6/2007) cria a Secretaria de Comunicação Social e devolve o titular ao par. único; MP 369 (7/5/2007; Lei 11.518, 5/9/2007) cria a Secretaria Especial de Portos, titular com equivalência (C). MP 377 (18/6/2007) rejeitada (Ato Declaratório nº 1/2007-SF): sem efeito.",
  "Par. único e equivalência lidos nas leis citadas.",
  extra_arqs=[B+"mpv-0360.html", B+"mpv-0369.html", B+"mpv-0377.html"])

Y(2009, "Lei nº 10.683/2003, art. 25, na redação da Lei nº 11.754, de 23/7/2008 (Secretaria de Assuntos Estratégicos) e Lei nº 11.693, de 11/6/2008 (SEPPIR)", "2008-07-23",
  B+"l11754.html", ("man", M05, [B+"l10683-original.html", B+"l10869.html"], B+"l10869.html", r"II - do Desenvolvimento Social e Combate à Fome", 140),
  [(B+"l11754.html", r"Parágrafo único\. São Ministros de Estado os titulares dos Ministérios, o Chefe da Casa Civil da Presidência da República, o Chefe do Gabinete de Segurança Institucional da Presidência da República, o Chefe da Secretaria-Geral da Presidência da República, o Chefe da Secretaria de Relações Institucionais da Presidência da República, o Chefe da Secretaria de Comunicação Social da Presidência da República, o Advogado-Geral da União, o Ministro de Estado do Controle e da Transparência, o Ministro de Estado Chefe da Secretaria de Assuntos Estratégicos da Presidência da República e o Presidente do Banco Central do Brasil", "art. 25, par. único (Lei 11.754)", [("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Gabinete de Segurança Institucional da Presidência da República", "Gabinete de Segurança Institucional"),
        ("A", "Secretaria-Geral da Presidência da República", "Secretaria-Geral"), ("A", "Secretaria de Relações Institucionais da Presidência da República", "Relações Institucionais"), ("A", "Secretaria de Comunicação Social da Presidência da República", "Comunicação Social"),
        ("A", "Advogado-Geral da União", "Advogado-Geral"), ("A", "Ministro de Estado do Controle e da Transparência", "Controle e da Transparência"), ("A", "Secretaria de Assuntos Estratégicos da Presidência da República", "Assuntos Estratégicos"), ("A", "Presidente do Banco Central do Brasil", "Banco Central")]),
   (B+"l11693.html", r"Art\. 4º-A\. Fica transformado o cargo de Secretário Especial de Políticas de Promoção da Igualdade Racial no cargo de Ministro de Estado Chefe da Secretaria Especial de Políticas de Promoção da Igualdade Racial", "Lei 10.678, art. 4º-A (Lei 11.693/2008): cargo de Ministro de Estado Chefe da SEPPIR (o par. único do art. 25 deixa de citá-lo na Lei 11.754)", [("A", "Ministro de Estado Chefe da Secretaria Especial de Políticas de Promoção da Igualdade Racial", "Igualdade Racial")]),
   (B+"l10683-original.html", ART38, "art. 38 e § 1º", [("C", "Secretário Especial de Aquicultura e Pesca", "Pesca"), ("C", "Secretário Especial dos Direitos Humanos", "Direitos Humanos"), ("C", "Secretário Especial de Políticas para as Mulheres", "Mulheres")]),
   (B+"l11518.html", PORTOS_C, "Lei 11.518/2007, art. 7º, par. único (Portos)", [("C", "Secretário Especial de Portos", "")])],
  "MP 419 (20/2/2008; Lei 11.693, 11/6/2008) transforma o Secretário Especial da SEPPIR em Ministro de Estado Chefe (C vira A). Lei 11.754 (23/7/2008) cria a SAE (A) e reescreve o par. único sem citar a SEPPIR. MP 437 (29/7/2008), que criava o Ministério da Pesca, foi revogada em 29/8/2008 (MP 439): sem efeito em 1/1/2009.",
  "Par. único lido na Lei 11.754. SEPPIR contada em A pelo cargo do art. 4º-A da Lei 10.678, não pelo par. único.",
  extra_arqs=[B+"mpv-0419.html", B+"mpv-0437.html", B+"mpv-0439.html", B+"l11805.html"])

Y(2010, "Lei nº 10.683/2003, art. 25, na redação da Lei nº 11.958, de 26/6/2009 (Ministério da Pesca e Aquicultura)", "2009-06-26",
  B+"l11958.html", ("man", M10, [B+"l10683-original.html", B+"l10869.html", B+"l11958.html"], B+"l11958.html", r"XXIII - do Turismo; e XXIV - da Pesca e Aquicultura\.", 90),
  [(B+"l11958.html", r"Parágrafo único\. São Ministros de Estado os titulares dos Ministérios, o Chefe da Casa Civil da Presidência da República, o Chefe do Gabinete de Segurança Institucional da Presidência da República, o Chefe da Secretaria-Geral da Presidência da República, o Chefe da Secretaria de Relações Institucionais da Presidência da República, o Chefe da Secretaria de Comunicação Social da Presidência da República, o Chefe da Secretaria de Assuntos Estratégicos da Presidência da República, o Chefe da Secretaria Especial de Políticas de Promoção da Igualdade Racial, o Advogado-Geral da União, o Ministro de Estado do Controle e da Transparência e o Presidente do Banco Central do Brasil", "art. 25, par. único (Lei 11.958)", [("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Gabinete de Segurança Institucional da Presidência da República", "Gabinete de Segurança Institucional"),
        ("A", "Secretaria-Geral da Presidência da República", "Secretaria-Geral"), ("A", "Secretaria de Relações Institucionais da Presidência da República", "Relações Institucionais"), ("A", "Secretaria de Comunicação Social da Presidência da República", "Comunicação Social"),
        ("A", "Secretaria de Assuntos Estratégicos da Presidência da República", "Assuntos Estratégicos"), ("A", "Secretaria Especial de Políticas de Promoção da Igualdade Racial", "Igualdade Racial"), ("A", "Advogado-Geral da União", "Advogado-Geral"),
        ("A", "Ministro de Estado do Controle e da Transparência", "Controle e da Transparência"), ("A", "Presidente do Banco Central do Brasil", "Banco Central")]),
   (B+"l10683-original.html", r"Art\. 38\. São criados os cargos de natureza especial de Secretário Especial do Conselho de Desenvolvimento Econômico e Social, de Secretário Especial de Aq.icultura e Pesca, de Secretário Especial dos Direitos Humanos e de Secretário Especial de Políticas para as Mulheres da Presidência da República\.(?: \(Vide[^)]*\))? § 1o Os cargos referidos no caput terão prerrogativas, garantias, vantagens e direitos equivalentes aos de Ministro de Estado", "art. 38 e § 1º (CDES extinto; Aquicultura e Pesca transformado em Ministério pela Lei 11.958, art. 5º, I)", [("C", "Secretário Especial dos Direitos Humanos", "Direitos Humanos"), ("C", "Secretário Especial de Políticas para as Mulheres", "Mulheres")]),
   (B+"l11518.html", PORTOS_C, "Lei 11.518/2007, art. 7º, par. único (Portos)", [("C", "Secretário Especial de Portos", "")])],
  "Lei 11.958 (26/6/2009) cria o Ministério da Pesca e Aquicultura (item XXIV; transforma a Secretaria Especial de Aquicultura e Pesca; Lei não é conversão de MP, ver nota) e restitui a SEPPIR ao par. único.",
  "Lista: texto original + inciso II (Lei 10.869) + inciso XXIV (Lei 11.958). Par. único e art. 5º lidos na Lei 11.958.",
  extra_arqs=[])

Y(2011, "Lei nº 10.683/2003, art. 25, na redação da Lei nº 12.314, de 19/8/2010 (conversão da MP 483, de 24/3/2010)", "2010-08-19",
  B+"l12314.html", ("man", M10, [B+"l10683-original.html", B+"l10869.html", B+"l11958.html"], B+"l11958.html", r"XXIII - do Turismo; e XXIV - da Pesca e Aquicultura\.", 90),
  [(B+"l12314.html", r"Parágrafo único\. São Ministros de Estado os titulares dos Ministérios, o Chefe da Casa Civil da Presidência da República, o Chefe do Gabinete de Segurança Institucional da Presidência da República, o Chefe da Secretaria-Geral da Presidência da República, o Chefe da Secretaria de Relações Institucionais da Presidência da República, o Chefe da Secretaria de Comunicação Social da Presidência da República, o Chefe da Secretaria de Assuntos Estratégicos da Presidência da República, o Chefe da Secretaria de Direitos Humanos da Presidência da República, o Chefe da Secretaria de Políticas de Promoção da Igualdade Racial da Presidência da República, o Chefe da Secretaria de Políticas para as Mulheres da Presidência da República, o Chefe da Secretaria de Portos da Presidência da República, o Advogado-Geral da União, o Ministro de Estado Chefe da Controladoria-Geral da União e o Presidente do Banco Central do Brasil", "art. 25, par. único (Lei 12.314)", [("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Gabinete de Segurança Institucional da Presidência da República", "Gabinete de Segurança Institucional"),
        ("A", "Secretaria-Geral da Presidência da República", "Secretaria-Geral"), ("A", "Secretaria de Relações Institucionais da Presidência da República", "Relações Institucionais"), ("A", "Secretaria de Comunicação Social da Presidência da República", "Comunicação Social"),
        ("A", "Secretaria de Assuntos Estratégicos da Presidência da República", "Assuntos Estratégicos"), ("A", "Secretaria de Direitos Humanos da Presidência da República", "Direitos Humanos"), ("A", "Secretaria de Políticas de Promoção da Igualdade Racial da Presidência da República", "Igualdade Racial"),
        ("A", "Secretaria de Políticas para as Mulheres da Presidência da República", "Mulheres"), ("A", "Secretaria de Portos da Presidência da República", "Portos"), ("A", "Advogado-Geral da União", "Advogado-Geral"),
        ("A", "Controladoria-Geral da União", "Controladoria-Geral"), ("A", "Presidente do Banco Central do Brasil", "Banco Central")])],
  "MP 483 (24/3/2010; Lei 12.314, 19/8/2010): transforma os Secretários Especiais de Direitos Humanos, Políticas para as Mulheres e Portos em Ministros de Estado Chefes (C vira A) e passa a Controladoria-Geral da União a ter Ministro Chefe (A).",
  "Par. único lido na Lei 12.314; lista de Ministérios inalterada.",
  extra_arqs=[B+"mpv-0483.html"])

Y(2012, "Lei nº 10.683/2003, art. 25, na redação da MP 527 (18/3/2011) e Lei nº 12.462 (4/8/2011); MP 541 (2/8/2011) e Lei nº 12.545 (14/12/2011)", "2011-12-14",
  B+"l12545.html", ("man", M12, [B+"l10683-original.html", B+"l10869.html", B+"l11958.html", B+"l12545.html", B+"mpv-0541.html"], B+"l12545.html", r"IV - da Ciência, Tecnologia e Inovação", 140),
  [(B+"l12462.html", PAR_12462, "art. 25, par. único (Lei 12.462)", [("A", "Advogado-Geral da União", "Advogado-Geral"), ("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Gabinete de Segurança Institucional da Presidência da República", "Gabinete de Segurança Institucional"),
        ("A", "Controladoria-Geral da União", "Controladoria-Geral"), ("A", "Presidente do Banco Central do Brasil", "Banco Central")]),
   (B+"l12462.html", ART1_12462, "art. 25, par. único, II: 'os titulares das Secretarias da Presidência da República' c/c art. 1º (as 9 Secretarias da lista)", [("A", "Secretaria-Geral da Presidência da República", "Secretaria-Geral"), ("A", "Secretaria de Relações Institucionais", "Relações Institucionais"), ("A", "Secretaria de Comunicação Social", "Comunicação Social"),
        ("A", "Secretaria de Assuntos Estratégicos", "Assuntos Estratégicos"), ("A", "Secretaria de Políticas para as Mulheres", "Mulheres"), ("A", "Secretaria de Direitos Humanos", "Direitos Humanos"),
        ("A", "Secretaria de Políticas de Promoção da Igualdade Racial", "Igualdade Racial"), ("A", "Secretaria de Portos", "Portos"), ("A", "Secretaria de Aviação Civil", "Aviação Civil")])],
  "MP 527 (18/3/2011; Lei 12.462, 4/8/2011): cria a Secretaria de Aviação Civil e reescreve o par. único em incisos, trocando a lista nominal de Chefes por 'os titulares das Secretarias da Presidência da República' (mudança na regra de definição). MP 541 (2/8/2011; Lei 12.545, 14/12/2011): Ministério da Ciência e Tecnologia passa a 'da Ciência, Tecnologia e Inovação'.",
  "Par. único e art. 1º lidos na Lei 12.462. O conjunto das Secretarias é o do art. 1º (excluídos Casa Civil, Gabinete Pessoal e GSI, que não são 'Secretarias').",
  extra_arqs=[B+"mpv-0527.html"])

_A12 = [("A", "Advogado-Geral da União", "Advogado-Geral"), ("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Gabinete de Segurança Institucional da Presidência da República", "Gabinete de Segurança Institucional"),
        ("A", "Controladoria-Geral da União", "Controladoria-Geral"), ("A", "Presidente do Banco Central do Brasil", "Banco Central")]
_S12 = [("A", "Secretaria-Geral da Presidência da República", "Secretaria-Geral"), ("A", "Secretaria de Relações Institucionais", "Relações Institucionais"), ("A", "Secretaria de Comunicação Social", "Comunicação Social"),
        ("A", "Secretaria de Assuntos Estratégicos", "Assuntos Estratégicos"), ("A", "Secretaria de Políticas para as Mulheres", "Mulheres"), ("A", "Secretaria de Direitos Humanos", "Direitos Humanos"),
        ("A", "Secretaria de Políticas de Promoção da Igualdade Racial", "Igualdade Racial"), ("A", "Secretaria de Portos", "Portos"), ("A", "Secretaria de Aviação Civil", "Aviação Civil")]
Y(2013, "Lei nº 10.683/2003, art. 25 e art. 1º, na redação da Lei nº 12.462, de 4/8/2011 (sem alteração em 2012)", "2011-08-04",
  B+"l12462.html", ("man", M12, [B+"l10683-original.html", B+"l10869.html", B+"l11958.html", B+"l12545.html", B+"mpv-0541.html"], B+"l12545.html", r"IV - da Ciência, Tecnologia e Inovação", 140),
  [(B+"l12462.html", PAR_12462, "art. 25, par. único (Lei 12.462)", _A12), (B+"l12462.html", ART1_12462, "art. 25, par. único, II c/c art. 1º", _S12)],
  "Nenhuma alteração de lista ou de Secretarias com status entre 14/12/2011 e 1/1/2013. A MP 595 (6/12/2012), dos portos, mexe nas competências da Secretaria de Portos (já em A) e foi convertida na Lei 12.815 (5/6/2013).",
  "Mesmos textos do ano anterior. Varredura das anotações do compilado: sem outra redação do art. 1º ou do art. 25 no período.",
  extra_arqs=[B+"mpv-0595.html", B+"l12815.html"])

Y(2014, "Lei nº 10.683/2003, art. 1º e art. 25, na redação da Lei nº 12.792, de 28/3/2013 (Secretaria da Micro e Pequena Empresa)", "2013-03-28",
  B+"l12792.html", ("man", M12, [B+"l10683-original.html", B+"l10869.html", B+"l11958.html", B+"l12545.html", B+"mpv-0541.html"], B+"l12545.html", r"IV - da Ciência, Tecnologia e Inovação", 140),
  [(B+"l12462.html", PAR_12462, "art. 25, par. único (Lei 12.462)", _A12), (B+"l12462.html", ART1_12462, "art. 25, par. único, II c/c art. 1º", _S12),
   (B+"l12792.html", r"XIII - pela Secretaria da Micro e Pequena Empresa", "art. 1º, XIII (Lei 12.792; ementa: 'cargo de Ministro de Estado')", [("A", "Secretaria da Micro e Pequena Empresa", "Micro e Pequena Empresa")])],
  "Lei 12.792 (28/3/2013) cria a Secretaria da Micro e Pequena Empresa (inciso XIII do art. 1º), inclusa em 'titulares das Secretarias da Presidência' (A).",
  "Lei 12.792 lida (art. 1º e ementa).", extra_arqs=[])

Y(2015, "Lei nº 10.683/2003, art. 1º e art. 25, na redação da Lei nº 12.792, de 28/3/2013 (sem alteração em 2014)", "2013-03-28",
  B+"l12792.html", ("man", M12, [B+"l10683-original.html", B+"l10869.html", B+"l11958.html", B+"l12545.html", B+"mpv-0541.html"], B+"l12545.html", r"IV - da Ciência, Tecnologia e Inovação", 140),
  [(B+"l12462.html", PAR_12462, "art. 25, par. único (Lei 12.462)", _A12), (B+"l12462.html", ART1_12462, "art. 25, par. único, II c/c art. 1º", _S12),
   (B+"l12792.html", r"XIII - pela Secretaria da Micro e Pequena Empresa", "art. 1º, XIII (Lei 12.792)", [("A", "Secretaria da Micro e Pequena Empresa", "Micro e Pequena Empresa")])],
  "Nenhuma alteração de lista ou de Secretarias entre 1/1/2014 e 1/1/2015 nas anotações do compilado.",
  "Varredura das anotações do compilado.")

Y(2016, "Lei nº 10.683/2003, art. 1º e art. 25, na redação da Medida Provisória nº 696, de 2/10/2015 (DOU extra de 5/10/2015; reforma administrativa)", "2015-10-02",
  B+"mpv-0696.html", ("man", M16, [B+"l10683-original.html", B+"l10869.html", B+"l11958.html", B+"l12545.html", B+"mpv-0541.html", B+"mpv-0696.html"], B+"mpv-0696.html", r"Art\. 25\. [. ]+XXI - do Trabalho e Previdência Social; \.+ XXV - das Mulheres, da Igualdade Racial e dos Direitos Humanos\.", 260),
  [(B+"l12462.html", PAR_12462, "art. 25, par. único (Lei 12.462); inciso V (GSI) revogado pela MP 696, art. 8º, XV", [("A", "Advogado-Geral da União", "Advogado-Geral"), ("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Controladoria-Geral da União", "Controladoria-Geral"), ("A", "Presidente do Banco Central do Brasil", "Banco Central")]),
   (B+"mpv-0696.html", r"Art\. 8º Ficam revogados os seguintes dispositivos da Lei nº 10\.683, de 28 de maio de 2003 : I - os incisos III , VII a X e XIII do caput do art\. 1º ;", "MP 696, art. 8º, I: revoga as Secretarias de Relações Institucionais, Assuntos Estratégicos, Mulheres, Direitos Humanos, Igualdade Racial e Micro e Pequena Empresa; permanecem Governo (ex-Secretaria-Geral), Comunicação Social, Portos e Aviação Civil", []),
   (B+"l12462.html", ART1_12462, "art. 1º da Lei 12.462 (Secretarias que permanecem: Secretaria-Geral/Governo, Comunicação Social, Portos, Aviação Civil)", [("A", "Secretaria de Governo da Presidência da República (ex-Secretaria-Geral)", "Secretaria-Geral"), ("A", "Secretaria de Comunicação Social", "Comunicação Social"), ("A", "Secretaria de Portos", "Portos"), ("A", "Secretaria de Aviação Civil", "Aviação Civil")]),
   (B+"mpv-0696.html", r"II - pela Secretaria de Governo da Presidência da República", "MP 696, art. 2º (art. 1º, II): Secretaria-Geral vira Secretaria de Governo; art. 3º, II transforma o cargo de Ministro Chefe da Secretaria-Geral", [])],
  "MP 696 (2/10/2015): extingue os Ministérios da Previdência Social e da Pesca e Aquicultura, transforma Trabalho e Emprego em 'Trabalho e Previdência Social', cria 'Mulheres, Igualdade Racial e Direitos Humanos', extingue as Secretarias de Relações Institucionais, Assuntos Estratégicos, Mulheres, Direitos Humanos, Igualdade Racial e Micro e Pequena Empresa e o Ministro Chefe do GSI (a Casa Militar assume). Convertida na Lei 13.266 (5/4/2016).",
  "Lista = lista de 2015 menos incisos revogados (XVIII, XXIV) com os incisos XXI e XXV da MP 696. Par. único: Lei 12.462 menos o inciso V (GSI). Efeitos sobre estruturas dependem de decretos de estrutura regimental (art. 9º, não verificados).",
  extra_arqs=[B+"l13266.html"])

Y(2017, "Lei nº 10.683/2003, art. 25, na redação das Leis nº 13.341 (29/9/2016; conversão da MP 726 de 12/5/2016) e nº 13.345 (10/10/2016; conversão da MP 728 de 23/5/2016)", "2016-10-10",
  B+"l13341.html", ("man", M17, [B+"l13341.html", B+"l10683-original.html"], B+"l13341.html", r"Art\. 25\. [. ]+II - da Ciência, Tecnologia, Inovações e Comunicações; III - da Defesa; IV - da Cultura; V - da Fazenda;", 330),
  [(B+"l13341.html", r"Parágrafo único\. [. ]+II - o Chefe da Secretaria de Governo da Presidência da República; III - o Advogado-Geral da União, até que seja aprovada emenda constitucional.{0,400}VII - o Presidente do Banco Central do Brasil.{0,300}VIII - o Chefe do Gabinete de Segurança Institucional da Presidência da República", "art. 25, par. único (Lei 13.341; incisos I, IV, V, VI não reproduzidos no ato: I titulares dos Ministérios e IV Casa Civil mantidos pela Lei 12.462, V e VI revogados)", [("A", "Secretaria de Governo da Presidência da República", "Secretaria de Governo"), ("A", "Advogado-Geral da União", "Advogado-Geral"), ("A", "Presidente do Banco Central do Brasil", "Banco Central"), ("A", "Gabinete de Segurança Institucional da Presidência da República", "Gabinete de Segurança Institucional")]),
   (B+"l12462.html", r"IV - o Chefe da Casa Civil da Presidência da República", "art. 25, par. único, IV (Lei 12.462; mantido)", [("A", "Casa Civil da Presidência da República", "Casa Civil")])],
  "MP 726 (12/5/2016; Lei 13.341, 29/9/2016): Temer reduz os Ministérios (Comunicações+Ciência e Tecnologia; Cultura+Educação, depois separadas; Desenvolvimento Agrário+Social; Transportes+Portos+Aviação Civil; Controladoria-Geral da União vira Ministério da Transparência...), extingue as Secretarias de Portos, Aviação Civil, Comunicação Social e o Ministro Chefe da CGU como cargo separado e restitui o GSI ao par. único. MP 728 (23/5/2016; Lei 13.345, 10/10/2016) recria o Ministério da Cultura e o da Educação. MP 717 (16/3/2016), que criava o Ministro Chefe do Gabinete Pessoal, foi revogada pela MP 726.",
  "Lista: itens do art. 25 reescritos pela Lei 13.341, mais I (Agricultura, não alterado) e XXVI (Educação, Lei 13.341/13.345). Par. único: Lei 13.341 (incisos II, III, VII, VIII) + inciso IV (Casa Civil, Lei 12.462). Efeitos sobre estruturas dependem de decretos (art. 19, I, não verificados). A MP 768 (2/2/2017) é posterior a 1/1/2017.",
  extra_arqs=[B+"mpv-0726.html", B+"l13345.html", B+"mpv-0728.html", B+"mpv-0717.html"])

Y(2018, "Lei nº 13.502, de 1º/11/2017 (conversão da MP 782, de 31/5/2017), art. 21 e art. 22", "2017-11-01",
  "bruto/l13502-compilada.html", ("man", M18, ["bruto/l13502-compilada.html"], "bruto/l13502-compilada.html", r"Art\. 21\. Os Ministérios são os seguintes: I - da Agricultura, Pecuária e Abastecimento; II - das Cidades;", 220),
  [("bruto/l13502-compilada.html", r"Art\. 22\. São Ministros de Estado: I - os titulares dos Ministérios; II - o Chefe da Casa Civil da Presidência da República; III - o Chefe da Secretaria de Governo da Presidência da República; IV - o Chefe do Gabinete de Segurança Institucional da Presidência da República; V - o Chefe da Secretaria-Geral da Presidência da República; VI - o Advogado-Geral da União.{0,200}VII - o Presidente do Banco Central do Brasil", "art. 22", [("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Secretaria de Governo da Presidência da República", "Secretaria de Governo"), ("A", "Gabinete de Segurança Institucional da Presidência da República", "Gabinete de Segurança Institucional"),
        ("A", "Secretaria-Geral da Presidência da República", "Secretaria-Geral"), ("A", "Advogado-Geral da União", "Advogado-Geral"), ("A", "Presidente do Banco Central do Brasil", "Banco Central")])],
  "A Lei 13.502 (1/11/2017) revoga a Lei 10.683 e a MP 768 e passa a ser a lei de organização. MP 768 (2/2/2017) tinha criado o Ministro Chefe da Secretaria-Geral e o dos Direitos Humanos; MP 782 (31/5/2017) foi a conversão. Alterações do art. 21 por MP 821 (2018, Ministério Extraordinário da Segurança Pública) e Lei 13.690 (2018) são posteriores a 1/1/2018.",
  "Lista: itens I a XXII do art. 21 (redação original, sem anotação no compilado). Art. 22 lido no compilado (sem anotação, redação original).",
  extra_arqs=[B+"mpv-0768.html", B+"mpv-0782.html"])

Y(2019, "Medida Provisória nº 870, de 1º/1/2019 (DOU de 1.1.2019), art. 19 e art. 20", "2019-01-01",
  B+"mpv-0870.html", ("auto", B+"mpv-0870.html", r"Art\. 19\. Os Ministérios são os seguintes:", r"Ministros de Estado Art\. 20"),
  [(B+"mpv-0870.html", r"Art\. 20\. São Ministros de Estado: I - os titulares dos Ministérios; II - o Chefe da Casa Civil da Presidência da República; III - o Chefe da Secretaria de Governo da Presidência da República; IV - o Chefe da Secretaria-Geral da Presidência da República; V - o Chefe do Gabinete de Segurança Institucional da Presidência da República; VI - o Advogado-Geral da União.{0,250}VII - o Presidente do Banco Central do Brasil", "art. 20", [("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Secretaria de Governo da Presidência da República", "Secretaria de Governo"), ("A", "Secretaria-Geral da Presidência da República", "Secretaria-Geral"),
        ("A", "Gabinete de Segurança Institucional da Presidência da República", "Gabinete de Segurança Institucional"), ("A", "Advogado-Geral da União", "Advogado-Geral"), ("A", "Presidente do Banco Central do Brasil", "Banco Central")])],
  "MP 870 (1/1/2019) revoga a Lei 13.502 (que valia em 1/1/2018); alterações da Lei 13.502 durante 2018 (MP 821, Lei 13.690) não chegam a 1/1/2019. Convertida na Lei 13.844 (18/6/2019). A Controladoria-Geral da União passa a constar da lista de Ministérios (item XVI).",
  "Lista e art. 20 lidos na MP 870 (entra em vigor na publicação, art. 86). Tem 16 itens, o último 'a Controladoria-Geral da União'.",
  extra_arqs=[B+"mpv-0886.html"])

Y(2020, "Lei nº 13.844, de 18/6/2019 (conversão da MP 870), art. 19 e art. 20", "2019-06-18",
  B+"l13844-texto-com-historico.html", ("man", M20, [B+"l13844-texto-com-historico.html"], B+"l13844-texto-com-historico.html", r"Art\. 19\. Os Ministérios são os seguintes: .{0,200}I - Ministério da Agricultura, Pecuária e Abastecimento; II - Ministério da Cidadania; III - Ministério da Ciência, Tecnologia, Inovações e Comunicações;", 330),
  [(B+"l13844-texto-com-historico.html", r"Art\. 20\. São Ministros de Estado: .{0,200}I - os titulares dos Ministérios; II - o Chefe da Casa Civil da Presidência da República; III - o Chefe da Secretaria de Governo da Presidência da República; IV - o Chefe da Secretaria-Geral da Presidência da República; V - o Chefe do Gabinete de Segurança Institucional da Presidência da República; VI - o Advogado-Geral da União.{0,250}VII - o Presidente do Banco Central do Brasil", "art. 20", [("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Secretaria de Governo da Presidência da República", "Secretaria de Governo"), ("A", "Secretaria-Geral da Presidência da República", "Secretaria-Geral"),
        ("A", "Gabinete de Segurança Institucional da Presidência da República", "Gabinete de Segurança Institucional"), ("A", "Advogado-Geral da União", "Advogado-Geral"), ("A", "Presidente do Banco Central do Brasil", "Banco Central")])],
  "MP 870 convertida na Lei 13.844 (18/6/2019). MP 886 (18/6/2019; Lei 13.901, 11/11/2019) mexe em competências, não na lista nem no art. 20.",
  "Lista: itens I a XVI do art. 19 (redação original, sem anotação). Art. 20 original no compilado.",
  extra_arqs=[B+"l13901.html"])

Y(2021, "Lei nº 13.844/2019, art. 19 e art. 20, na redação da Lei nº 14.074, de 14/10/2020 (conversão da MP 980, de 10/6/2020)", "2020-10-14",
  B+"l14074.html", ("man", M21, [B+"l13844-texto-com-historico.html", B+"l14074.html"], B+"l13844-texto-com-historico.html", r"III - Ministério da Ciência, Tecnologia e Inovações; \(Redação dada pela Lei nº 14\.074, de 2020\) III-A - Ministério das Comunicações;", 250),
  [(B+"l13844-texto-com-historico.html", r"Art\. 20\. São Ministros de Estado: .{0,200}I - os titulares dos Ministérios; II - o Chefe da Casa Civil da Presidência da República; III - o Chefe da Secretaria de Governo da Presidência da República; IV - o Chefe da Secretaria-Geral da Presidência da República; V - o Chefe do Gabinete de Segurança Institucional da Presidência da República; VI - o Advogado-Geral da União.{0,250}VII - o Presidente do Banco Central do Brasil", "art. 20", [("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Secretaria de Governo da Presidência da República", "Secretaria de Governo"), ("A", "Secretaria-Geral da Presidência da República", "Secretaria-Geral"),
        ("A", "Gabinete de Segurança Institucional da Presidência da República", "Gabinete de Segurança Institucional"), ("A", "Advogado-Geral da União", "Advogado-Geral"), ("A", "Presidente do Banco Central do Brasil", "Banco Central")])],
  "MP 980 (10/6/2020; Lei 14.074, 14/10/2020) divide o Ministério da Ciência, Tecnologia, Inovações e Comunicações em Ministério da Ciência, Tecnologia e Inovações (III) e Ministério das Comunicações (III-A).",
  "Lei 14.074 e compilado da Lei 13.844 lidos.", extra_arqs=[B+"mpv-0980.html"])

Y(2022, "Lei nº 13.844/2019, art. 19 e art. 20, na redação da Lei nº 14.261, de 16/12/2021 (conversão da MP 1.058, de 27/7/2021) e da LC nº 179, de 24/2/2021", "2021-12-16",
  B+"l14261.html", ("man", M22, [B+"l13844-texto-com-historico.html", B+"l14261.html"], B+"l13844-texto-com-historico.html", r"XIV-A - Ministério do Trabalho e Previdência; \(Incluído pela Medida Provisória nº 1\.058, de 2021\)", 110),
  [(B+"l13844-texto-com-historico.html", r"Art\. 20\. São Ministros de Estado: .{0,200}I - os titulares dos Ministérios; II - o Chefe da Casa Civil da Presidência da República; III - o Chefe da Secretaria de Governo da Presidência da República; IV - o Chefe da Secretaria-Geral da Presidência da República; V - o Chefe do Gabinete de Segurança Institucional da Presidência da República; VI - o Advogado-Geral da União", "art. 20, incisos I a VI (inciso VII, Presidente do Banco Central, revogado pela LC 179/2021, art. 13, I)", [("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Secretaria de Governo da Presidência da República", "Secretaria de Governo"), ("A", "Secretaria-Geral da Presidência da República", "Secretaria-Geral"),
        ("A", "Gabinete de Segurança Institucional da Presidência da República", "Gabinete de Segurança Institucional"), ("A", "Advogado-Geral da União", "Advogado-Geral")]),
   (B+"lc179.html", r"Art\. 13\. Ficam revogados: I - o inciso VII do caput do art\. 20 da Lei nº 13\.844, de 18 de junho de 2019", "LC 179, art. 13, I (DOU 25.2.2021): revoga o inciso VII (Presidente do Banco Central)", [])],
  "LC 179 (24/2/2021; DOU 25/2/2021) revoga o inciso VII do art. 20 (Presidente do Banco Central deixa de ser Ministro de Estado). MP 1.058 (27/7/2021; Lei 14.261, 16/12/2021) recria o Ministério do Trabalho e Previdência (item XIV-A, depois XVII).",
  "Lista: 17 itens de 2021 + Ministério do Trabalho e Previdência (Lei 14.261). Art. 20 lido no compilado com a revogação anotada.",
  extra_arqs=[B+"mpv-1058.html"])

Y(2023, "Medida Provisória nº 1.154, de 1º/1/2023 (DOU de 1.1.2023), art. 17 e art. 18; revoga a Lei 13.844/2019", "2023-01-01",
  B+"mpv-1154-2023.html", ("auto", B+"mpv-1154-2023.html", r"Art\. 17\. Os Ministérios são os seguintes:", r"Art\. 18\. São Ministros"),
  [(B+"mpv-1154-2023.html", r"Art\. 18\. São Ministros de Estado: I - os titulares dos Ministérios; II - o titular da Casa Civil da Presidência da República; III - o titular da Secretaria-Geral da Presidência da República; IV - o titular da Secretaria de Relações Institucionais da Presidência da República; V - o titular da Secretaria de Comunicação Social da Presidência da República; VI - o Chefe do Gabinete de Segurança Institucional da Presidência da República; e VII - o Advogado-Geral da União", "art. 18", [("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Secretaria-Geral da Presidência da República", "Secretaria-Geral"), ("A", "Secretaria de Relações Institucionais da Presidência da República", "Relações Institucionais"),
        ("A", "Secretaria de Comunicação Social da Presidência da República", "Comunicação Social"), ("A", "Gabinete de Segurança Institucional da Presidência da República", "Gabinete de Segurança Institucional"), ("A", "Advogado-Geral da União", "Advogado-Geral")])],
  "MP 1.154 (1/1/2023) revoga a Lei 13.844 e amplia de 18 para 31 itens a lista (Ministérios novos: Cultura, Cidades, Comunicações separados etc. — ver diferença de lista abaixo). Convertida na Lei 14.600 (19/6/2023). Inclui a Controladoria-Geral da União como item XXXI da lista.",
  "Lista e art. 18 lidos na MP 1.154 (art. 73: vigência na publicação).",
  extra_arqs=[B+"l14600-compilado.html"])

_A24 = [("A", "Casa Civil da Presidência da República", "Casa Civil"), ("A", "Secretaria-Geral da Presidência da República", "Secretaria-Geral"), ("A", "Secretaria de Relações Institucionais da Presidência da República", "Relações Institucionais"),
        ("A", "Secretaria de Comunicação Social da Presidência da República", "Comunicação Social"), ("A", "Gabinete de Segurança Institucional da Presidência da República", "Gabinete de Segurança Institucional"), ("A", "Advogado-Geral da União", "Advogado-Geral")]
_PAR24 = r"Art\. 18\. São Ministros de Estado: I - os titulares dos Ministérios; II - o titular da Casa Civil da Presidência da República; III - o titular da Secretaria-Geral da Presidência da República; IV - o titular da Secretaria de Relações Institucionais da Presidência da República; V - o titular da Secretaria de Comunicação Social da Presidência da República; VI - o Chefe do Gabinete de Segurança Institucional da Presidência da República; e VII - o Advogado-Geral da União"
M24 = None  # preenchido por gerar.py: lista da Lei 14.600 art. 17 (32 itens, com XII-A)
Y(2024, "Lei nº 14.600, de 19/6/2023, art. 17 e art. 18, com o inciso XII-A da MP 1.187 (13/9/2023; Lei 14.816, 16/1/2024)", "2023-09-13",
  B+"l14600-compilado.html", ("auto", B+"l14600-compilado.html", r"Art\. 17\. Os Ministérios são os seguintes:", r"Art\. 18\. São Ministros"),
  [(B+"l14600-compilado.html", _PAR24, "art. 18", _A24)],
  "Lei 14.600 (19/6/2023) converte a MP 1.154 sem mudar a lista de 31 itens; MP 1.187 (13/9/2023, em vigor na publicação; Lei 14.816, 16/1/2024) cria o Ministério do Empreendedorismo, da Microempresa e da Empresa de Pequeno Porte (item XII-A), por desmembramento do Ministério do Desenvolvimento, Indústria, Comércio e Serviços.",
  "Lista lida no compilado da Lei 14.600 (versão do Planalto baixada em 20/10/2026), item XII-A anotado como incluído pela MP 1.187/2023 e pela Lei 14.816/2024. Art. 18 sem anotações de alteração.",
  extra_arqs=[B+"mpv-1187-2023.html", B+"l14816.html"])

Y(2025, "Lei nº 14.600/2023, art. 17 e art. 18, na redação da Lei nº 14.816, de 16/1/2024 (sem alteração em 2024)", "2024-01-16",
  B+"l14600-compilado.html", ("auto", B+"l14600-compilado.html", r"Art\. 17\. Os Ministérios são os seguintes:", r"Art\. 18\. São Ministros"),
  [(B+"l14600-compilado.html", _PAR24, "art. 18", _A24)],
  "Nenhuma alteração do art. 17 ou do art. 18 em 2024 nas anotações do compilado (a Lei 14.875/2024 e a MP 1.317/2025 aparecem no compilado em outros dispositivos).",
  "Compilado do Planalto baixado em 20/10/2026; busca por anotações de 2024-2026 no art. 17/18: ver varredura_anotacoes.")

Y(2026, "Lei nº 14.600/2023, art. 17 e art. 18, na redação da Lei nº 14.816, de 16/1/2024 (sem alteração em 2025)", "2024-01-16",
  B+"l14600-compilado.html", ("auto", B+"l14600-compilado.html", r"Art\. 17\. Os Ministérios são os seguintes:", r"Art\. 18\. São Ministros"),
  [(B+"l14600-compilado.html", _PAR24, "art. 18", _A24)],
  "Nenhuma alteração do art. 17 ou do art. 18 em 2025 nas anotações do compilado (que já inclui a Lei 15.352, de 25/2/2026, em outro dispositivo).",
  "Compilado do Planalto baixado em 20/10/2026. Atos de 2025 posteriores à atualização do compilado, se existirem, não estariam refletidos.",
  nv="Lag possível do texto compilado do Planalto em relação a atos de 2025; não houve busca no DOU.")
