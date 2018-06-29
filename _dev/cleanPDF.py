# -*- coding: utf-8 -*-
######     ######     ######     ######     ######
##     / / / /    License    \ \ \ \ 
##  ConTextMe copyleft culture, Copyright (C)
##  is prohibited here. This work is licensed 
##  under a CC BY-SA 4.0,
##  Creative Commons Attribution-ShareAlike 4.0,
##  http://creativecommons.org/licenses/by-sa/4.0
######     ######     ######     ######     ######
##    / / / /    Code Climate    \ \ \ \ 
##    Language = python3
##    Indent = space;    2 chars;
######     ######     ######     ######     ######

def init(args):
  tmpdir = session['tmp_path'] + "/tmp/"
  os.makedirs(tmpdir, exist_ok=True)
  subprocess.Popen(['cp', args.fileLoc, tmpdir]).wait()
  subprocess.Popen(['pdftk', tmpdir + os.path.basename(args.fileLoc), 'output', tmpdir + os.path.basename(args.fileLoc) + '.unc', 'uncompress']).wait()
  subprocess.Popen(["sed -n '/^\/Annots/!p' " + tmpdir + os.path.basename(args.fileLoc) + '.unc > ' + tmpdir + os.path.basename(args.fileLoc) + '.unoannot'], env={'LANG':'C'}, shell=True).wait()
  subprocess.Popen(["pdftk", tmpdir + os.path.basename(args.fileLoc) + ".unoannot", "output", tmpdir + os.path.basename(args.fileLoc), "compress"]).wait()
  subprocess.Popen(["rm " + tmpdir + os.path.basename(args.fileLoc) + ".*"], shell=True).wait()
