// Prueba la web construida (web/) con un Excel, como un iPhone de 402 px, y guarda capturas de las cinco pestañas.
//   node herramientas/probar.js plantilla/hoja-ejemplo.xlsx        (o tu hoja: mi-hoja/mi-hoja.xlsx)
//   OSCURO=1 node herramientas/probar.js …     ·     ANCHO=1280 ALTO=900 node herramientas/probar.js …  (PC)
// Necesita Playwright:  npm i playwright && npx playwright install chromium
// Deja las capturas en capturas/ y escribe la tarjeta de Resumen, el cuadre y los errores de la página.
const http=require('http'), fs=require('fs'), path=require('path'); const {chromium}=require('playwright');
const R=path.join(__dirname,'..'), WEB=path.join(R,'web'), XL=path.resolve(process.argv[2]||path.join(R,'plantilla','hoja-ejemplo.xlsx'));
const W=+process.env.ANCHO||402, H=+process.env.ALTO||874, movil=W<760, oscuro=!!process.env.OSCURO;
const tipos={'.html':'text/html; charset=utf-8','.js':'text/javascript','.webp':'image/webp','.png':'image/png','.woff2':'font/woff2','.txt':'text/plain'};
const srv=http.createServer((q,r)=>{ let f=path.join(WEB,decodeURIComponent(q.url.split('?')[0])); if(f.endsWith(path.sep)) f=path.join(f,'index.html');
  fs.readFile(f,(e,d)=>{ if(e){ r.writeHead(404); return r.end(); } r.writeHead(200,{'Content-Type':tipos[path.extname(f)]||'application/octet-stream'}); r.end(d); }); });
srv.listen(0,async()=>{ const url=`http://localhost:${srv.address().port}/`; const out=path.join(R,'capturas'); fs.mkdirSync(out,{recursive:true});
  const b=await chromium.launch(); const pg=await b.newPage({viewport:{width:W,height:H},isMobile:movil,hasTouch:movil,deviceScaleFactor:2,colorScheme:oscuro?'dark':'light'});
  const errs=[]; pg.on('pageerror',e=>errs.push(String(e))); pg.on('console',m=>{ if(m.type()==='error') errs.push(m.text()); });
  await pg.goto(url); await pg.waitForSelector('#file',{state:'attached',timeout:20000}); await (await pg.$('#file')).setInputFiles(XL);
  await pg.waitForFunction(()=>document.querySelectorAll('#tmap .tile').length>0||!document.getElementById('notice').hidden,null,{timeout:30000}).catch(()=>{});
  await pg.waitForTimeout(1200);
  const aviso=await pg.evaluate(()=>{ const n=document.getElementById('notice'); return n&&!n.hidden?n.innerText.replace(/\s+/g,' ').slice(0,300):''; });
  if(aviso) console.log('AVISO:',aviso);
  console.log('Resumen:',await pg.evaluate(()=>{ const e=document.getElementById('hm3'); return e?e.innerText.replace(/\s+/g,' '):'(sin tarjeta)'; }));
  console.log('Cuadre:',await pg.evaluate(()=>{ const s=document.getElementById('s-check'); return s?s.innerText.replace(/\s+/g,' ').slice(0,500):''; }));
  for(const v of ['resumen','preseleccion','actualidad','analisis','movimientos']){ await pg.evaluate(v=>{ const a=document.querySelector(`#nav a[data-v="${v}"]`); if(a) a.click(); },v); await pg.waitForTimeout(1000);
    await pg.screenshot({path:path.join(out,`${v}${oscuro?'-oscuro':''}${movil?'':'-pc'}.png`),fullPage:true}); }
  console.log(errs.length?'ERRORES: '+errs.join(' | '):'Sin errores en la página'); console.log('Capturas en',out);
  await b.close(); srv.close(); });
