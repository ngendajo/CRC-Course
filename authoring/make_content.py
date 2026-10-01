from docx import Document
from docx.oxml.ns import qn
from pathlib import Path
import html,json,re,shutil
root=Path('/workspace/sites/college-application-course');out=root/'dist';src=Path('/workspace/scratch/95867915d940/output')
d=Document(src/'College_Application_Guide.docx');pages={};num=1;current={'title':'Welcome','body':[],'practice':[]};pages[1]=current
for e in d.element.body:
 if e.tag==qn('w:p'):
  txt=''.join(e.itertext()) if False else ''.join(e.xpath('.//w:t/text()'))
  match=re.match(r'(\d+)\s+EXPANDED COLLEGE APPLICATION GUIDE',txt)
  if match:num=int(match[1]);current={'title':'','body':[],'practice':[]};pages[num]=current;continue
  st=e.xpath('./w:pPr/w:pStyle/@w:val');st=st[0] if st else ''
  if st=='Heading1':current['title']=txt;continue
  if txt.startswith(('Try this','Practice  ')):
   current['practice'].append(re.sub(r'^(Try this|Practice)\s*','',txt));continue
  if '____' in txt:
   label=re.sub('_+','',txt).strip()
   if label:current['body'].append('<p class="worksheet-prompt">'+html.escape(label)+'</p>')
   continue
  links=e.xpath('.//w:hyperlink')
  if links:
   for a in links:
    rid=a.get(qn('r:id'));label=''.join(a.xpath('.//w:t/text()'));url=d.part.rels[rid].target_ref
    current['body'].append('<p><a target="_blank" rel="noopener" href="'+html.escape(url)+'">'+html.escape(label)+'</a></p>')
  elif txt:
   tag='h3' if st.startswith('Heading') else 'p'
   current['body'].append('<'+tag+'>'+html.escape(txt)+'</'+tag+'>')
  for blip in e.xpath('.//a:blip'):
   rid=blip.get(qn('r:embed'));part=d.part.related_parts[rid];name=Path(str(part.partname)).name
   (out/'assets'/name).write_bytes(part.blob);alt=e.xpath('.//wp:docPr/@descr')
   current['body'].append('<img class="lesson-graphic" src="assets/'+name+'" alt="'+html.escape(alt[0] if alt else 'Guide diagram')+'">')
 elif e.tag==qn('w:tbl'):
  table='<div class="table-scroll"><table>'
  for i,tr in enumerate(e.xpath('./w:tr')):
   table+='<tr>'
   for tc in tr.xpath('./w:tc'):
    tag='th' if i==0 else 'td';txt=' '.join(tc.xpath('.//w:t/text()'))
    table+='<'+tag+'>'+html.escape(txt or 'Record your answer in the activity below')+'</'+tag+'>'
   table+='</tr>'
  current['body'].append(table+'</table></div>')
