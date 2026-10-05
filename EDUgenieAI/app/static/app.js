const task = document.getElementById("task");

const topicWrap = document.getElementById("topicWrap");
const levelWrap = document.getElementById("levelWrap");

const topic = document.getElementById("topic");
const level = document.getElementById("level");

const inputLabel = document.getElementById("inputLabel");
const inputText = document.getElementById("inputText");

const submitBtn = document.getElementById("submitBtn");

const resultCard = document.getElementById("resultCard");
const result = document.getElementById("result");

const copyBtn = document.getElementById("copyBtn");
const status = document.getElementById("status");


const configs = {

    qa: {
        label: "Question",
        placeholder: "Example: What is a computer?",
        endpoint: "/qa"
    },

    explain: {
        label: "Topic",
        placeholder: "Example: Explain binary search trees",
        endpoint: "/explain"
    },

    quiz: {
        label: "Study Material",
        placeholder: "Paste your study material here...",
        endpoint: "/quiz"
    },

    summarize: {
        label: "Content",
        placeholder: "Paste your content here...",
        endpoint: "/summarize"
    },

    learn: {
        label: "Topic",
        placeholder: "Example: I want to learn Python",
        endpoint: "/learn/recommendations"
    }
};


/* UPDATE FORM */

function updateForm() {

    const selected = task.value;

    const config = configs[selected];

    inputLabel.textContent = config.label;

    inputText.placeholder = config.placeholder;


    if (selected === "quiz") {

        topicWrap.classList.remove("hidden");
        levelWrap.classList.add("hidden");

    }

    else if (selected === "learn") {

        topicWrap.classList.remove("hidden");
        levelWrap.classList.remove("hidden");

    }

    else {

        topicWrap.classList.add("hidden");
        levelWrap.classList.add("hidden");

    }
}


/* HEALTH CHECK */

async function checkHealth() {

    try {

        const response = await fetch("/health");

        const data = await response.json();

        if (data.gemini_configured) {

            status.textContent = "API Ready";

        } else {

            status.textContent = "Add Gemini API Key";

        }

    }

    catch (error) {

        status.textContent = "API Unavailable";

    }
}


/* ESCAPE HTML */

function escapeHtml(value) {

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


/* QUIZ */

function renderQuiz(data) {

    result.innerHTML = data.questions.map(
        (question, index) => {

            return `
                <div class="quiz-question">

                    <strong>
                        ${index + 1}.
                        ${escapeHtml(question.question)}
                    </strong>

                    ${question.options.map(
                        option => `
                            <div class="option">
                                ${escapeHtml(option)}
                            </div>
                        `
                    ).join("")}

                    <p>
                        <strong>Answer:</strong>
                        ${escapeHtml(question.answer)}
                    </p>

                </div>
            `;
        }
    ).join("");
}


/* SUBMIT */

submitBtn.addEventListener("click", async function () {

    const selected = task.value;

    const text = inputText.value.trim();


    if (!text) {

        alert("Please enter some text.");

        inputText.focus();

        return;
    }


    let body;


    if (selected === "qa") {

        body = {
            text: text,
            question: text
        };

    }


    else if (selected === "explain") {

        body = {
            text: text,
            topic: text
        };

    }


    else if (selected === "quiz") {

        body = {
            text: text,
            topic: topic.value.trim()
        };

    }


    else if (selected === "summarize") {

        body = {
            text: text
        };

    }


    else if (selected === "learn") {

        body = {
            text: text,
            topic: topic.value.trim() || text,
            level: level.value
        };

    }


    submitBtn.disabled = true;

    submitBtn.textContent = "Working...";

    resultCard.classList.remove("hidden");

    result.textContent = "Generating your result...";


    try {

        const response = await fetch(
            configs[selected].endpoint,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(body)
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail || "Request failed"
            );

        }


        if (selected === "quiz") {

            renderQuiz(data);

        }

        else {

            result.textContent = data.result;

        }

    }


    catch (error) {

        result.innerHTML = `
            <div class="error">
                ${escapeHtml(error.message)}
            </div>
        `;

    }


    finally {

        submitBtn.disabled = false;

        submitBtn.textContent = "Generate";

    }

});


/* COPY */

copyBtn.addEventListener("click", async function () {

    try {

        await navigator.clipboard.writeText(
            result.innerText
        );

        copyBtn.textContent = "Copied";

        setTimeout(function () {

            copyBtn.textContent = "Copy";

        }, 1200);

    }

    catch (error) {

        copyBtn.textContent = "Copy failed";

    }

});


/* TASK CHANGE */

task.addEventListener(
    "change",
    updateForm
);


/* START */

updateForm();

checkHealth();