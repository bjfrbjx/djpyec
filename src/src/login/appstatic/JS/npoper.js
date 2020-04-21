
/**
 * src="/static/JS/npoper.js"
 */
var d3WIDTH=600
var d3HEIGHT=400
var npinfo={}
var axisdicts={};
var ASelcteflag=true;
var NOW_keyid=undefined;

//npy浮动层上各个张量的选择显示和其余隐藏
function npcachelb(keyid){
    if(NOW_keyid!=keyid ){
        $("#"+NOW_keyid).css('display','none')
        $("#"+keyid).css('display','block')
        NOW_keyid=keyid;
        //ajaxgetM(NOW_keyid)
    }
}
//深拷贝
function deepCopy(obj) {
  // 只拷贝对象
  if (typeof obj !== 'object') return;
  // 根据obj的类型判断是新建一个数组还是一个对象
  var newObj = obj instanceof Array ? [] : {};
  for (var key in obj) {
    // 遍历obj,并且判断是obj的属性才拷贝
    if (obj.hasOwnProperty(key)) {
      // 判断属性值的类型，如果是对象递归调用深拷贝
      newObj[key] = typeof obj[key] === 'object' ? deepCopy(obj[key]) : obj[key];
    }
  }
  return newObj;
}

//生成中间子张量id的函数
function getuuid(){
  var len=32;//32长度
  var radix=16;//16进制
  var chars='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'.split('');
    var uuid=[],i;
    radix=radix||chars.length;
    if(len){
        for(i=0;i<len;i++)
            uuid[i]=chars[0|Math.random()*radix];
    }else{
        var r;uuid[8]=uuid[13]=uuid[18]=uuid[23]='-';
        uuid[14]='4';
        for(i=0;i<36;i++){
            if(!uuid[i]){
                r=0|Math.random()*16;
                uuid[i]=chars[(i==19)?(r&0x3)|0x8:r];
            }
        }
    }
  return uuid.join('');
}  

//加载浮动层额外添加的框体
function loadingrep(operations){
    var loadingstr='<div id="fountainG"><div id="fountainG_1" class="fountainG"></div><div id="fountainG_2" class="fountainG"></div><div id="fountainG_3" class="fountainG"></div><div id="fountainG_4" class="fountainG"></div><div id="fountainG_5" class="fountainG"></div><div id="fountainG_6" class="fountainG"></div><div id="fountainG_7" class="fountainG"></div><div id="fountainG_8" class="fountainG"></div></div>';
    $(".layui-layer-content").append(loadingstr);
    var loading = $('#fountainG');
    loading.hide();
    $(document)
    .ajaxStart(function () {loading.show();})
    .ajaxStop(function () {loading.hide();});
    
    var matORcoordstr="<div>切换转化格式<input type='checkbox' name='matORcoord' /><div class='grpconditions' ><form ><label>坐标格式</label></form><button onclick='addgrpcond()'>添加分组条件</button></div><div  class='colaxies' hidden='hidden'><form ><label>矩阵格式</label></form><button onclick='addcolaxis()'>添加轴作为列项目</button></div></div>"
    $(".layui-layer-content").append(matORcoordstr);
    $("input[name='matORcoord']").change(
        function() { 
            if($("input[name='matORcoord']").prop("checked")) {
                $(".grpconditions").hide();
                $('.colaxies').show();
            }else{

                $(".colaxies").hide();
                $('.grpconditions').show();
            }
        });
    
    var oper_btns="<div id='oper_btns' >"
    for(index in operations){
        oper_btns+="<button type='reset' onclick=tensoroper('"+operations[index]+"') >"+operations[index]+"</button>"
    }
    oper_btns+="</div>"
    $(".layui-layer-content").append(oper_btns)//添加操作按钮
}


