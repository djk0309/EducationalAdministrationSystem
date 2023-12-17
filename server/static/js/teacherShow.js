function handle(){

}

$(function (){

    let tableView =  {
        el: "#tableShow",
        url: "/projects/work/pageteacher/",
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
			}
        ],
        binds: (d) =>{

            handle();
        }
    }
    $.table(tableView);

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