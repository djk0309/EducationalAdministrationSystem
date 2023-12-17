function handle(){

    $("button[event=del]").on("click", (e)=>{

        $.confirm("确认要移除吗", () =>{

            $.ajax({
                url: "/projects/work/delwork/",
                type: "POST",
                async: false,
                data:{
                    id: $(e.target).attr("data"),
                },
                success: function(res){
                    if(res.code == 0){
                        $.alert(res.msg, () =>{

                            window.location.reload();
                        });
                    }else{
                        $.msg("error", res.msg);
                    }
                }
            });
        });
    });
}

$(function (){

    let tableView =  {
        el: "#tableShow",
        url: "/projects/work/pagegrade/",
        method: "GET",
        where: {
            gradeId: $("input[name=gradeId]").val(),
        },
        page: false,
        cols: [
            {
                type: "number",
                title: "序号",
            },
			{
				field: "gradeName",
				title: "班级名称",
				align: "center",
			},
			{
				field: "projectName",
				title: "课程名称",
				align: "center",
			},
			{
				field: "teacherName",
				title: "教师姓名",
				align: "center",
			},
			{
				field: "year",
				title: "学年",
				align: "center",
			},
			{
				field: "score",
				title: "学分",
				align: "center",
			},
			{
				field: "hours",
				title: "学时",
				align: "center",
			},
			{
				title: "学期",
				align: "center",
                template: (d)=>{

                    return (d.term == "U") ? "上学期" : "下学期";
                }
			},
			{
                title: "操作",
                template: (d)=>{

                    return `
                            <button type="button" event="del" data="${d.id}" class="fater-btn fater-btn-danger fater-btn-sm">
                                <span data="${d.id}" class="fa fa-trash"></span>
                            </button>
                            `;
                }
            }
        ],
        binds: (d) =>{

            handle();
        }
    }
    $.table(tableView);

    $("button[event=add]").on("click", ()=>{

        $.ajax({
            url: "/projects/work/gradeprojects/",
            type: "GET",
            async: false,
            data:{
                gradeId: $("input[name=gradeId]").val(),
            },
            success: function(res){
                $("select[name=projectId]").empty();
                if(res.data && res.data.length > 0){

                    res.data.forEach(item => {
                        $("select[name=projectId]").append(`<option value="${item.id}">${item.name}</option>`);
                    })

                    $.model(".workWin");
                }else{
                    $.msg("warn", "全部课程已安排");
                }
            }
        });

    });

    $("#workFormBtn").on("click", ()=>{

        let formVal = $.getFrom("workForm");

        $.ajax({
            url: "/projects/work/setwork/",
            type: "POST",
            data: formVal,
            success: function(res){
                if(res.code == 0){
                    $.alert(res.msg, () =>{

                        window.location.reload();
                    });
                }else{
                    $.msg("error", res.msg);
                }
            }
        });
    });
});