//提交当前张量进行指定操作 ，生成新张量
function tensoroper(oper){
    //收集{0:oper ,1:axisname,2:ndimcheck,3:ndimname,4axischeck}
    var operformdata=$("#"+NOW_keyid+" form").serializeJSON()
    var OLD_keyid=NOW_keyid
    var new_uuid="NP"+getuuid();
    var newshape=deepCopy(npinfo[OLD_keyid]["shape"])
    var nc=operformdata["ndimcheck"]||[];
    var ac=operformdata["axischeck"]||[];
    for(var i in nc){
        newshape[i]=parseInt(nc[i])
    }
    if(oper =='绝对值'||oper =='归一化')newshape=newshape;
    else if(oper =='累加'||oper =='累积'||oper =='最大值'||oper =='最小值'||oper =='中间值'||oper =='平均值'){
        var rtmp=0
        while(rtmp<ac.length){
              newshape.splice(parseInt(ac[rtmp])-rtmp,1)
              rtmp++;
              }
    }
    
    var new_ndimaxis = new Array(newshape.length);
    for(var i = 0;i < new_ndimaxis.length;i++){new_ndimaxis[i]=i;}
    console.log("new_uuid:"+new_uuid,newshape,new_ndimaxis)
    changenp(new_uuid,newshape,new_ndimaxis)//绘图绑定keyid
    //提交
    $.ajax({
    url:"/np_oper/",
    type:"post",
    data:JSON.stringify({axischeck:operformdata["axischeck"],
                         ndimcheck:operformdata["ndimcheck"],
                         oper:oper,keyid:OLD_keyid,new_keyid:new_uuid}),
    dataType: 'json',
    processData: false,
    contentType: "application/json",
    complete:function(){},
    success: function (data) {
        if(data["worning"]){
            alert(data["worning"])
        }
        else{
            var tm=data["tensor_model"]
            var new_keyid=tm["keyid"]
            var shape=tm["info"][0]
            var ndimaxis=tm["info"][1]
            var nameANDshape=[];
            for(var i=0;i<shape.length;i++){
                    nameANDshape[i]={"linenum":shape[i],"name":ndimaxis[i],"keyid":new_keyid,"idx":i }
            }
            d3.select("#"+new_keyid).select(".axiesCanvers").select(".axisnameInput")
            .selectAll('input')
            .data(nameANDshape)
            .enter()
            .append('input')
            .on("focus",getAxict);
                //设置M等信息
            ajaxgetM(new_keyid);
            npinfo[new_keyid]={"shape":shape,"ndimaxis":ndimaxis}
                }
            },
            error:function(data){
                console.log(data)
                alert("上传失败！");
    }
});
  
}

// 维度全选按钮
function ASelcte(){
    console.log(NOW_keyid)
    $("#"+NOW_keyid+" table tbody[hidden!='hidden'] input[type='checkbox']").prop("checked",ASelcteflag);
    ASelcteflag=!ASelcteflag;

}

//d3的箭头绘制
function makearrowMarker(svg){
    var defs = svg.append("defs");
    var  arrowid =Math.random()+"-id"
    var arrowMarker = defs.append("marker")
                            .attr("id",arrowid)
                            .attr("markerUnits","strokeWidth")
                            .attr("markerWidth","12")
                            .attr("markerHeight","12")
                            .attr("viewBox","0 0 12 12") 
                            .attr("refX","6")
                            .attr("refY","6")
                            .attr("orient","auto");

    var arrow_path = "M2,2 L10,6 L2,10 L6,6 L2,2";

    arrowMarker.append("path")
                .attr("d",arrow_path)
                .attr("fill","#000");
    console.log(arrowMarker,arrowid)
    return arrowid;
}


//获取某一阶的详细信息table
function getAxict(d){
    keyid_table="#"+d.keyid+" table"
    //1 ajax keyid  idx 
    if($( keyid_table+" #tbody_"+d.idx).length>0){
        $(keyid_table+" tbody").attr("hidden","hidden")
        $(keyid_table+" #tbody_"+d.idx).removeAttr("hidden"); return ;
    }
    else{
        $(keyid_table+" tbody").attr("hidden","hidden")
        if(axisdicts[d.keyid]==undefined||axisdicts[d.keyid][d.idx]==undefined){
        //1  ajax  
            if(axisdicts[d.keyid]==undefined)axisdicts[d.keyid]={};
//            axisdicts[d.keyid][d.idx]=["A","b","c"]
            ajaxgetAxict(d.keyid,d.idx);
        }
        else{
               var tbodytrstr="<tbody id='tbody_"+d.idx+"' >";
                m=axisdicts[d.keyid][d.idx]
                for(var i in m){
                 tbodytrstr+="<tr><td>"+i+"</td><td><input type='text' name='ndimname["+d.idx+"][]' style='width:100px' value='"+m[i]+"' />"
                    tbodytrstr+="</td><td><input type='checkbox' name='ndimcheck["+d.idx+"][]' value="+i+"></td></tr>";
                }
                tbodytrstr+="</tbody>"
                $(keyid_table).append(tbodytrstr);

        }



    }

} 

