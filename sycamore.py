#Sycamore is annotation software written by Tyler Kniess in 2023 for the
#Indiana Parsed Corpus of Historical High German. Sycamore is based on Annotald
#(Anton Karl Ingason, Jana E. Beck, Aaron Ecay) and Annotald X (Anton Karl Ingason). 

"""
sycamore.py
Created 2023/January/10
@author: Tyler Kniess
@copyright: GNU General Public License, v. 3 or (at your option) any later
version.  http://www.gnu.org/licenses/ This program is distributed in the hope
that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
Lesser General Public License for more details.
@contact: tyler.kniess@gmail.com
"""

#Prerequisites
#Before running this script, nltk and cherrypy must be installed using pip
import os.path
import platform
import re
import sys
import cherrypy
from datetime import datetime #for timestamps
from nltk import Tree

class TreeDraw(object):

    def __init__(self):
        self.filename = None
        if platform.system() == 'Windows':
            self.init_windows()

    def shutdown(self):
        cherrypy.engine.exit()

    def on_quit_callback(self, systray):
        self.shutdown()

    def load_browser(self, stuff):
        root.filename = filedialog.askopenfilename(title='Select file',filetypes=(('psd files','*.psd'),))
        self.filename = root.filename
        os.startfile('http://localhost:8080')

    def init_windows(self):
        # print('I am on Windows!')
        from infi.systray import SysTrayIcon
        menu_options = (("Open file ...", None, self.load_browser),)
        # menu_options = ()
        self.systray = SysTrayIcon('tre.ico','Annotald', menu_options, on_quit=self.on_quit_callback)
        self.systray.start()

    def pretty_tree(self, tree):
        t = Tree.fromstring(tree)
        s = t.pformat()
        if s.startswith('(\n'):
            s='(' + str(s[2:])
        return s

    def pretty_trees(self, trees):
        trees = trees.replace('\n','')
        treelist = re.sub(r'\)\s*\)\(\s*\(','))\n((',trees)
        treelist = treelist.split('\n')
        treelist = [self.pretty_tree(t) for t in treelist]
        return '\n\n'.join(treelist)

    @cherrypy.expose
    def doSave(self, trees=None):
        #for later implementation: add in timestamp to filenames
