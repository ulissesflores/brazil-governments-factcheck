"""html -> texto linha a linha (tr vira uma linha, celulas separadas por ' | '). Sem rede."""
import sys, re, html
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.out=[]; s.cell=[]; s.row=None; s.skip=0
    def handle_starttag(s,t,a):
        if t in('script','style'): s.skip+=1
        if t=='tr': s.row=[]
        if t in('td','th'): s.cell=[]
        if t in('p','div','br','h1','h2','h3','h4','li','table') and s.row is None: s.out.append('\n')
    def handle_endtag(s,t):
        if t in('script','style'): s.skip-=1
        if t in('td','th') and s.row is not None:
            c=re.sub(r'\s+',' ',''.join(s.cell)).strip()
            if c: s.row.append(c)
            s.cell=[]
        if t=='tr' and s.row is not None:
            if s.row: s.out.append(' | '.join(s.row)+'\n')
            s.row=None
        if t in('p','div') and s.row is None: s.out.append('\n')
    def handle_data(s,d):
        if s.skip: return
        if s.row is not None: s.cell.append(d)
        else: s.out.append(d)
def conv(src,dst):
    raw=open(src,'rb').read().decode('latin-1')
    if src.endswith('.txt'): txt=raw
    else:
        p=P(); p.feed(raw); txt=''.join(p.out).replace('\xa0',' ')
        txt=re.sub(r'[ \t]+',' ',txt); txt=re.sub(r'\n\s*\n+','\n',txt)
    open(dst,'w').write(txt)
if __name__=='__main__': conv(sys.argv[1],sys.argv[2])
