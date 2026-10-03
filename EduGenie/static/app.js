const state = {
    task: "qa"
};


const taskConfig = {

    qa: {
        title: "Ask your question",
        description: "Ask EduGenie any educational question.",
        label: "Q&A",
        placeholder: "Example: What is the largest ocean?",
        button: "Ask EduGenie",
        endpoint: "/qa"
    },

    explain: {
        title: "Explain a concept",
        description: "Enter a difficult topic and get a simple explanation.",
        label: "Explain",
        placeholder: "Example: Explain photosynthesis in simple words.",
        button: "Explain Concept",
        endpoint: "/explain"
    },

    quiz: {
        title: "Generate a quiz",
        description: "Paste educational content and generate 3 MCQs.",
        label: "Quiz",
        placeholder: "Paste a paragraph or lesson here...",
        button: "Generate Quiz",
        endpoint: "/quiz"
    },

    summarize: {
        title: "Summarize content",
        description: "Paste educational content for quick revision.",
        label: "Summary",
        placeholder: "Paste a long educational paragraph here...",
        button: "Summarize",
        endpoint: "/summarize"
    },

    learn: {
        title: "Build a learning path",
        description: "Create a personalized roadmap from beginner to advanced.",
        label: "Learning Path",
        placeholder: "Example: Python programming",
        button: "Create Learning Path",
        endpoint: "/learn/recommendations"
    }

};


const taskCards = document.querySelectorAll(".task-card");

const userInput = document.getElementById("userInput");

const inputTitle = document.getElementById("inputTitle");

const inputDescription =
    document.getElementById("inputDescription");

const taskLabel =
    document.getElementById("taskLabel");

const submitButton =
    document.getElementById("submitButton");

const buttonText =
    document.getElementById("buttonText");

const learningOptions =
    document.getElementById("learningOptions");

const characterCount =
    document.getElementById("characterCount");

const loading =
    document.getElementById("loading");

const errorBox =
    document.getElementById("errorBox");

const resultSection =
    document.getElementById("resultSection");

const resultTitle =
    document.getElementById("resultTitle");

const resultContent =
    document.getElementById("resultContent");

const copyButton =
    document.getElementById("copyButton");

const aiForm =
    document.getElementById("aiForm");


