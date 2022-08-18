
selected()

function selected(){

    var profile = document.querySelector(".profile").getAttribute("value").slice(2,-2).split("', '");
    var experience = profile[0];
    var industry = profile[1];
    var goal1 = profile[2];
    var goal2 = profile[3];
    var goal3 = profile[4];

    var exp = document.getElementById("experience");
    var indu = document.getElementById("industry");
    var selectg1 = document.getElementById("goal1");
    var selectg2 = document.getElementById("goal2");
    var selectg3 = document.getElementById("goal3");

    for (var i=0; i<exp.options.length; i++) {
        it = exp.options[i]

        if (it.value == experience){
            it.selected = true;
        }
    }

    for (var i=0; i<indu.options.length; i++) {
        it = indu.options[i]

        if (it.text == industry){
            it.selected = true;
        }
    }

    for (var i=0; i<selectg1.options.length; i++) {
        option1 = selectg1.options[i];

        if (option1.text == goal1) {
            option1.selected = true;
        }

        option2 = selectg2.options[i];

        if (option2.text == goal2) {
            option2.selected = true;
        }

        option3 = selectg3.options[i];

        if (option3.text == goal3) {
            option3.selected = true;
        }
    }

}