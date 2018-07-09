/**
 * Created by Mr.Lin on 2017/1/23.
 */
var indexName = pageName();
if(indexName != "index.html") {
	$("body").css("background", "none");
}

//获取页面名称
function pageName() {
	var strUrl = location.href;
	var arrUrl = strUrl.split("/");
	var strPage = arrUrl[arrUrl.length - 1];
	return strPage;
}
setTimeout(function() {
	$("body").css("visibility", "inherit");
}, 1000);
setInterval(function() {
	$("#loading").hide();
}, 2000)

$(function() {
	$(".navUl>li").hover(function() {
		$(this).find("dl").fadeIn(200);
	}, function() {
		$(this).find("dl").fadeOut(200);
	});
});
$(window).resize(function() {
	bodyHeight();
});
$(function() {
	bodyHeight();
});

function bodyHeight() {
	$(document.body).height($(document).height());
	$("iframe").height($(document).height() - 106);
}
//row 高度
$(function (){
	var height = [];
//	for(var i = 0;i<$(".row>div");i++){
//		
//	}
	$.each($(".row"), function(index,i) {
		height.push($(".row").eq(index).outerHeight());
	});
})
//地图
function map(city) {
	//初始化地图对象，加载地图
	var map = new AMap.Map("container", {
		resizeEnable: true,
		center: [123.629189, 47.208843], //地图中心点
		zoom: 10 //地图显示的缩放级别
	});
	map.setMapStyle("blue_night");

	$.getJSON("../json/fps.json", function(data) {
		var arr = //构建多边形经纬度坐标数组
			data.mapDate.data;
		return new AMap.Polygon({
			map: map,
			path: arr,
			strokeColor: "#0000ff",
			strokeOpacity: 1,
			strokeWeight: 3,
			fillColor: "#f5deb3",
			fillOpacity: 0.35
		});
	});

	function getRootPath_web() {
		//获取当前网址，如： http://localhost:8083/uimcardprj/share/meun.jsp
		var curWwwPath = window.document.location.href;
		//获取主机地址之后的目录，如： uimcardprj/share/meun.jsp
		var pathName = window.document.location.pathname;
		var pos = curWwwPath.indexOf(pathName);
		//获取主机地址，如： http://localhost:8083
		var localhostPaht = curWwwPath.substring(0, pos);
		//获取带"/"的项目名，如：/uimcardprj
		var projectName = pathName.substring(0, pathName.substr(1).indexOf('/') + 1);
		return(localhostPaht + projectName);
	}
}
//地图end
//search strat
$(function() {
	$(".search").click(function() {
		if($("#iframe").contents().find("#search").css("display") == "none") {
			$("#iframe").contents().find("#search").fadeIn();
		} else {
			$("#iframe").contents().find("#search").fadeOut();
		}
	})
});
//search end
//蜘蛛网
function zzw(id, data, num) {
	var myChartzzw = echarts.init(document.getElementById(id));
	var dataBJ = num;

	var lineStyle = {
		normal: {
			width: 1,
			opacity: 1
		}
	};

	var option = {

		radar: {
			indicator: data,
			shape: 'circle',
			splitNumber: 5,
			radius: 30,
			name: {
				textStyle: {
					color: 'rgb(238, 197, 102)'
				}
			},
			splitLine: {
				lineStyle: {
					color: [
						'rgba(238, 197, 102, 0.6)', 'rgba(238, 197, 102, 0.2)',
						'rgba(238, 197, 102, 0.4)', 'rgba(238, 197, 102, 0.6)',
						'rgba(238, 197, 102, 0.8)', 'rgba(238, 197, 102, 1)'
					].reverse()
				}
			},
			splitArea: {
				show: false
			},
			axisLine: {
				lineStyle: {
					color: 'rgba(238, 197, 102, 0.5)'
				}
			}
		},
		series: [{
			type: 'radar',
			lineStyle: lineStyle,
			data: dataBJ,
			symbol: 'none',
			itemStyle: {
				normal: {
					color: '#a6985c'
				}
			},
			areaStyle: {
				normal: {
					opacity: 0.5
				}
			}
		}]
	};
	myChartzzw.setOption(option);
}
//饼状图
function bzt(id, data, title, dataname, x, y) {

	var myChart = echarts.init(document.getElementById(id));
	var option4 = {
		title: {
			text: title,
			textStyle: {
				color: '#fff',
				fontSize: 14
			}
		},
		color: ["#16c7ff", "#085562", "#2858d3", "#84dbf6", "#0b4395"],
		tooltip: {
			trigger: 'item',
			backgroundColor: 'rgba(255,255,255,0.85)',
			extraCssText: 'box-shadow: 0 0 3px rgba(0, 0, 0, 0.3);',
			borderColor: '#FFF',
			borderRadius: 0,
			textStyle: {
				color: '#666666',
				extraCssText: 'box-shadow: 0 0 3px rgba(0, 0, 0, 0.3);'
			},
			formatter: '{a} {b} : {c} ({d}%)'
		},

		legend: {
			orient: 'vertical',
			x: 'left',
			data: dataname,
			textStyle: {
				color: "#fff",
				fontSize: 8
			}
		},
		series: [{
			type: 'pie',
			center: ['50%', '50%'],
			radius: ['65%', '75%'],
			label: {
				normal: {
					show: false,
					position: 'center'
				}
			},
			data: data
		}]
	};
	myChart.setOption(option4);
}
//柱状图
function duozhu(id, title, legend, dataX, dataY) {
	var zhu = echarts.init(document.getElementById(id));
	option = {
		title: {
			text: title,
			textStyle: {
				color: "#fff"
			}
		},
		tooltip: {
			trigger: 'axis'
		},
		legend: {
			data: legend,
			textStyle: {
				color: "#FFF"
			}
		},
		toolbox: {
			show: true,
			feature: {
				dataView: {
					show: true,
					readOnly: false
				},
				magicType: {
					show: true,
					type: ['line', 'bar']
				},
				restore: {
					show: true
				},
				saveAsImage: {
					show: true
				}
			}
		},
		calculable: true,
		xAxis: [{
			type: 'category',
			data: dataX,
			axisLabel: {
				textStyle: {
					color: '#fff'
				}
			}
		}],
		yAxis: [{
			type: 'value',
			axisLabel: {
				textStyle: {
					color: '#fff'
				}
			}
		}],
		series: dataY
	};
	zhu.setOption(option);
}

