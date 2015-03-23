#!/usr/bin/env python
import re
import subprocess
subprocess.Popen(
    ["grep -r -n '\.format(' |grep 'logger\.' | awk '{print $1}' > /tmp/bug"],
    shell=True)

f = open("/tmp/bug") 
foo = f.readlines()
tot = len(foo)
f.close()
bla = [ (i.split(":")[0], int(i.split(":")[1]))  for i in foo]
c = 0
log = {}
for file, num in bla:
    op = open(file)
    data = op.readlines()
    op.close()
    
    num -= 1
    oline = data[num].strip()
    try:
        reg = "bG9nZ2VyLiguKilcKFsnIl0oLiopWyInXS5mb3JtYXRcKCguKilcKVwp".decode('base64')
        match = re.match(reg, oline)    
        alph = match.group(1)
        beta = match.group(2)
        gama = match.group(3)
        assert((oline.count('\'') + oline.count('"')) < 3)
        assert(match.lastindex < 4)
        list = gama.split(", ")
        for i,j in enumerate(list):
            beta = beta.replace("{%d}"%i, "%s")
        assert("{i+1}" not in beta)
        gama = ", ".join(list)
        nline = "logger.%s('%s', %s)" % (alph, beta, gama)
        print nline
        op = open(file, "w")
        data[num] = data[num].replace(oline, nline)
        op.writelines(data)
        op.close()
        c+=1
    except:
        if file not in log:
            log[file]=[num+1]
        else:
            log[file].append(num+1)
print "%d%% Success" % (c * 100.0 / tot)
print "\n%d lines corrected :) %d need manual work :(" % (c, tot-c)
print "-log-"
for i in log:
    print "File %s line number %r" % (i, log[i])
