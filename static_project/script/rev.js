

let processStage = "open";
let reservationId = "open";


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function showSeats(tbl){
    // if (processStage == "closed"){
    //     cancelReserve(reservationId)
    // }


    let data = tbl;
    console.log(data)
    document.getElementById('returnData').innerHTML = 'Checking Availability...'

    const hr = new XMLHttpRequest()
    const url = "/ajax/"
    hr.open("POST", url, true)
    // hr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest");
    // hr.setRequestHeader("X-Requested-WITH", "XMLHttpRequest");
    hr.setRequestHeader("content-type", "application/x-www-form-urlencoded")
    hr.onreadystatechange = function(){
        if(hr.readyState == 4 && hr.status == 200 ){
            //document.getElementById('returnData').innerHTML = ""
            var return_data = JSON.parse(hr.responseText)
          document.getElementById('returnData').innerHTML = return_data;
            //containerElem.prepend(return_data)
            console.log("it got here "+return_data)
        }
    }
    hr.send("getSeatBtns="+data)
}

function reserveSeats([numSeats,numSeats2]){
    
    processStage = "closed"


    var a = numSeats
    var b = numSeats2
    document.getElementById("returnData").innerHTML = "Double Checking Availability";

    let xhr = new XMLHttpRequest();
    const url = "/revinit/";

    xhr.open("POST", url, true);
    xhr.setRequestHeader("content-type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function(){
        if(xhr.readyState == 4 && xhr.status == 200){
            var response_received = JSON.parse(xhr.responseText)
            console.log("it got here Test ")
            //reservationId = response_received[1];

            // var return_data = JSON.parse(hr.responseText)
            // document.getElementById('returnData').innerHTML = return_data;

            document.getElementById("returnData").innerHTML = response_received
            console.log("it got here again "+response_received)
        }

    }
    //console.log("reserve="+a+"&num="+b)
    xhr.send("reserve="+a+"&num="+b);

}
function ConfirmSeats(){
    const tn = document.getElementById("tabl_num").value
    const ns = document.getElementById("num_seats").value
    const ri = document.getElementById("reserveId").value
    const pn = document.getElementById("person_name").value
    const pe = document.getElementById("person_email").value

    if(tn == "" || ns == "" || ri == "" || pn == "" || pe == ""){
        return false
    }

    let confirmData = "tableN="+tn+"&numS="+ns+"&rId="+ri+"&Pn="+pn+"&Pe="+pe


    let xmlh = new XMLHttpRequest()
    const url = '/confirmrev/'
    xmlh.open('POST', url, true)
    xmlh.setRequestHeader("content-type", "application/x-www-form-urlencoded")
    xmlh.onreadystatechange = function(){
        if (xmlh.readyState == 4 && xmlh.status == 200){
            var data = xmlh.responseText.split("|")
            console.log(data[0])
            if(data[0] == false){
                document.getElementById("returnData").innerHTML = data[1]
                var processStage = "open"
                var reservationId = "open"
            }else{

                var processStage = "open"
                var reservationId = "open"
                document.getElementById("returnData").innerHTML = data[1]
                
                alert("you own the seat")
            }

        }
    
    }
    xmlh.send(confirmData)


}


function cancelReserve(resId){

    var data = resId
    let xr = new XMLHttpRequest()
    const url = '/cancelrev/'
    xr.open("POST", url, true)
    xr.setRequestHeader("content-type", "application/x-www-form-urlencoded")
    xr.onreadystatechange = function(){
        if(xr.readyState == 4 && xr.status == 200){
            var response_received = JSON.parse(xr.responseText)
            console.log("it got here Test ")
            //reservationId = response_received[1];

            // var return_data = JSON.parse(hr.responseText)
            // document.getElementById('returnData').innerHTML = return_data;

            document.getElementById("returnData").innerHTML = response_received
            console.log("it got here again "+response_received)
        }

    }
    //var postData = "reserve="+data 
    xr.send("cancelData="+data )

}