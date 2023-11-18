

//Browser Detector
let userAgent = navigator.userAgent;
      let browser;
      if(userAgent.match(/edg/i)){
        browser = "edge";
      }else if(userAgent.match(/firefox|fxios/i)){
        browser = "firefox";
      }else if(userAgent.match(/opr\//i)){
        browser = "opera";
      }else if(userAgent.includes('MSIE')){
        browser = "explorer";
      }else if(userAgent.match(/chrome|chromium|crios/i)){
        browser = "chrome";
      }else if(userAgent.match(/safari/i)){
        browser = "safari";
      }else{
        alert("Other browser");
      }
      const logo = document.querySelector(`.features .icon.${browser}`);
      if(logo){
        logo.style.display = "inline-block";
      }

    // Online/Actve Status
    const online = document.querySelector(".online");
    window.onload = ()=>{
        function ajax(){
            let xhr = new XMLHttpRequest(); //creating new XML object
            xhr.open("GET", "https://jsonplaceholder.typicode.com/posts", true); //sending get request on this URL
            xhr.onload = ()=>{ //once ajax loaded
                //if ajax status is equal to 200 or less than 300 that mean user is getting data from that provided url
                //or his/her response status is 200 that means he/she is online
                if(xhr.status == 200 && xhr.status < 300){
                    online.style.backgroundColor = "rgb(0, 255, 0)";
                }else{
                    offline(); //calling offline function if ajax status is not equal to 200 or not less that 300
                }
            }
            xhr.onerror = ()=>{
                offline(); ////calling offline function if the passed url is not correct or returning 404 or other error
            }
            xhr.send(); //sending get request to the passed url
        }
    
        function offline(){ //function for offline
            online.style.backgroundColor = "#ccc";
        }
    
        setInterval(()=>{ //this setInterval function call ajax frequently after 100ms
            ajax();
        }, 100);
    }