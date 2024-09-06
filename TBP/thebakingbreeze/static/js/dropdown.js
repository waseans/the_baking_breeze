document.addEventListener('DOMContentLoaded', function () {
    const profileIcon = document.getElementById('profile-icon');
    const profileDropdown = document.getElementById('profile-dropdown');
    const menuIcon = document.getElementById('menu-icon');
    const menuDropdown = document.getElementById('menu-dropdown');

    if (profileIcon && profileDropdown) {
        profileIcon.addEventListener('click', function () {
            profileDropdown.style.display = profileDropdown.style.display === 'block' ? 'none' : 'block';
            if (menuDropdown) menuDropdown.style.display = 'none'; // Hide menu dropdown if open
        });
    }

    if (menuIcon && menuDropdown) {
        menuIcon.addEventListener('click', function () {
            menuDropdown.style.display = menuDropdown.style.display === 'block' ? 'none' : 'block';
            if (profileDropdown) profileDropdown.style.display = 'none'; // Hide profile dropdown if open
        });
    }

    document.addEventListener('click', function (e) {
        if (profileDropdown && !profileIcon.contains(e.target)) {
            profileDropdown.style.display = 'none';
        }
        if (menuDropdown && !menuIcon.contains(e.target)) {
            menuDropdown.style.display = 'none';
        }
    });
});