modules=[
('Find your direction','Explore',[3,4,21],'Choose courses that fit your interests, qualifications and budget.','A researched college shortlist'),
('Plan your application','Plan',[5,6,42],'Work backwards from deadlines and understand application commitments.','Your application calendar'),
('Prepare your records','Prepare',[7,8,39],'Check academic records, testing requirements and application fields.','A document and testing checklist'),
('Discover your story','Reflect',[9,26,27,28,44],'Find honest experiences that reveal your values and thinking.','An essay topic and evidence bank'),
('Build and revise your essay','Write',[29,30,31,10,41],'Use structure, reflection and feedback to develop your own voice.','A personal essay draft'),
('Answer each prompt','Adapt',[32,33,34,35,36,37,40,11],'Adapt evidence to college, community, subject and UK prompts.','A set of focused supplemental responses'),
('Show your experience','Present',[12,13,38,22,25],'Describe contributions, support recommenders and prepare for interviews.','An activity record and recommendation pack'),
('Make funding realistic','Fund',[14,15,16],'Compare total costs, confirmed support and remaining funding gaps.','A cost comparison and scholarship plan'),
('Submit with care','Apply',[17,18,45,43],'Review, submit and track every part of an application.','A completed application audit'),
('Choose and prepare','Begin',[19,20],'Compare offers and prepare for a realistic transition to university.','An offer decision and arrival plan')]
# Questions use original course scenarios, not an official admissions assessment.
quiz=[
[("Which choice is a realistic financial backup?",["A college with a familiar name","A suitable college with a verified affordable plan","Any college with a high overall acceptance rate"],1,"Admission prospects and affordability are separate. Check that the course fits and the whole cost can be covered."),("Two computing degrees have the same title. What should you compare?",["Only their rankings","Their logos and publicity","Modules, teaching methods and entry requirements"],2,"Course titles can hide different curricula. Compare what you will actually study and how you qualify."),("A college’s international scholarship rules are unclear. What next?",["Record funding as unknown and ask the official office","Assume that all admitted students receive it","Use a friend’s award as a guarantee"],0,"An unconfirmed award is not available funding. Save the current official evidence or request clarification.")],
[("A scholarship nomination closes before admission. Which deadline drives your preparation?",["The admission deadline only","The earlier nomination deadline","The date a friend submits"],1,"Separate deadlines can affect the same application. Work backwards from the earliest relevant requirement."),("What does Early Decision normally involve?",["A binding commitment under the college’s agreement if admitted","Guaranteed full funding","An unrestricted chance to compare all offers"],0,"Read the actual agreement and discuss affordability before committing. Seek the college’s guidance if aid is unaffordable."),("A deadline says midnight. What must you verify?",["Whether the website looks current","Only your device clock","The deadline’s stated time zone and applicable rules"],2,"Some systems use local time and others institutional time. Record the exact rule and verify conversion.")],
[("Your transcript has percentages but no GPA. What should you do?",["Invent an approximate US GPA","Follow official instructions and ask about unclear fields","Copy another student’s GPA"],1,"Preserve the actual grading system. Use a conversion only when the receiving institution instructs you to do so."),("A college is test-optional. Does that automatically waive English evidence?",["Yes, for every applicant","Yes, if you prefer not to test","No, check the English-language policy separately"],2,"Admission-test and English-language requirements can differ. Check your course and applicant category."),("Your shared Common App section is complete. Are all college applications finished?",["Not necessarily; check each college’s questions and supplements","Yes, all are automatically submitted","Yes, references are automatically received"],0,"Each college sets requirements. Complete, submit and track each application and its supporting materials.")],
[("Which is the strongest starting point for an essay?",["A truthful moment with a decision and insight","The most impressive story you can invent","A list of positive adjectives"],0,"A concrete experience lets you explain your actions and thinking. Ordinary moments can provide useful evidence."),("How should you use published essay examples?",["Copy their personal experiences","Study their writing choices, then develop your own material","Replace the writer’s name with yours"],1,"Examples teach techniques. Your experiences, wording and claims must remain your own."),("An older workbook lists a university prompt. What should you check?",["Only the length of the example essay","Whether a friend likes the question","The current official prompt and limit"],2,"The workbook is a directory. A past-year title does not establish the current requirement.")],
[("What makes a montage work?",["Several unrelated achievements","One meaningful thread connecting distinct scenes","Using as many metaphors as possible"],1,"Each scene should add a different insight while contributing to the shared idea."),("Which sentence provides useful reflection?",["This was an amazing experience","I am a great leader","I began asking where my explanation became confusing"],2,"Reflection becomes persuasive when tied to a specific change in thinking or behaviour."),("What is helpful essay feedback?",["Questions that help you clarify your own meaning","A reviewer replacing the essay with their writing","Adding achievements you did not earn"],0,"The student retains authorship. Reviewers can point out confusion and invite better evidence.")],
[("What belongs in a strong college-fit response?",["Generic praise about prestige","An invented course title","Verified opportunities connected to your interests"],2,"Research matters when you explain its personal relevance and confirm that the opportunity is available."),("A community essay should usually help the reader understand…",["Your contribution and what you learned from others","Why you deserve all credit","Only the community’s size"],0,"Show the relationship in both directions and acknowledge other people’s effort."),("Where should a concise explanation of disrupted schooling go?",["In every essay with identical wording","In the relevant context field if needed, following its prompt","Nowhere, even if a required answer would be misleading"],1,"Use the appropriate field, avoid unnecessary repetition and consider what the school profile already explains.")],
[("Which activity description is most precise?",["Changed everyone’s life","An outstanding member","Prepared eight practice sessions and helped organise equipment"],2,"Specific actions and a supportable scope are clearer than broad praise."),("Who should write an official recommendation?",["The student pretending to be the teacher","The authorised recommender using their own evidence","A friend who has never met the student"],1,"Students supply factual context; recommenders write and submit their independent assessment."),("How should you prepare for an interview?",["Practise explaining real actions and lessons naturally","Memorise an invented perfect story","Avoid discussing any uncertainty"],0,"Prepare ideas rather than a script. Be honest about what happened and what you learned.")],
[("Tuition is fully covered. What should you check next?",["Nothing; the whole degree is paid for","Housing, living costs, travel and award conditions","Only the college ranking"],1,"Full tuition may leave substantial costs. Check coverage, renewal and the timing of payments."),("Annual total is $30,000, grants $15,000 and family support $8,000. What is the gap?",["$7,000","$15,000","$22,000"],0,"$30,000 − $15,000 − $8,000 = $7,000 still to fund. Do not count an unconfirmed job or award as guaranteed support."),("Which scholarship amount belongs in a confirmed funding plan?",["A hoped-for award","A scholarship a friend received","An award documented for you under understood conditions"],2,"Confirmed funding must apply to your case. Check duration, exclusions and renewal conditions.")],
[("Your school sent a transcript. What status should you record?",["Received, even if the portal disagrees","Submitted by school; receipt still to confirm","Admitted"],1,"Sending and receipt are different stages. Allow the stated processing time before following up."),("You discover a wrong grade after submitting. What next?",["Hide the error","Create another application immediately","Follow the college’s correction process and involve the school"],2,"Report material errors promptly through the authorised process. School records need authorised correction."),("Who remains responsible for the final application declarations?",["The student applicant","Any person who proofreads","The author of an example essay"],0,"Supporters can review, but the student must check accuracy and understand the final declarations.")],
[("Offer A is cheaper in year one but aid lasts one year. What should you compare?",["Only the first-year scholarship headline","Costs and confirmed support over the whole degree","Only the admission rate"],1,"An affordable first year does not guarantee an affordable degree. Check renewal and later-year costs."),("Does admission guarantee visa approval?",["Yes","Yes, if a scholarship is offered","No, these are separate processes"],2,"Follow current government and university instructions. Admission, funding and permission to enter are distinct."),("Your annual budget balances, but travel money is needed before the grant arrives. What is missing?",["A plan for the timing of payments","Another essay topic","A higher activity count"],0,"Cash may be needed before aid is credited. Agree how early deposits and travel will be funded.")]
]
result=[]
for i,(title,verb,ids,goal,output) in enumerate(modules):
 lessons=[]
 for j,n in enumerate(ids):
  z=pages[n];body=''.join(z['body']);words=len(re.sub('<[^>]+>',' ',body).split())
  act=' '.join(z['practice']) or ('Create '+output.lower()+'. Use the guidance above to record your evidence, unanswered questions and next action.')
  lessons.append({'id':str(n),'title':z['title'],'html':body,'activity':act,'minutes':max(5,round(words/150)+5),'guidePage':n})
 result.append({'id':i+1,'title':title,'verb':verb,'goal':goal,'output':output,'lessons':lessons,'quiz':[{'q':q,'options':o,'answer':a,'why':w} for q,o,a,w in quiz[i]]})
resources=''.join('<h2>'+html.escape(pages[n]['title'])+'</h2>'+''.join(pages[n]['body']) for n in [46,47,48,49,50])
# A short facilitator reference retains school support material from the source guide.
facilitator=''.join('<h2>'+html.escape(pages[n]['title'])+'</h2>'+''.join(pages[n]['body']) for n in [23,24])
(out/'course-data.js').write_text('window.COURSE='+json.dumps({'modules':result,'resources':resources,'facilitator':facilitator},ensure_ascii=False)+';')
for name in ['College_Application_Guide.pdf','College_Application_Guide.docx']:shutil.copy2(src/name,out/'assets'/name)
print('Created',sum(len(x['lessons']) for x in result),'lessons and',sum(len(x['quiz']) for x in result),'questions')