//从后端读取详细信息，并在右侧绘制table
function ajaxgetAxict(keyid,idx){
    var keyid_table="#"+keyid+" table";
    $.ajax({
        url:"/getNdimdict/",
        type:"post",
        async:true,
        data:JSON.stringify({keyid:keyid,axis:idx}),
        dataType: 'json',
        processData: false,
        contentType: "application/json",
        success: function (data) {
            if(data["worning"]){
                alert(data["worning"])
            }
            else{
                m=data["ndimlist"]
                var ajaxgetAxictstr="<tbody id='tbody_"+idx+"' >";
                for(var i in m){
                 ajaxgetAxictstr+="<tr><td>"+i+"</td><td><input type='text' name='ndimname["+idx+"][]' style='width:100px' value='"+m[i]+"' />"
                    ajaxgetAxictstr+="</td><td><input type='checkbox' name='ndimcheck["+idx+"][]' value="+i+"></td></tr>";
                }
                ajaxgetAxictstr+="</tbody>"
                $(keyid_table+" tbody").attr("hidden","hidden")
                $(keyid_table).append(ajaxgetAxictstr);
                axisdicts[keyid][idx]=m
                    }
                },
                error:function(data){
                    console.log(data)
                    alert("上传失败！");
        }
    });
}

// 获取最值等信息填充至框体
function ajaxgetM(keyid){
	console.log({keyid:keyid})
		$.ajax({
			url:"/getMInfo/",
			type:"post",
            async:true,
			data:JSON.stringify({keyid:keyid}),
            dataType: 'json',
            processData: false,
            contentType: "application/json",
			success: function (data) {
				var k=["MAX:","MIN: ","MEAN: ","MEDIAN: ","SHAPE: "]
				if(data["worning"]){
					alert(data["worning"])
				}
				else{
                    m=data["infolist"]
                    $("#"+keyid+" .info label").each(
                    		function(idx,node){
                        $(node).html(k[idx]+m[idx]);
                    });   
                        }
                    },
                    error:function(data){
                        console.log(data)
                        alert("获取最值信息失败！");
			}
		});
}
 //d3绘制对应轴
function CREATEAXISCANVERS(keyid,shape,names,w,h){
    //选择nparray所属画布
    keyid_canver=d3.select("#"+keyid).select(".axiesCanvers")
    keyid_info=d3.select("#"+keyid+" .info")
    var nameANDshape=[];
    for(var i=0;i<shape.length;i++){
            nameANDshape[i]={"linenum":shape[i],"name":names[i],"keyid":keyid,"idx":i }
        }
        function lxPos(linenum,idx){
                r=Math.sin(Math.PI*Math.log(idx+1));
                l=w/4 //Math.log(linenum)*w/16;
                return w/2+r*l;}
        function lyPos(linenum,idx){
                        r=Math.cos(Math.PI*(1+Math.log(idx+1)));
                        l=w/4 //Math.log(linenum)*w/16;
                        return h/2+r*l;}
    
//设置所属画布窗宽
    var svg = keyid_canver
    .append("svg")
    .attr("width", w)
    .attr("height", h);
//设置画布的箭头图库
    arrowid=makearrowMarker(svg);
//绘制箭头线条--轴
    svg.selectAll('g').data(shape)
         .enter()
         .append("line")
         .attr("x1",w/2)
         .attr("y1",h/2)
         .attr("x2",lxPos)
         .attr("y2",lyPos)
         .attr("stroke","red")
         .attr("stroke-width",2)
         .attr("marker-end","url(#"+arrowid+")")

//定位文字
//    svg.selectAll('g')
//        .data(nameANDshape)
//        .enter()
//        .append('text') 
//        .attr("x",function(d,idx){return lxPos(d.linenum,idx)})
//        .attr("y",function(d,idx){return lyPos(d.linenum,idx)})
//        .text(function(d) { return d.name;});

//定位axis的文本框
    keyid_canver.append('div').attr("class","axisnameInput")
    keyid_canver.append('div').attr("class","AxisSelect")
    keyid_canver.select(".axisnameInput")
      .selectAll('input')
      .data(nameANDshape)
      .enter()
      .append('input')
      .attr('type','text')
      .attr('name',function(d,idx){return "axisname["+idx+"]";})
      .attr('value',function(d) {return d.name;})
      .on('blur',function(d) {console.log(this);})
      .attr("style",function(d,idx){
                xr=Math.sin(Math.PI*Math.log(idx+1));
                l= w/4 //Math.log(d.linenum)*w/16;
                yr=Math.cos(Math.PI*(1+Math.log(idx+1)));
                return "position:absolute;left:"+(w/2+0.8*xr*l)+"px; top:"+(h/2+0.8*yr*l)+"px;width:30px;";

        })
      .on("focus",getAxict);//定位axis的文本触发table获取详细命名情况和截取
    

// 定位axis的复选框
     keyid_canver.select(".AxisSelect")
         .selectAll('input')
         .data(nameANDshape)
          .enter()
         .append('input')
          .attr('type','checkbox')
          .attr('name',"axischeck[]")
          .attr('value',function(d) {return d.idx;})
          .on('blur',function(d) {console.log(this);})
          .attr("style",function(d,idx){
                    xr=Math.sin(Math.PI*Math.log(idx+1));
                    l= w/4 //Math.log(d.linenum)*w/16;
                    yr=Math.cos(Math.PI*(1+Math.log(idx+1)));
                    return "position:absolute;left:"+(w/2+0.8*xr*l+30)+"px; top:"+(h/2+0.8*yr*l)+"px;width:30px;";
            });

    return svg;
        
    }

