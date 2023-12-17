function handle(){

}

function renderCol(){

    if($('#sessionUserType').val() == 0){

        return [
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
				field: "studentName",
				title: "学生姓名",
				align: "center",
			},
			{
				field: "year",
				title: "学年",
				align: "center",
			},
			{
				field: "score",
				title: "成绩",
				align: "center",
			},
			{
				title: "学期",
				align: "center",
                template: (d)=>{

                    return (d.term == "U") ? "上学期" : "下学期";
                }
			}
        ]
    }else if($('#sessionUserType').val() == 1){

        return [
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
				field: "studentName",
				title: "学生姓名",
				align: "center",
			},
			{
				field: "year",
				title: "学年",
				align: "center",
			},
			{
				field: "score",
				title: "成绩",
				align: "center",
			},
			{
				title: "学期",
				align: "center",
                template: (d)=>{

                    return (d.term == "U") ? "上学期" : "下学期";
                }
			}
        ]
    }else{

        return [
            {
                type: "number",
                title: "序号",
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
				title: "成绩",
				align: "center",
			},
			{
				title: "学期",
				align: "center",
                template: (d)=>{

                    return (d.term == "U") ? "上学期" : "下学期";
                }
			}
        ]
    }
}

$(function (){

    let tableView =  {
        el: "#tableShow",
        url: "/projects/score/pagescore/",
        method: "GET",
        where: {
            pageIndex: 1,
            pageSize: 10
        },
        page: true,
        cols: renderCol(),
        binds: (d) =>{

            handle();
        }
    }

    $.table(tableView);

        $(".fater-btn-form-qry").on("click", ()=>{

        tableView.where["studentName"] = $("[name=para1]").val();
        tableView.where["teacherName"] = $("[name=para2]").val();
        tableView.where["projectId"] = $("[name=para3]").val();
        tableView.where["gradeId"] = $("[name=para4]").val();

        $.table(tableView);
    });

    $("button[event=add]").on("click", ()=>{

        $.model(".addWin");
    });

    $("#addFormBtn").on("click", ()=>{

        let formVal = $.getFrom("addForm");

        $.ajax({
            url: "/projects/score/add/",
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