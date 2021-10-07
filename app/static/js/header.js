document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('nav-mode_switch').addEventListener('click', () => {
        document.body.classList.toggle('dark');

        localStorage.setItem(
            'theme',
            document.body.classList.contains('dark') ? 'dark' : 'light'
        );
    });

    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark');
    }
});