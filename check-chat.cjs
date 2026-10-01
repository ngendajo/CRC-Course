const fs=require('fs'),vm=require('vm'),assert=require('assert');
function text(html){return html.replace(/<[^>]*>/g,' ').replace(/&amp;/g,'&').replace(/\s+/g,' ').trim();}
const context={window:{},document:{createElement(){return{innerHTML:'',get textContent(){return text(this.innerHTML)},querySelectorAll(){return [...this.innerHTML.matchAll(/<(p|li)([^>]*)>([\s\S]*?)<\/\1>/g)].map(m=>({textContent:text(m[3]),classList:{contains:n=>m[2].includes(n)}}))}}}}};vm.createContext(context);vm.runInContext(fs.readFileSync('dist/course-data.js','utf8'),context);
let code=fs.readFileSync('dist/chat.js','utf8').split('const launcher=')[0]+'})();';vm.runInContext(code,context);const bot=context.window.CRCChat;
for(const [query,id] of [['How do I start my essay?','9'],['How can I find scholarships?','14'],['What is Early Decision?','6'],['Do I need the SAT?','8'],['How do I write a CV?','38'],['How do I explore careers?','explore-pathways'],['Tell me about Common App','39'],['How do I prepare for an interview?','25']]){const a=bot.respond(query);assert(a.ids.includes(id),query);assert(a.answer.length>50);}
assert(bot.respond('What is the weather on Mars?').answer.includes('could not find'));
assert(bot.respond('Write my personal essay for me').answer.includes('do not write submission-ready'));
assert(bot.respond('Where are my saved notes?').route[0]==='workbook');
assert(bot.respond('<script>alert(1)</script>').answer.includes('could not find'));
const ids=new Set(context.window.COURSE.modules.flatMap(m=>m.lessons.map(l=>l.id)));
for(const query of ['essays','scholarships','recommendations','budget','career','internship','deadline','UCAS','stress','AI','activities','first step'])for(const id of bot.respond(query).ids)assert(ids.has(id));
assert(bot.search('montage').some(x=>x.lesson.id==='30'));
assert(!/fetch\(|XMLHttpRequest|localStorage/.test(fs.readFileSync('dist/chat.js','utf8')));
console.log('Passed chatbot topic matching, unknown-question fallback, essay boundary, saved-work guidance, course links and retrieval. Chat has no network calls or persistent question storage.');
