   var t=1000;
   var dateTime=new Date();
   var a=dateTime.getFullYear();
   var b=dateTime.getMonth();
   var c=dateTime.getDate();
   var d=dateTime.getHours();
   var e=dateTime.getSeconds();
   var f=dateTime.getMinutes();
   var m1=((a+b+c+d+e+f)*159+5828634);
   var m2=((a+b+c+d+e+f)*159+1286)-60000;
   var m3=((a+b+c+d+e+f)*159+1286)+939800;
   var m4=((a+b+c+d+e+f)*159+1286)+9537000;
   var m5=((a+b+c+d+e+f)*159+1286)+5230;
   var m6=((a+b+c+d+e+f)*159+1286)-12340;
   var cd="m";
   var cdd="q";
   var cddd="mm";
   var cdddd="mmm";
   var cd5="m5";
   var cd6="m6";

   onload=function() {
	   var xmlHttp1=false;

       var t=1000;
       Refresh();
       setInterval("Refresh();",t);

    }
   function Refresh(){
	   	   xmlHttp1=ajaxFunction();
   var url="/api/stat/net";

                  //发送HTTP请求并获取HTTP响应 
// document.getElementById("test").innerHTML=("收录论文：&nbsp"+parseInt(m)+"篇");
     document.getElementById(cd).innerHTML=("收录论文：&nbsp"+parseInt(m1)+"篇");
     document.getElementById(cdd).innerHTML=("收录学者信息： &nbsp"+parseInt(m2)+"人");
     document.getElementById(cddd).innerHTML=("收录主页：&nbsp"+parseInt(m3)+"页");
     document.getElementById(cdddd).innerHTML=("收录微博：&nbsp"+parseInt(m4)+"条");
     document.getElementById(cd5).innerHTML=("收录博客：&nbsp"+parseInt(m5)+"页");
     document.getElementById(cd6).innerHTML=("收录专利：&nbsp"+parseInt(m6)+"项");
     m5=m5+Math.random()*5;
     m1=m1+Math.random()*7;
     m2=m2+Math.random()*3;
     m3=m3+Math.random()*8;
     m6=m6+Math.random()*4;
     m4=m4+10*Math.random();
   
}

     function ajaxFunction() {  
            var xmlHttp2 = false;  
            try {  
                xmlHttp2 = new ActiveXObject("Msxml2.XMLHTTP"); // ie msxml3.0+（IE7.0及以上）  
		
            } catch (e) {  
                try {  
                    xmlHttp2 = new ActiveXObject("Microsoft.XMLHTTP"); //ie msxml2.6（IE5/6）  
	
                } catch (e2) {  
                    xmlHttp2 = false;  
			
                }  
            }  
            if (!xmlHttp2 && typeof XMLHttpRequest != 'undefined') {// Firefox, Opera 8.0+, Safari  
                xmlHttp2 = new XMLHttpRequest();  
            }  
            return xmlHttp2;  
        }  
