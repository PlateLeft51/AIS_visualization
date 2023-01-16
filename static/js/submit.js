function verify(){
    // return false;
    let st = $("#start").val();
    let ed = $("#end").val();

    if (st.length === 0){
        alert("Please enter a start time");
        return false;
    }
    else if (st.length < 14){
        alert("invalid start time.");
        return false;
    }
    else if (ed.length === 0){
        alert("Please enter an end time");
        return false;
    }
    else if (ed.length < 14){
        alert("invalid end time.");
        return false;
    }
    else if(ed-st>3000){
        alert("invalid time interval. Make sure your time interval is within 30 minutes.");
        return false;
    }
    document.getElementById("timeform").submit();

}