document.addEventListener('DOMContentLoaded', function () {
    let duration = timerInSeconds;
    let timerElement = document.getElementById('timer');
    let timerInterval = setInterval(function() {
        hours = parseInt(duration / 3600, 10);
        minutes = parseInt((duration % 3600) / 60, 10);
        seconds = parseInt(duration % 60, 10);

        minutes = minutes < 10 ? '0' + minutes : minutes
        seconds = seconds < 10 ? '0' + seconds : seconds

        timerElement.textContent =`${hours}:${minutes}:${seconds}`;

        if (duration <= 0) {
            function disable(item) {
                item.disabled = true;
            }
            radios = document.getElementsByClassName('form-check-input');
            clearInterval(timerInterval);
            Array.from(radios).forEach(disable);
            timerElement.textContent = "Time's up! Good luck.";
            console.log('vasabmiteb')
            submit();
        } else {
            duration -= 1;
        }
    }, 1000);

    function submit() {
        clearInterval(timerInterval);
        let options = {
            'method': 'POST',
            'headers': {'X-CSRFToken': csrfToken},

        };
        let questions = document.querySelectorAll('.question');
        let requestData = {
                'classroom_id': classroomId,
                'questions': []
            };
        questions.forEach(function (elem) {
            let questionElem = elem.querySelector('h5').innerText.split(' ')[1];
            let answer = elem.querySelector('input[type="radio"]:checked');

            let finalAnswer = answer ? answer.value : 'No answer selected';
            let textAnswer = answer ? answer.id.split('_')[1] : "No answer selected";
            requestData['questions'].push({question: questionElem, answer: finalAnswer,
                answerText: textAnswer
            });
        });
        options['body'] = JSON.stringify(requestData);
        fetch(finishUrl, options)
            .then(response => response.json())
            .then(data => {
                if (data['status']==='ok') {
                    // clear quiz container
                    let quizDiv = document.querySelector('.quiz-container');
                    quizDiv.innerHTML = '';

                    // display results
                    let score = document.createElement('h1');
                    score.innerText = `Score: ${data['score']}`;
                    quizDiv.appendChild(score);
                    let urlToModule = document.createElement("a");
                    urlToModule.href = classroomUrl;
                    urlToModule.textContent = "Classroom";
                    urlToModule.classList.add("btn");
                    urlToModule.classList.add("btn-primary");
                    quizDiv.appendChild(urlToModule);
                    let questionsList = document.createElement('ul');
                    questionsList.classList.add('list-group');
                    for (let questionData of data['final_results']) {
                        let {question, answer, correct} = questionData;
                        let listItem = document.createElement('li');
                        listItem.classList.add('list-group-item');
                        listItem.innerHTML = `<h3>Question: ${question} | Your Answer: ${answer}</h3>`
                        // highlight background of listItem based on correctness
                        listItem.classList.add(correct ? 'bg-success' : 'bg-danger');
                        listItem.style.margin = '5px';
                        questionsList.appendChild(listItem);
                    }
                    if (data['final_quiz']===true) {
                        let urlToGraduate = document.createElement("a");
                        urlToGraduate.href = data['graduation_url'];
                        urlToGraduate.textContent = "Click here to graduate";
                        urlToGraduate.classList.add("btn");
                        urlToGraduate.classList.add("btn-primary");
                        quizDiv.appendChild(urlToGraduate);
                    }


                    quizDiv.appendChild(questionsList);

                }
            })
            .catch(error => {
                // Handle errors here
                console.error('Error:', error);
                let quizDiv = document.querySelector('.quiz-container');

                // Display error message
                let errorMessage = document.createElement('p');
                errorMessage.innerText = 'An error occurred. Please try again or contact the teacher.';
                let urlToModule = document.createElement("a");
                urlToModule.href = classroomUrl;
                urlToModule.textContent = "Classroom";
                urlToModule.classList("btn btn-primary");
                quizDiv.appendChild(questionsList);
                quizDiv.appendChild(urlToModule);
                quizDiv.appendChild(errorMessage);
            });
        }
    submitButton = document.querySelector('.submit-button');
    submitButton.addEventListener('click', () => {
        submit();
    })

});