document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing Nepali date pickers...');
    var nep_date_elements = document.getElementsByClassName("nep_date");
    console.log('Found elements:', nep_date_elements.length);
    
    Array.from(nep_date_elements).forEach(function(element) {
        console.log('Initializing date picker for:', element.id);
        element.nepaliDatePicker({
            ndpYear: true,
            ndpMonth: true,
            ndpYearCount: 10,
            readOnlyInput: true,
            dateFormat: "YYYY-MM-DD"
        });
    });
});