function escapeHtml(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


function setTask(task) {

    state.task = task;

    const config = taskConfig[task];

    taskCards.forEach(card => {

        card.classList.toggle(
            "active",
            card.dataset.task === task
        );

    });


    inputTitle.textContent = config.title;

    inputDescription.textContent =
        config.description;

    taskLabel.textContent =
        config.label;

    buttonText.textContent =
        config.button;

    userInput.placeholder =
        config.placeholder;


    learningOptions.classList.toggle(
        "hidden",
        task !== "learn"
    );


    if (task === "quiz") {

        userInput.placeholder =
            "Paste educational content here. EduGenie will create exactly 3 questions with 4 options each.";

    }


    clearResult();

    updateCharacterCount();
}


function updateCharacterCount() {

    const length = userInput.value.length;

    characterCount.textContent =
        `${length} / 20000`;
}


function clearResult() {

    resultSection.classList.add("hidden");

    errorBox.classList.add("hidden");

    resultContent.innerHTML = "";
}


function showError(message) {

    errorBox.textContent =
        `⚠️ ${message}`;

    errorBox.classList.remove("hidden");
}


function showLoading(show) {

    loading.classList.toggle(
        "hidden",
        !show
    );

    submitButton.disabled = show;

    if (show) {

        buttonText.textContent =
            "Generating...";

    } else {

        buttonText.textContent =
            taskConfig[state.task].button;
    }
}


function showResult(title, html) {

    resultTitle.textContent =
        title;

    resultContent.innerHTML =
        html;

    resultSection.classList.remove(
        "hidden"
    );

    resultSection.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


function renderText(text) {

    return escapeHtml(text)
        .replace(/\n/g, "<br>");
}


function renderQuiz(quiz) {

    let html = "";

    html += `
        <div class="quiz-title">
            <h3>${escapeHtml(quiz.title)}</h3>
            <p style="color:#6b7280;margin:6px 0 18px;">
                Select an answer for each question.
            </p>
        </div>
    `;


    quiz.questions.forEach(
        (question, index) => {

            html += `
                <div
                    class="quiz-question"
                    data-question-index="${index}"
                >

                    <h3>
                        ${index + 1}.
                        ${escapeHtml(question.question)}
                    </h3>
            `;


            question.options.forEach(
                option => {

                    html += `
                        <button
                            type="button"
                            class="quiz-option"
                            data-answer="${escapeHtml(option)}"
                            data-correct="${escapeHtml(question.correct_answer)}"
                            data-explanation="${escapeHtml(question.explanation)}"
                        >
                            ${escapeHtml(option)}
                        </button>
                    `;

                }
            );


            html += `
                    <div
                        class="quiz-explanation hidden"
                    ></div>

                </div>
            `;

        }
    );


    return html;
}


async function submitTask(event) {

    event.preventDefault();

    clearResult();

    const text =
        userInput.value.trim();


    if (!text) {

        showError(
            "Please enter some content first."
        );

        return;
    }


    const config =
        taskConfig[state.task];


    let payload;


    if (state.task === "qa") {

        payload = {
            question: text
        };

    } else if (state.task === "learn") {

        payload = {
            topic: text,

            level:
                document.getElementById("level").value,

            days_per_week:
                Number(
                    document.getElementById(
                        "daysPerWeek"
                    ).value
                ),

            hours_per_day:
                Number(
                    document.getElementById(
                        "hoursPerDay"
                    ).value
                )
        };

    } else {

        payload = {
            text: text
        };
    }


    showLoading(true);


    try {

        const response =
            await fetch(
                config.endpoint,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(payload)
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Something went wrong."
            );
        }


        if (!data.success) {

            throw new Error(
                "The AI request was not successful."
            );
        }


        if (state.task === "quiz") {

            showResult(
                "Your AI Quiz",
                renderQuiz(data.result)
            );

            attachQuizHandlers();

        } else {

            showResult(
                config.label,
                renderText(data.result)
            );
        }

    } catch (error) {

        showError(
            error.message ||
            "Unable to connect to EduGenie."
        );

    } finally {

        showLoading(false);
    }
}


function attachQuizHandlers() {

    const options =
        document.querySelectorAll(
            ".quiz-option"
        );


    options.forEach(option => {

        option.addEventListener(
            "click",
            () => {

                const parent =
                    option.closest(
                        ".quiz-question"
                    );


                if (
                    parent.dataset.answered === "true"
                ) {
                    return;
                }


                parent.dataset.answered =
                    "true";


                const correct =
                    option.dataset.correct;


                const selected =
                    option.dataset.answer;


                const explanation =
                    option.dataset.explanation;


                const allOptions =
                    parent.querySelectorAll(
                        ".quiz-option"
                    );


                allOptions.forEach(
                    button => {

                        if (
                            button.dataset.answer ===
                            correct
                        ) {

                            button.classList.add(
                                "correct"
                            );

                        }

                    }
                );


                if (selected !== correct) {

                    option.classList.add(
                        "wrong"
                    );

                }


                const explanationBox =
                    parent.querySelector(
                        ".quiz-explanation"
                    );


                explanationBox.innerHTML =
                    `<strong>Explanation:</strong> ${escapeHtml(explanation)}`;

                explanationBox.classList.remove(
                    "hidden"
                );
            }
        );

    });
}


taskCards.forEach(card => {

    card.addEventListener(
        "click",
        () => {

            setTask(
                card.dataset.task
            );

        }
    );

});


userInput.addEventListener(
    "input",
    updateCharacterCount
);


aiForm.addEventListener(
    "submit",
    submitTask
);


copyButton.addEventListener(
    "click",
    async () => {

        const text =
            resultContent.innerText;


        try {

            await navigator.clipboard.writeText(
                text
            );

            copyButton.textContent =
                "✓ Copied";

            setTimeout(
                () => {

                    copyButton.textContent =
                        "📋 Copy";

                },
                1500
            );

        } catch {

            copyButton.textContent =
                "Copy failed";

        }

    }
);


setTask("qa");