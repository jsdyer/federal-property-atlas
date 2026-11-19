import {facts,tabular,href,node,primaryColumns} from './view.mjs';
export const config={slug:'federal-property-atlas',groups:{BC:'British Columbia',NS:'Nova Scotia'},defaultGroup:'NS',defaultQuery:'Halifax',center:[47,-82],zoom:4,allKind:'Every primary use',allStatus:'Every interest type',allOwner:'All custodians',extras:[['','All parcels'],['heritage','With reviewed heritage links'],['floor','With floor area above zero'],['sites','With a linked contaminated-site ID'],['unknown','Without a map position']]};
export function qualifies(r,k){return !k||({heritage:r.heritage.length>0,floor:r.floor>0,sites:r.contaminated.length>0,unknown:!r.geo})[k]}
export const extraTerms=r=>[...(r.heritage||[]).map(x=>x[1]),...r.structures.map(x=>x[0])];
export function details(r,d){
 facts(d,[['Property / parcel',r.property+' / '+r.parcel],['Custodian',r.owner],['Recorded address',r.address],['Land area (ha)',r.land],['Floor area (m²)',r.floor],['Reported buildings',r.buildings],['Position accuracy (m)',r.accuracy],['Source record modified',r.updated]]);
 tabular(d,'Structures on this parcel',['Name','Construction year','Recorded condition'],r.structures);
 if(r.heritage.length){tabular(d,'Reviewed Parks Canada designations',['Register ID','Designation','Type','Date'],r.heritage);href(d,'Open the heritage register','https://parks.canada.ca/culture/adpf-dfhd')}
 if(r.contaminated.length){d.append(node('h3','Contaminated-site records linked to this property'));for(const id of r.contaminated)href(d,'Open site '+id+' in Toxic Ground','https://coolcode.ca/toxic-ground/?region='+r.group+'&id='+encodeURIComponent(id))}
}
export const columns=()=>[...primaryColumns,['Property number',r=>r.property],['Parcel',r=>r.parcel],['Floor area m²',r=>r.floor],['Land area ha',r=>r.land],['Reported buildings',r=>r.buildings],['Reviewed heritage designation IDs',r=>r.heritage.map(x=>x[0]).join(' · ')]];

export const sorts=[['','Property name'],['floor','Largest floor area',(a,b)=>(b.floor??-1)-(a.floor??-1)],['land','Largest land area',(a,b)=>(b.land??-1)-(a.land??-1)],['buildings','Most reported buildings',(a,b)=>(b.buildings??-1)-(a.buildings??-1)]];
