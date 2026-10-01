from pathlib import Path
import zipfile,json
r=Path(__file__).parent; d=r/'dist'
p=d/'app.js';s=p.read_text()
s=s.replace("const main=document.getElementById('main');","const totalLessons=lessons.length,totalModules=modules.length,totalUnits=totalLessons+totalModules,totalQuestions=modules.reduce((n,m)=>n+m.quiz.length,0);\nconst main=document.getElementById('main');")
s=s.replace("document.getElementById('progress').value=n;","document.getElementById('progress').max=totalUnits;document.getElementById('progress').value=n;")
s=s.replace('n/51*100','n/totalUnits*100').replace("s.done+'/41 lessons · '+s.passed+'/10 quizzes passed'","s.done+'/'+totalLessons+' lessons · '+s.passed+'/'+totalModules+' quizzes passed'")
s=s.replace('s.done===41&&s.passed===10','s.done===totalLessons&&s.passed===totalModules')
s=s.replace('<strong>10</strong> modules','<strong>${totalModules}</strong> modules').replace('<strong>41</strong> lessons','<strong>${totalLessons}</strong> lessons').replace('<strong>30</strong> quiz questions','<strong>${totalQuestions}</strong> quiz questions').replace('6–8 hours','10–12 hours')
s=s.replace("?'<div class=\"success\">",'?`<div class="success">').replace('all 41 lessons and passed all 10 knowledge checks','all ${totalLessons} lessons and passed all ${totalModules} knowledge checks').replace("requirements with your counsellor.</p></div>':''}","requirements with your counsellor.</p></div>`:''}")
s=s.replace('m.id<10','m.id<totalModules').replace('${s.done}/41','${s.done}/${totalLessons}').replace('${s.passed}/10','${s.passed}/${totalModules}').replace('totalLessons:41,totalQuizzes:10','totalLessons,totalQuizzes:totalModules')
s=s.replace('Companion guide · page ${l.guidePage}',"${l.guidePage?'Companion guide · page '+l.guidePage:esc(l.sourceLabel)}")
s=s.replace('<a class="button secondary" href="#workbook">Open my workbook</a>','<a class="button secondary" href="#pathways">Choose my year group</a><a class="button secondary" href="#roadmap">Explore the roadmap</a>')
s=s.replace('Source guide updated 29 September 2026. Based on the supplied conference notes, CEG resource library and cited official sources.','Course expanded 30 September 2026 with the supplied Further Education Pathway curriculum, career readiness topics and college roadmaps. The original 50-page guide remains available; the new lessons are online and their activities appear in your workbook.')
s=s.replace("else if(kind==='support')support();","else if(kind==='support')support();else if(kind==='pathways')pathways();else if(kind==='roadmap')roadmap();else if(kind==='career-resources')careerResources();")
s=s.replace('<article class="resource-content">${window.COURSE.resources}</article>','<div class="actions"><a class="button secondary" href="#career-resources">Career readiness resources · 38 topics</a><a class="button secondary" href="#roadmap">Two visual roadmaps</a><a class="button secondary" href="#pathways">EY–S6 learning paths</a></div><article class="resource-content">${window.COURSE.resources}</article>')
s=s.replace('<h2>Use the course in a group</h2>','<h2>Align the course with EY–S6</h2><p>The <a href="#pathways">year-group learning paths</a> adapt the supplied CRC Further Education Pathway outline (29 August 2025). Its school learning targets are planning benchmarks, not universal admission requirements. The internal source document is not offered as a public download.</p><p>Use a simple portfolio rubric: 0 = missing, 1 = draft, 2 = clear evidence with a next step. Review authenticity, research quality, feasibility and reflection. Give one specific improvement before the next checkpoint. Do not require students to disclose private experiences in a group.</p><h2>Use the course in a group</h2>')
p.write_text(s)
p=d/'index.html';s=p.read_text().replace('41 practical lessons','53 practical lessons').replace('<script defer src="app.js">','<script defer src="extension-data.js"></script><script defer src="extension-ui.js"></script><script defer src="app.js">').replace('<div id="modules-nav">','<a class="navlink" href="#pathways">My year-group pathway</a><a class="navlink" href="#roadmap">Visual application roadmap</a><div id="modules-nav">').replace('<a class="navlink" href="#support">','<a class="navlink" href="#career-resources">Career readiness resources</a><a class="navlink" href="#support">');p.write_text(s)
# Optional source readings, unchanged, retain source attribution in each PDF.
z=zipfile.ZipFile('/workspace/scratch/95867915d940/upload/Career Readiness Curriculum Guide-20260929T171503Z-1-001.zip')
items=json.loads((d/'extension-data.js').read_text().removeprefix('window.CAREER_TOPICS=').rstrip(';\n'))
folder=d/'assets/career';folder.mkdir(exist_ok=True)
for i,name in enumerate(n for n in z.namelist() if n.endswith('.pdf')):
 title=name.split('/')[-1][:-4].split('_ ',1)[-1].replace('_',' / ')
 item=next(x for x in items if x['title']==title);item['file']=f'assets/career/topic-{i:02}.pdf';(d/item['file']).write_bytes(z.read(name))
(d/'extension-data.js').write_text('window.CAREER_TOPICS='+json.dumps(items,ensure_ascii=False)+';\n')