//折线图
function zhexian(id, title, legend, dataX, dataY) {
	var zhe = echarts.init(document.getElementById(id));
	option = {
		title: {
			text: title,
			textStyle: {
				color: "#fff"
			}
		},
		legend: {
			data: legend,
			textStyle: {
				color: "#fff"
			}
		},
		grid: {
			left: '3%',
			right: '4%',
			bottom: '5%',
			containLabel: true
		},
		xAxis: [{
				type: 'category',
				boundaryGap: false,
				data: dataX,
				"axisLine": {
					lineStyle: {
						color: '#fff'
					}
				}
			}

		],
		yAxis: [{
			type: 'value',
			"axisLine": {
				lineStyle: {
					color: '#fff'
				}
			}
		}],
		"dataZoom": [{
			"show": true,
			"height": 30,
			"xAxisIndex": [
				0
			],
			bottom: 0,
			"start": 0,
			"end": 7,
			handleIcon: 'path://M306.1,413c0,2.2-1.8,4-4,4h-59.8c-2.2,0-4-1.8-4-4V200.8c0-2.2,1.8-4,4-4h59.8c2.2,0,4,1.8,4,4V413z',
			handleSize: '110%',
			handleStyle: {
				color: "#fff"
			},
			textStyle: {
				color: "#fff"
			},
			borderColor: "#fff"

		}, {
			"type": "inside",
			"show": true,
			"height": 15,
			"start": 1,
			"end": 35
		}],
		series: dataY
	};
	zhe.setOption(option);
}

//柱状图单
function dzhu(id, title, dataX, dataY) {
	var zhu = echarts.init(document.getElementById(id));
	option = {
		title: {
			text: '',
			textStyle: {
				color: "#fff"
			}
		},
		tooltip: {
			trigger: 'axis',
			axisPointer: { // 坐标轴指示器，坐标轴触发有效
				type: 'shadow' // 默认为直线，可选为：'line' | 'shadow'
			}
		},
		grid: {
			left: '3%',
			right: '4%',
			bottom: '3%',
			containLabel: true
		},
		xAxis: [{
			type: 'category',
			data: dataX,
			axisTick: {
				alignWithLabel: true
			},
			axisLabel: {
				textStyle: {
					color: '#fff'
				}
			}
		}],
		yAxis: [{
			type: 'value',
			axisLabel: {
				textStyle: {
					color: '#fff'
				}
			}
		}],
		series: [{
			name: title,
			type: 'bar',
			barWidth: '60%',
			data: dataY,
			itemStyle: {
				normal: {
					color: "#16c7ff"
				}
			}
		}]
	};
	zhu.setOption(option);
}

