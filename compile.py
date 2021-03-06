#!/usr/bin/env python
import json
import os
import io

def custom_listdir(path):
    dirs = sorted([d for d in os.listdir(path) if os.path.isdir(path + os.path.sep + d)])
    dirs.extend(sorted([f for f in os.listdir(path) if os.path.isfile(path + os.path.sep + f)]))
    dirs = [x for x in dirs if x.endswith('.json')]

    return dirs

path = 'output/'
listing = custom_listdir(path)
listingLength = len(listing)

#counting variables
robotsTrue = 0
robotsFalse = 0
humansTrue = 0
doctypes = {}
serversSummary = {}
frameworksSummary = {}
serversFull = {}
frameworksFull = {}
sitemapTrue = 0
sslTrue = 0
siteList = {}

#the loop
for infile in listing:
    jsonFile = open(path + infile)
    siteJSON = json.load(jsonFile)
    siteList[infile[:-5]] = siteJSON['name']
    if siteJSON['robots'] == True:
        robotsTrue+=1
    else:
        robotsFalse+=1
    if siteJSON['humans'] == True:
        humansTrue+=1
    doctypes[siteJSON['doctype']] = doctypes.setdefault(siteJSON['doctype'],0) + 1
    serversFull[siteJSON['headers']['server']] = serversFull.setdefault(siteJSON['headers']['server'],0) + 1
    frameworksFull[siteJSON['headers']['poweredBy']] = frameworksFull.setdefault(siteJSON['headers']['poweredBy'],0) + 1
    serverSummary = siteJSON['headers']['server'] and siteJSON['headers']['server'].split('/')[0]
    serversSummary[serverSummary] = serversSummary.setdefault(serverSummary, 0) + 1
    frameworkSummary = siteJSON['headers']['poweredBy'] and siteJSON['headers']['poweredBy'].split('/')[0]
    frameworksSummary[frameworkSummary] = frameworksSummary.setdefault(frameworkSummary,0) + 1
    if siteJSON['sitemap'] == True:
        sitemapTrue+=1
    if siteJSON['ssl'] == 'yes':
        sslTrue+=1
#create JSONfile
overJSON = {
    'robotsTrue':robotsTrue,
    'robotsFalse':robotsFalse,
    'humansTrue':humansTrue,
    'doctypes':doctypes,
    'servers':serversSummary,
    'frameworks':frameworksSummary,
    'serversFull':serversFull,
    'frameworksFull':frameworksFull,
    'sitemap':sitemapTrue,
    'ssl':sslTrue
}
#print
outfile = io.open('overview.json', 'wb')
json.dump(overJSON, outfile, sort_keys = True, indent=4, separators=(',', ': '))
outfile.write('\n')

outfile = io.open('list.json', 'wb')
json.dump(siteList, outfile, sort_keys = True, indent=4, separators=(',', ': '))
outfile.write('\n')
