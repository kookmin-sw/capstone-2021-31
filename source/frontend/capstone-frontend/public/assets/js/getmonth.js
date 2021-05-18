Date.prototype.getWeekOfMonth = function() {
	var firstWeekday = new Date(this.getFullYear(), this.getMonth(), 1).getDay() - 1;
	if (firstWeekday < 0) firstWeekday = 6;

	var offsetDate = this.getDate() + firstWeekday-1;
	return Math.floor(offsetDate / 7 + 1);
}
	function get_title_date(){
		var title_str = document.getElementById("title_week").innerText;
		var title_month = title_str.split('월')[0].trim() - 1;
		var title_weekOfMonth = title_str.split('월')[1].split('주차')[0].trim();

		let title_date = new Date();
		title_date.setDate(1);
		title_date.setMonth(title_month);
		title_date.setDate(title_date.getDate() - title_date.getDay() + (title_date.getDay()==0?-6:1))
		title_date.setTime(title_date.getTime() + (title_weekOfMonth-1) * 86400000 * 7)
		return title_date;
	}

	function get_init_week(){
		let today = new Date();
		let init_week = new Date(today.setDate(today.getDate()-today.getDay() + (today.getDay() ==0? -6:1)));
		return init_week
	}

	function click_week(arrow){
			let title_date = get_title_date();
			title_date.setTime(title_date.getTime() + arrow * 86400000 * 7);
			var title_month = title_date.getMonth();
			var title_weekOfMonth = title_date.getWeekOfMonth();
			var title_day = title_date.getDate();
			document.getElementById("title_week").innerText = `${title_month+1}월 ${title_weekOfMonth}주차`;
	}

	function read_keyword(){
		var keyword_file_name = "W_21" + "-"+ (viewWeek.getMonth() + 1)
					+ "-" + viewWeek.getWeekOfMonth() + "_f.csv";
	}

	window.onload = function(){
		let init_date = get_init_week();
		init_date.setDate(1);
		var init_month = init_date.getMonth();
		var init_weekOfMonth = init_date.getWeekOfMonth();
		var init_day = init_date.getDate();
		document.getElementById("title_week").innerText = `${init_month+1}월 ${init_weekOfMonth}주차`;

	}
