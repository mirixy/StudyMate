document.addEventListener('DOMContentLoaded', () => {
    // Elemente für das Hinzufügen-Modal
    const modal = document.getElementById('todo-modal');
    const addTodoButton = document.getElementById('add-todo-button');
    const closeButton = document.querySelector('.close-button');

    // Initial hide modals
    modal.style.display = 'none';
    
    // Modal öffnen für Hinzufügen
    addTodoButton.addEventListener('click', () => {
        modal.style.display = 'block';
    });

    // Modal schließen für Hinzufügen
    closeButton.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    // Modal schließen, wenn außerhalb des Modals geklickt wird
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Elemente für das Bearbeiten-Modal
    const editModal = document.getElementById('edit-modal');
    const editCloseButton = document.querySelector('.edit-close-button');
    const editForm = document.getElementById('edit-form');
    const editTitle = document.getElementById('edit-title');
    const editDescription = document.getElementById('edit-description');

    // Initial hide edit modal
    editModal.style.display = 'none';

    // Modal öffnen für Bearbeiten
    document.querySelectorAll('.actions a[href^="/edit/"]').forEach((editLink) => {
        editLink.addEventListener('click', (event) => {
            event.preventDefault(); // Standard-Linkverhalten verhindern

            // ToDo-ID aus dem Link extrahieren
            const todoId = editLink.getAttribute('href').split('/edit/')[1];

            // Abrufen von ToDo-Daten über API
            fetch(`/api/todos/${todoId}`)
                .then((response) => response.json())
                .then((data) => {
                    // Formular mit ToDo-Daten füllen
                    editForm.action = `/edit/${todoId}`;
                    editTitle.value = data.title;
                    editDescription.value = data.description || '';

                    // Modal anzeigen
                    editModal.style.display = 'block';
                })
                .catch((error) => {
                    console.error('Fehler beim Abrufen der ToDo-Daten:', error);
                });
        });
    });

    // Modal schließen für Bearbeiten
    editCloseButton.addEventListener('click', () => {
        editModal.style.display = 'none';
    });

    // Modal schließen, wenn außerhalb des Modals geklickt wird
    window.addEventListener('click', (event) => {
        if (event.target === editModal) {
            editModal.style.display = 'none';
        }
    });

    // Add form submission handler
    const addForm = document.getElementById('add-form');
    addForm.addEventListener('submit', (event) => {
        event.preventDefault();
        
        const formData = new FormData(addForm);
        fetch('/add', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                window.location.reload(); // Reload page to show new todo
            } else {
                console.error('Error adding todo');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
        
        modal.style.display = 'none';
    });

    // Edit form submission handler
    editForm.addEventListener('submit', (event) => {
        event.preventDefault();
        
        const formData = new FormData(editForm);
        fetch(editForm.action, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                window.location.reload(); // Reload page to show updated todo
            } else {
                console.error('Error updating todo');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
        
        editModal.style.display = 'none';
    });
    // Grade Tracker functionality
    const gradeModal = document.getElementById('grade-modal');
    const addGradeButton = document.getElementById('add-grade-button');
    const closeGradeButton = gradeModal.querySelector('.close-button');
    const gradeForm = document.getElementById('grade-form');
    const gradesSection = document.querySelector('.grades-section');
    let subjectsGrid = document.querySelector('.subjects-grid');
    const averagePointsElement = document.querySelector('.average-points');
    const finalGradeElement = document.querySelector('.final-grade');

    // Show/hide grade tracker section
    document.querySelector('a[href="#"].nav-item:nth-child(3)').addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelector('.todo-list').style.display = 'none';
        gradesSection.style.display = 'block';
        loadGrades();
    });

    // Modal controls
    addGradeButton.onclick = () => gradeModal.style.display = 'block';
    closeGradeButton.onclick = () => gradeModal.style.display = 'none';

    // Close modal when clicking outside
    window.onclick = (event) => {
        if (event.target === gradeModal) {
            gradeModal.style.display = 'none';
        }
    };

    // Handle grade form submission
    gradeForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = {
            subject: document.getElementById('subject').value,
            semester: document.getElementById('semester').value,
            grade_type: document.getElementById('grade-type').value,
            points: parseInt(document.getElementById('points').value)
        };

        try {
            const response = await fetch('/grades/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                gradeModal.style.display = 'none';
                gradeForm.reset();
                loadGrades();
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });

    // Load and display grades
    async function loadGrades() {
        try {
            const response = await fetch('/grades');
            const data = await response.json();
            
            subjectsGrid.innerHTML = '';
            let totalPoints = 0;
            let totalGrades = 0;

            data.forEach(subject => {
                const subjectCard = createSubjectCard(subject);
                subjectsGrid.appendChild(subjectCard);

                // Calculate averages
                subject.grades.forEach(grade => {
                    totalPoints += grade.points;
                    totalGrades++;
                });
            });

            // Update statistics
            const averagePoints = totalGrades ? (totalPoints / totalGrades).toFixed(1) : '0.0';
            const finalGrade = calculateFinalGrade(averagePoints);
            
            averagePointsElement.textContent = averagePoints;
            finalGradeElement.textContent = finalGrade;
        } catch (error) {
            console.error('Error:', error);
        }
    }

    function createSubjectCard(subject) {
        const card = document.createElement('div');
        card.className = 'subject-card';
        
        const gradesList = subject.grades.map(grade => `
            <li class="grade-item">
                <div class="grade-info">
                    <span>${grade.semester}</span>
                    <span>${grade.grade_type}</span>
                </div>
                <span class="points-badge">${grade.points} Punkte</span>
            </li>
        `).join('');

        card.innerHTML = `
            <h3>${subject.name}</h3>
            <ul class="grade-list">
                ${gradesList}
            </ul>
        `;
        
        return card;
    }

    function calculateFinalGrade(points) {
        // German Abitur grade calculation
        const gradeTable = {
            15: 1.0, 14: 1.0, 13: 1.3,
            12: 1.7, 11: 2.0, 10: 2.3,
            9: 2.7, 8: 3.0, 7: 3.3,
            6: 3.7, 5: 4.0, 4: 4.3,
            3: 4.7, 2: 5.0, 1: 5.3,
            0: 6.0
        };

        const numPoints = Math.round(parseFloat(points));
        return gradeTable[numPoints] || 0.0;
    }

    const subjectModal = document.getElementById('subject-modal');
    const gradeModal = document.getElementById('grade-modal');
    const addSubjectButton = document.getElementById('add-subject-button');
    const addGradeButton = document.getElementById('add-grade-button');
    const closeButtons = document.querySelectorAll('.close-button');

    console.log('JavaScript loaded');

    addSubjectButton.onclick = function() {
        console.log('Add Subject button clicked');
        subjectModal.style.display = 'block';
    };

    addGradeButton.onclick = function() {
        console.log('Add Grade button clicked');
        gradeModal.style.display = 'block';
    };

    closeButtons.forEach(button => {
        button.onclick = function() {
            console.log('Close button clicked');
            subjectModal.style.display = 'none';
            gradeModal.style.display = 'none';
        };
    });

    window.onclick = function(event) {
        if (event.target == subjectModal) {
            console.log('Clicked outside subject modal');
            subjectModal.style.display = 'none';
        }
        if (event.target == gradeModal) {
            console.log('Clicked outside grade modal');
            gradeModal.style.display = 'none';
        }
    };
});