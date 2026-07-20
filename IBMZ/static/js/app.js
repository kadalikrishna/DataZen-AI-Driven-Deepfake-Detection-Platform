const $=id=>document.getElementById(id);let selectedFile=null;
const input=$("file-input"),drop=$("dropzone"),form=$("upload-form"),button=$("analyze-button");

document.querySelectorAll(".nav").forEach(tab=>tab.addEventListener("click",()=>{
 document.querySelectorAll(".nav,.view").forEach(x=>x.classList.remove("active"));tab.classList.add("active");
 $(tab.dataset.view+"-view").classList.add("active");if(tab.dataset.view==="history")loadHistory();
}));

fetch("/api/v1/model/status").then(r=>r.json()).then(s=>{$("model-state").textContent=`Local CPU · ${s.visual_loaded||s.audio_loaded?"models active":"ready on first scan"}`}).catch(()=>{$("model-state").textContent="Server unavailable"});

function choose(file){
 if(!file)return;if(file.size>50*1024*1024){toast("File exceeds the 50 MB limit");return}
 selectedFile=file;const ext=file.name.split(".").pop().toUpperCase();$("file-type").textContent=ext;
 $("file-name").textContent=file.name;$("file-meta").textContent=`${(file.size/1024/1024).toFixed(2)} MB · ${file.type||"media"}`;
 $("file-card").classList.remove("hidden");button.disabled=false;
}
input.addEventListener("change",()=>choose(input.files[0]));
["dragenter","dragover"].forEach(e=>drop.addEventListener(e,event=>{event.preventDefault();drop.classList.add("drag")}));
["dragleave","drop"].forEach(e=>drop.addEventListener(e,event=>{event.preventDefault();drop.classList.remove("drag")}));
drop.addEventListener("drop",e=>choose(e.dataTransfer.files[0]));
$("remove-file").addEventListener("click",()=>{selectedFile=null;input.value="";$("file-card").classList.add("hidden");button.disabled=true});

function state(name){["empty-result","loading-result","error-result","result"].forEach(id=>$(id).classList.toggle("hidden",id!==name))}
form.addEventListener("submit",async event=>{
 event.preventDefault();if(!selectedFile)return;state("loading-result");button.disabled=true;button.querySelector("span").textContent="Analyzing locally…";
 const data=new FormData();data.append("file",selectedFile);
 try{const response=await fetch("/api/v1/upload",{method:"POST",body:data});const result=await response.json();if(!response.ok)throw new Error(result.error||"Analysis failed");renderResult(result);state("result");toast("Analysis complete")}
 catch(error){$("error-copy").textContent=error.message;state("error-result")}
 finally{button.disabled=false;button.querySelector("span").textContent="Run forensic analysis"}
});

function renderResult(data){
 const result=$("result");result.className=`result ${data.verdict}`;$("verdict-label").textContent=data.verdict_label;$("result-file").textContent=data.filename;
 $("fake-score").textContent=`${Math.round(data.fake_probability*100)}%`;$("score-marker").style.left=`calc(${data.fake_probability*100}% - 1px)`;
 $("media-type").textContent=data.media_type;$("sample-count").textContent=data.frames_analyzed||data.segments_analyzed||1;$("process-time").textContent=`${(data.processing_time_ms/1000).toFixed(1)} s`;
 $("model-name").textContent=data.model;$("limitations").textContent=data.limitations;
 $("evidence-list").innerHTML=data.evidence.map(item=>{const pct=Math.round(item.fake_probability*100);const label=item.timestamp_seconds===undefined?`Sample ${item.sample}`:`${item.timestamp_seconds.toFixed(1)} s`;return `<div class="evidence-row"><span>${label}</span><div class="mini-track"><i style="width:${pct}%"></i></div><strong>${pct}%</strong></div>`}).join("");
}

async function loadHistory(){
 const [items,stats]=await Promise.all([fetch("/api/v1/incidents").then(r=>r.json()),fetch("/api/v1/stats").then(r=>r.json())]);
 const labels=[["total_analyses","Total"],["likely_real","Likely real"],["inconclusive","Inconclusive"],["likely_fake","Likely fake"]];
 $("stats").innerHTML=labels.map(([key,label])=>`<div class="stat"><strong>${stats[key]}</strong><span>${label}</span></div>`).join("");
 $("history-list").innerHTML=items.length?items.map(item=>`<article class="history-item"><div><strong>${escapeHtml(item.filename)}</strong><small>${new Date(item.timestamp).toLocaleString()}</small></div><span class="pill">${item.media_type}</span><span>${Math.round(item.fake_probability*100)}% fake</span><strong>${item.verdict_label}</strong></article>`).join(""):`<div class="history-empty">No media analyzed in this session.</div>`;
}
$("clear-history").addEventListener("click",async()=>{await fetch("/api/v1/clear",{method:"POST"});loadHistory();toast("History cleared")});
function escapeHtml(value){const node=document.createElement("div");node.textContent=value;return node.innerHTML}
function toast(message){const node=$("toast");node.textContent=message;node.classList.add("show");setTimeout(()=>node.classList.remove("show"),2600)}