//折线图无工具条
function zhexianno(id, title, legend, dataX, dataY) {
	var zhe = echarts.init(document.getElementById(id));
	option = {
		title: {
			text: title,
			textStyle: {
				color: "#fff"
			}
		},
		legend: {
			data: legend,
			textStyle: {
				color: "#fff"
			}
		},
		grid: {
			left: '3%',
			right: '4%',
			bottom: '5%',
			containLabel: true
		},
		xAxis: [{
				type: 'category',
				boundaryGap: false,
				data: dataX,
				"axisLine": {
					lineStyle: {
						color: '#fff'
					}
				}
			}

		],
		yAxis: [{
			type: 'value',
			"axisLine": {
				lineStyle: {
					color: '#fff'
				}
			}
		}],
		series: dataY
	};
	zhe.setOption(option);
}
//横柱
function hzhu(id, title, datax, datay) {
	var zhu = echarts.init(document.getElementById(id));
	option = {
		title: {
			text: title,
			textStyle: {
				color: "#fff"
			}
		},
		tooltip: {
			trigger: 'axis',
			axisPointer: {
				type: 'shadow'
			}
		},
		grid: {
			left: '3%',
			right: '4%',
			bottom: '3%',
			containLabel: true
		},
		xAxis: {
			type: 'value',
			boundaryGap: [0, 0.01],
			axisLabel: {
				textStyle: {
					color: '#fff'
				}
			}
		},
		yAxis: {
			type: 'category',
			data: datax,
			axisLabel: {
				textStyle: {
					color: '#fff'
				}
			}
		},
		series: [{
			name: title,
			type: 'bar',
			data: datay
		}, ]
	};
	zhu.setOption(option);
}

//导航
$(function() {
	$(".navUl").find("a").click(function() {
		$("#loading").show();
		var innerHtml = $(this).html();
		var href = $(this).attr("href");
		var pphrefl = $(this).parent().parent().parent().children().attr("href");
		var ppinnreHtml = $(this).parent().parent().parent().children().html();
		//console.log($(this).parent().siblings().find("a").html());
		//console.log($(this).parents("li").index());
		switch($(this).parents("li").index()) {
			case 0:
				$(".logoText").html("精准扶贫大数据");
				break;
			case 1:
				$(".logoText").html("综治维稳大数据");
				break;
			case 2:
				$(".logoText").html("农业大数据");
				break;
			case 3:
				$(".logoText").html("旅游大数据");
		}

		if($(this).parent("dt").length == 0) {
			$("#break").html("<li><a href='" + href + "' target='iframe'>" + innerHtml + "</a><li>");
		} else {
			$("#break").html("<li><a href='" + pphrefl + "' target='iframe'>" + ppinnreHtml + "</a>&gt;<li><li><a href='" + href + "' target='iframe'>" + innerHtml + "</a><li>");
		}
	})
});

