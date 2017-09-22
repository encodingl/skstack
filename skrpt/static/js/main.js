;(function($,window,document,undefined){

$.fn.dataAnalysis = function(options){
	var o = new dataAnalysis(this,options);
	o.init();
	return this;
};

var dataAnalysis = function(ele,opt){
	this.el = ele;
	this.defaults = {
		isControl : false,
		bathSpace : 30, //坐标偏移
/*		data : {
			type : "line-number",
			horizontal: [0,5,10,15,20,25], //横坐标
			vertical  : [0,10,20,30,40,50,60],  //纵坐标
			horiUnit : "分钟", //横坐标单位
			vertUnit : "人",   //纵坐标单位
			title	: "图书馆周末人流量", //图表标题
			project : [
				{
					name : "China",
					style: "#66ccff",
					points:[[0,10],[13,20],[15,50],[17,10],[25,20]]
				},
				{
					name : "Jppan",
					style: "#F5601F",
					points:[[5,20],[10,22],[15,30],[17,40],[25,60]]
				}
			]
		}
*/
/*		data : {
			type : "line-string",
			horizontal: ["1月","2月","3月","4月","5月","6月"], //横坐标
			vertical  : [0,10,20,30,40,50,60],  //纵坐标
			title	: "2015年每月得奖人数", //图表标题
			project : [
				{
					name : "China",
					style: "#66ccff",
					points:[["1月",10],["2月",20],["3月",50],["4月",10],["5月",20],["6月",15]]
				},
				{
					name : "Jppan",
					style: "#F5601F",
					points:[["1月",20],["2月",22],["3月",30],["4月",40],["5月",60],["6月",16]]
				}
			]
		}
*/
/*		data : {
			type : "cylindricality",
			horizontal: ["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"], //横坐标
			vertical  : [0,10,20,30,40,50,60],  //纵坐标
			title	: "2015年每月得奖人数", //图表标题
			project : [
				{
					name : "China",
					style: "#66ccff",
					points:[["1月",10],["2月",20],["3月",50],["4月",10],["5月",20],["6月",15],
					["7月",10],["8月",20],["9月",50],["10月",10],["11月",20],["12月",15]]
				},
				{
					name : "Jppan",
					style: "#F5601F",
					points:[["1月",20],["2月",60],["3月",20],["4月",30],["5月",40],["6月",10],
					["7月",20],["8月",20],["9月",40],["10月",50],["11月",10],["12月",15]]
				},
				{
					name : "US",
					style: "#F52C9D",
					points:[["1月",30],["2月",30],["3月",40],["4月",50],["5月",60],["6月",15],
					["7月",10],["8月",10],["9月",20],["10月",30],["11月",40],["12月",15]]
				}
			]
		}
*/
		data : {
			type : "circle",
			title	: "2015年GDP所占比预测", //图表标题
			project : [
				{
					name : "China",
					style: "#66ccff",
					percent: 20
				},
				{
					name : "Jppan",
					style: "#F5601F",
					percent: 10
				},
				{
					name : "US",
					style: "#F52C9D",
					percent: 25
				},
				{
					name : "Others",
					style: "#A2BC1D",
					percent: 45
				}
			]
		}
	};
	this.options = $.extend({},this.defaults,opt);
};

dataAnalysis.prototype = {
	init : function(){
		this.angle = 0; // 记录圆形统计图角度
		this.errorExist = false; //记录是否存在错误

		this.eleCreate().canvasCreate();
		//是否显示控制元件
		if(this.options.isControl){
			this.eleCreate().controlEleCreate();
			this.elEvent();
		} else {
			var opt = this.options;
			this.handing(opt);
		}
	},

	handing : function(opt){
		this.canvasAll().canvasInit();

		if(opt.data.type!="circle") //非圆形统计图时
		this.canvasAll().canvasAxis(opt.data.horizontal,opt.data.vertical);

		for(var i=0,j=opt.data.project.length;i<j;i++)
		{
			var pro = opt.data.project[i],
				len = opt.data.project.length,
				pos = (i+1) * opt.bathSpace;
			this.dataHandling().nameHanding(pro.name,(opt.data.title || ""),pro.style,pos);

			if(opt.data.type!="circle")
			this.dataHandling().pointsHanding(pro.points,pro.style,len,i);
			else
			this.dataHandling().circleHanding(pro.percent,pro.style,i);
		}

		//错误检测
		if(this.errorExist)
		{
			var cv = $('#canvas')[0],
				ct = cv.getContext('2d');
			ct.clearRect(0,0,cv.width,cv.height);
			return;
		}
	},

	eleCreate : function(){
		var $el = $(this.el);
		var dataAna = this;
		var ec = {
			canvasCreate:function(){
				var canvas = document.createElement('canvas');
				var $width = $el.width(),
					$height= $el.height();

				canvas.width = $width;
				canvas.height= $height;
				canvas.id	 = "canvas";


				dataAna.addToHtml($el,canvas);
			},

			controlEleCreate:function(){
				var temp = '<div id="control-fn">'+
							'<div class="points">'+
							'</div>'+
							'<div class="selector"><select>'+
							'<option selected="selected">请选择</option>'+
							'<option value="line-number">折线图(数字)</option>'+
							'<option value="line-string">折线图(横坐标为字符)</option>'+
							'<option value="cylindricality">柱状图</option>'+
							'<option value="circle">圆形图</option>'+
							'</select>'+
							'<span>图表标题：</span><input type="text" class="cTitle"/>'+
							'<span class="unit"><span>横坐标单位：</span><input type="text" class="horiUnit"/>'+
							'<span>纵坐标单位：</span><input type="text" class="vertUnit"/></span>'+
							'</div>'+
							'<div class="axis">'+
							'<input type="text" placeholder="请按顺序输入横坐标，以“,”分隔" class="hori"/>'+
							'<input type="text" placeholder="请按顺序输入纵坐标，以“,”分隔" class="vert"/>'+
							'<button class="axis-create">生成坐标</button>'+
							'</div>'+
							'<div class="control">'+
							'<div>'+
							'<button id="add">增加</button>'+
							'<input type="text" placeholder="1" id="point-num">'+
							'<span>个点</span>'+
							'</div>'+
							'<div>'+
							'<button id="do">生成</button>'+
							'</div>'+
							'</div>'+
							'</div>';

				dataAna.addToHtml($el,temp);
			},

			pointsPositionCreate:function(num){
				if(!num || num=="") num = 0;
				num = num>=20?20:num;
				var temp = "";

				if(dataAna.options.data.type!="circle")
				{
					temp = '<div><em>名称：</em><input type="text" placeholder="Zhang" class="lName"><em>颜色：</em><input type="text" placeholder="#ccffee" class="lStyle"></div>';
					for(var i=1,j=num;i<=j;i++){
						temp+='<span><em>'+i+'.</em>( <input type="text" placeholder="0"> , <input type="text" placeholder="0"> )</span>';
					}
				}
				

				if(dataAna.options.data.type=="circle"){
					for(var i=1,j=num;i<=j;i++){
						temp+='<span><em>'+i+'.</em>(名称：<input type="text" placeholder="ABC" class="cName">，所占比：<input type="text" placeholder="0" class="cPercent">%，颜色：<input type="text" placeholder="#000" class="cStyle"></span>)。';
					}
				}
				

				var $points = $('.points');
				$points.html("");

				dataAna.addToHtml($points,temp);
			}
		};

		return ec;
	},

	addToHtml : function($wrapElement,ele){
		$wrapElement.append(ele);
	},

	elEvent : function(){
		var $el = $(this.el);
		var dataAna = this;
		var cv = $('#canvas')[0],
			ct = cv.getContext('2d');

		evInit();

		function evInit(){
			$('.axis').hide();
			$('.control').hide();
			$('.unit').hide();

			domControl();
			axisCreate();
		}
		
		function addPoints(){
			$('#add').off('click').on('click',function(e){
				var num = $("#point-num").val();
				dataAna.eleCreate().pointsPositionCreate(num);
			});
		}

		function domControl(){
			$('.selector>select').on('change',function(e){
				var val = $(this).val();
				dataAna.options.data.type = val;

				$('.unit').hide();
				$('.axis').show();
				$('.control').hide();
				$('.points').html("");
				$('.axis>input').val("");
				ct.clearRect(0,0,cv.width,cv.height);
				dataAna.options.data.project.length = 0;

				if(val=="line-number")
				$('.unit').show();

				if(val=="circle")
				{
					$('.axis').hide();
					$('.control').fadeIn(200);
				}

				addPoints();
				buildImage();
			});
		}

		function axisCreate(){
			$('.axis-create').off('click').on('click',function(e){
				var horiaxis = $('.hori').val(),
					vertaxis = $('.vert').val();

				if(!horiaxis || !vertaxis)
				return;


				dataAna.options.data.horizontal = horiaxis.split(',');
				dataAna.options.data.vertical	= vertaxis.split(',');

				var hori = dataAna.options.data.horizontal,
					vert = dataAna.options.data.vertical;

				for(i=0,j=vert.length;i<j;i++){
					vert[i] = Number(vert[i]);
				}

				if(dataAna.options.data.type=="line-number")
				for(i=0,j=hori.length;i<j;i++)
				{
					hori[i] = Number(hori[i]);
				}

				$('.control').fadeIn(200);
			});
		}

		function buildImage(){
			$('#do').off('click').on('click',function(e){
				var length = $('.points>span').length;
				if(length==0)
				return;
				var x,y,z;
				var pro = dataAna.options.data.project;
				dataAna.options.data.title = $('.cTitle').val()?$('.cTitle').val():"";

				var len = pro.length;

				pro[len] = {};
				pro[len].points = new Array();

				for(var i=0,j=length;i<j;i++)
				{
					x = $('.points>span').eq(i).find('input').eq(0).val();
					y = $('.points>span').eq(i).find('input').eq(1).val();

					if(!x || !y){
						alert("请确定所以点坐标均填写完成！");
						pro.length = 0;
						return;
					}

					if(dataAna.options.data.type!="circle")
					{
						if(dataAna.options.data.type=="line-number")
						{
							x = Number(x);
							dataAna.options.data.vertUnit = $('.vertUnit').val()?$('.vertUnit').val():"";
							dataAna.options.data.horiUnit = $('.horiUnit').val()?$('.horiUnit').val():"";
						}

						pro[len].points[i] = new Array();
						pro[len].points[i][0] = x;
						pro[len].points[i][1] = Number(y);
						pro[len].name = $('.lName').val()?$('.lName').val():"未知";
						pro[len].style = $('.lStyle').val()?$('.lStyle').val():"#66ccff";
					} else {
						pro.length = j;
						pro[i] = {};
						var z = $('.points>span').eq(i).find('input').eq(2).val();
						pro[i].name = x?x:"未知";
						pro[i].style = z?z:"#5cc3de";
						pro[i].percent = Number(y)?Number(y):"";
					}	
				}

				if(dataAna.options.data.type=="cylindricality" || dataAna.options.data.type=="circle")
				{
					var cv = $('#canvas')[0],
						ct = cv.getContext('2d');

					ct.clearRect(0,0,cv.width,cv.height);
				}

				dataAna.handing(dataAna.options);
			});
		}
		
	},

	canvasAll : function(){
		var dataAna = this;
		var $el = $(this.el);
		var cv = $('#canvas')[0],
			ct = cv.getContext('2d');

		var $width = $('#canvas').width(),
			$height= $('#canvas').height();

		var bathSpace = this.options.bathSpace;

		var ev = {
			canvasInit : function(){
				var space = 10;
				var lenX = Math.floor($width/space),
					lenY = Math.floor($height/space);

				for(var i=1,j=lenX;i<=j;i++)
				{
					var x = i * space;
					dataAna.canvasAll().canvasDraw.drawLine(x,0,x,$height,"#E7E7E7");
				}

				for (var i = 1,j=lenY; i <= j; i++) {
					var y = i * space;
					dataAna.canvasAll().canvasDraw.drawLine(0,$height-y,$width,$height-y,"#E7E7E7");
				};

			},

			canvasAxis : function(hor,ver){
				if(dataAna.options.data.type=="cylindricality" && hor[0]!=0)
				{
					hor.reverse();
					hor.push(0);
					hor.reverse();
				}

				var lenHor = hor.length,
					lenVer = ver.length;

				if(lenHor==0 || lenVer==0)
				return;

				var	bathLength= 10;

				//hori
				dataAna.canvasAll().canvasDraw.drawLine(bathSpace,$height-bathSpace,$width,$height-bathSpace,"#000000");
				//画X坐标点
				for(var i = 0;i<lenHor;i++)
				{
					//错误检测
					dataAna.errorHanding("横坐标",hor[i]);

					var x = bathSpace + (i / lenHor)*($width-bathSpace);
					dataAna.canvasAll().canvasDraw.drawLine(x,$height-bathSpace,x,$height-bathLength-bathSpace,"#000000");
					dataAna.canvasAll().canvasDraw.drawText(hor[i],x,$height-bathSpace/2,"14px tohoma");
				}
				
				//vert
				dataAna.canvasAll().canvasDraw.drawLine(bathSpace,$height-bathSpace,bathSpace,0,"#000000");
				//画Y坐标点
				for(var i = 0;i<lenVer;i++)
				{
					//错误检测
					dataAna.errorHanding("纵坐标",ver[i],"ver");

					var y = bathSpace + (i / lenVer)*($height-bathSpace);
					dataAna.canvasAll().canvasDraw.drawLine(bathSpace,$height-y,bathLength+bathSpace,$height-y,"#000000");
					dataAna.canvasAll().canvasDraw.drawText(ver[i],bathSpace/2,$height-y,"14px tohoma");
				}

				//绘制单位
				if(dataAna.options.data.type=="line-number"){
					dataAna.canvasAll().canvasDraw.drawText("("+dataAna.options.data.horiUnit+")",$width-bathSpace,$height-bathSpace/2,"12px Microsoft YaHei");
					dataAna.canvasAll().canvasDraw.drawText("("+dataAna.options.data.vertUnit+")",bathSpace/2,bathSpace/2,"12px Microsoft YaHei");
				}

			},

			canvasDraw  : {
				drawLine : function(x1,y1,x2,y2,lineStyle){
					if(!lineStyle || lineStyle=="")
					lineStyle = "#66ccff";

					ct.save();
					ct.strokeStyle = lineStyle;
					ct.beginPath();
					ct.moveTo(x1,y1);
					ct.lineTo(x2,y2);
					ct.closePath();
					ct.stroke();
					ct.restore();
				},

				drawCircle : function(x,y,startAngle,endAngle,radius,circleStyle){
					startAngle = startAngle/180 * Math.PI;
					endAngle   = endAngle/180 * Math.PI;

					if(!circleStyle || circleStyle=="")
					circleStyle = "#66ccff";

					ct.save();
					ct.beginPath();
					ct.strokeStyle = "#c0c0c0";
					ct.fillStyle = circleStyle;
					ct.arc(x,y,radius,startAngle,endAngle,false);
					ct.closePath();
					ct.fill();
					ct.stroke();
					ct.restore();

				},

				drawText : function(text,x,y,font,align,base,color){
					if(!font || font=="")
					font = "12px tohoma";

					if(!align || align=="")	
					align = "center";

					if(!base || base =="")
					base = "middle";

					if(!color || color == "")
					color = "#000000";

					ct.save();
					ct.font = font;
					ct.textAlign = align;
					ct.textBaseline = base;
					ct.fillStyle = color;
					ct.fillText(text,x,y);
					ct.restore();
				},

				drawRect : function(x,y,width,height,style){
					ct.save();
					ct.fillStyle = style;
					ct.fillRect(x,y,width,height);
					ct.restore();

					ct.save();
					ct.beginPath();
					ct.strokeStyle = "#c0c0c0";
					ct.rect(x,y,width,height);
					ct.closePath();
					ct.stroke();
					ct.restore();
				},

				drawSector : function(x,y,startAngle,endAngle,radius,sectorStyle){
					startAngle = startAngle/180 * Math.PI;
					endAngle   = endAngle/180 * Math.PI;

					if(!sectorStyle || sectorStyle=="")
					circleStyle = "#66ccff";

					ct.save();
					ct.beginPath();
					ct.translate(x,y);
					ct.strokeStyle = "#c0c0c0";
					ct.fillStyle = sectorStyle;
					ct.moveTo(0,0);
					ct.arc(0,0,radius,startAngle,endAngle,false);
					ct.closePath();
					ct.fill();
					ct.stroke();
					ct.restore();
				}
			}
		};

		return ev;	
	},

	dataHandling : function(){
		var dataAna = this,
			$ev = $(this.el),
			opt = this.options,
			bathSpace = opt.bathSpace,
			cv = $('#canvas')[0],
			ct = cv.getContext('2d'),
			$width = $('#canvas').width(),
			$height= $('#canvas').height();

		var ev = {
			nameHanding : function(name,title,style,pos){
				dataAna.canvasAll().canvasDraw.drawText(name,$width-bathSpace,pos,"14px impact","center","top");
				dataAna.canvasAll().canvasDraw.drawRect($width-bathSpace*3,pos,bathSpace,bathSpace/2,style);
				dataAna.canvasAll().canvasDraw.drawText(title,$width/2,6,"24px Microsoft YaHei","center","top","#a0c010");
			},

			circleHanding : function(percent,style,index){
				//错误检测
				dataAna.errorHanding("百分比",percent);

				var x = ($width - bathSpace)/2 + bathSpace,
					y = ($height - bathSpace)/2;

				var radius = bathSpace*3;

				var angle = dataAna.angle + percent/100*360;

				//绘制扇形
				dataAna.canvasAll().canvasDraw.drawSector(x,y,dataAna.angle,angle,radius,style);
				//绘制数据
				dataAna.canvasAll().canvasDraw.drawRect(bathSpace*(index+1)*2,$height-bathSpace,bathSpace,bathSpace/2,style);
				dataAna.canvasAll().canvasDraw.drawText(percent+"%",bathSpace*(index+1.75)*2,$height-bathSpace*3/4,"13px Microsoft YaHei");

				dataAna.angle = angle;
			},

			pointsHanding : function(points,style,num,index){
				var len = points.length, //点数
					horizontal = opt.data.horizontal,
					vertical   = opt.data.vertical,
					lenHor = horizontal.length || 0,
					lenVer = vertical.length || 0;


				for(var i=0;i<len;i++){
					var horVal = points[i][0], //横坐标值
						vertVal = points[i][1];//纵坐标值

					//错误检测
					dataAna.errorHanding("点-横坐标",horVal,"hor");
					dataAna.errorHanding("点-纵坐标",vertVal,"ver");

					switch(opt.data.type){
						case "line-number" : //全数字折线图
						allNumber(i);
						break;
						case "line-string" : //横坐标为字符串的折线图
						lineString(i);
						break;
						case "cylindricality": //柱形
						cylindricality(i);
						break;
						defaults :
						alert("error");
						break;
					}
				}

				function allNumber(i){
					horVal = horVal - horizontal[0];
					vertVal = vertVal - vertical[0];

					var	x_before = bathSpace + (horVal/(horizontal[lenHor-1]-horizontal[0])) * ($width-bathSpace)*((lenHor-1)/lenHor),
						y_before = $height -(bathSpace + (vertVal/(vertical[lenVer-1]-vertical[0])) * ($height-bathSpace)*((lenVer-1)/lenVer));
					
					//绘制点
					dataAna.canvasAll().canvasDraw.drawCircle(x_before,y_before,0,360,4,style);

					//绘制线
					if(i!=len-1){
						var x_after = bathSpace + ((points[i+1][0]-horizontal[0])/(horizontal[lenHor-1]-horizontal[0])) * ($width-bathSpace)*((lenHor-1)/lenHor),
							y_after = $height -(bathSpace + ((points[i+1][1]-vertical[0])/(vertical[lenVer-1]-vertical[0])) * ($height-bathSpace)*((lenVer-1)/lenVer));
						dataAna.canvasAll().canvasDraw.drawLine(x_before,y_before,x_after,y_after,style);
					}
				}

				function lineString(i){
					vertVal = vertVal - vertical[0];

					var	x_before = bathSpace + ($width-bathSpace)*(i/lenHor),
						y_before = $height -(bathSpace + (vertVal/(vertical[lenVer-1]-vertical[0])) * ($height-bathSpace)*((lenVer-1)/lenVer));
					
					//绘制点
					dataAna.canvasAll().canvasDraw.drawCircle(x_before,y_before,0,360,4,style);

					//绘制线
					if(i!=len-1){
						var x_after = bathSpace + ($width-bathSpace)*((i+1)/lenHor),
							y_after = $height -(bathSpace + ((points[i+1][1]-vertical[0])/(vertical[lenVer-1]-vertical[0])) * ($height-bathSpace)*((lenVer-1)/lenVer));
						dataAna.canvasAll().canvasDraw.drawLine(x_before,y_before,x_after,y_after,style);
					}
				}

				function cylindricality(i){
					i = i+1;
					var w = ($width-bathSpace)*(1/lenHor),//单个坐标所有柱形总宽度
						single_w = (w/num-4);	//单个坐标每个柱形宽度

					var	x_center = bathSpace + ($width-bathSpace)*(i/lenHor),
						y = $height -(bathSpace + (vertVal/vertical[lenVer-1]) * ($height-bathSpace)*((lenVer-1)/lenVer));
					
					var x_start = x_center - w/2; //使图形居中

					
					var x = x_start + index*single_w;
					//绘制柱形
					dataAna.canvasAll().canvasDraw.drawRect(x,y,single_w,$height-y-bathSpace-1,style);
				}
			}
		};

		return ev;
	},

	errorHanding : function(position,val,type){
		var dataAna = this;

		switch(dataAna.options.data.type)
		{
			case "line-number":
			lineNumHanding();
			break;
			case "circle" :
			circleNumHanding();
			break;
			case "line-string":
			lineStrHanding();
			break;
			case "cylindricality":
			cylindHanding();
			break;
		}

		
		function lineNumHanding(){
			if(typeof(val)!="number")
			errorMsg(position);
		}

		function lineStrHanding(){
			if(type=="ver")
			{
				if(typeof(val)!="number")
				errorMsg(position);
			} else if(type == "hor"){
				if(dataAna.options.data.horizontal.indexOf(val)<0)
				errorMsg(position);
			}
		}

		function cylindHanding(){
			if(type=="ver")
			{
				if(typeof(val)!="number")
				errorMsg(position);
			} else if(type == "hor"){
				if(dataAna.options.data.horizontal.indexOf(val)<0)
				errorMsg(position);
			}
		}

		function circleNumHanding(){
			if(typeof(val)!="number")
			errorMsg(position);
		}

		function errorMsg(position){
			var temp = "在"+position+"处出现了错误，请检查您的输入数据！";
			dataAna.errorExist = true;
			alert(temp);
		}		
	}
};

})(jQuery,window,document)