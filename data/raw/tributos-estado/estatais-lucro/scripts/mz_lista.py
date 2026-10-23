"""lê catálogo MZ (bruto) e imprime 'destino<TAB>url' para anos pedidos. Sem rede.
uso: mz_lista.py <catalogo.json> <prefixo-destino> <ano_ini> <ano_fim> [so_q4] [excluir_texto]"""
import json,sys,re,unicodedata
f,pref,a,b=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
q4=len(sys.argv)>5 and sys.argv[5]=='q4'
exc=sys.argv[6] if len(sys.argv)>6 else None
m=json.load(open(f))['data']['document_metas']
for x in sorted(m,key=lambda x:(x['file_year'],x['file_quarter'],x['file_name_original'])):
    if not(a<=x['file_year']<=b): continue
    if q4 and x['file_quarter']!=4: continue
    if exc and exc in x['file_name_original']: continue
    import os
    if (int(x['file_size'] or 0)==0 and not os.environ.get('INCLUIR_ZERO')) or int(x['file_size'])>25*1024*1024:
        print('#PULADO',x['file_name_original'],x['file_size'],file=sys.stderr); continue
    n=unicodedata.normalize('NFKD',x['file_name_original']).encode('ascii','ignore').decode()
    n=re.sub(r'[^A-Za-z0-9]+','-',n).strip('-')
    print(f"bruto/{pref}-{x['file_year']}T{x['file_quarter']}-{n}.pdf\t{x['file_url']}")
