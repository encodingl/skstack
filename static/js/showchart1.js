$(function(){
            var flow =  num_list_stg ;
             var labels2 =  date_list;
             var labels = new Array()
             var temp = new Array()

             for(var i=0; i<labels2.length;i++){
                temp=labels2[i].split("-")
                 labels[i] = temp[1]+"-"+temp[2]+'\n' + temp[0]
             }



             var data = [
			         	{
			         		name : '运维工单数量统计表',
			         		value:flow,
			         		<!--color:'#ec4646',-->
						    color:'#4b94c0',
			         		line_width:4
			         	}
			         ];



			var chart = new iChart.LineBasic2D({
				render : 'canvasDivStg',
				data: data,
				align:'center',
				title : {
					text:'STG数量统计表',
					font : '微软雅黑', //字体
					fontsize:00, //字体大小设置
					color:'#000'
				},


				width : 1260,
				height : 400,
				shadow:false,
				shadow_color : '#fff',
				shadow_blur : 0,
				shadow_offsetx : 0,
				shadow_offsety : 0,
                background_color:'#ffffff',

				tip:{
					enable:true,
					shadow:true,
					listeners:{
						 //tip:提示框对象、name:数据名称、value:数据值、text:当前文本、i:数据点的索引
						parseText:function(tip,name,value,text,i){
							return "<span style='color:#000000;font-size:12px;'>"+labels[i]+"日工单执行数为:<br/>"+
							"</span><span style='color:#000000;font-size:20px;'>"+value+"个</span>";
						}
					}
				},
				sub_option : {
					smooth : true,
					label:false,
					hollow:false,
					hollow_inside:false,
					point_size:8
				},
				coordinate:{
					width:1160,
					height:260,
					striped_factor : 0.18,

                    grid_line_width:0.7,
					// grid_color:'#ffffff',
					axis:{
						color:'#fff',
						width:[0,0,0,0]
					},
					gridVStyle:{
						color:'#fff',
					},
					scale:[{
						 position:'left',
						 start_scale:0,
						 end_scale:20,
						 scale_space:4,
						 scale_size:1000,
						 scale_enable : true,
						 // label : {color:'#000000',font : '微软雅黑',fontsize:12,fontweight:600},
						 scale_color:'#fff'
					},{
						 position:'bottom',
						 // label : {color:'#000000',font : '微软雅黑',fontsize:12,fontweight:600},
						 scale_enable : false,
						 labels:labels
					}]
				}
			});
			// //利用自定义组件构造左侧说明文本
			// chart.plugin(new iChart.Custom({
			// 		drawFn:function(){
			// 			//计算位置
			// 			var coo = chart.getCoordinate(),
			// 				x = coo.get('originx'),
            //
			// 				y = coo.get('originy'),
			// 				w = coo.width,
			// 				h = coo.height;
            //
			// 			//在左上侧的位置，渲染一个单位的文字
			// 			chart.target.textAlign('start')
			// 			.textBaseline('bottom')
			// 			.textFont('600 11px 微软雅黑')
			// 			// .fillText('任务数（单位个)',x-40,y-12,false,'#000000')
			// 			.textBaseline('top')
            //
            //
			// 		}
			// }));
		//开始画图
		chart.draw();
	});