//组合柱状图and饼状图 斜字体
function zuandbing(id, zuTitle, bingTitle, zhuTitPos, bingTitPos) {
	//id,柱状图标题，饼状图标题，柱状图标题x轴位置，饼状图标题x轴位置，饼状图大小
	var myChart = echarts.init(document.getElementById(id));
	var builderJson = {
		"all": 32156,
		"charts": {
			"bar": 22612,
			"line": 23476,
			"pie": 21905,
			"lines": 5515,
			"scatter": 6058,
			"candlestick": 5144,
			"radar": 5659,
			"heatmap": 4451,
			"treemap": 4068,
			"map": 8774,
			"graph": 5246,
			"boxplot": 3881,
			"parallel": 4995,
			"gauge": 5352,
			"funnel": 4253,
			"sankey": 4077
		},
		"ie": 28022
	};

	var downloadJson = {
		"echarts.min.js": 41934,
		"echarts.simple.min.js": 11908,
		"echarts.common.min.js": 18612,
		"echarts.js": 53093
	};

	var option = {
		title: [{
			text: zuTitle,
			subtext: '总计 ' + builderJson.all,
			x: zhuTitPos,
			textAlign: 'center'
		}, {
			text: bingTitle,
			subtext: '总计 ' + Object.keys(downloadJson).reduce(function(all, key) {
				return all + downloadJson[key];
			}, 0),
			x: bingTitPos,
			textAlign: 'center'
		}],
		grid: [{
			top: 50,
			width: '50%',
			bottom: '45%',
			left: 10,
			containLabel: true
		}, {
			top: '55%',
			width: '50%',
			bottom: 0,
			left: 10,
			containLabel: true
		}],
		xAxis: [{
			type: 'value',
			max: builderJson.all,
			splitLine: {
				show: false
			}
		}],
		yAxis: [{
			type: 'category',
			data: Object.keys(builderJson.charts),
			axisLabel: {
				interval: 0,
				rotate: 30
			},
			splitLine: {
				show: false
			}
		}],
		series: [{
			type: 'bar',
			stack: 'chart',
			z: 3,
			label: {
				normal: {
					position: 'right',
					show: true
				}
			},
			data: Object.keys(builderJson.charts).map(function(key) {
				return builderJson.charts[key];
			})
		}, {
			type: 'bar',
			stack: 'chart',
			silent: true,
			itemStyle: {
				normal: {
					color: '#eee'
				}
			},
			data: Object.keys(builderJson.charts).map(function(key) {
				return builderJson.all - builderJson.charts[key];
			})
		}, {
			type: 'pie',
			radius: [0, '30%'],
			center: ['75%', '25%'],
			data: Object.keys(downloadJson).map(function(key) {
				return {
					name: key.replace('.js', ''),
					value: downloadJson[key]
				}
			})
		}]
	};
	myChart.setOption(option);
}
//男女占比
function man(id, womenValue, womenName, manValue, manName, border, border01, title, show, pos, pos1) {
	var man = echarts.init(document.getElementById(id));
	var option = {
		title: {
			text: title,
			x: "center",
			y: "top",
			textStyle: {
				color: '#fff',
				fontSize: 12
			}
		},
		"series": [{
			"center": [
				"25.0%",
				"50%"
			],
			"radius": [
				"49%",
				"50%"
			],
			"clockWise": pos1,
			"hoverAnimation": pos1,
			"type": "pie",
			"itemStyle": {
				"normal": {
					"label": {
						"show": show,
						"textStyle": {
							"fontSize": 15,
							"fontWeight": "bold"
						},
						"position": pos
					},
					"labelLine": {
						"show": pos1
					},
					"color": "#5886f0",
					"borderColor": "#5886f0",
					"borderWidth": border
				},
				"emphasis": {
					"label": {
						"textStyle": {
							"fontSize": 15,
							"fontWeight": "bold"
						}
					},
					"color": "#5886f0",
					"borderColor": "#5886f0",
					"borderWidth": border01
				}
			},
			"data": [{
				"value": manValue,
				"name": manName
			}, {
				"name": " ",
				"value": 47.3,
				"itemStyle": {
					"normal": {
						"label": {
							"show": false
						},
						"labelLine": {
							"show": false
						},
						"color": "#5886f0",
						"borderColor": "#5886f0",
						"borderWidth": 0
					},
					"emphasis": {
						"color": "#5886f0",
						"borderColor": "#5886f0",
						"borderWidth": 0
					}
				}
			}]
		}, {
			"center": [
				"75.0%",
				"50%"
			],
			"radius": [
				"49%",
				"50%"
			],
			"clockWise": pos1,
			"hoverAnimation": pos1,
			"type": "pie",
			"itemStyle": {
				"normal": {
					"label": {
						"show": show,
						"textStyle": {
							"fontSize": 15,
							"fontWeight": "bold"
						},
						"position": pos
					},
					"labelLine": {
						"show": pos1
					},
					"color": "#ee3a3a",
					"borderColor": "#ee3a3a",
					"borderWidth": border
				},
				"emphasis": {
					"label": {
						"textStyle": {
							"fontSize": 15,
							"fontWeight": "bold"
						}
					},
					"color": "#ee3a3a",
					"borderColor": "#ee3a3a",
					"borderWidth": border01
				}
			},
			"data": [{
				"value": womenValue,
				"name": womenName
			}, {
				"name": " ",
				"value": 52.7,
				"itemStyle": {
					"normal": {
						"label": {
							"show": false
						},
						"labelLine": {
							"show": false
						},
						"color": "#ee3a3a",
						"borderColor": "#ee3a3a",
						"borderWidth": 0
					},
					"emphasis": {
						"color": "#ee3a3a",
						"borderColor": "#ee3a3a",
						"borderWidth": 0
					}
				}
			}]
		}]
	};
	man.setOption(option);
}
//双饼状图
function doubleBing(id) {
	var double = echarts.init(document.getElementById(id));
	var option = {
		tooltip: {
			trigger: 'item',
			formatter: "{a} <br/>{b}: {c} ({d}%)"
		},
		legend: [{
			orient: 'vertical',
			left: 'left',
			top: 'center',
			data: ['直达', '营销广告', '搜索引擎', '邮件营销', '联盟广告', '视频广告']
		}, {
			orient: 'vertical',
			left: 'right',
			top: 'center',
			data: ['百度', '谷歌', '必应', '其他']
		}],
		series: [{
			type: 'pie',
			selectedMode: 'single',
			radius: [0, '20%'],

			label: {
				normal: {
					position: 'inner'
				}
			},
			labelLine: {
				normal: {
					show: false
				}
			},
			data: [{
				value: 335,
				name: '直达',
				selected: true
			}, {
				value: 679,
				name: '营销广告'
			}, {
				value: 1548,
				name: '搜索引擎'
			}]
		}, {
			name: '访问来源',
			type: 'pie',
			radius: ['40%', '55%'],

			data: [{
				value: 335,
				name: '直达'
			}, {
				value: 310,
				name: '邮件营销'
			}, {
				value: 234,
				name: '联盟广告'
			}, {
				value: 135,
				name: '视频广告'
			}, {
				value: 1048,
				name: '百度'
			}, {
				value: 251,
				name: '谷歌'
			}, {
				value: 147,
				name: '必应'
			}, {
				value: 102,
				name: '其他'
			}]
		}]
	};
	double.setOption(option);
}
//套饼
function tbing(id, wailegend, waidata, neilegend, neidata) {
	var tbdiv = echarts.init(document.getElementById(id));
	var option = {
		tooltip: {
			trigger: 'item',
			formatter: "{a} <br/>{b}: {c} ({d}%)"
		},
		legend: [{
			orient: 'vertical',
			left: 'left',
			top: 'center',
			data: wailegend,
			textStyle: {
				color: "#fff"
			}
		}, {
			orient: 'vertical',
			left: 'right',
			top: 'center',
			data: neilegend,
			textStyle: {
				color: "#fff"
			}
		}],
		series: [{
			name: '',
			type: 'pie',
			selectedMode: 'single',
			radius: [0, '30%'],

			label: {
				normal: {
					position: 'inner',
					show: false
				}
			},
			labelLine: {
				normal: {
					show: false
				}
			},
			data: neidata
		}, {
			name: '',
			type: 'pie',
			radius: ['40%', '55%'],

			data: waidata
		}]
	};
	tbdiv.setOption(option);
}
//实心饼
function sxbing(id, blegend, datas) {
	var sxdiv = echarts.init(document.getElementById(id));
	var option = {
		tooltip: {
			trigger: 'item',
			formatter: "{a} <br/>{b} : {c} ({d}%)"
		},
		legend: {
			orient: 'vertical',
			x: 'left',
			data: blegend,
			textStyle: {
				color: "#fff"
			}
		},
		textStyle: {
			color: "#fff"
		},
		series: [{
			name: '访问来源',
			type: 'pie',
			selectedMode: 'single',
			radius: '55%',
			center: ['50%', '60%'],
			data: datas,
			itemStyle: {
				normal: {
					color: '',
					borderWidth: 0.5,
					borderColor: '#ffffff'
				},
				emphasis: {
					color: '#fff',
					shadowBlur: 10,
					shadowOffsetX: 0,
					shadowColor: 'rgba(0, 0, 0, 0.5)'
				}
			}
		}]
	};
	sxdiv.setOption(option);
}