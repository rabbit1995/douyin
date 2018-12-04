window.onload=function (){ 
	var allCheck=document.getElementById("allCheck"); 
	var ghostCheck=document.getElementById("ghostCheck"); 
	var noneCheck=document.getElementById("noneCheck"); 
	var dowmCheck=document.getElementById("dowmCheck"); 
	var list=document.getElementById("video_list");
	var checK=list.getElementsByTagName("input");
 
	allCheck.onclick=function(){    //全选 
        for(var i=0; i<checK.length ; i++){
		checK[i].checked=true;
		}   
	};

	ghostCheck.onclick=function(){    //反选 
        for(var i=0; i<checK.length ; i++){
            if(checK[i].checked==true){
               checK[i].checked=false;
            } 
            else{
                checK[i].checked=true;
            }
        }
	};

	noneCheck.onclick=function(){    //取消
        for(var i=0; i<checK.length ; i++){
              checK[i].checked=false;
        }
	};

	dowmCheck.onclick=function(){    //获取下载链接
		var check_val = "未选中";
		var text = document.getElementById('cptext');
		text.innerHTML = '';
		for(i in checK){
			if(checK[i].checked){
				link = checK[i].nextSibling.nextSibling;
				text.innerHTML += link.href;
				text.innerHTML += "<br>";
				check_val = "复制成功";
			};
		};
		alert(check_val)
	};

    function copyArticle(event) {
		const range = document.createRange();
		range.selectNode(document.getElementById('cptext'));

		const selection = window.getSelection();
		if(selection.rangeCount > 0) selection.removeAllRanges();
		selection.addRange(range);
		document.execCommand('copy');
    }
 
    document.getElementById('dowmCheck').addEventListener('click', copyArticle, false);
}