//切换当前张量
function changenp(keyid,now_shape,now_ndimaxis){
    var npkeyidstr='<div style="background-color: aqua;width: '+d3WIDTH+'px;height:'+d3HEIGHT+'px" id="'+keyid+'"><form id="form" ><div style="float: left"><div style="background-color:green;width: '+0.75*d3WIDTH+'px;height: '+0.67*d3HEIGHT+'px;" class="axiesCanvers"></div><div style="background-color:fuchsia;width: '+0.75*d3WIDTH+'px;height: '+0.33*d3HEIGHT+'px;" class="info"><label class="MAX">MAX:</label><br/><label class="MIN">MIN:</label><br/><label class="MEAN">MEAN:</label><br/><label class="MEDIAN">MEDIAN:</label><br/><label class="SHAPE">SHAPE: '+now_shape+'</label></div></div><div style="background-color:blue;width: '+0.25*d3WIDTH+'px;height: '+d3HEIGHT+'px;float: left;overflow:scroll;" class="table"><table><thead><tr><th>索引</th><th>名称</th><th>选择<input type="radio" onclick="ASelcte()"/> </th></tr></thead></table></div></form></div>'
    $("#npdiv").append(npkeyidstr);//插入np
    var svg=CREATEAXISCANVERS(keyid,now_shape,now_ndimaxis,0.75*d3WIDTH,0.67*d3HEIGHT);//绘图
    var idx=$("#npcachediv input").length
    $("#npcachediv")
        .append("<input name='"+keyid+"_NAME' onclick=\"npcachelb('"+keyid+"')\" value='张量"+idx+"' style='width:50px' />")//添加缓存框架
    npcachelb(keyid);
}

//构建浮动层
function np_prompt(){
	layer.prompt({
		formType: 2,
		value: 'CSV名称',
		placeholder: '输入标题',
		title: '详细配置',
		area: ['200px', '30px'] 
		} ,
		function(value, index, elem){
            var operformdata=$("#"+NOW_keyid+" form").serializeJSON();
            var ismat=$("input[name='matORcoord']").prop("checked")
            console.log("check ",ismat)
            var basedata={keyid:NOW_keyid,name:$("#npcachediv input[name='"+NOW_keyid+"_NAME']").val(),ismat:ismat,
                                     axisname:operformdata["axisname"],ndimname:operformdata["ndimname"]}
            if(ismat){
                var colaxiesformdata=$(".colaxies form").serializeJSON()["colaxis"];
                console.log(colaxiesformdata)
                basedata["tagargs"]=colaxiesformdata;
            }else{
                var grpcondformdata=$(".grpconditions form").serializeJSON()["grpcondition"];
                console.log(grpcondformdata)
            	basedata["tagargs"]=grpcondformdata;
            }
            
			$.ajax({
				url:"/npy2df/",
				type:"post",
				data:JSON.stringify(basedata),
				processData: false,
				dataType: 'json',
				contentType: "application/json",
				success: function (data) {
					if(data["worning"]){
						alert(data["worning"])
					}
					else{
						$("#datalist").children("div").remove()
						items=data["items"]
						$('#section-4').click();
						var files=data["files"]
						$("#fileslist div.fileList").find("div.rows").remove();
						for (file in files){
							console.log(file)
							$("#fileslist div.fileList").append("<div class='rows'><label class='protocol' style='display:flex;'><input type='checkbox' class='input_agreement_protocol' name='datafile'  value='"+files[file]+"'><span></span></label><a class='btn' name='"+files[file]+"' >"+files[file]+"</a></div>")
						}

						$('#file_location').val("");
						layer.close(index);
					}
					
				},
				error: function (data) {
					console.log(data)
					alert("上传失败！");

				}
			});
			
			});
    $("textarea.layui-layer-input").remove();
    var npdivstr="<div id='npdiv' style='width: "+d3WIDTH+"px;height:"+d3HEIGHT+"px'></div><div id='npcachediv' style='width: "+d3WIDTH+"px;height:50px'></div>"
    $(".layui-layer-content").append(npdivstr);//添加框架
}