#        rightnow = datetime.now()
#        rightnow_string = rightnow.strftime("%Y.%m.%d.%H.%M.%S")
        with open(self.filename,'w',encoding='utf-8') as f:
            tosave = trees.strip()#[1:-1]
            tosave = self.pretty_trees(tosave)
            # f.write(tosave.encode("utf8"))
            f.write(tosave)
            f.close()
            #os.system('java -classpath ~/icecorpus/parsing/CS_Tony_oct19.jar csearch.CorpusSearch ~/icecorpus/treedrawing/nothing.q '+self.thefile)
            #os.system('mv '+self.thefile+'.out '+self.thefile)


    @cherrypy.expose
    def doExit(self):
        print ("Exit message received")
        #os._exit(0)
        cherrypy.engine.exit()


    def loadPsd(self, fileName):
        self.thefile = fileName
        with open(fileName, encoding='utf-8') as f:
            currentText = f.read()
        allchars = 'a-zA-Z0-9þæðöÞÆÐÖáéýúíóÁÉÝÚÍÓćĺŕśźĆĹŔŚŹäëïüÿÄËÏÜŸâîôûÂÎÔÛãñõÃÑÕàèìòùÀÈÌÒÙçÇģĢķĶņŅşŞţŢłŁđĐăĂğĞąęįǫųĄĘĮǪŲœŒďěčňšťžĎĚČŇŠŽāēīōūĀĒĪŌŪűŰßżŻİı„“”¿¡¢£¥©®\*\"\,\.\?\!\:$\+\-\{\}\_\<\>\/\&\;'
        currentText = currentText.replace("<","&lt;")
        currentText = currentText.replace(">","&gt;")
        trees = currentText.split("\n\n")	

        alltrees = '<div class="snode">'
        for tree in trees:
            tree0 = tree.strip()
            tree0 = re.sub('^\(','',tree0)
            tree0 = re.sub('\)$','',tree0).strip()
            tree0 = re.sub('\((['+allchars+']+) (['+allchars+']+)\)','<div class="snode">\\1<span class="wnode">\\2</span></div>',tree0)
            tree0 = re.sub('\(','<div class="snode">',tree0)
            tree0 = re.sub('\)','</div>',tree0)		
            tree0 = tree0.replace('\n','')
            alltrees = alltrees + tree0

        alltrees = alltrees + '</div>'
        return alltrees

    @cherrypy.expose
    def error(self):
        return("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> 
<html>
<head>  <title>Annotald X</title>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <style type='text/css'>
       body, input {
           font-family: verdana;
       }
    </style>
</head>  
<body>

<div style='text-align:center;font-weight:bold;'>Annotald Error. Please load a file.</div>


</body>
""")


    @cherrypy.expose
    def index(self):

        if len(sys.argv) == 2:
            self.filename = sys.argv[1]

        if not self.filename:
            raise cherrypy.HTTPRedirect('/error')
        #else:
        #    self.filename = filename

        if True: # len(sys.argv)==2:
            currentSettings = open( "./settings.js", encoding='utf-8').read()
            # filename = sys.argv[1]
            currentTree=self.loadPsd(self.filename)                
        else:
            print("Usage: annotald [settingsFile.js] file.psd")
        
        return """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> 
<html>
<head>  <title>Sycamore Beta</title>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <link rel="stylesheet" type="text/css" href="/static/css/treedrawing.css" type="text/css"></link>
    <script type= "application/javascript"/>"""+ currentSettings + """    </script>
	<script type= "application/javascript" src="/static/scripts/jquery.js"/></script>		
	<script type= "application/javascript" src="/static/scripts/treedrawing.js"/></script>		
	<script type= "application/javascript" src="/static/scripts/treedrawing.contextMenu.js"/></script>		

</head>
<body oncontextmenu="return false;">
<div style="display:none"><span>Sel1: </span><span id="labsel1">null</span></div>
<div style="display:none"><span>Sel2: </span><span id="labsel2">null</span></div>

<br />

<div id="floatMenu">
<div style="background-color: #2E2E2E; color: white; font-weight: bold;">Sycamore Beta</div>

Editing: """+os.path.basename(self.thefile)+""" <br />
<input class="menubutton" type="button" value="Save" id="butsave"><br />
<input class="menubutton" type="button" value="Undo" id="butundo"><br />
<input class="menubutton" type="button" value="Redo" id="butredo"><br />
<input class="menubutton" type="button" value="Exit" id="butclose"><br />

<div id="debugpane">x</div>
</div>
<div id="editpane">"""+currentTree+"""</div>


		<div id="conMenu">		
		  <div id="conLeft" class="conMenuColumn">			
			<div class="conMenuItem"><a href="#edit">IP-SUB</a></div>
			<div class="conMenuItem"><a href="#cut">IP-INF</a></div>
			<div class="conMenuItem"><a href="#copy">IP-SMC</a></div>
			<div class="conMenuItem"><a href="#paste">-SPE</a></div>
			<div class="conMenuItem"><a href="#delete">-PRN</a></div>
			<div class="conMenuItem"><a href="#quit">-XXX</a></div>
 		  </div>

		  <div id="conRight" class="conMenuColumn">			
			<div class="conMenuItem"><a href="#edit">XXX</a></div>
			<div class="conMenuItem"><a href="#cut">XXX</a></div>
 		  </div>
 		  
          <div id="conRightest" class="conMenuColumn">            
            <div class="conMenuItem"><a href="#edit">XXX</a></div>
            <div class="conMenuItem"><a href="#cut">XXX</a></div>
           </div> 		  
		</div>

</body>
</html>"""




if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir' : './public',
        },
        'global': {
            'engine.autoreload.on' : False
            #'environment' : 'production'
        }
    }

    cherrypy.request.headers["Accept-Charset"] = "UTF-8"
    cherrypy.quickstart(TreeDraw(), '/', conf)
