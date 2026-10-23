import sys, urllib.parse, urllib.request, re
def post(defpath, linha, coluna, incr, arquivos, extra=None, formato='prn'):
    pairs=[('Linha',linha),('Coluna',coluna),('Incremento',incr)]
    for a in arquivos: pairs.append(('Arquivos',a))
    for k,v in (extra or []): pairs.append((k,v))
    pairs += [('pesqmes1','Digite o texto e ache fácil')]
    pairs += [('formato',formato),('mostre','Mostra')]
    body='&'.join(urllib.parse.quote(k,encoding='latin1',safe='')+'='+urllib.parse.quote(v,encoding='latin1',safe='') for k,v in pairs).encode()
    req=urllib.request.Request('http://tabnet.datasus.gov.br/cgi/tabcgi.exe?'+defpath,data=body,headers={'User-Agent':'Mozilla/5.0','Content-Type':'application/x-www-form-urlencoded'})
    return urllib.request.urlopen(req,timeout=120).read()
if __name__=='__main__':
    yrs=[f'obtbr{y%100:02d}.dbf' for y in range(1996,2025)]
    out=post('sim/cnv/obt10br.def','Capítulo_CID-10','Ano_do_Óbito','Óbitos_p/Residênc',yrs)
    open('t1.out','wb').write(out); print(len(out)); print(out.decode('latin1')[:3000])
