//后台管理界面用到的一些函数

function batch_do(entityName, action)
{
    if (confirm("确定要" + entityName + "?"))
    {
        if (!atleaseOneCheck())
        {
            alert('请至少选择一条记录' + entityName + '！');
            return;
        }
        var form = document.forms.dataform;
        form.action = action;
        form.submit();
    }
}

function openwin(url, width, height, scroll)
{
    if (!document.all)
    {
        document.captureEvents(Event.MOUSEMOVE);
        x = e.pageX + width - 30;
        y = e.pageY + height - 30;
    }
    else
    {
        x = document.body.scrollLeft + event.clientX + width - 30;
        y = document.body.scrollTop + event.clientY + height - 30;
    }
    window.open(url, "newWindow", "height=" + height + ", width=" + width + ", toolbar =no, menubar=no, scrollbars=" + scroll + ", resizable=no, location=no, status=no, top=" + y + ", left=" + x + "") //写成一行
}

//checkbox中至少有一项被选中
function atleaseOneCheck()
{
    var items = document.getElementsByName('itemlist');
    if (items.length > 0) {
        for (var i = 0; i < items.length; i++)
        {
            if (items[i].checked == true)
            {
                return true;
            }
        }
    } else {
        if (items.checked == true) {
            return true;
        }
    }
    return false;
}
function atleaseOneCheck()
{
    var items = document.getElementsByName('btSelectItem');
    if (items.length > 0) {
        for (var i = 0; i < items.length; i++)
        {
            if (items[i].checked == true)
            {
                return true;
            }
        }
    } else {
        if (items.checked == true) {
            return true;
        }
    }
    return false;
}

	function openNewWindow(viewPage)
     {
      window.open(viewPage,'','status=no,resizable=no,width=300,height=380,left=450,top=220');
     }



    //unselect all   
    function unselect() {   
      var i = document.getElementsByName("itemlist").length;   
      if (i == 1) {   
        document.forms.ec.itemlist.checked = false;   
      } else {   
        if (i > 1) {   
          for (i = 0; i < document.forms.ec.itemlist.length; i++) {   
            document.forms.ec.itemlist[i].checked = false;   
          }   
        }   
      }   
    }
function unselect() {
    var i = document.getElementsByName("btSelectItem").length;
    if (i == 1) {
        document.forms.ec.itemlist.checked = false;
    } else {
        if (i > 1) {
            for (i = 0; i < document.forms.ec.itemlist.length; i++) {
                document.forms.ec.itemlist[i].checked = false;
            }
        }
    }
}

// reference ext js 2.1
   function insertHTML(where, el, html){
	        where = where.toLowerCase();
	        if(el.insertAdjacentHTML){
	            switch(where){
	                case "beforebegin":
	                    el.insertAdjacentHTML('BeforeBegin', html);
	                    return el.previousSibling;
	                case "afterbegin":
	                    el.insertAdjacentHTML('AfterBegin', html);
	                    return el.firstChild;
	                case "beforeend":
	                    el.insertAdjacentHTML('BeforeEnd', html);
	                    return el.lastChild;
	                case "afterend":
	                    el.insertAdjacentHTML('AfterEnd', html);
	                    return el.nextSibling;
	            }
	            throw 'Illegal insertion point -> "' + where + '"';
	        }
	  			var range = el.ownerDocument.createRange();
	        var frag;
	        switch(where){
	             case "beforebegin":
	                range.setStartBefore(el);
	                frag = range.createContextualFragment(html);
	                el.parentNode.insertBefore(frag, el);
	                return el.previousSibling;
	             case "afterbegin":
	                if(el.firstChild){
	                    range.setStartBefore(el.firstChild);
	                    frag = range.createContextualFragment(html);
	                    el.insertBefore(frag, el.firstChild);
	                    return el.firstChild;
	                }else{
	                    el.innerHTML = html;
	                    return el.firstChild;
	                }
	            case "beforeend":
	                if(el.lastChild){
	                    range.setStartAfter(el.lastChild);
	                    frag = range.createContextualFragment(html);
	                    el.appendChild(frag);
	                    return el.lastChild;
	                }else{
	                    el.innerHTML = html;
	                    return el.lastChild;
	                }
	            case "afterend":
	                range.setStartAfter(el);
	                frag = range.createContextualFragment(html);
	                el.parentNode.insertBefore(frag, el.nextSibling);
	                return el.nextSibling;
	            }
	            throw 'Illegal insertion point -> "' + where + '"';
   			 }  
  
  //table event   
  function runTableOnClick(TableHandle){   
    var e = event.srcElement;   
    //alert("e.tagName is "+e.tagName);   
    //alert("e.rowIndex is "+e.rowIndex);   
    //alert("e.parentElement is "+e.parentElement);   
       
    if(typeof(e.tagName)=='undefined') return;     
    if (e.tagName == 'TABLE' || e.tagName == 'TR' || e.tagName == 'TBODY') return;   
    while (e.tagName != 'TR') e = e.parentElement;   
    //alert("e.tagName is "+e.tagName);   
    if (e.rowIndex == 0 || e.className == 'itemDisabled') return;   
    var el = e;   
    while (el.tagName != 'TABLE') el = el.parentElement;   
    //alert("el.rows.length is "+el.rows.length);   
    for (var i = 0; i < el.rows.length; i++){   
      if (el.rows(i).className == 'itemOver'){   
        el.rows(i).className = 'itemOut';   
        break;   
      }   
    }   
    e.className = 'itemOver';   
    //if (TableHandle != null){   
    //  if (event.button == 2) menuShow(TableHandle); else menuHide(TableHandle);   
    //}   
    }   
       
    //number only   
    function JHshNumberText()   
            {   
              if ( !(((window.event.keyCode >= 48) && (window.event.keyCode <= 57))&& (window.event.keyCode <= 90)))   
                {   
                  window.event.keyCode = 0 ;   
                  alert("请输入0-9之间的字符!");   
                }   
            }  
            
       //全选功能       
    function selectAll() {
      var i = document.getElementsByName("itemlist").length;   
   
          for (i = 0; i < document.getElementsByName("itemlist").length; i++) {   
            document.getElementsByName("itemlist")[i].checked = true;   
          }   
        
    }

      //全不选功能
   function unselect() {
      var i = document.getElementsByName("itemlist").length;

          for (i = 0; i < document.getElementsByName("itemlist").length; i++) {
            document.getElementsByName("itemlist")[i].checked = false;
      }
    }

    //反选功能
    function switchselect() {   
      var i = document.getElementsByName("itemlist").length;     
          for (i = 0; i < document.getElementsByName("itemlist").length; i++) {   
            document.getElementsByName("itemlist")[i].checked = !document.getElementsByName("itemlist")[i].checked;   
      }   
    }  

   //清空
   function queryReset() {
		for(i = 0; i < document.forms.queryform.length; i++){  
			if(document.forms.queryform[i].type == 'text' || document.forms.queryform[i].type == 'hidden') {  
				document.forms.queryform[i].value = '';  
			}
			else if(document.forms.queryform[i].type == 'select-one'){
				document.forms.queryform[i].selectedIndex=0;
			}
		}  
    }
function rowStyle(row, index) {
    var classes = [ 'success', 'info', 'warning', 'danger'];
    if (index % 2 === 0 && index / 2 < classes.length) {
        return {
            classes: classes[index / 2]
        };
    }
    return {};
}