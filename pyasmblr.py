from requests import get,utils
from requests import status_codes
from bs4 import BeautifulSoup
import requests
import sys
uencode=utils.quote
list_arch={
'arm':'arm'
,'armthumb':'arm-t'
,'arm64':'arm64'
,'mips32':'mips32'
,'mips64':'mips64'
,'ppc32':'ppc32'
,'ppc64':'ppc64'
,'sparc':'sparc'
,'intel16':'x86-16'
,'intel32':'x86-32'
,'intel64':'x86-64'
}
url="http://shell-storm.org/online/Online-Assembler-and-Disassembler/"
url+="?inst=%s&arch=%s&as_format=inline"
ua=None
if 'win' in sys.platform:
	ua='Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
else:
	ua='Mozilla/5.0 (X11; U; Linux x86_64; rv:1.9.2.3) Gecko/20100403 Firefox/54.0'
hdr={
'Host':'shell-storm.org'
,'Accept-Language':'en-US,en;q=0.5'
,'Accept-Encoding':'gzip,deflate'
,'Referer':'http://shell-storm.org/online/Online-Assembler-and-Disassembler/'
,'Upgrade-Insecure-Requests':'1'
,'Connection':'close'
,'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
,'User-Agent':ua
}
try:
	raw_input
except:
	raw_input=input
def exec_asm_command(cmnd,arh):
	u=url%(uencode(cmnd),arh)
	try:
		r=requests.get(u,headers=hdr)
	except Exception as e:
		print ('Error : %s'%(e))
		sys.exit()
	else:
		if r.status_code==200:
			hp=BeautifulSoup(r.text,'html.parser')
			src=hp.find_all('pre')[0].text[1:-1]
			if 'valid instruc' in src:
				return 'Invalid Instruction'
			return src
		else:
			return status_codes._codes[r.status_code]
def help_banner():
	print ("""
+--------------------------------------------------------+
| Usage :                                                |
|        pyasmblr -h        => Show This Message         |
|        pyasmblr -f [FILE] => InPut File                |
|        pyasmblr -o [FILE] => OutPut File               |
|        pyasmblr -i        => Interactive Shell         |
|        pyasmblr -l        => List Support Arch         |
|        pyasmblr -a        => Set Arch(def intel32)     |
|                                                        |
| example :                                              |
|        pyasmblr -f file_inp.asm -o file_out.raw -a arm |
|        pyasmblr -i                                     |
+--------------------------------------------------------+
""")
def help_incom():
	print ("""
archl        => list support arch
archc        => current arch
archs [ARCH] => set arch
quit         => ...
""")
def show_arch_list():
	print ('+-=[ Arch ]=-+\n')
	for i in list_arch:
		print (i)
def shelli():
	def_arch='intel32'
	while True:
		command=raw_input('>>> ')
		if command.split()[0] in ['archl','archc','archs','help','quit']:
			if command=='archl':
				show_arch_list()
			if command=='archc':
				print (def_arch)
			if command.startswith('archs'):
				def_arch=command.split(' ')[1]
			if command=='quit':
				sys.exit()
			if command=='help':
				help_incom()
		else:
			print (exec_asm_command(command,list_arch[def_arch]))
def corform(oc):
	nw=oc.split('\\x')
	del nw[0]
	out=''
	for i in nw:
		out+=chr(int(i,16))
	return out
asm=lambda cmd,ah='intel32':corform(exec_asm_command(cmd,list_arch[ah]))
if __name__=='__main__':
	if len(sys.argv)>1:
		if sys.argv[1]=='-h':
			help_banner()
			sys.exit()
		elif sys.argv[1]=='-l':
			show_arch_list()
			sys.exit()
		elif sys.argv[1]=='-i':
			shelli()
		elif ('-f' in sys.argv) and ('-o' in sys.argv) and ('-a' in sys.argv):
			inputfile=sys.argv[sys.argv.index('-f')+1]
			outputfile=sys.argv[sys.argv.index('-o')+1]
			sarch=sys.argv[sys.argv.index('-a')+1].lower()
			srca=open(inputfile,'rb').read()
			res=exec_asm_command(srca,list_arch[sarch])
			f=open(outputfile,'wb')
			f.write(res)
			f.close()
		else:
			print ('Error : Use -h Show Args')
