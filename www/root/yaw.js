var fps = 3;
var quality = 20;
var timeout = 1000/fps;
var baseURL = "http://127.0.0.1:8081/"; //change this to "http://_yawcam_computer_address:port/" when running on own server.
var t_;
var i_;
var ct_;
var id;
var xmlHttp;
var firstReq=true;
var state = "null";

function updateID()
{
	id = Math.random();
}

function setFps(val)
{
	fps = val;
	timeout = Math.round(1000.0/fps);
}

function setQ(val)
{
	quality = val;
}

function scaleIn()
{
	document.images.camImg.width = document.images.camImg.width + 40;
	document.images.camImg.height = document.images.camImg.height + 30;
}

function scaleOut()
{
	document.images.camImg.width = document.images.camImg.width - 40;
	document.images.camImg.height = document.images.camImg.height - 30;
}

function scaleOrg()
{
	document.images.camImg.width = 320;
	document.images.camImg.height = 240;
}

function showLayer(theLayer)
{
	getLayer(theLayer).style.display = "block";
}

function hideLayer(theLayer)
{
	getLayer(theLayer).style.display = "none";
}

function hideAllMenuLayers()
{
	hideLayer('menu_fps');
	hideLayer('menu_fps_child');
	hideLayer('menu_quality');
	hideLayer('menu_quality_child');
	hideLayer('menu_scale');
	hideLayer('menu_scale_child');
	hideLayer('menu_about');
	hideLayer('menu_about_child');
}

function hideAllMenuChildren()
{
	hideLayer('menu_fps_child');
	hideLayer('menu_quality_child');
	hideLayer('menu_scale_child');
	hideLayer('menu_about_child');
}

function showAllMenuCols()
{
	showLayer('menu_fps');
	showLayer('menu_quality');
	showLayer('menu_scale');
	showLayer('menu_about');
}

function fixMenuColPos(owner)
{
	setLyr(owner,'menu_fps',false,0);
	setLyr(owner,'menu_quality',false,1);
	setLyr(owner,'menu_scale',false,2);
	setLyr(owner,'menu_about',false,3);
}

function getLayer(theLayer)
{
	var obj = null;
	if (document.getElementById)
	{
		obj = document.getElementById(theLayer);
	}
	else if (document.all)
	{
		obj = document.all[theLayer];
	}
	else if (document.layers)
	{
		obj = document.layers[theLayer];
	}
	return obj;
}

function getMarker(val,testVal)
{
	var str = null;
	if(val == testVal)
	{
		str = "<img src=\"img/mrk.gif\" style=\"border:none;vertical-align: text-bottom;margin: 0px;\" alt=\"<--\">";
	}
	else 
	{
		str = "";
	}
	return str;
}

function showErrorImage()
{
	clearTimeout(t_);
	clearInterval(i_);
	document.images.camImg.onload = "";
	document.images.camImg.src = "/img/offline.jpg";
	window.status = "Webcam offline";
}

function reloadImage()
{
	var theDate = new Date();
	var url = baseURL + "out.jpg?";
	url += ("q="+quality);
	url += ("&id="+id);
	url += "&r=";
	url += theDate.getTime().toString();
	document.images.camImg.src = url;	
	window.status = "Yawcam streaming...";
}

function fixImageTimeout()
{
	t_ = setTimeout("reloadImage();",timeout);
}

function cTO()
{
	if(state=="running")
	{
		clearTimeout(t_);
		reloadImage();
	}
}

function updateFpsMenu()
{
	document.getElementById('fps_30').innerHTML = "30 " + getMarker(fps,30);
	document.getElementById('fps_15').innerHTML = "15 " + getMarker(fps,15);
	document.getElementById('fps_10').innerHTML = "10 " + getMarker(fps,10);
	document.getElementById('fps_5').innerHTML = "5 " + getMarker(fps,5);
	document.getElementById('fps_1').innerHTML = "1 " + getMarker(fps,1);
}

function updateQualityMenu()
{
	document.getElementById('q_75').innerHTML = "75 % " + getMarker(quality,75);
	document.getElementById('q_50').innerHTML = "50 % " + getMarker(quality,50);
	document.getElementById('q_40').innerHTML = "40 % " + getMarker(quality,40);
	document.getElementById('q_30').innerHTML = "30 % " + getMarker(quality,30);
	document.getElementById('q_20').innerHTML = "20 % " + getMarker(quality,20);
	document.getElementById('q_10').innerHTML = "10 % " + getMarker(quality,10);
	document.getElementById('q_5').innerHTML = "5 % " + getMarker(quality,5);
	document.getElementById('q_1').innerHTML = "1 % " + getMarker(quality,1);
}

function setLyr(obj,lyr,drop,col)
{
	var coors = findPos(obj);
	var x = document.getElementById(lyr);
	if(drop == true)
	{
		coors[1] = coors[1]+26;
	}
	x.style.top = coors[1] + 'px';
	coors[0] = coors[0]+(col*80);
	x.style.left = coors[0] + 'px';
}

function findPos(obj)
{
	var curleft = curtop = 0;
	if (obj.offsetParent) 
	{
		curleft = obj.offsetLeft
		curtop = obj.offsetTop
		while (obj = obj.offsetParent) 
		{
			curleft += obj.offsetLeft
			curtop += obj.offsetTop
		}
	}
	return [curleft,curtop];
}

function startPoll()
{	
	document.images.camImg.onload=fixImageTimeout
	var url=baseURL+"get?id="+id+"&r="+Math.random()
	document.images.camImg.src = url;	
	setTimeout("document.images.camImg.onerror=showErrorImage",2000);
}

function fixStatusTimeout()
{
	ts_ = setTimeout("getStatus();",2000);
}

function fixConnectTimeout()
{
	ct_ = setTimeout("showErrorImage();",4000);
}