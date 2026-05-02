// script.js - PaulTech Exam Portal
// COMPLETE FIXED VERSION - No pre-selected answers

document.addEventListener("DOMContentLoaded", function () {

    // ================= LOGIN VALIDATION =================
    const loginForm = document.getElementById("loginForm");

    if (loginForm) {
        loginForm.addEventListener("submit", function (event) {
            const username = document.getElementById("loginUsername");
            const password = document.getElementById("loginPassword");

            if (!username || !password) return;

            if (!username.value.trim() || !password.value.trim()) {
                alert("Please enter username and password");
                event.preventDefault();
            }
        });
    }

    // ================= LOGOUT =================
    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", function (e) {
            e.preventDefault();
            window.location.href = "/logout/";
        });
    }

    // ================= EXAM SYSTEM =================
    if (document.querySelector('.question-card')) {
        
        const questionCards = document.querySelectorAll(".question-card");
        const navigatorButtons = document.querySelectorAll(".question-nav-btn");
        const answeredCountDisplay = document.getElementById("answeredCount");
        const progressBar = document.getElementById("progressBar");
        const counterDisplay = document.getElementById("questionCounter");
        const nextBtn = document.getElementById("nextBtn");
        const prevBtn = document.getElementById("prevBtn");

        let currentQuestion = 0;
        let examSubmitted = false;
        let autoSubmitTriggered = false;

        const allRadios = document.querySelectorAll("input[type='radio']");
        
        // ================= CLEAR ALL PRE-SELECTED ANSWERS =================
        allRadios.forEach(radio => {
            radio.checked = false;
            radio.removeAttribute("checked");
        });

        // ================= CLEAR LOCALSTORAGE FOR NEW EXAM SESSION =================
        Object.keys(localStorage).forEach(key => {
            if (key.startsWith("question_")) {
                localStorage.removeItem(key);
            }
        });
        
        // Clear sessionStorage for exam
        sessionStorage.removeItem("exam_time_left");
        sessionStorage.removeItem("current_exam_session");

        function showQuestion(index) {
            if (examSubmitted) return;
            if (index < 0 || index >= questionCards.length) return;

            questionCards.forEach(card => card.style.display = "none");
            questionCards[index].style.display = "block";
            currentQuestion = index;
            updateUI();
            updateNavigatorCurrentHighlight();
        }

        function updateUI() {
            updateButtons();
            updateProgress();
            updateCounter();
        }

        function updateButtons() {
            if (prevBtn) {
                prevBtn.disabled = currentQuestion === 0 || examSubmitted;
            }
            if (nextBtn) {
                nextBtn.innerText = currentQuestion === questionCards.length - 1 ? "Finish Exam" : "Next";
                nextBtn.disabled = examSubmitted;
            }
        }

        function updateProgress() {
            if (!progressBar) return;
            const progress = ((currentQuestion + 1) / questionCards.length) * 100;
            progressBar.style.width = progress + "%";
        }

        function updateCounter() {
            if (!counterDisplay) return;
            counterDisplay.innerText = `Question ${currentQuestion + 1} of ${questionCards.length}`;
        }

        function updateNavigatorCurrentHighlight() {
            navigatorButtons.forEach((btn, index) => {
                btn.classList.remove("current");
                if (index === currentQuestion) {
                    btn.classList.add("current");
                }
            });
        }

        if (nextBtn) {
            nextBtn.addEventListener("click", function () {
                if (examSubmitted) return;
                
                if (currentQuestion < questionCards.length - 1) {
                    showQuestion(currentQuestion + 1);
                } else {
                    if (confirm("Are you sure you want to submit the exam? You cannot change answers after submission.")) {
                        submitExam();
                    }
                }
            });
        }

        if (prevBtn) {
            prevBtn.addEventListener("click", function () {
                if (examSubmitted) return;
                
                if (currentQuestion > 0) {
                    showQuestion(currentQuestion - 1);
                }
            });
        }

        navigatorButtons.forEach((btn, index) => {
            btn.addEventListener("click", () => {
                if (examSubmitted) return;
                showQuestion(index);
            });
        });

        // ================= RADIO OPTIONS - SAVE CURRENT EXAM ANSWERS =================
        allRadios.forEach(radio => {
            radio.addEventListener("click", function(e) {
                if (examSubmitted) {
                    e.preventDefault();
                    return false;
                }
                
                this.checked = true;
                updateAnsweredCount();
                highlightNavigator();
            });
            
            radio.addEventListener("change", function () {
                if (examSubmitted) return;
                updateAnsweredCount();
                highlightNavigator();
            });
        });

        function updateAnsweredCount() {
            const answered = new Set();
            allRadios.forEach(radio => {
                if (radio.checked) {
                    answered.add(radio.name);
                }
            });
            if (answeredCountDisplay) {
                answeredCountDisplay.innerText = `${answered.size} Answered`;
            }
        }

        function highlightNavigator() {
            navigatorButtons.forEach((btn, index) => {
                const card = questionCards[index];
                const checked = card.querySelector("input[type='radio']:checked");
                if (checked) {
                    btn.classList.remove("btn-outline-primary");
                    btn.classList.add("btn-success");
                } else {
                    btn.classList.remove("btn-success");
                    btn.classList.add("btn-outline-primary");
                }
            });
        }

        // ================= TIMER WITH AUTO-SUBMIT =================
        const timerDisplay = document.getElementById("timerDisplay");

        if (timerDisplay) {
            let timeLeft = 60 * 60; // 60 minutes in seconds
            
            const timer = setInterval(() => {
                if (autoSubmitTriggered || examSubmitted) return;
                
                const min = Math.floor(timeLeft / 60);
                const sec = timeLeft % 60;
                
                timerDisplay.innerText = String(min).padStart(2, "0") + ":" + String(sec).padStart(2, "0");
                
                if (timeLeft <= 60) {
                    timerDisplay.classList.add("timer-danger");
                    timerDisplay.classList.remove("timer-warning");
                } else if (timeLeft <= 300) {
                    timerDisplay.classList.add("timer-warning");
                    timerDisplay.classList.remove("timer-danger");
                } else {
                    timerDisplay.classList.remove("timer-warning", "timer-danger");
                }
                
                if (timeLeft <= 0) {
                    clearInterval(timer);
                    if (!autoSubmitTriggered && !examSubmitted) {
                        autoSubmitTriggered = true;
                        alert("Time is over! Your exam will be submitted automatically.");
                        submitExam();
                    }
                }
                
                timeLeft--;
            }, 1000);
        }

        // ================= SUBMIT EXAM FUNCTION =================
        function submitExam() {
            if (examSubmitted) return;
            
            examSubmitted = true;
            
            const examForm = document.getElementById("examForm");
            if (examForm) {
                examForm.submit();
            }
        }

        const submitExamBtn = document.getElementById("submitExamBtn");
        if (submitExamBtn) {
            submitExamBtn.addEventListener("click", function (e) {
                e.preventDefault();
                if (examSubmitted) return;
                
                let answeredCount = 0;
                allRadios.forEach(radio => {
                    if (radio.checked) answeredCount++;
                });
                
                const totalQuestions = questionCards.length;
                const confirmMessage = answeredCount === 0 
                    ? "You haven't answered any questions! Are you sure you want to submit?"
                    : `You have answered ${answeredCount} out of ${totalQuestions} questions.\n\nAre you sure you want to submit the exam?`;
                
                if (confirm(confirmMessage)) {
                    submitExam();
                }
            });
        }

        // ================= PREVENT PAGE REFRESH LOSS =================
        window.addEventListener("beforeunload", function (e) {
            if (!examSubmitted && !autoSubmitTriggered) {
                let hasAnswers = false;
                allRadios.forEach(radio => {
                    if (radio.checked) hasAnswers = true;
                });
                
                if (hasAnswers) {
                    e.preventDefault();
                    e.returnValue = "You have unsaved answers. Are you sure you want to leave? Your progress will be lost.";
                    return e.returnValue;
                }
            }
        });

        // ================= PREVENT CHEATING =================
        // Prevent right click
        document.addEventListener("contextmenu", function(e) {
            if (window.location.pathname.includes("start_exam")) {
                e.preventDefault();
                return false;
            }
        });

        // Prevent copy/paste
        document.addEventListener("copy", function(e) {
            if (window.location.pathname.includes("start_exam")) {
                e.preventDefault();
                return false;
            }
        });

        document.addEventListener("cut", function(e) {
            if (window.location.pathname.includes("start_exam")) {
                e.preventDefault();
                return false;
            }
        });

        document.addEventListener("paste", function(e) {
            if (window.location.pathname.includes("start_exam")) {
                e.preventDefault();
                return false;
            }
        });

        // Prevent keyboard shortcuts
        document.addEventListener("keydown", function(e) {
            if (window.location.pathname.includes("start_exam")) {
                // Prevent F5 refresh
                if (e.key === "F5") {
                    e.preventDefault();
                    alert("Page refresh is disabled during exam.");
                    return false;
                }
                // Prevent Ctrl+R refresh
                if ((e.ctrlKey || e.metaKey) && e.key === "r") {
                    e.preventDefault();
                    alert("Page refresh is disabled during exam.");
                    return false;
                }
                // Prevent Ctrl+Shift+R hard refresh
                if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === "R") {
                    e.preventDefault();
                    alert("Page refresh is disabled during exam.");
                    return false;
                }
                // Prevent F12 Developer Tools
                if (e.key === "F12") {
                    e.preventDefault();
                    alert("Developer tools are disabled during exam.");
                    return false;
                }
                // Prevent Ctrl+U view source
                if ((e.ctrlKey || e.metaKey) && e.key === "u") {
                    e.preventDefault();
                    alert("View source is disabled during exam.");
                    return false;
                }
                // Prevent Ctrl+S save
                if ((e.ctrlKey || e.metaKey) && e.key === "s") {
                    e.preventDefault();
                    alert("Save is disabled during exam.");
                    return false;
                }
            }
        });

        // ================= INITIALIZE =================
        showQuestion(0);
        
        console.log("Exam initialized - Fresh exam started with no pre-selected answers");
    }

    // ================= RESULT PAGE FUNCTIONALITY =================
    if (document.querySelector('.result-item')) {
        const unansweredItems = document.querySelectorAll('.result-item-unanswered');
        unansweredItems.forEach(item => {
            item.style.borderLeft = "4px solid #f59e0b";
            item.style.backgroundColor = "#fffef7";
        });
        
        const correctItems = document.querySelectorAll('.result-item-correct');
        correctItems.forEach(item => {
            item.style.borderLeft = "4px solid #10b981";
            item.style.backgroundColor = "#f8fff9";
        });
        
        const wrongItems = document.querySelectorAll('.result-item-wrong');
        wrongItems.forEach(item => {
            item.style.borderLeft = "4px solid #ef4444";
            item.style.backgroundColor = "#fff8f8";
        });
    }

    // ================= DASHBOARD FUNCTIONALITY =================
    const examCards = document.querySelectorAll('.exam-card');
    examCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-6px)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // ================= NAVBAR ACTIVE LINK =================
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath.includes(href) && href !== '/') {
            link.classList.add('active');
        } else if (currentPath === '/' || currentPath === '/login/') {
            if (link.getAttribute('href') === '/login/') {
                link.classList.add('active');
            }
        }
    });

    // ================= TOOLTIP INITIALIZATION =================
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // ================= POPOVER INITIALIZATION =================
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // ================= EXAM INSTRUCTIONS PAGE - TERMS & CONDITIONS VALIDATION =================
    const agreeTermsCheckbox = document.getElementById("agreeTermsCheckbox");
    const startExamBtn = document.getElementById("startExamBtn");

    if (agreeTermsCheckbox && startExamBtn) {
        function validateTerms() {
            if (agreeTermsCheckbox.checked) {
                startExamBtn.disabled = false;
            } else {
                startExamBtn.disabled = true;
            }
        }
        
        // Initial validation
        validateTerms();
        
        // Add event listener
        agreeTermsCheckbox.addEventListener("change", validateTerms);
        
        // Start exam button click handler
        startExamBtn.addEventListener("click", function() {
            if (agreeTermsCheckbox.checked) {
                window.location.href = "/start-exam/";
            }
        });
    }
});