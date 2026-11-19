from edition import PROVINCES, source, elements, txt, num, coordinates, save
URL='https://map-carte.tbs-sct.gc.ca/dfrp-rbif/oddo/dfrp-rbif.zip'
CATALOG='https://open.canada.ca/data/en/dataset/08013e71-101a-457c-af76-c7b13a08ff64'
def records(raw):
    for site in elements(raw,{'Property'}):
        property_id=txt(site,'Property_Number')
        sites=[s.get('FederalSiteIdentifier') for s in site.findall('.//FederalContaminatedSites/Site') if s.get('FederalSiteIdentifier')]
        for p in site.findall('Parcels/Parcel'):
            prov=txt(p,'Location/Province_E')
            if prov not in PROVINCES:continue
            key=p.get('Number')
            if not property_id or key is None:raise ValueError('Missing parcel identifier')
            buildings=[(txt(s,'Structure_Name_E'),txt(s,'Construction_Year'),txt(s,'Condition_E')) for s in p.findall('Structures/Structure')]
            yield {'group':PROVINCES[prov],'id':property_id+'-'+key,'title':txt(site,'Property_Name_E') or 'Unnamed property',
                   'place':txt(p,'Location/Municipality_E') or txt(p,'Location/Place_Name_EN'),'province':prov,'kind':txt(site,'Primary_Use_E'),
                   'status':txt(site,'Interest_Type_E'),'owner':txt(site,'Custodian/Name_E'),'address':txt(site,'Address_E'),
                   'geo':coordinates(txt(p,'Location/Latitude'),txt(p,'Location/Longitude')),
                   'accuracy':num(txt(p,'Location/Positional_Accuracy')),'land':num(txt(p,'Land_Area')),'floor':num(txt(p,'Floor_Area')),
                   'buildings':num(txt(p,'Building_Count')),'structures':buildings,'contaminated':list(dict.fromkeys(sites)),
                   'updated':site.get('lastModifiedDate','')[:10],'property':property_id,'parcel':key}
HERITAGE_PAGE='https://open.canada.ca/data/en/dataset/49d5ba7d-d860-40d9-9183-892979e4acbe'
HERITAGE=HERITAGE_PAGE.replace('/en/','/')+'/resource/682d1e12-26dd-4d30-bb40-f04658502bcd/download/dataset-of-federal-heritage-designations-as-of-march-31-2026.csv'
# Reviewed property-to-designation references in Parks Canada’s March 2026 edition.
MATCHES={'17454':['98','8083','14432'],'17109':['87'],'17414':['99'],'02990':['278'],
         '03640':['303'],'02893':['299'],'02778':['318'],'02991':['281']}
def join_heritage(rows,raw):
    import csv,io
    entries={r['Directory of Federal Heritage Designations Identifier']:r for r in csv.DictReader(io.StringIO(raw.decode('cp1252',errors='replace')))}
    matches=0
    for row in rows:
        refs=MATCHES.get(row['property'],[])
        row['heritage']=[]
        for key in refs:
            r=entries[key]
            if r['Province or territory']!=row['province']:raise ValueError('Heritage reference changed')
            row['heritage'].append([key,r['Designation name'],r['Designation type'],r['Designation date']])
        matches+=bool(refs)
    if matches<len(MATCHES):raise ValueError('A reviewed property reference vanished')
if __name__=='__main__':
    rows=list(records(source(URL,'dfrp.zip')))
    join_heritage(rows,source(HERITAGE,'heritage.csv'))
    if set(r['group'] for r in rows)!=set(PROVINCES.values()) or len(rows)<3000:raise ValueError('Unexpected regional coverage')
    save(rows,[{'name':'Directory of Federal Real Property','url':CATALOG,'download':URL},{'name':'Parks Canada heritage designations (March 2026)','url':HERITAGE_PAGE,'download':HERITAGE}],{'properties':len({r['property'] for r in rows})})
