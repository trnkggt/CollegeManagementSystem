document.addEventListener('DOMContentLoaded', function () {
    const endDateInput = document.getElementById('end-date');
    const ending = flatpickr(endDateInput, {
        enableTime: true
    });

    const startDateInput = document.getElementById('start-date');
    flatpickr(startDateInput, {
        enableTime: true,
        onChange: function(selectedDates, dateStr, instance) {
            let starting = selectedDates[0];
            let weeksInMilliseconds = 15 * 7 * 24 * 60 * 60 * 1000;
            let futureDateTime = new Date(starting.getTime() + weeksInMilliseconds);
            ending.setDate(futureDateTime, false);
        }
    });

    function updateCourseChoices() {
        var options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin',  // Include credentials for same-origin requests
        };
        var teacher = document.querySelector('#teacher').value
        options['body'] = JSON.stringify(teacher);
        fetch(subjects_ajax, options)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Request failed with status: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'ok') {
                    console.log(data);
                    var courseSelect = document.querySelector('#subjects');
                    courseSelect.innerHTML = '<option value="">---------</option>';

                    data.subjects.forEach(subject => {
                        var option = document.createElement('option');
                        option.value = subject.id;
                        option.textContent = subject.name;
                        courseSelect.appendChild(option);
                    });
                }
            })
            .catch(error => {
                console.error(error);
            });
    }

    document.getElementById('teacher').addEventListener('change', updateCourseChoices);
    updateCourseChoices();
});
