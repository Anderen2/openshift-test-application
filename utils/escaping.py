#!/usr/bin/python

# BRF (Basefarm Request Funneler)
# Component: Utilities
# Module: Various text escaping utils

#Python modules
import re

def escape_string(data, html_escape=True):
    data = data.replace('\\x', '\\ x')
    data = data.replace('\\', '\\\\')
    # try: dec = data.decode('string_escape').decode('utf-8')
    # except: dec = data.decode('string_escape').decode('iso-8859-1')
    if type(data) != unicode:
        try: 
            data = unicode(data, "utf-8")
        except:
            try: data = unicode(data, "iso-8859-1")
            except: data = unicode(data, "utf-8", errors="replace")

    after = ''
    if html_escape:
        for i in data:
            val = ord(i)
            if val < 0x20 or val > 0x7F: after = after + ('&#x%x;' % val)
            else: after = after + i
        
        return after

    else:
        return data

def escape_tags(data):
    data = data.replace('&lt;','&lt')
    data = data.replace('&gt;','&gt')
    data = data.replace('<','&lt')
    data = data.replace('>','&gt')

    data = data.replace('&ltbr&gt','\n')
    data = data.replace("&#xa;","\n")
    data = re.sub(r"<base\shref(.*)>",'', data)

    return data