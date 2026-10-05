import { Ctx, Env, probeRect } from './core';
import { Film } from './film';
// Canvas adaptation of phases(), blueprint-animation/example-scene.jsx (CC BY-NC 4.0).
const cl=(v:number)=>Math.max(0,Math.min(1,v)),ease=(v:number)=>v<.5?4*v*v*v:1-Math.pow(-2*v+2,3)/2;
const tw=(t:number,a:number,b:number)=>ease(cl((t-a)/(b-a)));
function phases(t:number){return {wipe:tw(t,1.2,2.6),p:tw(t,2.8,5.2),rev:tw(t,5.5,6.9)}}
const rows=[
['Patrimoine','9 339 fichiers / références Git','Archives, actifs et dépendances mêlés','1 341 sources importées et traçables','Le reste reste inventorié et qualifiable','IMPORTÉ','Conserver le sens, les relations et la provenance de chaque actif.','3 249 archives · 4 736 entrées à qualifier · 7 binaires · 6 gitlinks'],
['Life Core','3 630 entrées Life OS','Dont 3 249 archives ; LD01 surreprésenté','L1 : 8 domaines + 6 frameworks','L2 : Business OS dans LD01','REGISTRE RELIÉ','Rétablir la place des huit domaines sans inventer leur équilibre.','Doctor 11 · Amy / Rory / River · Ikigai · Wheel · 12WY Curie · PARA · GTD · DEAL'],
['Mémoire','40 Memory, distillation, ontologies','Implémentations temporelles en mémoire vive','Sources historiques + journal durable','Contexte temporel, replay et sauvegarde','TESTÉ','Une nouvelle session doit retrouver les raisons et reprendre le travail.','Graham garde le contexte ; une observation passée ne devient pas un état actuel.'],
['Agents','Identités, mandats et harnesses dispersés','Des règles historiques contradictoires','Holons complets, rôles non exclusifs','Gateway + adaptateurs + return_to','À RACCORDER','Préserver la cognition et la subsidiarité ; borner les effets autorisés.','3 Doctors · 9 Compagnons · 5 Apps : Gateway / A0 / S1 / S2 / S3'],
['Forge GitHub','Code, PR, intentions et contrats existants','Documenter ne prouve pas le fonctionnement','Décision → mission → preuve','Branches Doctors ; autorité par Apps','PARTIEL','Relier les primitives GitHub aux missions et à leurs preuves d’exécution.','Projects · Milestones · Discussions/RACI · Issues · PR · Actions · Wiki · Releases'],
['Portabilité','Dépendances locales et état fragmenté','Reprise entre machines non démontrée','PC moniteur ; harnesses sur compute','Instance portable avec mémoire et reprise','PREUVE PARTIELLE','Changer de compute en conservant mission, contexte et identité des effets.','Reprise SQLite isolée validée ; migration entre deux VPS encore à vérifier.']
];
const ink='#183b39',muted='#54716d',green='#176a55',cyan='#0B8FC2',amber='#96611d';
function draw(c:Ctx,f:number,e:Env){
 c.save();c.scale(e.scale,e.scale);const t=f/24,idx=t<6?-1:Math.min(5,Math.floor((t-6)/12)),end=t>=78;
 const local=idx<0?0:t-(6+idx*12),ph=phases(local);
 const txt=(s:string,x:number,y:number,size=22,color=ink,weight=400)=>{c.fillStyle=color;c.font=`${weight} ${size}px Arial, sans-serif`;c.fillText(s,x,y);probeRect(c,e,x,y-size,c.measureText(s).width,size+5,s,'text')};
 const box=(x:number,y:number,w:number,h:number,col:string,fill:string)=>{c.fillStyle=fill;c.fillRect(x,y,w,h);c.strokeStyle=col;c.lineWidth=1;c.strokeRect(x,y,w,h)};
 c.fillStyle='#f5f4ed';c.fillRect(0,0,1600,1000);
 txt('A’SPACE  /  TRANSFERT INTELLIGENT',54,46,18,green,700);
 txt('V3 → V4 : transmettre sans réduire',54,104,44,ink,700);
 txt('Une refondation autonome. Un patrimoine conservé. Des capacités prouvées une par une.',56,146,23,muted);
 txt(end?'V4 · ÉTAT ET CIBLE':idx<0?'V3 · PATRIMOINE':'TRANSFORMATION '+String(idx+1).padStart(2,'0')+' / 06',56,195,17,green,700);
 txt('AVANT  /  POINT DE DÉPART',340,195,16,muted,700);txt('APRÈS  /  ÉTAT ET DESTINATION',865,195,16,muted,700);
 function scene(bp:boolean){
  if(bp){c.fillStyle='#fff';c.fillRect(40,207,1520,555);c.strokeStyle='#2accff20';for(let x=40;x<1560;x+=24){c.beginPath();c.moveTo(x,207);c.lineTo(x,762);c.stroke()}for(let y=207;y<762;y+=24){c.beginPath();c.moveTo(40,y);c.lineTo(1560,y);c.stroke()}}
  rows.forEach((r,i)=>{const y=216+i*89,active=i===idx&&!end,done=end||i<idx||(active&&local>=5.2),col=bp?cyan:active?green:'#bccac2';
   box(54,y,1490,78,col,bp?'#f5fcff':active?'#e8f0e7':'#fff');
   txt(String(i+1).padStart(2,'0'),70,y+30,17,bp?cyan:muted,700);txt(r[0],108,y+34,23,bp?cyan:ink,700);
   txt(r[1],340,y+30,20,bp?cyan:muted);txt(r[2],340,y+57,18,bp?cyan:muted);
   c.strokeStyle=col;c.beginPath();c.moveTo(824,y+39);c.lineTo(847,y+39);c.lineTo(841,y+34);c.moveTo(847,y+39);c.lineTo(841,y+44);c.stroke();
   const moving=bp&&active&&ph.p>.05&&ph.p<.95;
   if(!moving){txt(done?r[3]:'Capacité à transmettre',865,y+30,20,bp?cyan:done?ink:muted,done?700:400);txt(done?r[4]:'Sources · relations · contrats · preuves',865,y+57,18,bp?cyan:muted)}
   if(bp&&active){const w=520+ph.p*140;c.setLineDash([3,5]);c.strokeRect(859,y+5,w,68);c.setLineDash([]);for(const x of [859,859+w])for(const yy of [y+5,y+73]){c.fillStyle=cyan;c.fillRect(x-3,yy-3,6,6)}}
   if(!bp){c.fillStyle=done&&i<3?'#d8ecdf':'#f4e8d3';c.fillRect(1360,y+10,171,24);txt(done?r[5]:'À QUALIFIER',1370,y+27,12,done&&i<3?green:amber,700)}
  });
 }
 scene(false);
 if(idx>=0&&!end&&ph.wipe>0&&ph.rev<1){c.save();c.beginPath();c.rect(40,207+555*ph.rev,1520,555*(ph.wipe-ph.rev));c.clip();scene(true);c.restore();const yy=207+555*(ph.rev>0?ph.rev:ph.wipe);c.strokeStyle=cyan;c.lineWidth=2;c.beginPath();c.moveTo(40,yy);c.lineTo(1560,yy);c.stroke()}
 box(54,779,1490,151,'#cbd5ca','#ecf0e5');
 if(idx<0){txt('TRANSMETTRE UNE CAPACITÉ COMPLÈTE',78,818,20,green,700);txt('Identité + sources + contrats + code + données + projections + preuves + reprise',78,859,27,ink,700);txt('Inventaire complet du snapshot Git ; lecture sémantique ciblée. Les volumes ne mesurent pas le fonctionnement.',78,899,20,muted)}
 else if(end){txt('CE QUI EST LIVRÉ',78,816,18,green,700);txt('1 341 sources · 8 LD · 6 frameworks · mémoire durable · 51 tests passants',78,852,29,ink,700);txt('PR #8 ouverte · Gateway / Doctors / GWS à raccorder · reprise multi-VPS à prouver',78,889,22,amber);txt('75 services OMK déclarés, surfaces et Factory restent dans le périmètre à qualifier.',78,917,18,muted)}
 else{const r=rows[idx];txt(String(idx+1).padStart(2,'0')+'  '+r[0].toUpperCase(),78,815,19,green,700);txt(r[6],78,853,27,ink,700);txt(r[7],78,890,20,muted);txt(local<7?'FOCUS → BLUEPRINT → RECONSTRUCTION → RÉVÉLATION':'ÉTAT : '+r[5],78,917,14,local<7?cyan:green,700)}
 c.fillStyle='#d6dfd5';c.fillRect(54,951,1490,4);c.fillStyle=green;c.fillRect(54,951,1490*cl(t/90),4);
 txt('05 OCT 2026 · V3 ad5e68e · V4 69bca77 · Analyse + PR #8',54,978,15,muted);
 txt('Anidoodle × Blueprint adapté · CC BY-NC 4.0',1136,978,14,muted);c.restore();
}
export const aspace:Film={meta:{title:'A’Space — Analyse du transfert intelligent V3 → V4',W:1600,H:1000,fps:24,bpm:60,durationFrames:2160,kind:'drawing'},assets:{images:{}},shots:[{id:'transfert',start:0,end:2160,draw}]};
