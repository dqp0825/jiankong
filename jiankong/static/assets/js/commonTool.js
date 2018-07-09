$(function () {
    $(".ajax-load").click(function () {
		
        var menuHref = $(this).attr("href");
        console.log($(this).attr("href"));
        if(menuHref&&menuHref!='#'){
            localStorage.setItem("menuClicked", menuHref);
        }

        localStorage.setItem("background", document.body.style.background);
    });
});
$(function () {

    var navnav = localStorage.getItem("navnav");
    if(navnav!=null){
        document.getElementById("navnav").className=navnav;
    }
    var logo = localStorage.getItem("logo");
    if(logo!=null){
        document.getElementById("logo").innerHTML=logo;
    }
    var background = localStorage.getItem("background");
    document.body.style.background=background;
    var menuHref = localStorage.getItem("menuClicked");
    if (menuHref&&menuHref!="#") {
        var theMenu = $("[href='" + menuHref + "']");
        theMenu.parent().addClass("lsl");
        var pMenu = theMenu.parent().parent().prev();
        var temp =pMenu.parent().parent().prop("class");
        if (temp && temp.indexOf("topnav menu-left-nest") >= 0) {
            //alert("选中菜单的所属菜单夹");
           // pMenu.trigger("click");//选中菜单的所属菜单夹
            setTimeout(function() {
                pMenu.click();
            }, 1000)

        } else {
            var ppMenu = pMenu.parent().parent().prev();
            ppMenu.trigger("click");
            pMenu.trigger("click");
        }

        //pMenu.parent().parent().prop("class").indexOf();//再上一层
    }
    localStorage.setItem("menuClicked", menuHref);
});
$.extend({goTo:function(url){//忽略项目根目录
    window.location.href = window.location.origin+"/"+window.location.pathname.split("/")[1]+url
}});
$.extend({getRootURL:function(){//忽略项目根目录
    return window.location.origin+"/"+window.location.pathname.split("/")[1];
}});
$.confirm = $.confirm || {};
$.confirm.options = {
    title: "请确认",
    confirmButton: "确认",
    cancelButton: "取消",
    post: false,
    confirmButtonClass: "btn-success",
    cancelButtonClass: "btn-default",
    dialogClass: "modal-dialog modal-sm"
};
