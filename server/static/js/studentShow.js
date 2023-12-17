function handle(){

    $("button[event=select]").on("click", (e)=>{

        $.confirm("确认要选择吗", () =>{

            $.ajax({
                url: "/projects/select/selectproject/",
                type: "POST",
                async: false,
                data:{
                    term: $(e.target).attr("data-term"),
                    projectId: $(e.target).attr("data-pid"),
                    gradeId: $(e.target).attr("data-gid"),
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

    $("button[event=cancle]").on("click", (e)=>{

        $.confirm("确认要取消吗", () =>{

            $.ajax({
                url: "/projects/select/cancelproject/",
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
        url: "/projects/work/pagestudent/",
        method: "GET",
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
				title: "授课教师",
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

                    console.log(d.isSelect);
                    if(d.isSelect){

                        return `
                            <button type="button" event="cancle" data="${d.id}" class="fater-btn fater-btn-danger fater-btn-sm">
                                <span data="${d.id}">取消</span>
                            </button>
                            `;
                    }else{

                        return `
                            <button type="button" event="select" data="${d.id}" class="fater-btn fater-btn-primary fater-btn-sm">
                                <span data-term="${d.term}" data-pid="${d.projectId}" data-gid="${d.gradeId}">选择</span>
                            </button>
                            `;
                    }
                }
            }
        ],
        binds: (d) =>{

            handle();
        }
    }
    $.table(tableView);
});