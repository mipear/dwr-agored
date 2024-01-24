document.addEventListener("DOMContentLoaded", function () {
    // sidenav initialization
    let sidenav = document.querySelectorAll(".sidenav");
    M.Sidenav.init(sidenav);

    // datepicker initialization
    let datepicker = document.querySelectorAll('.datepicker');
    M.Datepicker.init(datepicker, {
        format: "dd mmmm, yyyy",
        i18n: { done: "Select" }
    });

    // select initialization
    let selects = document.querySelectorAll("select");
    M.FormSelect.init(selects);

    // collapsible initialization
    let collapsibiles = document.querySelectorAll('.collapsible');
    M.Collapsible.init(collapsibiles);

    // modal initialization
    let modal = document.querySelectorAll('.modal');
    M.Modal.init(modal);

  });
