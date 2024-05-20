function expandSearch() {
    //document.getElementById("searchbar").style.padding = "5px 5px 5px 5px";   works but doesnt wait for it to finish
    document.getElementById("searchform").style.display = "block";
    document.getElementById("searchbar").style.display = "none";
    document.getElementById("border").style.border = "solid green";
    //document.getElementById("border").style.display = "block";
}

function dateFromInfo(disp) {
    document.getElementById("infoDateFrom").style.display = disp;
}

function dateToInfo(disp) {
    document.getElementById("infoDateTo").style.display = disp;
}

function levelInfo(disp) {
    document.getElementById("infoLevel").style.display = disp;
}

function assocInfo(disp) {
    document.getElementById("infoAssoc").style.display = disp;
}

function hostClubInfo(disp) {
    document.getElementById("infoHostClub").style.display = disp;
}

function searchQueryInfo(disp) {
    if (disp == 'none') {
        document.getElementById("infoClub").style.display = disp;
        document.getElementById("infoAgeClass").style.display = disp;
        document.getElementById("noRadioChecked").style.display = disp;
    } else {
        if (document.searchParams.typeofsearch[0].checked) {
            document.getElementById("infoClub").style.display = disp;
            document.getElementById("searchQuery").placeholder = "club abbreviation";
        } else if (document.searchParams.typeofsearch[1].checked) {
            document.getElementById("infoAgeClass").style.display = disp;
            document.getElementById("searchQuery").placeholder = "e.g. M14";
        } else {
            document.getElementById("noRadioChecked").style.display = disp;
        }
    }
}

function open_menu() {
    document.getElementById("sidebar").style.display = "block";
  }
  
  function w3_close() {
    document.getElementById("sidebar").style.display = "none";
  }