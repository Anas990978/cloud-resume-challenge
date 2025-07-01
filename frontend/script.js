function toggleSidebar() {
    document.querySelector('.sidebar').classList.toggle('active');
}

function setActiveNav() {
    const sections = document.querySelectorAll('section'); // Include all sections, including hero-section
    const navIcons = document.querySelectorAll('.nav-icon');
    let currentSection = '';

    window.addEventListener('scroll', () => {
        let found = false;
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            const sectionHeight = section.offsetHeight;
            if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
                currentSection = section.getAttribute('id');
                found = true;
            }
        });

        // If at the top (scrollY < first section's offset), default to 'home'
        if (!found && window.scrollY < sections[0].offsetTop - 100) {
            currentSection = 'home';
        }

        navIcons.forEach(icon => {
            icon.classList.remove('active');
            if (icon.getAttribute('href') === `#${currentSection}`) {
                icon.classList.add('active');
            }
        });
    });

    navIcons.forEach(icon => {
        icon.addEventListener('click', () => {
            navIcons.forEach(i => i.classList.remove('active'));
            icon.classList.add('active');
            const sectionId = icon.getAttribute('href').substring(1);
            document.querySelector(`#${sectionId}`).scrollIntoView({ behavior: 'smooth' });
        });
    });
}

document.addEventListener('DOMContentLoaded', setActiveNav);
console.log("JS loaded");