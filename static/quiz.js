// We are doing same as in classroom.js,
// get ending date based on opening date using flatpickr datetimepicker
document.addEventListener('DOMContentLoaded', function () {
    const closeDate = document.querySelector('#close-date');
    const closeDatePicker = flatpickr(
        closeDate, {
            enableTime: true
        }
    );
    const openDate = document.querySelector('#open-date');
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    flatpickr(openDate, {
        enableTime: true,
        onChange: function(selectedDates, dateStr, instance) {
            let starting = selectedDates[0];
            let hoursInMilliseconds = 6 * 60 * 60 * 1000;
            let closingDateTime = new Date(starting.getTime() + hoursInMilliseconds);
            closeDatePicker.setDate(closingDateTime, false);
        },
        minDate: tomorrow
    });
});